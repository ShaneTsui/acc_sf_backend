from typing import Optional

from sqlalchemy.orm import mapped_column, Mapped

from app.models.database import Base


class Report(Base):
    __tablename__ = "report"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column(unique=True)

    # From DL
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    dob_year: Mapped[str]
    dob_month: Mapped[str]
    dob_day: Mapped[str]
    gender: Mapped[str]

    home_address_st_number: Mapped[str]
    home_address_st_name: Mapped[str]
    # home_address_st_type: Mapped[str]
    # home_address_post_dir: Mapped[str]
    # home_address_apt_unit: Mapped[str]
    home_address_city: Mapped[str] = mapped_column(default="San Francisco")
    home_address_state: Mapped[str] = mapped_column(default="California")
    home_address_zip: Mapped[str]

    # Optional
    work_address_st_number: Mapped[str]
    work_address_st_name: Mapped[str]
    # work_address_st_type: Mapped[str]
    # work_address_post_dir: Mapped[str]
    # work_address_apt_unit: Mapped[str]
    work_address_city: Mapped[str]
    work_address_state: Mapped[str]
    work_address_zip: Mapped[str]

    # Second photo
    type: Mapped[str]
    make: Mapped[str]
    model: Mapped[str]
    color: Mapped[str]
    year: Mapped[str]
    license_plate_no: Mapped[str]
    licensing_state: Mapped[str]

    # From the photo
    incident_address_st_number: Mapped[str]
    incident_address_st_name: Mapped[str]
    incident_address_st_type: Mapped[str]
    incident_address_direction: Mapped[str]
    incident_address_apt_unit: Mapped[str]
    incident_city: Mapped[str] = mapped_column(default="San Francisco")
    incident_state: Mapped[str] = mapped_column(default="California")
    incident_zip_code: Mapped[str]
    incident_start_month: Mapped[str]
    incident_start_day: Mapped[str]
    incident_start_year: Mapped[str]
    incident_start_hour: Mapped[str]
    incident_start_minute: Mapped[str]
    incident_start_am_pm: Mapped[str]
    incident_end_month: Mapped[str]
    incident_end_day: Mapped[str]
    incident_end_year: Mapped[str]
    incident_end_hour: Mapped[str]
    incident_end_minute: Mapped[str]
    incident_end_am_pm: Mapped[str]

    street_address_section: Mapped[str]
    # use_standard_address: Mapped[bool]
    # use_common_place: Mapped[bool]
    # use_cross_street: Mapped[bool]

    # Ask from user
    night_phone_number: Mapped[str]  # daytime_phone_number
    email: Mapped[str]
    incident_type: Mapped[str] = mapped_column(default="Vehicle Burglary")
    have_suspect_info: Mapped[bool] = mapped_column(default=False)
    have_filed_original_report: Mapped[bool] = mapped_column(default=False)
    # report_type: Mapped[str]
    # victim_type: Mapped[str]

    location_type: Mapped[str]
    theft_type: Mapped[str]
    entry_location: Mapped[str]
    point_of_entry: Mapped[str]
    method_of_entry: Mapped[str]
    have_additional_person_info: Mapped[bool]
