from datetime import datetime
import calendar
from flet import *
from constants import *
from .helpers.appbar import create_appbar

def calen_view(page: Page) -> View:
    now = datetime.now()
    year = now.year
    month = now.month
    month_name = calendar.month_name[month]

    # Calendar heading
    heading = Text(
        f"{month_name} {year}",
        size=20,
        weight=FontWeight.BOLD,
        font_family="Trasandina",
        text_align=TextAlign.CENTER
    )

    # Optional placeholder - you can add calendar rendering logic here
    placeholder = Text(
        "Calendar content goes here...",
        size=16,
        font_family="Trasandina",
        color=colors.GREY
    )

    return View(
        route="/calendar",
        appbar=create_appbar(page, route_back="/home", home=False),
        controls=[
            Column(
                controls=[heading, placeholder],
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.CENTER
            )
        ],
        vertical_alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )