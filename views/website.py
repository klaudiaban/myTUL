from flet import Page, View, Text, Row, MainAxisAlignment, ScrollMode, Colors, TextAlign, Column
import webbrowser
from constants import *
from .helpers.appbar import create_appbar
from .helpers.faculty_storage import load_selected_faculty
from assets.info.faculties_data import FACULTIES_DATA

def website_view(page: Page) -> View:
    appbar = create_appbar(page, route_back="/home", home=False)

    selected = load_selected_faculty()

    news_url = FACULTIES_DATA.get(selected, {}).get("website")
    
    webbrowser.open(news_url)

    fallback_message = Text(
        "The faculty website has been opened in your default browser.",
        size=16,
        font_family="Trasandina",
        color=Colors.GREY,
        text_align=TextAlign.CENTER,
        max_lines=None
    )

    content = Column(
        controls=[fallback_message],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment="center"
    )

    return View(
        route="/website",
        appbar=appbar,
        controls=[content],
        scroll=ScrollMode.AUTO,
        padding=20,
        bgcolor=Colors.WHITE
    )
