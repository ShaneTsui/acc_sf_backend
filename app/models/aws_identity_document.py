from collections import defaultdict

from dateutil import parser


class AWSIdentityDocument:
    def __init__(self, fields):
        self.fields = defaultdict(lambda: {"value": "", "confidence": 0})
        for field in fields:
            name = field["Type"]["Text"].lower()
            val = field["ValueDetection"]
            self.fields[name] = {
                "value": val["Text"],
                "confidence": val["Confidence"]
            }
            if "date" in name:
                date_obj = parser.parse(val["NormalizedValue"]["Value"]).date()
                self.fields[name]["value"] = date_obj.isoformat()

    def get_field_value(self, field_name):
        return self.fields[field_name]["value"]

    def to_dict(self):
        return self.fields
