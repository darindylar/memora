# memora/memora.py
import reflex as rx
from memora.pages.index import index
from memora.pages.auth import auth
from memora.pages.signin import signin
from memora.pages.signup import signup
from memora.state.auth_state import AuthState


app = rx.App()
app.add_page(index, route="/", title="Home", on_load=AuthState.require_login)
app.add_page(auth, route="/auth", title="Auth")
app.add_page(signin, route="/signin", title="Sign In")
app.add_page(signup, route="/signup", title="Sign Up")
