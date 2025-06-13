from flet import Page, View, Text, TextStyle, dropdown, Dropdown, ElevatedButton, ButtonStyle, RoundedRectangleBorder, Container, Column, alignment, colors, BoxShadow, Offset, CrossAxisAlignment, MainAxisAlignment
from constants import *
from assets.info.faculties_data import faculties
from .helpers.faculty_storage import save_selected_faculty, load_selected_faculty

def open_view(page: Page) -> View:
    selected = load_selected_faculty()
    if selected:
        page.go("/home")
        return View(route="/open", controls=[])

    text = Text(
        "Choose your faculty",
        size=26,
        font_family="Trasandina",
        weight="bold",
        color=TUL_DARK_RED,
        text_align="center"
    )

    dropdown_options = [dropdown.Option(faculty) for faculty in faculties.keys()]

    faculty_dropdown = Dropdown(
                        label="Faculty",
                        text_size=16,
                        text_style=TextStyle(font_family="Trasandina"),
                        options=dropdown_options,
                        width=300
                    )

    def submit_click(e):
        if faculty_dropdown.value:
            save_selected_faculty(faculty_dropdown.value)
            page.go("/home")

    button = ElevatedButton(
        text="Submit",
        bgcolor=TUL_RED,
        color=WHITE,
        width=200,
        height=50,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=12),
            elevation={"pressed": 4, "hovered": 2}
        ),
        on_click=submit_click
    )

    return View(
        route="/open",
        padding=30,
        bgcolor=colors.WHITE,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        vertical_alignment=MainAxisAlignment.CENTER,
        controls=[
            Container(
                content=Column(
                    [
                        text,
                        Container(height=20),
                        faculty_dropdown,
                        Container(height=30),
                        button,
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                alignment=alignment.center,
                padding=30,
                border_radius=20,
                bgcolor=colors.WHITE,
                shadow=BoxShadow(
                    blur_radius=10,
                    color=colors.BLACK12,
                    offset=Offset(0, 4),
                ),
                width=350,
            )
        ]
    )
