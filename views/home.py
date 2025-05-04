import flet as ft
import flet_easy as fs
from constants import *
from .ui_helpers import create_appbar

home = fs.AddPagesy(
    route_prefix='/home'
)
@home.page('/init', title='Init')
def home_view(data: fs.Datasy):

    # AppBar
    appbar = create_appbar()

    # Item list
    items = [
        ("About TUL", ft.icons.ACCOUNT_TREE, ""),
        ("Campus Map", ft.icons.MAP, ""),
        ("Calendar", ft.icons.CALENDAR_MONTH, '/calen'),
        ("News", ft.icons.NEWSPAPER, ""),
        ("Wikamp", ft.icons.DASHBOARD, ""),
        ("WebDziekanat", ft.icons.PAGES, ""),
        ("Study Places", ft.icons.BOOK, '/study_places'),
        ("Website", ft.icons.WEB, ""),
        ("E-mail", ft.icons.EMAIL, "")
    ]

    def create_card(title, icon, url):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=45, color=TUL_RED),
                    ft.Text(title, size=13, text_align=ft.TextAlign.CENTER, font_family="Trasandina"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=110,
            height=110,
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center,
            on_click=data.go(url)
        )

    # Break items into rows of 3
    rows = []

    rows.append(appbar)

    for i in range(0, len(items), 3):
        row = ft.Row(
            controls=[create_card(*item) for item in items[i:i+3]],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
        rows.append(row)

    return (ft.Column(rows, spacing=15))
