from flet import Page, View, Container, Column, Row, Icon, Text, Colors, MainAxisAlignment, CrossAxisAlignment, Icons, alignment, TextAlign
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
        ("About TUL", Icons.ACCOUNT_TREE, "/about_tul"),
        ("Campus Map", Icons.MAP, "/campus_map"),
        ("Calendar", Icons.CALENDAR_MONTH, '/calendar'),
        ("News", Icons.NEWSPAPER, "/news"),
        ("Wikamp", Icons.DASHBOARD, '/wikamp'),
        ("WebDziekanat", Icons.PAGES, "/webdziekant"),
        ("Study Places", Icons.BOOK, '/study_places'),
        ("Website", Icons.WEB, "/website"),
        ("E-mail", Icons.EMAIL, "/email")
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
            bgcolor=Colors.WHITE,
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