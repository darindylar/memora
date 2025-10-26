# memora/pages/auth.py
import reflex as rx
from memora.components.footer import footer
from memora.components.heading import heading

def _primary_button(label: str, href: str) -> rx.Component:
    return rx.link(
        rx.button(label, size="3", border_radius="xl"),
        href=href,
        style={"textDecoration": "none"},
    )

def _card(title: str, body: str, cta: str, href: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(title, weight="bold", size="4"),
            rx.text(body, color="gray"),
            rx.hstack(
                _primary_button(cta, href),
                justify="between",
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        size="3",
        variant="surface",
        width="100%",
        height="100%",
    )

def auth() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.vstack(
                heading(),
                rx.text(
                    "Here you are able to log in to your memora account, or sign up if you don't have one, and begin your studies.",
                    size="4",
                    color="gray",
                ),
            ),
            rx.grid(
                _card(
                    "Sign in 📂",
                    "Click here to sign in to your memora account, if you have an existing account.",
                    "Sign-In",
                    "/signin",
                ),
                _card(
                    "Sign up 🗃️",
                    "If you don't have an account, create a new memora account and get started.",
                    "Sign-Up",
                    "/signup",
                ),
                columns="2",
                width="100%",
                spacing="6",      
                justify="center",  
                gap="2rem",        
            ),

            rx.spacer(),
            footer(),
            spacing="6",
            width="100%",
        ),
        size="4",
        py="28px",
    )
