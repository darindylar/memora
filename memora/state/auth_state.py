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
        name="session_token", path="/", secure=True, same_site="lax", max_age=60 * 60 * 24 * 30
    )

    user: Optional[dict] = None
    current_user_email: str = ""
    current_username: str = ""

    def _load_current_user(self):
        if not self.session_token:
            self.current_user_email = ""
            self.current_username = ""
            self.user = None
            return
        user = get_user_by_token(self.session_token)
        if not user:
            self.session_token = ""
            self.current_user_email = ""
            self.current_username = ""
            self.user = None
            return
        self.user = user
        self.current_user_email = user.get("email", "")
        self.current_username = user.get("username", "")

    def signup(self):
        if not (self.email and self.username and self.password):
            self.error = "Please fill all fields."
            return
        self.loading = True
        self.error = ""
        try:
            if "@" not in self.email and "." not in self.email:
                self.error = "Invalid email entered."
                return
            if get_user_by_email(self.email):
                self.error = "Email already in use."
                return
            if get_user_by_username(self.username):
                self.error = "Username already in use."
                return
            if len(self.password) < 8:
                self.error = "Password must be 8 or more characters."
                return
            
            user = create_user(self.username, self.email, self.password)
            token = create_session(user["id"])
            self.session_token = token
            self.user = user
            self.current_username = user["username"]
            self.current_user_email = user["email"]
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
            self.user = user
            self.current_username = user["username"]
            self.current_user_email = user["email"]
            return rx.redirect("/")
        except Exception as e:
            self.error = str(e) or "Could not sign in."
        finally:
            self.loading = False

    def signout(self):
        try:
            if self.session_token:
                delete_session(self.session_token)
        except Exception:
            pass

        self.session_token = ""
        self.user = None
        self.current_username = ""
        self.current_user_email = ""
        return rx.redirect("/auth")

    def require_login(self):
        if not self.session_token:
            return rx.redirect("/auth")

        user = get_user_by_token(self.session_token)
        if not user:
            self.session_token = ""
            self.user = None
            self.current_user_email = ""
            self.current_username = ""
            return rx.redirect("/auth")

        self.user = user
        self.current_user_email = user["email"]
        self.current_username = user["username"]

    def logout(self):
        return self.signout()
