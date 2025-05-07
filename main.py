import flet as ft
from views.home import home_view
from views.calendar import calen_view
from views.study_places import study_places_view
from views.wikamp import wikamp_view
from constants import gradient_background

def main(page: ft.Page):

    # Page configuration
    page.window.width = 390
    page.window.height = 844
    page.window.resizable = False
    page.horizontal_alignment = 'center'
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.bgcolor = gradient_background
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "myTUL"
    page.fonts = {
        "Trasandina": "fonts/Trasandina.otf"
    }

    # Handle routing
    def route_change(e):
        page.views.clear()

        if page.route == "/home/init":
            page.views.append(home_view(page))
        elif page.route == "/calendar":
            page.views.append(calen_view(page))
        elif page.route == "/study_places":
            page.views.append(study_places_view(page))
        elif page.route == "/wikamp":
            page.views.append(wikamp_view(page))
        else:
            page.views.append(ft.View("/", [ft.Text("404 - Page not found")]))

        page.update()

    page.on_route_change = route_change
    page.go("/home/init")

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")