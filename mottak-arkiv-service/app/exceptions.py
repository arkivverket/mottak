class MetadatafilNotFound(Exception):
    """
    Exception raised when metadatafil doesn't exist in database

    Attributes:
        id -- Integer ID for the metadatafil in the database
        message -- explanation of the error
    """

    def __init__(self, id_: int, message="Fant ikke metadatafil med id="):
        self.id = id_
        self.message = message + str(id_)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class MetadatafilMissingInnhold(Exception):
    """
       Exception raised when metadatafil doesn't include content

       Attributes:
           message -- explanation of the error
       """

    def __init__(self, id_: int, message="Mangler innhold i metadatafil med id="):
        self.id = id_
        self.message = message + str(id_)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ArkivuttrekkNotFound(Exception):
    """
    Exception raised when arkivuttrekk doesn't exist in database

    Attributes:
        id -- Integer ID for the arkivuttrekk in the database
        message -- explanation of the error
    """

    def __init__(self, id_: int, message="Fant ikke arkivuttrekk med id="):
        self.id = id_
        self.message = message + str(id_)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidContentType(Exception):
    """
    Exception raised when the content type of an FastAPI UploadFile object is not of a valid type.

    Attributes:
        content_type -- The invalid content type
        message -- explanation of the error
    """

    def __init__(self, content_type: str):
        self.content_type = content_type
        self.message = f"Content type {content_type} is not a valid type"
        super().__init__(self.message)

    def __str__(self):
        return self.message
