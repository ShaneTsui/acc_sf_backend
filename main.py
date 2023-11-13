import base64
import io
import logging
import pickle

import aiofiles
import boto3
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from app.models.aws_identity_document_parser import IdentityDocParser
from utils.geo import extract_lat_lon, get_geocode

app = FastAPI()

# TODO: Change this to the actual frontend URL
allow_origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_FILE_PATH = "report_database.pkl"
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load_db():
    try:
        with open(DATABASE_FILE_PATH, "rb") as db_file:
            return pickle.load(db_file)
    except (FileNotFoundError, EOFError):
        with open(DATABASE_FILE_PATH, "wb") as db_file:
            pickle.dump({}, db_file)
        return {}


def save_database(report_database):
    with open(DATABASE_FILE_PATH, "wb") as db_file:
        pickle.dump(report_database, db_file)


# Amazon Textract client
textract = boto3.client("textract", region_name="us-west-2")


@app.get("/hello")
async def hello():
    return "Hello SnapReport!"


@app.get("/get_report/")
async def get_report_endpoint():
    return load_db()


@app.post("/update_report/")
async def update_report_endpoint(update_data: dict):
    report_database = load_db()
    report_database.update(update_data)
    save_database(report_database)
    return report_database


@app.post("/analyze_driver_license/")
async def analyze_driver_license(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="No file found in the request")

    def process_file(file):
        try:
            contents = file.file.read()
            textract_result = textract.analyze_id(DocumentPages=[{"Bytes": contents}])
            return IdentityDocParser.parse(textract_result)
        except Exception as e:
            return None

    result = process_file(file)

    if result is not None:
        report_database = load_db()
        report_database.update(result)
        save_database(report_database)
        return report_database
    else:
        raise HTTPException(status_code=500, detail="Failed to process file")


class ImageData(BaseModel):
    image_base64: str


@app.post("/analyze_photo/")
async def analyze_photo(data: ImageData):
    try:
        logger.info("Received photo for analysis.")
        contents = base64.b64decode(data.image_base64)
        file_name = "temp_image.jpg"  # Temporary file name

        async with aiofiles.open(file_name, "wb") as f:
            await f.write(contents)
        logger.info(f"File written to disk: {file_name}")

        image = Image.open(io.BytesIO(contents))
        logger.info("Image opened for EXIF data extraction.")

        exif_data = image._getexif()
        logger.info("EXIF data extracted.")
        gps_info = get_gps_info(exif_data)
        logger.info("GPS info extracted from EXIF data.")
        lat, lon = extract_lat_lon(gps_info)
        logger.info(f"Latitude and Longitude extracted: {lat}, {lon}")
        update_data = get_geocode(lat, lon)
        logger.info(f"Geocode information retrieved: {update_data}")
        report_database = load_db()
        logger.info("Database loaded.")
        report_database.update(update_data)
        logger.info("Database updated with new data.")
        save_database(report_database)
        logger.info("Database saved.")
        return report_database
    except Exception as e:
        logger.error(f"Error encountered: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


def get_gps_info(exif_data):
    gps_info = {}
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            for gps_tag in value:
                sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                gps_info[sub_decoded] = value[gps_tag]
    return gps_info
