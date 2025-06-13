from flet import Page, View, Text, Image, ImageFit, Container, Column, Row, Chip, BorderSide, ClipBehavior, MainAxisAlignment, CrossAxisAlignment, padding, colors, FontWeight, ScrollMode
import pandas as pd
from constants import *
from .helpers.appbar import create_appbar
from .helpers.helpers_study_places import check_facilities

def study_place_details_view(page: Page, place_name: str) -> View:
    df = pd.read_csv("assets/info/study_places_table.csv")
    row = df[df["Name of the place"] == place_name].iloc[0]

    facilities = check_facilities(row)

    # Clean image file
    image_path = row["Name of image file"]
    if "HEIC" in image_path:
        image_path = image_path.replace("HEIC", "jpg")

    # Create chips
    facility_chips = [
        Chip(
            border_side=BorderSide(color=colors.GREY_300, width=1),
            label=Text(fac, font_family="Trasandina", size=14, color=TUL_DARK_RED),
            bgcolor=colors.WHITE,
        ) for fac in facilities
    ]

    return View(
        route=f"/study_places_details/{place_name}",
        appbar=create_appbar(page, route_back="/study_places", home=False),
        padding=10,
        bgcolor=colors.WHITE,
        scroll=ScrollMode.AUTO,
        controls=[
            Column([
                Container(
                    content=Image(
                        src=f"assets/study_places_images/{image_path}",
                        height=250,
                        width=400,
                        fit=ImageFit.COVER
                    ),
                    border_radius=12,
                    clip_behavior=ClipBehavior.ANTI_ALIAS
                ),
                Text(
                    value=row["Name of the place"],
                    size=28,
                    weight=FontWeight.BOLD,
                    font_family="Trasandina",
                    color=TUL_DARK_RED
                ),
                Text(
                    value=f"Building: {row['Building']}",
                    size=18,
                    color=colors.GREY_700,
                    font_family="Trasandina"
                ),
                Container(
                    content=Row(
                        controls=facility_chips,
                        wrap=True,
                        spacing=6,
                        run_spacing=6,
                        alignment=MainAxisAlignment.CENTER
                    ),
                    padding=padding.symmetric(vertical=10)
                ),
                Text(
                    value=row.get("Description", "No description available."),
                    size=16,
                    font_family="Trasandina",
                    color=colors.GREY_800
                )
            ],
            spacing=20,
            horizontal_alignment=CrossAxisAlignment.CENTER)
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER
    )
