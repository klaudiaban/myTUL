import flet as ft
from core.init import initialize_page

def main(page: ft.Page):
    initialize_page(page)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")