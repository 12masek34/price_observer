import re
from dataclasses import (
    dataclass,
)
from time import sleep

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
        name = self.get_name()

        if not name:
            return

        price = self.get_price()

        if not price:
            return

        self.display.stop()

        return ProductData(name=name, price=float(price))

    async def init_tab(self) -> bool | None:

        co = ChromiumOptions()
        co.headless(False)
        co.set_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        )
        co.set_argument("--no-sandbox")
        co.set_argument("--disable-infobars")
        co.set_argument("--disable-extensions")
        co.set_argument("--no-first-run")
        co.set_argument("--no-service-autorun")
        co.set_argument("--password-store=basic")
        co.set_argument("--start-maximized")
        co.set_argument("--remote-allow-origins=*")
        co.set_argument("--no-first-run")
        co.set_argument("--no-service-autorun")
        co.set_argument("--no-default-browser-check")
        co.set_argument("--homepage=about:blank")
        co.set_argument("--no-pings")
        co.set_argument("--password-store=basic")
        co.set_argument("--disable-infobars")
        co.set_argument("--disable-breakpad")
        co.set_argument("--disable-component-update")
        co.set_argument("--disable-backgrounding-occluded-windows")
        co.set_argument("--disable-renderer-backgrounding")
        co.set_argument("--disable-background-networking")
        co.set_argument("--disable-dev-shm-usage")
        co.set_argument("--disable-features=IsolateOrigins,site-per-process")
        co.set_argument("--disable-session-crashed-bubble")
        co.set_argument("--disable-search-engine-choice-screen")
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

                    const getParameter = WebGLRenderingContext.prototype.getParameter;
                    WebGLRenderingContext.prototype.getParameter = function(param) {
                        if (param === 37445) return 'Intel Inc.';
                        if (param === 37446) return 'Intel(R) UHD Graphics 620';
                        return getParameter.apply(this, arguments);
                    };

                    HTMLCanvasElement.prototype.getContext = (function(orig) {
                        return function(type, attributes) {
                            let ctx = orig.call(this, type, attributes);
                            if (type === '2d') {
                                const fillText = ctx.fillText;
                                ctx.fillText = function() {
                                    return fillText.apply(this, arguments);
                                };
                            }
                            return ctx;
                        };
                    })(HTMLCanvasElement.prototype.getContext);

                    setInterval(() => {
                        const event = new MouseEvent('mousemove', {
                            bubbles: true,
                            cancelable: true,
                            clientX: Math.random() * window.innerWidth,
                            clientY: Math.random() * window.innerHeight
                        });
                        document.dispatchEvent(event);
                    }, 2000);

                    setTimeout(() => {
                        window.scrollTo({top: Math.random() * document.body.scrollHeight, behavior: 'smooth'});
                    }, 5000);
                """)
            except Exception:
                continue
            else:
                return

    def connect(self) -> None:
        self.tab.get(self.url, retry=self.retries, timeout=self.timeout)

    def get_elem_by_xpath(self, xpaths: str, pattern: str | None = None) -> str:

        for _ in range(self.retries):
            for xpath in xpaths:
                try:
                    sleep(2)
                    tag = self.tab.ele(xpath, timeout=self.timeout)
                except Exception:
                    log.error(f"Ошибка при парсинге html")
                    # self.connect()
                    self.tab.refresh()
                    continue

                if not tag:
                    log.info(f"не найден {xpath}")
                    # self.connect()
                    self.tab.refresh()
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
            result = repr(text).replace(r"\u2009", "").replace(r"\u2006", "").replace(r"\n", "")

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
        return self.get_elem_by_xpath(self.price_product_xpath, self.price_re).replace(" ", "")
