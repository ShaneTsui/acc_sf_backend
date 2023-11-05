from app.models.aws_identity_document import AWSIdentityDocument


class IdentityDocParser:
    @staticmethod
    def parse(docs: dict) -> dict:
        print(docs)
        return {
            doc["DocumentIndex"]: AWSIdentityDocument(
                doc["IdentityDocumentFields"]
            ).to_dict()
            for doc in docs["IdentityDocuments"]
        }
