import reflex as rx
from memora.state.auth_state import AuthState
from memora.components.footer import footer

def signin() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.text("Sign in to your account", size="7", weight="bold"),
            rx.form(
                rx.vstack(
                    rx.input(placeholder="Email", value=AuthState.email, on_change=AuthState.set_email, width="100%"),
                    rx.input(placeholder="Password", type="password", value=AuthState.password, on_change=AuthState.set_password, width="100%"),
                    rx.button("Sign in", type="submit", width="100%", loading=AuthState.loading),
                    rx.cond(AuthState.error != "", rx.text(AuthState.error, color="red")),
                    spacing="3", width="100%",
                ),
                on_submit=AuthState.signin, reset_on_submit=False,
            ),
            footer(),
            spacing="6", width="100%",
        ),
        size="4", py="28px",
    )
