# memora/memora.py
import reflex as rx
from memora.pages.index import index

app = rx.App()
app.add_page(index, route="/", title="Home")
