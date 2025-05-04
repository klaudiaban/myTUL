import flet as ft
import flet_easy as fs
from constants import *
from .ui_helpers import create_appbar

study_places = fs.AddPagesy()
@study_places.page('/study_places', title='Study Places')
def study_places_view(data: fs.Datasy):

    appbar = create_appbar()

    page_title = ft.Container(
                    ft.Text("Room Booking", size=24, weight="bold", color=TUL_RED),
                    alignment=ft.alignment.center
                )

    search_field = ft.TextField(
                    label="Search buildings",
                    prefix_icon=ft.icons.SEARCH,
                    border_color=TUL_RED)

    categories_scroll = ft.Container(
                        padding=10,
                        content=ft.Row(
                            scroll=ft.ScrollMode.AUTO,
                            controls=[
                                ft.Container(
                                    padding=ft.padding.all(8),
                                    bgcolor=TUL_RED,
                                    border=ft.border.all(color=TUL_RED),
                                    border_radius=8,
                                    content=ft.Text(
                                        cat,
                                        color="white",
                                        size=14
                                    ),
                                ) for cat in
                                ["All", "Computer Labs", "Lecture Halls", "Study Rooms", "Conference Rooms"]
                            ]
                        )
                    )
    
    cards_container = ft.Column()

    def create_card(place):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Image(src=place["image_url"], height=100, fit=ft.ImageFit.COVER),
                    ft.Text(place["name"], size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(place["location"], size=12, color=ft.colors.GREY),
                    ft.Text(f"Category: {place['category']}", size=12, color=ft.colors.GREY),
                ]),
                padding=10
            ),
            on_click=lambda e: data.page.snack_bar.open(f"You selected {place['name']}")
        )
    

    return ft.Container(
            padding=10,
            bgcolor="white",
            content=appbar)