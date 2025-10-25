# memora/pages/index.py
import reflex as rx
from memora.state.auth_state import AuthState
from memora.components.footer import footer

try:
    from dotenv import load_dotenv  
    load_dotenv()
except Exception:
    pass

ENV_URL_KEYS = ["SUPABASE_URL"]
ENV_KEY_KEYS = ["SUPABASE_KEY"]

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

def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.vstack(
                rx.text("memora", size="9", weight="bold"),
                rx.text(
                    "AI-powered flashcards with spaced repetition, imports, and quizzes.",
                    size="4",
                    color="gray",
                ),
                rx.hstack(
                    _primary_button("➕ Create Deck", "/create"),
                    _primary_button("📤 Import Notes", "/import"),
                    _primary_button("🧪 Practice", "/practice"),
                    wrap="wrap",
                    spacing="3",
                ),
                spacing="4",
                align="start",
                width="100%",
                py="24px",
            ),

            rx.grid(
                _card(
                    "Your Decks",
                    "Browse, edit, and share your flashcard decks.",
                    "Open Decks",
                    "/decks",
                ),
                _card(
                    "Generate from Notes",
                    "Upload PDF/image/text; auto-generate flashcards.",
                    "Import",
                    "/import",
                ),
                _card(
                    "Practice & Review",
                    "Smart scheduling with spaced repetition.",
                    "Practice",
                    "/practice",
                ),
                _card(
                    "Insights",
                    "Track progress, streaks, and weak topics.",
                    "Insights",
                    "/insights",
                ),
                columns=rx.breakpoints(initial="1", sm="2", md="2", lg="4"),
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
