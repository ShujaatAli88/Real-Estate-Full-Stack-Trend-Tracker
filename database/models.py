from pydantic import BaseModel

class ZillowDataValidator(BaseModel):
    """This Model Will be Used to Validate the Extrcated Data from Zillow."""
    scraped_date: str
    status_type: str
    property_detail_url: str
    property_price: str
    property_address : str
    property_city : str
    property_state : str
    property_address_zip_code : str
    bedrooms_available : float | None = None
    bathrooms_available : float | None = None
    broker_name : str | None = None
    property_images : list