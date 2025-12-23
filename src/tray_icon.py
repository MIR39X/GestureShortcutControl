import pystray
from PIL import Image, ImageDraw
import threading

class TrayIcon:
    def __init__(self, on_settings, on_quit):
        self.on_settings = on_settings
        self.on_quit = on_quit
        self.icon = None

    def create_image(self):
        # Generate a simple icon (Green circle on black background)
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), (0, 0, 0))
        dc = ImageDraw.Draw(image)
        dc.ellipse((16, 16, 48, 48), fill='lightgreen')
        return image

    def setup_icon(self):
        menu = pystray.Menu(
            pystray.MenuItem("Settings", self.on_settings_clicked),
            pystray.MenuItem("Quit", self.on_quit_clicked)
        )
        self.icon = pystray.Icon("LazyHands", self.create_image(), "LazyHands", menu)

    def on_settings_clicked(self, icon, item):
        if self.on_settings:
            self.on_settings()

    def on_quit_clicked(self, icon, item):
        if self.on_quit:
            self.icon.stop()
            self.on_quit()

    def run(self):
        self.setup_icon()
        self.icon.run()

    def run_detached(self):
        # Run in a separate thread
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
