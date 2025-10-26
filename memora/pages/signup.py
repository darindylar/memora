import reflex as rx
from memora.state.auth_state import AuthState
from memora.components.footer import footer
from memora.components.heading import heading

def signup() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                heading(),
                rx.text(
                    "Create your Memora account and begin your learning journey!",
                    size="4",
                    color="gray",
                    align="center",
                ),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Username",
                            value=AuthState.username,
                            on_change=AuthState.set_username,
                            width="100%",
                            size="3",
                            radius="large",
                            variant="soft",
                        ),
                        rx.input(
                            placeholder="Email",
                            value=AuthState.email,
                            on_change=AuthState.set_email,
                            width="100%",
                            size="3",
                            radius="large",
                            variant="soft",
                        ),
                        rx.input(
                            placeholder="Password",
                            type="password",
                            value=AuthState.password,
                            on_change=AuthState.set_password,
                            width="100%",
                            size="3",
                            radius="large",
                            variant="soft",
                        ),
                        rx.button(
                            "Sign up",
                            width="100%",
                            size="3",
                            color_scheme="blue",
                            radius="large",
                            loading=AuthState.loading,
                            on_click=AuthState.signup,
                        ),
                        rx.cond(
                            AuthState.error != "",
                            rx.text(AuthState.error, color="red", weight="medium"),
                        ),
                        spacing="4",
                        width="100%",
                    ),
                ),
                footer(),
                spacing="6",
                width="100%",
                align="center",
            ),
            padding="40px",
            width="100%",
            max_width="400px",
            shadow="lg",
            border_radius="2xl",
        ),
        min_height="100vh",
        padding="20px",
    )
