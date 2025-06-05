from enum import Enum

DATA_DIRECTORY = "data"
LOGS_FILE_NAME = "zillow_crawler.log"

class ZillowURLs(Enum):
    """
    Enum for Zillow URLs.
    """
    BASE_URL = "https://www.zillow.com/async-create-search-page-state"

class ZillowRequestConstants(Enum):
    """
    Constants for Zillow API requests.
    """
    cookies = {
        'web-platform-data': '%7B%22wp-dd-rum-session%22%3A%7B%22doNotTrack%22%3Atrue%7D%7D',
        'zguid': '24|%24c591ffd1-cf7d-4c6b-be66-7910d15703a7',
        'zgsession': '1|9d5d2991-31d4-44d9-8937-059dd60a088b',
        '_ga': 'GA1.2.172887670.1748956541',
        '_gid': 'GA1.2.1425692023.1748956541',
        'zjs_anonymous_id': '%22c591ffd1-cf7d-4c6b-be66-7910d15703a7%22',
        'zg_anonymous_id': '%221d94c3f4-a2d9-4162-8caa-4a67c372923f%22',
        'JSESSIONID': '9BB023C60F8834259E7E48D9B4FB325D',
        'pxcts': 'd98efc18-407c-11f0-bb9a-a0628ed6130e',
        '_pxvid': 'd98ee969-407c-11f0-bb9a-201a6d8b7dcb',
        'zjs_user_id_type': '%22encoded_zuid%22',
        '_px3': '462a5a046246b989932a94098fa2a68a86d57b11c145819d43b136ec5b3b2994:CFsh3R42fwrNcNLWvS+PDExj4nbepYqVe/lK6PrZE0OqpIF3bpZRQnCE8ODE6/2tTXZnZHsk+PFCQtp1dE6iYw==:1000:0jUhRN9MHd2bcBykWXyTIaGQJU4KAFH8WhkFLOMky1CnZpCm4bIBhWXxtSUS19L4Cr2W5HMmNcQKa0jkLULRfiGsowQVGn6l8cVC07rd4Dis9+vxHY0jqFD0j0QtTiL75kaZhSh7uU5r/wF1g+RJ9TTTLVaw1Pyie3YeJl0HbvQC0g+0SSxSnK2cz68sMtpeENzzK6TCeOSdWJXCVcNallcZjdYnKjuaar/dqV2l8N8=',
        '_gcl_au': '1.1.2099854350.1748956548',
        '_rdt_uuid': '1748956549042.1348e3ac-7d57-4045-87be-8d789bb1fb22',
        '_scid': 'PHmR1rZhqTqVmNSTYWyY7VOOXVX4jg0m',
        '_scid_r': 'PHmR1rZhqTqVmNSTYWyY7VOOXVX4jg0m',
        'DoubleClickSession': 'true',
        '_fbp': 'fb.1.1748956549771.899370975755732088',
        '_uetsid': 'de592e10407c11f08db7ddf113c63c68',
        '_uetvid': 'de597200407c11f0a69f95b0064f6ce5',
        '_tt_enable_cookie': '1',
        '_ttp': '01JWTYY4WM60H1W80DEABFEYAN_.tt.1',
        '_pin_unauth': 'dWlkPU16Um1OVGsyWkdRdE56RXlZUzAwTnpobUxXRTFZVFV0WkRJeFl6Z3hZVEUzWmpNdw',
        '_ScCbts': '%5B%5D',
        'tfpsi': '70cadd21-4311-4a4f-953e-a3f069e8c780',
        '_clck': 'rfztxg%7C2%7Cfwg%7C0%7C1980',
        '_sctr': '1%7C1748890800000',
        'userid': 'X|3|3be30ac9910c4fc2%7C10%7CgruIjWWDlFrKPjjq_Qjjd6kEpgGoQDYCeHnzGJuVmuY%3D',
        'ZILLOW_SID': '1|AAAAAVVbFRIBVVsVEsXnP3xr6WfsNISatl9agqMeIKhl1WL8xNZFVyqum%2Ftq67jSs4IaJWscCYANvKDfwdUSKq8cuBfGBEtIfQ',
        'loginmemento': '1|b9e4b34cd84ee3231db624f04b1f1be68c32dc60633579ca0c240ef18bf07f21',
        'ZILLOW_SSID': '1|AAAAAVVbFRIBVVsVEtO%2BoiL%2F%2B1sLsYsqQwy1mRjIEvzRVDlefBFrUhw7mvJ1k2oVe%2FKr%2F7t9Qwili8e6uE51V7rsoGQFWP0GXQ',
        'zjs_user_id': '%22X1-ZU17fbknf22dr7t_3wgux%22',
        'AWSALB': 'q15revq/0RkU8oOM45o9p9lUfJ7qfh9gmPVw65JCOPSbwPNwFJ/4wJW+QZHpdz4KYkFg+MHfHQjSEINlO/Qt6cQRHdGYCcMFlfFyo4JJScfaD6y12x3O2TJphXK5',
        'AWSALBCORS': 'q15revq/0RkU8oOM45o9p9lUfJ7qfh9gmPVw65JCOPSbwPNwFJ/4wJW+QZHpdz4KYkFg+MHfHQjSEINlO/Qt6cQRHdGYCcMFlfFyo4JJScfaD6y12x3O2TJphXK5',
        '__gads': 'ID=79d396f9415384b7:T=1748956555:RT=1748956555:S=ALNI_Mbpf87ya-P-diL5C4KqEVk2gH7xZA',
        '__gpi': 'UID=000010ce276441ae:T=1748956555:RT=1748956555:S=ALNI_MaMdFDT2QDhZqwIGGBtxr_Jbnk-Rg',
        '__eoi': 'ID=f869d2a6ef12cc76:T=1748956555:RT=1748956555:S=AA-Afja7WnUfsqeVyj7aFOpjmOLd',
        'search': '6|1751548583695%7Crect%3D40.03994895103091%2C-104.41790186718751%2C39.49739731693118%2C-105.26384913281251%26rid%3D11093%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26singlestory%3D0%26housing-connector%3D0%26parking-spots%3Dnull-%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26showcase%3D0%26featuredMultiFamilyBuilding%3D0%26onlyRentalStudentHousingType%3D0%26onlyRentalIncomeRestrictedHousingType%3D0%26onlyRentalMilitaryHousingType%3D0%26onlyRentalDisabledHousingType%3D0%26onlyRentalSeniorHousingType%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0911093%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Afalse%7D%09%09%09%09%09',
        'ttcsid': '1748956550061::Gfd3V6AKB1XVFA-ZbfI9.1.1748956583906',
        '_clsk': 's1fc2o%7C1748956585337%7C2%7C0%7Ci.clarity.ms%2Fcollect',
        'ttcsid_CN5P33RC77UF9CBTPH9G': '1748956550060::xRL0K0U9-7CT1eIwIWCD.1.1748956589113',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.zillow.com',
        'priority': 'u=1, i',
        'referer': 'https://www.zillow.com/denver-co/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Afalse%2C%22mapBounds%22%3A%7B%22west%22%3A-105.26384913281251%2C%22east%22%3A-104.41790186718751%2C%22south%22%3A39.49739731693118%2C%22north%22%3A40.03994895103091%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A11093%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }

    json_data = {
        'searchQueryState': {
            'pagination': {
                'currentPage': 1,
            },
            'isMapVisible': False,
            'mapBounds': {
                'west': -105.26384913281251,
                'east': -104.41790186718751,
                'south': 39.49739731693118,
                'north': 40.03994895103091,
            },
            'regionSelection': [
                {
                    'regionId': 11093,
                    'regionType': 6,
                },
            ],
            'filterState': {
                'sortSelection': {
                    'value': 'globalrelevanceex',
                },
            },
            'isListVisible': True,
        },
        'wants': {
            'cat1': [
                'listResults',
            ],
            'cat2': [
                'total',
            ],
        },
        'requestId': 4,
        'isDebugRequest': False,
    }