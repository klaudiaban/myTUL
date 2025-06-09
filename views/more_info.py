import flet as ft
import pandas as pd
from constants import *
from .helpers.appbar import create_appbar
from .helpers.helpers_study_places import FACILITY_COLUMNS, check_facilities

def study_place_details_view(page: ft.Page, place_name: str) -> ft.View:
    df = pd.read_csv("assets/info/study_places_table.csv")
    row = df[df["Name of the place"] == place_name].iloc[0]

    facilities = check_facilities(row)

    # Clean image file
    image_path = row["Name of image file"]
    if "HEIC" in image_path:
        image_path = image_path.replace("HEIC", "jpg")

    # Create chips
    facility_chips = [
        ft.Chip(
            border_side=ft.BorderSide(color=ft.colors.GREY_300, width=1),
            label=ft.Text(fac, font_family="Trasandina", size=14, color=TUL_DARK_RED),
            bgcolor=ft.colors.WHITE,
        ) for fac in facilities
    ]

    return ft.View(
        route=f"/study_places_details/{place_name}",
        appbar=create_appbar(page, route_back="/study_places", home=False),
        padding=10,
        bgcolor=ft.colors.WHITE,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Column([
                ft.Container(
                    content=ft.Image(
                        src=f"assets/study_places_images/{image_path}",
                        height=250,
                        width=400,
                        fit=ft.ImageFit.COVER
                    ),
                    border_radius=12,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS
                ),
                ft.Text(
                    value=row["Name of the place"],
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    font_family="Trasandina",
                    color=TUL_DARK_RED
                ),
                ft.Text(
                    value=f"Building: {row['Building']}",
                    size=18,
                    color=ft.colors.GREY_700,
                    font_family="Trasandina"
                ),
                ft.Container(
                    content=ft.Row(
                        controls=facility_chips,
                        wrap=True,
                        spacing=6,
                        run_spacing=6,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=10)
                ),
                ft.Text(
                    value=row.get("Description", "No description available."),
                    size=16,
                    font_family="Trasandina",
                    color=ft.colors.GREY_800
                )
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
