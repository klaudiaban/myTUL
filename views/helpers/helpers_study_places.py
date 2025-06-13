from flet import Colors, Chip, Card, Container, Image, ImageFit, Text, Row, Column, ElevatedButton, BorderSide, RoundedRectangleBorder, ClipBehavior, padding, MainAxisAlignment, ButtonStyle, FontWeight
from constants import *
import pandas as pd

FACILITY_COLUMNS = [
    "Group", "Individual", "Cafeteria", "Power Outlets",
    "Whiteboards", "Computers", "Comfortable Chairs/Couches"
]

def check_facilities(row):
    facilities = []
    
    campus_val = str(row.get("Campus", "")).strip()
    if campus_val.startswith("A"):
        facilities.append("Campus A")
    elif campus_val.startswith("B"):
        facilities.append("Campus B")
    
    for facility_col in FACILITY_COLUMNS:
        if facility_col in row:
            val = row[facility_col]
            if pd.notna(val) and float(val) == 1.0:
                facilities.append(facility_col)
                
    return facilities

def create_study_place_card(page, image_path, name, building, facilities, availability="Available"):
    availability_color = Colors.GREEN if availability == "Available" else Colors.RED

    on_more_info=lambda e: page.go(f"/study_places_details/{name}")

    # Create facility chips
    facility_chips = []
    for facility in facilities:
        facility_chips.append(
            Chip(
                label=Text(facility, size=14, font_family="Trasandina", color=Colors.BLACK),
                bgcolor=Colors.WHITE,
                border_side=BorderSide(color=Colors.INDIGO_200, width=1),
            )
        )

    if "HEIC" in image_path:
        image_path = image_path.replace("HEIC", "jpg")

    return Card(
        width=350,
        shape=RoundedRectangleBorder(radius=12),
        shadow_color=Colors.GREY_100,
        content=Container(
            padding=10,
            border_radius=12,
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            content=Column([
                Container(
                    content=Image(src=f"assets/study_places_images/{image_path}", height=180, width=350, fit=ImageFit.COVER),
                    border_radius=12,
                    clip_behavior=ClipBehavior.ANTI_ALIAS,
                ),
                Row(
                    height=30,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text(name, size=22, weight=FontWeight.BOLD, font_family="Trasandina"),
                    ]
                ),
                Text(building, size=16, color=Colors.GREY_700, font_family="Trasandina"),
                Container(
                    content=Row(
                        controls=facility_chips,
                        wrap=True,
                        spacing=5,
                        run_spacing=5
                    ),
                    padding=padding.symmetric(vertical=5)
                ),
                Row(
                    height=30,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text(
                            availability,
                            size=16,
                            color=availability_color,
                            weight=FontWeight.BOLD,
                            font_family="Trasandina"
                        ),
                        ElevatedButton(
                            text="More Info",
                            color=Colors.INDIGO_500,
                            on_click=on_more_info,
                            style=ButtonStyle(shape=RoundedRectangleBorder(radius=8))
                        )
                    ]
                )
            ])
        )
    )