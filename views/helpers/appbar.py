from flet import AppBar, PopupMenuButton, PopupMenuItem, Row, Text, IconButton, Image, Colors, FontWeight, Icons, ImageFit
import os
from constants import *

def create_appbar(page, route_back=None, home=True) -> AppBar:

    def change_faculty(e):
        file_path = os.path.join(os.path.dirname(__file__), "selected_faculty.txt")
        if os.path.exists(file_path):
            os.remove(file_path)
        e.page.go("/open")

    settings_menu = PopupMenuButton(
        icon=Icons.SETTINGS,
        icon_color=Colors.GREY,
        items=[
            PopupMenuItem(
                content=Row([Text("Change faculty", font_family="Trasandina", size=16)]),
                on_click=change_faculty)
        ]
    )

    if home:
        appbar = AppBar(
            leading=Image(src="images/logo_PŁ.jpg", fit=ImageFit.CONTAIN),
            title=Text("myTUL", size=30, weight=FontWeight.BOLD, font_family="Trasandina"),
            center_title=True,
            bgcolor=Colors.WHITE,
            actions=[
                settings_menu
            ]
        )
    else:
        appbar = AppBar(
            leading=IconButton(
                Icons.ARROW_BACK,
                icon_color=Colors.GREY,
                on_click=lambda e: e.page.go(route_back)
            ),
            title=Text("myTUL", size=30, weight=FontWeight.BOLD, font_family="Trasandina"),
            center_title=True,
            bgcolor=Colors.WHITE,
            actions=[
                settings_menu
            ]
        )

    return appbar
