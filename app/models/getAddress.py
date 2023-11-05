from PIL import Image
from io import BytesIO
import base64


from geopy.geocoders import OpenCage
from geopy.exc import GeocoderTimedOut
from opencage.geocoder import OpenCageGeocode
from pprint import pprint


from app.models.sampleDate import dataUrl


# Replace with your OpenCage Data API key
api_key = "e2ed6602b3724c6980aabeaba286c11b"


def reverse_geocode(latitude: float, longitude: float, api_key):
    geolocator = OpenCage(api_key=api_key)
    # print("GPS", latitude, longitude)

    try:
        geocoder = OpenCageGeocode(api_key)
        results = geocoder.reverse_geocode(latitude, longitude)
        return results[0]["formatted"]
        # addres = results["results"][0]["components"]["street"]
    except GeocoderTimedOut:
        print("Geocoding service timed out. Try again later.")
        return "Address not found"


def extract_exif_from_dataurl(dataurl):
    try:
        # Split the data URL to get the image data part (after "base64,")
        data = dataurl.split(",")[1]

        # Decode the Base64 data
        image_data = base64.b64decode(data)

        # Create a BytesIO object to open the image using Pillow
        image_stream = BytesIO(image_data)

        # Open the image using Pillow
        img = Image.open(image_stream)

        # Check if the image format is supported (PNG or JPEG)
        if img.format not in ["PNG", "JPEG"]:
            raise ValueError("Unsupported image format")

        # Extract EXIF data
        exif_data = img._getexif()

        # If exif_data is None, try using the getexif method
        if exif_data is None:
            exif_data = img.getexif()

        return exif_data
    except Exception as e:
        print(f"Error: {e}")
        return None


def extract_gps_and_time(exif_data):
    gps_info = None
    time_info = None

    if exif_data:
        # Extract GPS information
        gps_info = exif_data.get(34853)  # 34853 corresponds to GPS info in EXIF data

        # Extract time information
        time_info = exif_data.get(
            36867
        )  # 36867 corresponds to DateTimeOriginal in EXIF data

    return gps_info, time_info


def gps_tuple_to_float(gps_tuple, convert=False):
    if len(gps_tuple) != 3:
        raise ValueError(
            "GPS tuple should have three elements (degrees, minutes, seconds)"
        )

    degrees, minutes, seconds = gps_tuple
    decimal_degrees = float(degrees + minutes / 60 + seconds / 3600)
    return decimal_degrees if convert else -decimal_degrees


def getAddressFromDataUrl(dataUrl: str = dataUrl) -> str:
    exif_data = extract_exif_from_dataurl(dataUrl)
    if exif_data:
        # print(exif_data)
        gps_info, time_info = extract_gps_and_time(exif_data)

        if gps_info:
            # print("GPS Info:\n", gps_info)
            latitude = gps_info.get(2, None)
            longitude = gps_info.get(4, None)
            convertLatitude = gps_info.get(1, 'N') == 'N'
            convertLongitude = gps_info.get(3, 'E') == 'E'
            address = reverse_geocode(
                gps_tuple_to_float(latitude, convert=convertLatitude),
                gps_tuple_to_float(longitude, convert=convertLongitude),
                api_key,
            )
            print("Address:", address)
            return address

        if time_info:
            print(f"DateTimeOriginal: {time_info}")

    return ""


if __name__ == "__main__":
    getAddressFromDataUrl()
