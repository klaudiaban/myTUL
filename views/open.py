import flet as ft
from constants import *
from assets.info.faculties_data import faculties
from .helpers.faculty_storage import save_selected_faculty, load_selected_faculty

def open_view(page: ft.Page) -> ft.View:
    selected = load_selected_faculty()
    if selected:
        page.go("/home")
        return ft.View(route="/open", controls=[])

    text = ft.Text(
        "Choose your faculty",
        size=26,
        font_family="Trasandina",
        weight="bold",
        color=TUL_DARK_RED,
        text_align="center"
    )

    dropdown_options = [ft.dropdown.Option(faculty) for faculty in faculties.keys()]

    dropdown = ft.Dropdown(
        label="Faculty",
        text_size=16,
        text_style=ft.TextStyle(font_family="Trasandina"),
        options=dropdown_options,
        width=300
    )

    def submit_click(e):
        if dropdown.value:
            save_selected_faculty(dropdown.value)
            page.go("/home")

    button = ft.ElevatedButton(
        text="Submit",
        bgcolor=TUL_RED,
        color=WHITE,
        width=200,
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            elevation={"pressed": 4, "hovered": 2}
        ),
        on_click=submit_click
    )

    return ft.View(
        route="/open",
        padding=30,
        bgcolor=ft.colors.WHITE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        text,
                        ft.Container(height=20),
                        dropdown,
                        ft.Container(height=30),
                        button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                padding=30,
                border_radius=20,
                bgcolor=ft.colors.WHITE,
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    color=ft.colors.BLACK12,
                    offset=ft.Offset(0, 4),
                ),
                width=350,
            )
        ]
    )
