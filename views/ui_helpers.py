import flet as ft
import flet_easy as fs
from constants import *

def create_appbar() -> ft.AppBar:
    appbar = ft.AppBar(
        leading=ft.Image(src=f"images/logo_PŁ.jpg", fit=ft.ImageFit.CONTAIN),
        title=ft.Text("myTUL", size=30, weight=ft.FontWeight.BOLD, font_family="Trasandina"),
        center_title=True,
        bgcolor=ft.colors.WHITE,
        actions=
        [
            ft.IconButton(ft.Icons.NOTIFICATIONS, icon_color=ft.colors.GREY),
            ft.IconButton(ft.Icons.PERSON, icon_color=ft.colors.GREY),
        ]
        )
    return appbar
