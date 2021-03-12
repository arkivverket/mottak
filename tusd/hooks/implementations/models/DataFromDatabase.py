from __future__ import annotations


class DataFromDatabase:
    """
    Parameter class for data read from the mottak database.
    """
    invitasjon_id: int
    ekstern_id: str
    koordinator_epost: str
    arkivuttrekk_obj_id: str

    def __init__(self,
                 invitasjon_id=None,
                 ekstern_id=None,
                 koordinator_epost=None,
                 arkivuttrekk_obj_id=None):
        self.invitasjon_id = invitasjon_id
        self.ekstern_id = ekstern_id
        self.koordinator_epost = koordinator_epost
        self.arkivuttrekk_obj_id = arkivuttrekk_obj_id

    def __eq__(self, other) -> bool:
        if isinstance(other, DataFromDatabase):
            return self.invitasjon_id == other.invitasjon_id and \
                   self.ekstern_id == other.ekstern_id and \
                   self.koordinator_epost == other.koordinator_epost and \
                   self.arkivuttrekk_obj_id == other.arkivuttrekk_obj_id
        return False

    @staticmethod
    def init_from_dict(metadata: dict) -> DataFromDatabase:
        invitasjon_id = metadata.get('invitasjon_id')
        ekstern_id = metadata.get('ekstern_id')
        koordinator_epost = metadata.get('koordinator_epost')
        arkivuttrekk_obj_id = metadata.get('arkivuttrekk_obj_id')

        return DataFromDatabase(invitasjon_id=invitasjon_id,
                                ekstern_id=ekstern_id,
                                koordinator_epost=koordinator_epost,
                                arkivuttrekk_obj_id=arkivuttrekk_obj_id)
