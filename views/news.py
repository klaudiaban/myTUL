import flet as ft
import webbrowser
from constants import *
from .helpers.appbar import create_appbar

def news_view(page: ft.Page) -> ft.View:
    appbar = create_appbar(page, route_back="/home", home=False)

    webbrowser.open("https://edu.p.lodz.pl/")

    fallback_message = ft.Text(
        "Wikamp has been opened in your default browser.",
        size=16,
        font_family="Trasandina",
        color=ft.colors.GREY,
    )
    content = ft.Row(controls=[fallback_message], alignment=ft.MainAxisAlignment.CENTER)

    return ft.View(
        route="/news",
        appbar=appbar,
        controls=[content],
        scroll=ft.ScrollMode.AUTO,
        padding=0,
        bgcolor=ft.colors.WHITE
    )
