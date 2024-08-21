import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HotelsSpider(scrapy.Spider):
    name = "hotels"
    start_urls = [
        "https://www.resortpass.com/results?state=CA"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10
            )

    def parse(self, response):
        driver = response.meta['driver']

        self.logger.info("Starting to click 'Show More' buttons")

        while True:
            try:
                show_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show more hotels')]"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
                show_more_button.click()
                WebDriverWait(driver, 5).until(EC.staleness_of(show_more_button))
                self.logger.info("Clicked 'Show More' button")
            except Exception as e:
                self.logger.info(f"No more 'Show More' button found or error: {e}")
                break

        self.logger.info("Parsing the page content")

        html = driver.page_source
        response = scrapy.Selector(text=html)

        # Update the selector based on actual page structure
        hotels = response.xpath('//div[contains(@class, "hotel-class-selector")]')

        for hotel in hotels:
            hotel_name = hotel.xpath('.//h2/text()').get().strip()
            hotel_link = hotel.xpath('.//a[contains(@class, "hotel-link-class")]/@href').get()
            hotel_link = response.urljoin(hotel_link)

            yield {
                'name': hotel_name,
                'url': hotel_link
            }
