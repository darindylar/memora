from __future__ import annotations
import reflex as rx
from typing import Optional
from memora.services.auth_repo import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    verify_password,
    create_session,
    get_user_by_token,
    delete_session,
)

class AuthState(rx.State):
    email: str = ""
    username: str = ""   
    password: str = ""
    error: str = ""
    loading: bool = False
    session_token: str = rx.Cookie(
    name="session_token", path="/", secure=True, same_site="lax", max_age=60*60*24*30
    )
    user: Optional[dict] = None

    session_token: str = rx.Cookie(
        "", name="memora_token", path="/", max_age=60 * 60 * 24 * 7, same_site="lax"
    )

    current_user_email: str = ""
    current_username: str = ""

    def _load_current_user(self):
        if not self.session_token:
            self.current_user_email = ""
            self.current_username = ""
            return
        user = get_user_by_token(self.session_token)
        if not user:
            self.session_token = ""
            self.current_user_email = ""
            self.current_username = ""
            return
        self.current_user_email = user["email"]
        self.current_username = user["username"]

    def signup(self):
        if not (self.email and self.username and self.password):
            self.error = "Please fill all fields."
            return
        self.loading = True
        self.error = ""
        try:
            if get_user_by_email(self.email):
                self.error = "Email already in use."
                return
            if get_user_by_username(self.username):
                self.error = "Username already in use."
                return

            user = create_user(self.username, self.email, self.password)
            token = create_session(user["id"])
            self.session_token = token
            rx.set_cookie(
                "session_token",
                token,
                max_age=60 * 60 * 24 * 30,  
                httponly=True,
                samesite="Lax",
                secure=True, 
            )
            return rx.redirect("/")
        except Exception as e:
            self.error = str(e) or "Could not sign up."
        finally:
            self.loading = False

    def signin(self):
        if not (self.email and self.password):
            self.error = "Email and password required."
            return
        self.loading = True
        self.error = ""
        try:
            user = get_user_by_email(self.email)
            if not user or not verify_password(self.password, user["password_hash"]):
                self.error = "Invalid credentials."
                return
            token = create_session(user["id"])
            self.session_token = token
            return rx.redirect("/")
        except Exception as e:
            self.error = str(e) or "Could not sign in."
        finally:
            self.loading = False

    def signout(self):
        if self.session_token:
            try:
                delete_session(self.session_token)
            except Exception:
                pass
        self.session_token = ""
        return rx.redirect("/auth")

    def require_login(self):
        if not self.session_token:
            return rx.redirect("/auth")

        user = get_user_by_token(self.session_token)
        if not user:
            self.session_token = ""
            rx.remove_cookie("session_token")
            return rx.redirect("/auth")

        self.current_user_email = user["email"]
        self.current_username = user["username"]

    def logout(self):
        token = self.session_token
        if token:
            try:
                delete_session(token)  
            except Exception:
                pass

        self.session_token = ""   
        self.current_username = "" 
        self.current_user_email = "" 
        self.user = None

        return rx.redirect("/auth")
