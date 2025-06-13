from flet import Page, View, Geolocator, GeolocatorSettings, GeolocatorPositionAccuracy, Colors, Column, Text, TextField, IconButton, Icons, Row, MainAxisAlignment, CrossAxisAlignment, Container, Chip, BorderSide, ScrollMode, border_radius, TextStyle
import pandas as pd
from constants import *
from .helpers.appbar import create_appbar
from .helpers.helpers_study_places import FACILITY_COLUMNS, check_facilities, create_study_place_card
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

def study_places_view(page: Page) -> View:
    gl = Geolocator(
        location_settings=GeolocatorSettings(
            accuracy=GeolocatorPositionAccuracy.HIGH
        ),
    )

    page.overlay.append(gl)

    sort_by_location_enabled = False

    async def handle_get_current_position(e):
        nonlocal sort_by_location_enabled
        if not sort_by_location_enabled:
            p = await gl.get_current_position_async()
            location = (p.latitude, p.longitude)
            print(f"get_current_position: {location}")

            geolocator = Nominatim(user_agent="my_tracking_app_12345")
            location_info = geolocator.reverse(location, language='pl')
            print("Address:", location_info.address)

            on_location_received(location)

            sort_location_button.icon_color = TUL_DARK_RED
        else:
            # Disable sorting if already enabled
            sort_by_location_enabled = False
            update_content_based_on_filters(search_field.value)
            sort_location_button.icon_color = Colors.GREY_700

        page.update()

    df = pd.read_csv("assets/info/study_places_table.csv")
    df = df.dropna(subset=["Name of the place", "Campus", "Building", "Name of image file"])

    user_location = [None, None]

    def sort_by_distance(user_location, places):
        return sorted(
            places,
            key=lambda place: geodesic(
                (user_location[0], user_location[1]),
                (place['latitude'], place['longitude'])
            ).meters
        )
        
    def on_location_received(location):
        nonlocal sort_by_location_enabled
        user_location[0], user_location[1] = location
        sort_by_location_enabled = True  # enable sorting by location
        
        # Filter and sort
        filtered_places = filter_places_by_search_and_amenities(search_field.value, selected_amenities)
        sorted_places = sort_by_distance(location, filtered_places)

        content_column.controls = create_cards_from_data(sorted_places)
        page.update()

    appbar = create_appbar(page, route_back="/home", home=False)

    places_data = []
    for _, row in df.iterrows():
        facilities = check_facilities(row)
        place_data = {
            'image_path': row["Name of image file"],
            'name': row["Name of the place"],
            'building': row["Building"],
            'facilities': facilities,
            'latitude': float(row["Latitude"]),
            'longitude': float(row["Longitude"]),
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

    content_column = Column(controls=create_cards_from_data(places_data))

    def update_content_based_on_filters(current_search_text):
        filtered_places = filter_places_by_search_and_amenities(current_search_text, selected_amenities)
        
        if sort_by_location_enabled and user_location[0] is not None:
            filtered_places = sort_by_distance(user_location, filtered_places)
        
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
        chip = Chip(
            border_side=BorderSide(color=Colors.GREY_300, width=1),
            check_color=TUL_RED,
            label=Text(amenity, font_family="Trasandina", size=16, color=TUL_DARK_RED),
            bgcolor=Colors.WHITE,
            on_select=lambda e, amenity=amenity: amenity_selected(e, amenity),
            selected=(amenity == "All")
        )
        amenity_chips.append(chip)

    search_field = TextField(
        hint_text="Search for a place", 
        hint_style=TextStyle(font_family="Trasandina", size=18, color=Colors.GREY_700),
        width=300, 
        height=40,
        dense=True,
        border_color=Colors.GREY_300,
        border_radius=border_radius.all(10),
        on_change=lambda e: update_content_based_on_filters(e.control.value),
        text_style=TextStyle(font_family="Trasandina", size=18, color=Colors.GREY_700)
    )

    sort_location_button = IconButton(
        icon=Icons.MY_LOCATION,
        icon_color=Colors.GREY_700, 
        tooltip="Toggle sort by distance",
        icon_size=28,
        on_click=handle_get_current_position
    )

    search_row = Row(
        spacing=5,
        alignment=MainAxisAlignment.CENTER,
        vertical_alignment=CrossAxisAlignment.CENTER,
        controls=[
            search_field,
            sort_location_button
        ]
    )

    return View(
        route="/study_places", 
        appbar=appbar,
        padding=10,
        bgcolor=Colors.WHITE, 
        scroll=ScrollMode.AUTO, 
        controls=[
            Column([
                search_row,
                Row(scroll=ScrollMode.HIDDEN, controls=amenity_chips),
                Container(content=content_column)
            ], spacing=20, horizontal_alignment=CrossAxisAlignment.CENTER)
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER
    )
