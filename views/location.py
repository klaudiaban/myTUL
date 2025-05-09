import flet as ft
import json
from constants import *
from .ui_helpers import create_appbar

def location_view(page: ft.Page) -> ft.View:
    appbar = create_appbar()

    location_text = ft.Text("Fetching location...")

    def position_handler(e: ft.ControlEvent):
        lat = e.latitude
        lon = e.longitude
        location_text.value = f"Location: ({lat}, {lon})"
        page.update()

    gl = ft.Geolocator(
        location_settings=ft.GeolocatorSettings(
            accuracy=ft.GeolocatorPositionAccuracy.LOW
        ),
        on_position_change=position_handler
    )

    view = ft.View(
        appbar=appbar,
        route="/location",
        padding=10,
        bgcolor=ft.colors.WHITE,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Column([location_text, gl])
        ]
    )
    def on_push(e):
        gl.get_current_position()

    page.on_view_push = on_push

    return view