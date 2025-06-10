import flet as ft
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
    availability_color = ft.colors.GREEN if availability == "Available" else ft.colors.RED

    on_more_info=lambda e: page.go(f"/study_places_details/{name}")

    # Create facility chips
    facility_chips = []
    for facility in facilities:
        facility_chips.append(
            ft.Chip(
                label=ft.Text(facility, size=14, font_family="Trasandina", color=ft.colors.BLACK),
                bgcolor=ft.colors.WHITE,
                border_side=ft.BorderSide(color=ft.colors.INDIGO_200, width=1),
            )
        )

    if "HEIC" in image_path:
        image_path = image_path.replace("HEIC", "jpg")

    return ft.Card(
        width=350,
        shape=ft.RoundedRectangleBorder(radius=12),
        shadow_color=ft.colors.GREY_100,
        content=ft.Container(
            padding=10,
            border_radius=12,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Column([
                ft.Container(
                    content=ft.Image(src=f"assets/study_places_images/{image_path}", height=180, width=350, fit=ft.ImageFit.COVER),
                    border_radius=12,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ),
                ft.Row(
                    height=30,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(name, size=22, weight=ft.FontWeight.BOLD, font_family="Trasandina"),
                    ]
                ),
                ft.Text(building, size=16, color=ft.colors.GREY_700, font_family="Trasandina"),
                ft.Container(
                    content=ft.Row(
                        controls=facility_chips,
                        wrap=True,
                        spacing=5,
                        run_spacing=5
                    ),
                    padding=ft.padding.symmetric(vertical=5)
                ),
                ft.Row(
                    height=30,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            availability,
                            size=16,
                            color=availability_color,
                            weight=ft.FontWeight.BOLD,
                            font_family="Trasandina"
                        ),
                        ft.ElevatedButton(
                            text="More Info",
                            color=ft.colors.INDIGO_500,
                            on_click=on_more_info,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                        )
                    ]
                )
            ])
        )
    )