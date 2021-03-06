from __future__ import annotations


class DataFromDatabase:
    """
    Parameter class for data read from the mottak database.
    """
    invitasjon_id: int
    ekstern_id: str
    sjekksum: str
    koordinator_epost: str
    arkivuttrekk_obj_id: str
    tittel: str

    def __init__(self,
                 invitasjon_id=None,
                 ekstern_id=None,
                 sjekksum=None,
                 koordinator_epost=None,
                 arkivuttrekk_obj_id=None,
                 tittel=None):
        self.invitasjon_id = invitasjon_id
        self.ekstern_id = ekstern_id
        self.sjekksum = sjekksum
        self.koordinator_epost = koordinator_epost
        self.arkivuttrekk_obj_id = arkivuttrekk_obj_id
        self.tittel = tittel

    def __eq__(self, other) -> bool:
        if isinstance(other, DataFromDatabase):
            return self.invitasjon_id == other.invitasjon_id and \
                   self.ekstern_id == other.ekstern_id and \
                   self.sjekksum == other.sjekksum and \
                   self.koordinator_epost == other.koordinator_epost and \
                   self.arkivuttrekk_obj_id == other.arkivuttrekk_obj_id and \
                   self.tittel == other.tittel
        return False

    @staticmethod
    def init_from_dict(metadata: dict) -> DataFromDatabase:
        invitasjon_id = metadata.get('invitasjon_id')
        ekstern_id = metadata.get('ekstern_id')
        sjekksum = metadata.get('sjekksum')
        koordinator_epost = metadata.get('koordinator_epost')
        arkivuttrekk_obj_id = metadata.get('arkivuttrekk_obj_id')
        arkivuttrekk_tittel = metadata.get('arkivuttrekk_tittel')

        return DataFromDatabase(invitasjon_id=invitasjon_id,
                                ekstern_id=ekstern_id,
                                sjekksum=sjekksum,
                                koordinator_epost=koordinator_epost,
                                arkivuttrekk_obj_id=arkivuttrekk_obj_id,
                                tittel=arkivuttrekk_tittel)
