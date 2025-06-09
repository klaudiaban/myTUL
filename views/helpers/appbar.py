import flet as ft
import os
from constants import *
from geopy.geocoders import Nominatim

def create_appbar(page, route_back=None, home=True) -> ft.AppBar:
    gl = ft.Geolocator(
        location_settings=ft.GeolocatorSettings(
            accuracy=ft.GeolocatorPositionAccuracy.HIGH
        ),
    )

    page.overlay.append(gl)

    async def handle_get_current_position(e):
        p = await gl.get_current_position_async()
        print(f"get_current_position: ({p.latitude}, {p.longitude})")
        geolocator = Nominatim(user_agent="my_tracking_app_12345")
        location = geolocator.reverse((p.latitude, p.longitude), language='pl')
        print("Address:", location.address)

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
                ft.IconButton(
                    icon=ft.icons.GPS_FIXED,
                    icon_color=ft.colors.GREY,
                    on_click=handle_get_current_position
                ),
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
                ft.IconButton(
                    icon=ft.icons.GPS_FIXED,
                    icon_color=ft.colors.GREY,
                    on_click=handle_get_current_position
                ),
                settings_menu
            ]
        )

    return appbar
