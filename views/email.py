from flet import Page, View, Text, Row, MainAxisAlignment, ScrollMode, Colors, TextAlign, Column
import webbrowser
from constants import *
from .helpers.appbar import create_appbar

def email_view(page: Page) -> View:
    appbar = create_appbar(page, route_back="/home", home=False)

    webbrowser.open("https://outlook.office365.com/mail/")

    fallback_message = Text(
        "The e-mail website has been opened in your default browser.",
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
        route="/email",
        appbar=appbar,
        controls=[content],
        scroll=ScrollMode.AUTO,
        padding=10,
        bgcolor=Colors.WHITE
    )
