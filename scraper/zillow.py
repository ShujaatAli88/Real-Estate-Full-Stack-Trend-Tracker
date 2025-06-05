import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from constants import ZillowURLs, ZillowRequestConstants
from custom_exceptions import DataAPIRequestError
from utils import log_exception
import requests
import json
from log_handler import _logger
from database.models import ZillowDataValidator
from database.operations import insert_property_data
from datetime import date

class ZillowCrawler:
    def __init__(self):
        self.total_pages = None

    def data_api_request(self, page_number):
        """
        This method is a placeholder for making API requests to Zillow.
        It should be implemented to fetch data from the Zillow API.
        """
        try:
            ZillowRequestConstants.json_data.value["searchQueryState"]["pagination"][
                "currentPage"
            ] = f"{page_number}"
            _logger.info("Making API request to Fetch Data from Zillow.")
            response = requests.put(
                ZillowURLs.BASE_URL.value,
                # cookies=ZillowRequestConstants.cookies.value,
                headers=ZillowRequestConstants.headers.value,
                json=ZillowRequestConstants.json_data.value,
            )
            if response.status_code == 200:
                jsoned_data = json.dumps(response.json(), ensure_ascii=True, indent=4)
                with open("zillow_response.json", "w") as file:
                    file.write(jsoned_data)
                _logger.info("Data fetched successfully.")
                return response.json()
            else:
                _logger.error(
                    f"Failed to fetch data. Status code: {response.status_code}"
                )
                return None
        except Exception as e:
            sentry_message = (
                f"An error occurred while making the data API request for zillow: {e}"
            )
            log_exception(exception=DataAPIRequestError, message=sentry_message)
            _logger.error(
                "An error occurred while making the data API request for Zillow."
            )
            return None

    def parse_response(self, data_api_response):
        """
        This method is a placeholder for parsing the response from the Zillow API.
        It should be implemented to extract and process the data as needed.
        """
        try:
            _logger.info("Parsing response from Zillow API.")
            cat_1 = data_api_response.get("cat1")

            #get The total pages from the response...
            searchList = cat_1.get("searchList")
            self.total_pages = searchList.get("totalPages")
            if cat_1:
                searchResults = cat_1.get("searchResults")
                if searchResults:
                    listResults = searchResults.get("listResults")
                    if listResults:
                        _logger.info("Results Found.")
                        return listResults
                    else:
                        _logger.error("Results Not Found.")
                        return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            sentry_message = f"An error occurred while parsing the response: {e}"
            log_exception(exception=DataAPIRequestError, message=sentry_message)
            _logger.error("An error occurred while parsing the response from Zillow.")
            return False

    def validate_data(self, data_dic):
        """Use The Data Model to validate The Data Extrcated."""
        _logger.info("Validating The data.")
        data_model = ZillowDataValidator(
            scraped_date= data_dic["scraped_date"],
            status_type=data_dic["status_type"],
            property_detail_url=data_dic["property_detail_url"],
            property_price=data_dic["property_price"],
            property_address=data_dic["property_address"],
            property_city=data_dic["property_city"],
            property_state=data_dic["property_state"],
            property_address_zip_code=data_dic["property_address_zip_code"],
            bedrooms_available=data_dic["bedrooms_available"],
            bathrooms_available=data_dic["bathrooms_available"],
            broker_name=data_dic["broker_name"],
            property_images=data_dic["property_images"],
        )
        return data_model

    def snake_to_title(self, key_value):
        """convert The Data into appropriate format."""
        return key_value.replace("_", " ")


def main():
    zillow_crawler = ZillowCrawler()
    STATUS = True
    pages_availabale = True
    page_number = 1

    while pages_availabale:
        _logger.info(f"Processing Page Number:{page_number}")
        data_api_response = zillow_crawler.data_api_request(page_number)
        if not data_api_response:
            STATUS = False
            _logger.error("Data API request failed. Exiting...")
            return STATUS

        results_list = zillow_crawler.parse_response(data_api_response)
        if not results_list:
            _logger.error("Results List Not Found.")
            STATUS = False
            return STATUS

        _logger.info(f"Found {len(results_list)} records for page :{page_number}")
        for index, result in enumerate(results_list, start=1):
            _logger.info(f"Processing Record {index} of Page {page_number}")
            status_type = result.get("statusType")
            property_detail_url = result.get("detailUrl")
            property_price = result.get("price")
            property_address = result.get("address")
            city = result.get("addressCity")
            state = result.get("addressState")
            address_zip_code = result.get("addressZipcode")
            bedrooms = result.get("beds")
            bathrooms = result.get("baths")
            home_info = result.get("hdpData").get("homeInfo")
            home_info.get("homeType")
            broker_name = result.get("brokerName")
            property_pics = result.get("carouselPhotos")
            property_images = []
            if not property_pics:
                _logger.warning(
                    f"No property images found for Record {index} of Page {page_number}"
                )
                property_images = ["No Images Found"]
            else:
                for pic in property_pics:
                    url = pic.get("url")
                    property_images.append(url)

            data_dic = {
                "scraped_date": date.today().isoformat(),
                "status_type": status_type,
                "property_detail_url": property_detail_url,
                "property_price": property_price,
                "property_address": property_address,
                "property_city": city,
                "property_state": state,
                "property_address_zip_code": address_zip_code,
                "bedrooms_available": bedrooms,
                "bathrooms_available": bathrooms,
                "broker_name": broker_name,
                "property_images": property_images,
            }
            validated_data = zillow_crawler.validate_data(data_dic)
            model_data = validated_data.model_dump()

            data = {
                zillow_crawler.snake_to_title(key): value
                for key, value in model_data.items()
            }
            _logger.info(f"Data for Record {index} of Page {page_number}: {data}")

            # insert The Scraped Data into database...
            insert_property_data(data)
            
        if page_number == zillow_crawler.total_pages:
            _logger.info("All pages processed successfully.")
            pages_availabale = False
        else:
            _logger.info(
                f"Moving to the next page: {page_number + 1} of {zillow_crawler.total_pages}"
            )
            page_number += 1
