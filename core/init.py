import flet as ft
from views.home import home_view
from views.calendar import calen_view
from views.study_places import study_places_view
from views.wikamp import wikamp_view
from views.location import location_view
from views.open import open_view

def initialize_page(page: ft.Page):
    
    # Page configuration
    from core.config import PAGE_CONFIG
    page.window.width = PAGE_CONFIG["width"]
    page.window.height = PAGE_CONFIG["height"]
    page.window.resizable = PAGE_CONFIG["resizable"]
    page.horizontal_alignment = PAGE_CONFIG["horizontal_alignment"]
    page.vertical_alignment = PAGE_CONFIG["vertical_alignment"]
    page.padding = PAGE_CONFIG["padding"]
    page.bgcolor = PAGE_CONFIG["bgcolor"]
    page.scroll = PAGE_CONFIG["scroll"]
    page.theme_mode = PAGE_CONFIG["theme_mode"]
    page.title = PAGE_CONFIG["title"]
    page.fonts = PAGE_CONFIG["fonts"]
    
    # Handle routing
    def route_change(e):
        page.views.clear()

        if page.route == "/open":
            page.views.append(open_view(page))
        elif page.route == "/home":
            page.views.append(home_view(page))
        elif page.route == "/calendar":
            page.views.append(calen_view(page))
        elif page.route == "/study_places":
            page.views.append(study_places_view(page))
        elif page.route == "/wikamp":
            page.views.append(wikamp_view(page))
        elif page.route == "/location":
            page.views.append(location_view(page))
        else:
            page.views.append(ft.View("/", [ft.Text("404 - Page not found")]))

        page.update()
    
    page.on_route_change = route_change
    page.go("/open")