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

    def __init__(self, container_id: str):
        self.container_id = container_id
        self.message = f"Fant ikke container med id={self.container_id} ved generering av SAS token"
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class ArkivkopiNotFound(Exception):
    """
    Exception raised when arkivkopi of an archive doesn't exist in database for the given invitasjon id

    Attributes:
        arkivuttrekk_obj_id -- UUID of the arkivuttrekk object id
        invitasjon_id -- Integer ID for the invitasjon in the database
        is_object -- Boolean flag indicating if this arkivkopi is a copy of a whole archive (is_object=False)
                     or an overforingspakke (is_object=True)
        message -- explanation of the error
    """
    def __init__(self, arkivuttrekk_obj_id: UUID, invitasjon_id: int, is_object: bool):
        self.arkivuttrekk_obj_id = arkivuttrekk_obj_id
        self.invitasjon_id = invitasjon_id
        self.is_object = is_object
        self.message = self.get_message()

    def __str__(self):
        return self.message

    def get_message(self) -> str:
        if self.is_object:
            message = "Fant ikke arkivkopi av en overforingspakke: "
        else:
            message = "Fant ikke arkivkopi av et arkiv: "
        message += f"arkivuttrekk objekt id={self.arkivuttrekk_obj_id} - invitasjon_id={self.invitasjon_id}"
        return message


class ArkivkopiOfArchiveRequestFailed(Exception):
    """
    Exception raised when ordering an arkivkopi of an archive fails

    Attributes:
        arkivuttrekk_id -- Integer ID for the arkivuttrekk in the database
        container_id -- string used to identify the container in which the archive to be copied is stored.
        message -- explanation of the error
    """

    def __init__(self, arkivuttrekk_id: int, container_id: str):
        self.arkivuttrekk_id = arkivuttrekk_id
        self.container_id = container_id
        self.message = f"Bestilling av nedlasting feilet for arkiv i container med id={self.container_id} " \
                       f"assosiert med arkivuttrekk med id={self.arkivuttrekk_id}"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ArkivkopiOfOverforingspakkeRequestFailed(Exception):
    """
    Exception raised when ordering an arkivkopi of an overforingspakke fails.

    Attributes:
        arkivuttrekk_id -- Integer ID for the arkivuttrekk in the database
        container_id -- string used to identify the container in which the overforingspakke to be copied is stored
        message -- explanation of the error
    """

    def __init__(self, arkivuttrekk_id: int, container_id: str):
        self.arkivuttrekk_id = arkivuttrekk_id
        self.container_id = container_id
        self.message = f"Bestilling av nedlasting feilet for overforingspakke i container {container_id} " \
                       f"assosiert med arkivuttrekk med id={self.arkivuttrekk_id}"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class OverforingspakkeNotFound(Exception):
    """
    Exception raised when overforingspakke doesn't exist in database

    Attributes:
        invitasjon_id -- Integer ID for the invitasjon in the database
        message -- explanation of the error
    """

    def __init__(self, invitasjon_id: int):
        self.invitasjon_id = invitasjon_id
        self.message = f"Fant ikke overforingspakke assosiert med invitasjon_id={self.invitasjon_id}"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvitasjonNotFound(Exception):
    """
    Exception raised when invitasjon doesn't exist in database

    Attributes:
        arkivuttrekk_id -- Integer ID for the arkivuttrekk in the database
        message -- explanation of the error
    """

    def __init__(self, arkivuttrekk_id: int):
        self.arkivuttrekk_id = arkivuttrekk_id
        self.message = f"Fant ikke invitasjon assosiert med arkivuttrekk_id={self.arkivuttrekk_id}"
        super().__init__(self.message)

    def __str__(self):
        return self.message

