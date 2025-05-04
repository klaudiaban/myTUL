import flet as ft
from constants import *
from .ui_helpers import create_appbar

def study_places_view(page: ft.Page) -> ft.View:
    appbar = create_appbar()

    tabs_categories = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        height=30,
        divider_color=ft.colors.GREY_300,
        indicator_color=TUL_RED,
        label_color=TUL_DARK_RED,
        tabs=[
            ft.Tab(tab_content=ft.Text('All', font_family="Trasandina", size=16)),
            ft.Tab(tab_content=ft.Text('Group', font_family="Trasandina", size=16)),
            ft.Tab(tab_content=ft.Text('Silent', font_family="Trasandina", size=16)),
        ]
    )

    search_field = ft.TextField(
        hint_text="Search for a place", 
        hint_style=ft.TextStyle(font_family="Trasandina", size=18),
        width=350, 
        height=50,
        border_color=ft.colors.GREY_300,
        border_radius=ft.border_radius.all(10)
    )

    card = ft.Card(
        width=350,
        shape=ft.RoundedRectangleBorder(radius=10),
        content=ft.Container(
            border_radius=10,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Column([
                ft.Image(src="images/DSCF0265.JPG", fit=ft.ImageFit.COVER),
                ft.Row([ft.Text("Room 1", font_family="Trasandina")]),
                ft.Row([ft.Text("Library", font_family="Trasandina")]),
            ])
        )
    )

    return ft.View(
        route="/study_places", 
        appbar=appbar,
        padding=10,
        bgcolor=ft.colors.WHITE, 
        scroll=ft.ScrollMode.AUTO, 
        controls=[
            ft.Column([
                search_field,
                tabs_categories,
                card
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )