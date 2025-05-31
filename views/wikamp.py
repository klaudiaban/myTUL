import flet as ft
import flet_webview as ftwv
import webbrowser
from constants import *
from .ui_helpers import create_appbar

def wikamp_view(page: ft.Page) -> ft.View:
    appbar = create_appbar(page, route_back="/home", home=False)

    webbrowser.open("https://edu.p.lodz.pl/")
    fallback_message = ft.Text(
        "Wikamp has been opened in your default browser.",
        size=16,
        font_family="Trasandina",
        color=ft.colors.GREY
    )
    content = [fallback_message]

    return ft.View(
        route="/wikamp",
        appbar=appbar,
        controls=content,
        scroll=ft.ScrollMode.AUTO,
        padding=0,
        bgcolor=ft.colors.WHITE
    )