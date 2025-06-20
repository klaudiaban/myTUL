from flet import Page, View, Text, Row, MainAxisAlignment, ScrollMode, Colors
import webbrowser
from constants import *
from .helpers.appbar import create_appbar
from .helpers.faculty_storage import load_selected_faculty
from assets.info.faculties_data import FACULTIES_DATA

def news_view(page: Page) -> View:
    appbar = create_appbar(page, route_back="/home", home=False)

    selected = load_selected_faculty()

    news_url = FACULTIES_DATA.get(selected, {}).get("news")
    
    webbrowser.open(news_url)

    fallback_message = Text(
        "The news website has been opened in your default browser.",
        size=16,
        font_family="Trasandina",
        color=Colors.GREY,
    )
    content = Row(controls=[fallback_message], alignment=MainAxisAlignment.CENTER)

    return View(
        route="/news",
        appbar=appbar,
        controls=[content],
        scroll=ScrollMode.AUTO,
        padding=0,
        bgcolor=Colors.WHITE
    )
