import re
from collections import (
    namedtuple,
)

from DrissionPage import (
    Chromium,
    ChromiumOptions,
)
from pyvirtualdisplay import (
    Display,
)


ProductData = namedtuple("Product", ("name", "price"))


class OzonParser:
    name_product_xpath = ".lt7_27 tsHeadline550Medium"
    price_product_xpath = ".l6s_27 sl4_27"

    def __init__(self, url: str) -> None:
        self.display = Display(visible=False, size=(1920, 1080), backend="xvfb")
        self.url = url
        self.tab = None

    async def parse(self) -> ProductData:
        self.display.start()
        self.init_tab()
        name = self.get_name()
        price = self.get_price()
        self.display.stop()

        return ProductData(name=name, price=price)

    def init_tab(self) -> None:

        co = ChromiumOptions()
        co.headless(False)
        co.set_argument("--no-sandbox")
        co.set_argument("--disable-infobars")
        co.set_argument("--disable-extensions")
        co.set_argument("--no-first-run --no-service-autorun --password-store=basic")
        co.set_argument("--start-maximized")
        co.set_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        )
        self.tab = Chromium(co).latest_tab
        self.tab.run_js("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.navigator.chrome = {runtime: {}};
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        """)
        self.tab.run_js("""
            const mouseEvent = document.createEvent('MouseEvents');
            mouseEvent.initMouseEvent('mousemove', true, true, window, 1, 0, 0, 10, 10, false, false, false, false, 0, null);
            document.dispatchEvent(mouseEvent);
        """)
        self.tab.get(self.url)

    def get_elem_by_xpath(self, xpath: str, pattern: str | None = None) -> str:
        tags = self.tab.eles(xpath)

        if tags:
            text = tags[0].text

            if pattern:
                if match := re.search(pattern, text):
                    text = match.group()

            return text

        return ""

    def get_name(self) -> str:
        return self.get_elem_by_xpath(self.name_product_xpath)

    def get_price(self) -> str:
        return self.get_elem_by_xpath(self.price_product_xpath, r"\d+")
