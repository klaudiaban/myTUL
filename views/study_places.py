import flet as ft
import pandas as pd
from constants import *
from .ui_helpers import create_appbar

def study_places_view(page: ft.Page) -> ft.View:
    df = pd.read_csv("assets/info/study_places_table.csv")
    df = df.dropna(subset=["Name of the place", "Campus", "Building", "Name of image file"])

    FACILITY_COLUMNS = [
        "Group", "Individual", "Cafeteria", "Power Outlets",
        "Whiteboards", "Computers", "Comfortable chairs/Poufs/Couches"
    ]

    def create_study_place_card(image_path, name, building, facilities, on_more_info=lambda e: page.go("/study_place_details"), availability="Available"):
        availability_color = ft.colors.GREEN if availability == "Available" else ft.colors.RED

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

    appbar = create_appbar(page, route_back="/home", home=False)

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

    places_data = []
    for _, row in df.iterrows():
        facilities = check_facilities(row)
        place_data = {
            'image_path': row["Name of image file"],
            'name': row["Name of the place"],
            'building': row["Building"],
            'facilities': facilities
        }
        places_data.append(place_data)

    def create_cards_from_data(data_list):
        cards = []
        for place in data_list:
            card = create_study_place_card(
                place['image_path'],
                place['name'],
                place['building'],
                place['facilities'],
                lambda e: page.go("/study_place_details")
            )
            cards.append(card)
        return cards

    def filter_places_by_search_and_amenities(search_text, selected_amenities):
        search_text = search_text.lower().strip()
        filtered = []

        for place in places_data:
            matches_amenity = "All" in selected_amenities or any(
                amenity in place['facilities'] for amenity in selected_amenities
            )
            matches_search = search_text in place['name'].lower()
            
            if matches_amenity and matches_search:
                filtered.append(place)

        return filtered

    selected_amenities = set(["All"])
    amenities = ["All", "Campus A", "Campus B"] + FACILITY_COLUMNS
    amenity_chips = []

    content_column = ft.Column(controls=create_cards_from_data(places_data))

    def update_content_based_on_filters(current_search_text):
        filtered_places = filter_places_by_search_and_amenities(current_search_text, selected_amenities)
        content_column.controls = create_cards_from_data(filtered_places)
        page.update()

    def amenity_selected(e, amenity):
        nonlocal selected_amenities
        
        if amenity == "All":
            if e.control.selected:
                selected_amenities = set(["All"])
                for chip in amenity_chips:
                    chip.selected = (chip.label.value == "All")
            else:
                if len(selected_amenities) == 1 and "All" in selected_amenities:
                    e.control.selected = True
                    page.update()
                    return
                else:
                    selected_amenities.discard("All")
        else:
            if "All" in selected_amenities:
                selected_amenities.remove("All")
                for chip in amenity_chips:
                    if chip.label.value == "All":
                        chip.selected = False
                        break
            
            if e.control.selected:
                selected_amenities.add(amenity)
            else:
                selected_amenities.discard(amenity)
        
        if not selected_amenities:
            selected_amenities = set(["All"])
            for chip in amenity_chips:
                chip.selected = (chip.label.value == "All")

        update_content_based_on_filters(search_field.value)

    for amenity in amenities:
        chip = ft.Chip(
            border_side=ft.BorderSide(color=ft.colors.GREY_300, width=1),
            check_color=TUL_RED,
            label=ft.Text(amenity, font_family="Trasandina", size=16, color=TUL_DARK_RED),
            bgcolor=ft.Colors.WHITE,
            on_select=lambda e, amenity=amenity: amenity_selected(e, amenity),
            selected=(amenity == "All")
        )
        amenity_chips.append(chip)

    search_field = ft.TextField(
        hint_text="Search for a place", 
        hint_style=ft.TextStyle(font_family="Trasandina", size=18, color=ft.colors.GREY_700),
        width=350, 
        height=50,
        border_color=ft.colors.GREY_300,
        border_radius=ft.border_radius.all(10),
        on_change=lambda e: update_content_based_on_filters(e.control.value),
        text_style=ft.TextStyle(font_family="Trasandina", size=18, color=ft.colors.GREY_700),
    )

    return ft.View(
        route="/study_places", 
        appbar=appbar,
        padding=10,
        bgcolor=ft.colors.WHITE, 
        scroll=ft.ScrollMode.AUTO, 
        controls=[
            ft.Column([
                search_field,
                ft.Row(scroll=ft.ScrollMode.HIDDEN, controls=amenity_chips),
                ft.Container(content=content_column)
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
