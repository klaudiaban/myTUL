from flet import Page, View, Container, Column, Row, Icon, Text, colors, MainAxisAlignment, CrossAxisAlignment, icons, alignment, TextAlign
from constants import *
from .helpers.appbar import create_appbar

def home_view(page: Page) -> View:
    # AppBar
    appbar = create_appbar(page, home=True)

    # Navigation handler
    def navigate(url):
        def handler(e):
            if url:
                page.go(url)
        return handler

    # Item list
    items = [
        ("About TUL", icons.ACCOUNT_TREE, ""),
        ("Campus Map", icons.MAP, ""),
        ("Calendar", icons.CALENDAR_MONTH, '/calendar'),
        ("News", icons.NEWSPAPER, ""),
        ("Wikamp", icons.DASHBOARD, '/wikamp'),
        ("WebDziekanat", icons.PAGES, ""),
        ("Study Places", icons.BOOK, '/study_places'),
        ("Website", icons.WEB, ""),
        ("E-mail", icons.EMAIL, "")
    ]

    def create_card(title, icon, url):
        return Container(
            content=Column(
                [
                    Icon(icon, size=45, color=TUL_RED),
                    Text(title, size=13, text_align=TextAlign.CENTER, font_family="Trasandina"),
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
            width=110,
            height=110,
            padding=10,
            border_radius=10,
            bgcolor=colors.WHITE,
            alignment=alignment.center,
            on_click=navigate(url)
        )

    # Compose UI
    rows = []
    for i in range(0, len(items), 3):
        row = Row(
            controls=[create_card(*item) for item in items[i:i+3]],
            alignment=MainAxisAlignment.SPACE_EVENLY,
        )
        rows.append(row)

    return View(
        route="/home",
        appbar=appbar,
        controls=[
            Column(rows, spacing=15)
        ],
        vertical_alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )