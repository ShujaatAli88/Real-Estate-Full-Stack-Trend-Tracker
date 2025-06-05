def snake_to_title(key_value):
        """convert The Data into appropriate format."""
        
        return key_value.replace("_"," ")
                

if __name__ == "__main__":
        data_dic = {
            "status_type": "status_type",
            "property_detail_url": "property_detail_url",
            "property_price": "property_price",
            "property_address" : "property_address",
            "Property_City" : "city",
            "Property State" : "state",
            "property_address_zip_code" : "address_zip_code",
            "Bedrooms_available" : "bedrooms",
            "Bathrooms_available" : "bathrooms",
            "Broker_Name" : "broker_name",
            "Property_Pucs" : "property_images"
        }
        data = {
            snake_to_title(key): value for key, value in data_dic.items()
        }
        print(data)