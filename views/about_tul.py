from flet import Page, View, Text, Row, MainAxisAlignment, ScrollMode, Colors, TextAlign, Column
import webbrowser
from constants import *
from .helpers.appbar import create_appbar

def about_tul_view(page: Page) -> View:
    appbar = create_appbar(page, route_back="/home", home=False)
    
    webbrowser.open("https://p.lodz.pl/en/about-tul/tul-glance")

    fallback_message = Text(
        "The About TUL website has been opened in your default browser.",
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
        route="/about_tul",
        appbar=appbar,
        controls=[content],
        scroll=ScrollMode.AUTO,
        padding=10,
        bgcolor=Colors.WHITE
    )
