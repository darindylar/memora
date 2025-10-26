import reflex as rx

def heading() -> rx.Component:
    return rx.text(
        "memora", size="9", weight="bold"
    )