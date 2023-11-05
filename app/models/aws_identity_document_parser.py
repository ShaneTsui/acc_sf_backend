from app.models.aws_identity_document import AWSIdentityDocument


FIELDS_TO_KEEP = [
    "first_name",
    "last_name",
    "middle_name",
    "city_in_address",
    "zip_code_in_address",
    "state_in_address",
    "state_name",
    "date_of_birth",
]


def extract_fields(data):
    result = {}
    for key, fields in data.items():
        for field_name, field_data in fields.items():
            if field_name in FIELDS_TO_KEEP:
                if field_name == "date_of_birth":
                    date_parts = field_data["value"].split("-")
                    result["year_of_birth"] = date_parts[0]
                    result["month_of_birth"] = date_parts[1]
                    result["day_of_birth"] = date_parts[2]
                else:
                    result[field_name] = field_data["value"]
    return result


class IdentityDocParser:
    @staticmethod
    def parse(docs: dict) -> dict:
        print(docs)
        return extract_fields(
            {
                doc["DocumentIndex"]: AWSIdentityDocument(
                    doc["IdentityDocumentFields"]
                ).to_dict()
                for doc in docs["IdentityDocuments"]
            }
        )
