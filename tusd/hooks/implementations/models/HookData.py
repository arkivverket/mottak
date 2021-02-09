from __future__ import annotations
from uuid import UUID


class HookData:
    """
    Parameter class for data read from the hook event (stdin)
    """
    tusd_id: UUID
    ekstern_id: UUID
    transferred_bytes: int
    objekt_navn: str

    def __init__(self,
                 tusd_id=None,
                 ekstern_id=None,
                 transferred_bytes=0,
                 objekt_navn=None):
        self.tusd_id = tusd_id
        self.ekstern_id = ekstern_id
        self.transferred_bytes = transferred_bytes
        self.objekt_navn = objekt_navn

    def __eq__(self, other) -> bool:
        if isinstance(other, HookData):
            return self.tusd_id == other.tusd_id and \
                   self.ekstern_id == other.ekstern_id and \
                   self.transferred_bytes == other.transferred_bytes and \
                   self.objekt_navn == other.objekt_navn
        return False

    @staticmethod
    def init_from_dict(json_dict: dict) -> HookData:
        tusd_id = json_dict.get('Upload').get('ID')
        ekstern_id = json_dict.get('Upload').get('MetaData').get('invitasjonEksternId')
        transferred_bytes = json_dict.get('Upload').get('Offset')
        objekt_navn = json_dict.get('Upload').get('Storage').get('Key')

        return HookData(tusd_id=tusd_id,
                        ekstern_id=ekstern_id,
                        transferred_bytes=transferred_bytes,
                        objekt_navn=objekt_navn)
