

class MetadatafilNotFound(Exception):
    """
    Exception raised when metadatafil doesn't exist in database

    Attributes:
        id -- Integer ID for the metadatafil in the database
        message -- explanation of the error
    """

    def __init__(self, id: int, message="Fant ikke metadatafil med id="):
        self.id = id
        self.message = message + str(id)
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

    def __init__(self, id: int, message="Fant ikke arkivuttrekk med id="):
        self.id = id
        self.message = message + str(id)
        super().__init__(self.message)

    def __str__(self):
        return self.message
