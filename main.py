import flet as ft
import flet_easy as fs
from views.home import *
from constants import *
from views.calendar import *
from views.study_places import *

def main(page: ft.Page):

    app = fs.FletEasy(
        route_init='/home/init', on_Keyboard=True
    )

    @app.config
    def config(page: ft.Page):
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

    app.add_pages([home])
    app.add_pages([calen])
    app.add_pages([study_places])

    app.start(page)

ft.app(target=main, assets_dir="assets")