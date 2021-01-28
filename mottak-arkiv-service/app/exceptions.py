from uuid import UUID


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


class SASTokenPreconditionFailed(Exception):
    """
    Exception raised when sas generator returns a 412 error, because the container does not exist.

    Attributes:
        container_id -- Object ID for the container
        message -- explanation of the error
    """

    def __init__(self, container_id: UUID):
        self.container_id = container_id
        self.message = f"The container '{container_id}' does not exist"
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class ArkivkopiNotFound(Exception):
    """
    Exception raised when arkivkopi doesn't exist in database

    Attributes:
        id -- Integer ID for the arkivuttrekk in the database
        message -- explanation of the error
    """

    def __init__(self, id_: int):
        self.id_ = id_
        self.message = f"Fant ikke arkivkopi med id={self.id_}"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ArkivkopiRequestFailed(Exception):
    """
    Exception raised when ordering an arkivkopi fails

    Attributes:
        id -- Integer ID for the arkivuttrekk in the database
        message -- explanation of the error
    """

    def __init__(self, id_: int, obj_id: int):
        self.id_ = id_
        self.obj_id = obj_id
        self.message = f"Bestilling nr {self.id_} av nedlasting av arkiv med obj_id={self.obj_id} feilet"
        super().__init__(self.message)

    def __str__(self):
        return self.message
