from flet import Page, View, Text, Row, Colors, MainAxisAlignment, ScrollMode
import webbrowser
from constants import *
from .helpers.appbar import create_appbar

def news_view(page: Page) -> View:
    appbar = create_appbar(page, route_back="/home", home=False)

    webbrowser.open("https://edu.p.lodz.pl/")

    fallback_message = Text(
        "Wikamp has been opened in your default browser.",
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
