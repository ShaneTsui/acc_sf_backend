import io

import aiofiles
import boto3
import uvicorn
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from fastapi import FastAPI, UploadFile, HTTPException

from app.models.aws_identity_document_parser import IdentityDocParser
from utils.geo import extract_lat_lon, get_geocode

app = FastAPI()

report_database = {}

# Amazon Textract client
textract = boto3.client("textract", region_name="us-west-2")



@app.get("/get_report/")
async def get_report_endpoint():
    return report_database


@app.post("/update_report/")
async def update_report_endpoint(update_data: dict):
    report_database.update(update_data)


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
        report_database.update(result)
        return report_database
    else:
        raise HTTPException(status_code=500, detail="Failed to process file")


@app.post("/analyze_photo/")
async def analyze_photo(file: UploadFile):
    try:
        print("Start analyzing photo")
        contents = await file.read()
        async with aiofiles.open(file.filename, "wb") as f:
            await f.write(contents)
        image = Image.open(io.BytesIO(contents))
        exif_data = image._getexif()
        gps_info = get_gps_info(exif_data)
        lat, lon = extract_lat_lon(gps_info)
        update_data = get_geocode(lat, lon)

        report_database.update(update_data)
        return report_database
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()


def get_gps_info(exif_data):
    gps_info = {}
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            for gps_tag in value:
                sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                gps_info[sub_decoded] = value[gps_tag]
    return gps_info


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
