from flet import Page, View, Text
from views.home import home_view
from views.calendar import calen_view
from views.study_places import study_places_view
from views.wikamp import wikamp_view
from views.open import open_view
from views.news import news_view
from views.more_info import study_place_details_view
from views.intro import intro_view

def initialize_page(page: Page):
    
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
        elif page.route == "/intro":
            page.views.append(intro_view(page))
        elif page.route == "/home":
            page.views.append(home_view(page))
        elif page.route == "/calendar":
            page.views.append(calen_view(page))
        elif page.route == "/study_places":
            page.views.append(study_places_view(page))
        elif page.route == "/wikamp":
            page.views.append(wikamp_view(page))
        elif page.route == "/news":
            page.views.append(news_view(page))
        elif page.route.startswith("/study_places_details/"):
            # Extract place name from the route
            place_name = page.route.split("/study_places_details/")[1]
            page.views.append(study_place_details_view(page, place_name))
        else:
            page.views.append(View("/", [Text("404 - Page not found")]))

        page.update()
    
    page.on_route_change = route_change
    page.go("/open")