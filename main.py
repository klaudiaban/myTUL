from flet import app, Page
from core.init import initialize_page

def main(page: Page):
    initialize_page(page)

if __name__ == "__main__":
    app(target=main, assets_dir="assets")


