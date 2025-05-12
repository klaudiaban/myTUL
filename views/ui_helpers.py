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


def create_tabs(a_cards, b_cards):
    
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
    
    return tabs_categories