import boto3
import uvicorn
from fastapi import Depends, Request
from fastapi import FastAPI, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.models.aws_identity_document_parser import IdentityDocParser
from app.models.database import SessionLocal, Base, engine
from app.models.report import Report
from app.schemas import ReportUpdate

from app.models.getAddress import getAddressFromDataUrl

app = FastAPI()

# Amazon Textract client
textract = boto3.client("textract", region_name="us-west-2")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()  # Replace with your actual database session maker
    try:
        yield db
    finally:
        db.close()


@app.post("/update_report/")
async def update_report_endpoint(
    request: Request, update_data: ReportUpdate, db: Session = Depends(get_db)
):
    # Extract session_id from the request header
    session_id = request.headers.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID is required.")

    # Fetch or create the report by session_id
    report = db.query(Report).filter(Report.session_id == session_id).first()
    if report:
        # If the report exists, update it with the provided data
        for var, value in vars(update_data).items():
            setattr(report, var, value) if value is not None else None
        db.commit()
        return report
    else:
        # If the report does not exist, create a new one
        new_report_data = update_data.model_dump(exclude_defaults=True)
        new_report = Report(session_id=session_id, **new_report_data)
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return new_report


@app.post("/analyze_driver_license/")
async def analyze_driver_license(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="No file found in the request")

    def process_file(file):
        try:
            contents = file.file.read()
            textract_result = textract.analyze_id(DocumentPages=[{"Bytes": contents}])
            return file.filename, IdentityDocParser.parse(textract_result)
        except Exception as e:
            return file.filename, None

    result = process_file(file)

    if result is not None:
        return {"ocr_result": result}
    else:
        raise HTTPException(status_code=400, detail="Failed to process file")


@app.post("/get_address/")
def get_address(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="No file found in the request")

    result = getAddressFromDataUrl(file)

    if result is not None:
        return {"address": result}
    else:
        raise HTTPException(status_code=400, detail="Failed to process file")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
