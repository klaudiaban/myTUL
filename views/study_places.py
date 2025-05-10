import flet as ft
from constants import *
from .ui_helpers import create_appbar

def study_places_view(page: ft.Page) -> ft.View:
    room_data = [
        {
            "name": "Ground Floor of Library",
            "campus": "B",
            "building": "Library",
            "floor": 0,
            "image": "images/parter_4.JPG",
            "latitude": 51.123456,
            "longitude": 17.123456,
        },
        {
            "name": "Second Floor of Library",
            "campus": "A",
            "building": "Library",
            "floor": 2,
            "image": "images/drugie_2.JPG",
            "latitude": 51.123456,
            "longitude": 17.123456,
        },
    ]

    def create_study_place_card(image_path, name, building, availability, on_more_info):
        availability_color = ft.colors.GREEN if availability == "Available" else ft.colors.RED

        return ft.Card(
            width=350,
            shape=ft.RoundedRectangleBorder(radius=12),
            shadow_color=ft.colors.GREY_100,
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

    appbar = create_appbar(route_back="/home/init", home=False)

    a_cards = []
    b_cards = []
    for room in room_data:
        if room["campus"] == "A":
            a_cards.append(
                create_study_place_card(
                    room["image"],
                    room["name"],
                    room["building"],
                    "Available",
                    lambda e: page.go("/study_place_details")
                )
            )
        elif room["campus"] == "B":
            b_cards.append(
                create_study_place_card(
                    room["image"],
                    room["name"],
                    room["building"],
                    "Available",
                    lambda e: page.go("/study_place_details")
                )
            )

    all_cards = a_cards + b_cards

    tabs_categories = ft.Tabs(
                            selected_index=0,
                            animation_duration=300,
                            divider_color=ft.colors.GREY_300,
                            indicator_color=TUL_RED,
                            label_color=TUL_DARK_RED,
                            tabs=[
                                ft.Tab(
                                    tab_content=ft.Text('All', font_family="Trasandina", size=16),
                                    content=ft.Container(
                                        padding=ft.Padding(0, 10, 0, 0),  # Top padding of 16
                                        content=ft.Column(controls=all_cards)
                                    )
                                ),
                                ft.Tab(
                                    tab_content=ft.Text('Campus A', font_family="Trasandina", size=16),
                                    content=ft.Container(
                                        padding=ft.Padding(0, 10, 0, 0),
                                        content=ft.Column(controls=a_cards)
                                    )
                                ),
                                ft.Tab(
                                    tab_content=ft.Text('Campus B', font_family="Trasandina", size=16),
                                    content=ft.Container(
                                        padding=ft.Padding(0, 10, 0, 0),
                                        content=ft.Column(controls=b_cards)
                                    )
                                ),
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

    return ft.View(
        route="/study_places", 
        appbar=appbar,
        padding=10,
        bgcolor=ft.colors.WHITE, 
        scroll=ft.ScrollMode.AUTO, 
        controls=[
            ft.Column([
                search_field,
                tabs_categories
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )