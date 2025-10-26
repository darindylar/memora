import reflex as rx
from memora.state.auth_state import AuthState

def footer() -> rx.Component:
    return rx.cond(
        AuthState.current_username != "",
        rx.hstack(
            rx.text("memora", size="3", color="gray", weight="bold"),
            rx.text("|", size="3", color="gray"),
            rx.text("You are logged in.", size="3", color="gray"),
            rx.spacer(),
            rx.link("Status", href="/test", underline="hover"),
            rx.link("Settings", href="/settings", underline="hover"),
            width="100%",
            padding_y="1em",
        ),
        rx.hstack(
            rx.text("memora", size="3", color="gray", weight="bold"),
            rx.spacer(),
            rx.link("Status", href="/test", underline="hover"),
            rx.link("Settings", href="/settings", underline="hover"),
            width="100%",
            padding_y="1em",
        ),
    )
