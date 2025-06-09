import flet as ft
import pandas as pd
from constants import *
from .helpers.appbar import create_appbar
from .helpers.helpers_study_places import FACILITY_COLUMNS, check_facilities, create_study_place_card

def study_places_view(page: ft.Page) -> ft.View:
    df = pd.read_csv("assets/info/study_places_table.csv")
    df = df.dropna(subset=["Name of the place", "Campus", "Building", "Name of image file"])

    appbar = create_appbar(page, route_back="/home", home=False)

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
                page,
                place['image_path'],
                place['name'],
                place['building'],
                place['facilities'],
            )
            cards.append(card)
        return cards

    def filter_places_by_search_and_amenities(search_text, selected_amenities):
        search_text = search_text.lower().strip()
        filtered = []

        for place in places_data:
            matches_amenity = "All" in selected_amenities or all(
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
