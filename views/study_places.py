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

    def create_study_place_card(image_path, name, building, availability, on_more_info):
        availability_color = ft.colors.GREEN if availability == "Available" else ft.colors.RED

        return ft.Card(
            width=350,
            elevation=4,
            shape=ft.RoundedRectangleBorder(radius=12),
            content=ft.Container(
                padding=10,
                border_radius=12,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Column([
                    ft.Container(
                        content=ft.Image(src=image_path, height=180, width=350, fit=ft.ImageFit.COVER),
                        border_radius=12,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    ),
                    ft.Row(
                        height=30,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(name, size=20, weight=ft.FontWeight.BOLD),
                        ]
                    ),
                    ft.Text(building, size=16, color=ft.colors.GREY),
                    ft.Row(
                        height=30,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                availability,
                                size=14,
                                color=availability_color,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.ElevatedButton(
                                text="More Info",
                                on_click=on_more_info,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                            )
                        ]
                    )
                ])
            )
        )
    
    card = create_study_place_card(
        "images/parter_4.JPG",
        "Roomy 1",
        "Library",
        "Available",
        lambda e: page.go("/study_place_details")
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