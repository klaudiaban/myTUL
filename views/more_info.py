from flet import Page, View, Text, Image, ImageFit, Container, Column, Row, Chip, BorderSide, ClipBehavior, MainAxisAlignment, CrossAxisAlignment, padding, Colors, FontWeight, ScrollMode, TextAlign
import pandas as pd
from flet.plotly_chart import PlotlyChart
from constants import *
from .helpers.appbar import create_appbar
from .helpers.helpers_study_places import check_facilities
from .helpers.plot_more_info import create_occupancy_card

def study_place_details_view(page: Page, place_name: str) -> View:
    df = pd.read_csv("assets/info/study_places_table.csv")
    row = df[df["Name of the place"] == place_name].iloc[0]

    facilities = check_facilities(row)

    image_path = row["Name of image file"]
    if "HEIC" in image_path:
        image_path = image_path.replace("HEIC", "jpg")

    # Create chips
    facility_chips = [
        Chip(
            label=Text(fac, size=16, font_family="Trasandina", color=Colors.BLACK),
            bgcolor=Colors.WHITE,
            border_side=BorderSide(color=Colors.INDIGO_200, width=1),
        ) for fac in facilities
    ]

    occupancy_card, init_chart = create_occupancy_card()

    view = View(
        route=f"/study_places_details/{place_name}",
        appbar=create_appbar(page, route_back="/study_places", home=False),
        padding=20,
        bgcolor=Colors.WHITE,
        scroll=ScrollMode.AUTO,
        controls=[
            Column([
                Container(
                    content=Image(
                        src=f"assets/study_places_images/{image_path}",
                        width=350,
                        fit=ImageFit.COVER,
                        border_radius=12,
                    ),
                    border_radius=12,
                    clip_behavior=ClipBehavior.ANTI_ALIAS,
                ),
                Text(
                    value=row["Name of the place"],
                    size=28,
                    weight=FontWeight.BOLD,
                    font_family="Trasandina",
                    color=TUL_DARK_RED,
                    text_align=TextAlign.CENTER
                ),
                Text(
                    value=row['Building'],
                    size=18,
                    color=Colors.GREY_700,
                    font_family="Trasandina",
                    text_align=TextAlign.CENTER
                ),
                Container(
                    content=Row(
                        controls=facility_chips,
                        wrap=True,
                        spacing=5,
                        run_spacing=5,
                        alignment=MainAxisAlignment.CENTER
                    ),
                    padding=padding.symmetric(vertical=5)
                ),
                Text(
                    value=row.get("Description", "No description available."),
                    size=16,
                    font_family="Trasandina",
                    color=Colors.GREY_800,
                    text_align=TextAlign.CENTER
                ),
                occupancy_card
            ],
            spacing=10,
            horizontal_alignment=CrossAxisAlignment.CENTER)
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

    return view, init_chart
