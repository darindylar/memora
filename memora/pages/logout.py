import reflex as rx
from memora.state.auth_state import AuthState

def logout() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.spinner(size="3"),
            rx.text("Signing you out…"),
            spacing="3",
            align="center",
        ),
        min_h="80vh",
        on_mount=AuthState.logout,
    )