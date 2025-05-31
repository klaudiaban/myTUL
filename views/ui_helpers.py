import flet as ft
from constants import *

def create_appbar(route_back=None, home=True) -> ft.AppBar:
    if home == True:
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
    else:
        appbar = ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color=ft.colors.GREY, on_click=lambda e: e.page.go(route_back)),
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



