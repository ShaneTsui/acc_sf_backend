from sqlalchemy.orm import Session

from app.models.report import Report


def create_report(db: Session, report_data: dict) -> Report:
    report = Report(**report_data)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_report(db: Session, report_id: int) -> Report:
    return db.query(Report).filter(Report.id == report_id).first()


def get_reports(db: Session, skip: int = 0, limit: int = 100) -> list[Report]:
    return db.query(Report).offset(skip).limit(limit).all()


def update_report(db: Session, report_id: int, update_data: dict) -> Report:
    db.query(Report).filter(Report.id == report_id).update(update_data)
    db.commit()
    return get_report(db, report_id)


def delete_report(db: Session, report_id: int) -> None:
    report = db.query(Report).get(report_id)
    db.delete(report)
    db.commit()
