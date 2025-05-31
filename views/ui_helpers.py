import flet as ft
import os
from constants import *

def create_appbar(route_back=None, home=True) -> ft.AppBar:
    def change_faculty(e):
        file_path = os.path.join(os.path.dirname(__file__), "selected_faculty.txt")
        if os.path.exists(file_path):
            os.remove(file_path)
        e.page.go("/open")

    settings_menu = ft.PopupMenuButton(
        icon=ft.icons.SETTINGS,
        icon_color=ft.colors.GREY,
        items=[
            ft.PopupMenuItem(
                content=ft.Row([ft.Text("Change faculty", font_family="Trasandina", size=16)]),
                on_click=change_faculty)
        ]
    )

    if home:
        appbar = ft.AppBar(
            leading=ft.Image(src="images/logo_PŁ.jpg", fit=ft.ImageFit.CONTAIN),
            title=ft.Text("myTUL", size=30, weight=ft.FontWeight.BOLD, font_family="Trasandina"),
            center_title=True,
            bgcolor=ft.colors.WHITE,
            actions=[
                settings_menu
            ]
        )
    else:
        appbar = ft.AppBar(
            leading=ft.IconButton(
                ft.Icons.ARROW_BACK,
                icon_color=ft.colors.GREY,
                on_click=lambda e: e.page.go(route_back)
            ),
            title=ft.Text("myTUL", size=30, weight=ft.FontWeight.BOLD, font_family="Trasandina"),
            center_title=True,
            bgcolor=ft.colors.WHITE,
            actions=[
                settings_menu
            ]
        )

    return appbar
