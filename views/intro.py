from flet import Page, View, CrossAxisAlignment, Colors, FilterQuality
import flet_video as fv
import asyncio

def intro_view(page: Page) -> View:
    page.title = "TheEthicalVideo"
    page.window.always_on_top = True

    sample_media = [
        fv.VideoMedia("assets/videos/intro.mp4"),
    ]

    async def delayed_navigation():
        await asyncio.sleep(3.5)
        print("4 seconds passed. Navigating to home view...")
        page.go("/open")

    def handle_video_loaded(e):
        print("Video loaded successfully!")
        page.run_task(delayed_navigation)

    video = fv.Video(
        expand=True,
        playlist=sample_media,
        playlist_mode=fv.PlaylistMode.SINGLE,
        fill_color=Colors.WHITE,
        aspect_ratio=16 / 9,
        volume=100,
        autoplay=True,
        filter_quality=FilterQuality.HIGH,
        muted=False,
        show_controls=False,
        on_loaded=handle_video_loaded,
        on_enter_fullscreen=lambda e: print("Video entered fullscreen!"),
        on_exit_fullscreen=lambda e: print("Video exited fullscreen!"),
    )

    return View(
        route="/intro",
        controls=[video],
        spacing=20,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )
