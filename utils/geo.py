import os

import requests


def create_address_dict(address_components):
    address_dict = {}
    for component in address_components:
        types = component["types"]
        for type_ in types:
            if type_ == "street_number":
                address_dict["incident_address_st_number"] = component["long_name"]
            elif type_ == "route":
                address_dict["incident_address_st_name"] = component["long_name"]
                # If needed, address type can be inferred from common street type names
                # This part assumes 'Avenue' is the type in this context
                address_dict["incident_address_st_type"] = "Ave"
            elif type_ == "neighborhood":
                address_dict["incident_address_neighborhood"] = component["long_name"]
            elif type_ == "sublocality" or type_ == "sublocality_level_1":
                address_dict["incident_city"] = component["long_name"]
            elif type_ == "administrative_area_level_2":
                address_dict["incident_county"] = component["long_name"]
            elif type_ == "administrative_area_level_1":
                address_dict["incident_state"] = component["short_name"]
            elif type_ == "country":
                address_dict["incident_country"] = component["short_name"]
            elif type_ == "postal_code":
                address_dict["incident_zip_code"] = component["long_name"]
    return address_dict


def get_geocode(lat, long):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{long}&key={os.environ['GOOGLE_MAP_API_KEY']}"
    response = requests.get(url)
    if response.ok:
        return create_address_dict(response.json()["results"][0]["address_components"])
    else:
        return response.raise_for_status()


def dms_to_dd(dms, ref):
    degrees, minutes, seconds = dms
    decimal_degrees = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
    if ref in ["S", "W"]:
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def extract_lat_lon(gps_info):
    lat = dms_to_dd(gps_info["GPSLatitude"], gps_info["GPSLatitudeRef"])
    lon = dms_to_dd(gps_info["GPSLongitude"], gps_info["GPSLongitudeRef"])
    return (lat, lon)


if __name__ == "__main__":
    gps_info = {"latitude": 37.7749, "longitude": 122.4194}

    address = get_geocode(lat=40.714224, long=-73.961452)
    print(address)
