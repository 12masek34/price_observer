import re
from dataclasses import (
    dataclass,
)

from DrissionPage import (
    Chromium,
    ChromiumOptions,
)
from pyvirtualdisplay import (
    Display,
)

from app.config.settings import (
    PARSE_RETRIES,
    PARSE_TIMEOUT,
    log,
)


@dataclass(frozen=True)
class ProductData:
    name: str
    price: float


class BaseParser:
    name_product_xpath = None
    price_product_xpath = None
    price_re = None

    def __init__(self, url: str) -> None:
        self.display = Display(visible=False, size=(1920, 1080), backend="xvfb")
        self.url = url
        self.tab = None
        self.retries = PARSE_RETRIES
        self.timeout = PARSE_TIMEOUT

    async def parse(self) -> ProductData | None:
        self.display.start()
        await self.init_tab()
        import pdb; pdb.set_trace();
        name = self.get_name()

        if not name:
            return

        price = self.get_price()

        if not price:
            return

        self.display.stop()

        return ProductData(name=name, price=price)

    async def init_tab(self) -> bool | None:

        co = ChromiumOptions()
        co.headless(False)
        co.set_argument("--no-sandbox")
        co.set_argument("--disable-infobars")
        co.set_argument("--disable-extensions")
        co.set_argument("--no-first-run")
        co.set_argument("--no-service-autorun")
        co.set_argument("--password-store=basic")
        co.set_argument("--start-maximized")
        co.set_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        )
        self.tab = Chromium(co).latest_tab
        self.run_js()
        self.connect()

    def run_js(self):
        for _ in range(self.retries):
            try:
                self.tab.run_js("""
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    window.navigator.chrome = {runtime: {}};
                    Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru']});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
                    const mouseEvent = document.createEvent('MouseEvents');
                    mouseEvent.initMouseEvent('mousemove', true, true, window, 1, 0, 0, 10, 10, false, false, false, false, 0, null);
                    document.dispatchEvent(mouseEvent);
                """)
            except Exception:
                continue
            else:
                return

    def connect(self) -> None:
        self.tab.get(self.url, retry=self.retries, timeout=self.timeout)

    def get_elem_by_xpath(self, xpaths: str, pattern: str | None = None) -> str:
        for xpath in xpaths:
            for _ in range(self.retries):
                try:
                    tag = self.tab.ele(xpath, timeout=self.timeout)
                except Exception:
                    log.error(f"Ошибка при парсинге html")
                    self.connect()
                    continue

                if not tag:
                    self.connect()
                    continue

                if tag:
                    text = self.clean_text(tag.text)

                    if pattern:
                        if match := re.findall(pattern, text):
                            if match:
                                text = match[0]

                    return text

        return ""

    def clean_text(self, text: str | None) -> str:
        if text:
            result = repr(text).replace(r"\u2009", "").replace(r"\n", "")

            if result and result.startswith("'"):
                result = result[1:]

            if result and result.endswith("'"):
                result = result[:-1]

            return result

        else:
            return ""


    def get_name(self) -> str:
        return self.get_elem_by_xpath(self.name_product_xpath)

    def get_price(self) -> str:
        return self.get_elem_by_xpath(self.price_product_xpath, self.price_re)
