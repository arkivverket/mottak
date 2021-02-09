from __future__ import annotations


class DataFromDatabase:
    """
    Parameter class for data read from the mottak database.
    """

    def __init__(self,
                 invitasjon_id=None,
                 ekstern_id=None,
                 sjekksum=None,
                 avgiver_navn=None,
                 avgiver_epost=None,
                 koordinator_epost=None,
                 arkiv_type=None,
                 arkivuttrekk_id=None,
                 storrelse=None):
        self.invitasjon_id = invitasjon_id
        self.ekstern_id = ekstern_id
        self.sjekksum = sjekksum
        self.avgiver_navn = avgiver_navn
        self.avgiver_epost = avgiver_epost
        self.koordinator_epost = koordinator_epost
        self.arkiv_type = arkiv_type
        self.arkivuttrekk_id = arkivuttrekk_id
        self.storrelse = storrelse

    def __eq__(self, other) -> bool:
        if isinstance(other, DataFromDatabase):
            return self.invitasjon_id == other.invitasjon_id and \
                   self.ekstern_id == other.ekstern_id and \
                   self.sjekksum == other.sjekksum and \
                   self.avgiver_navn == other.avgiver_navn and \
                   self.avgiver_epost == other.avgiver_epost and \
                   self.koordinator_epost == other.koordinator_epost and \
                   self.arkiv_type == other.arkiv_type and \
                   self.arkivuttrekk_id == other.arkivuttrekk_id and \
                   self.storrelse == other.storrelse
        return False

    @staticmethod
    def init_from_dict(metadata: dict) -> DataFromDatabase:
        invitasjon_id = metadata.get('invitasjon_id')  # Brukes denne?
        ekstern_id = metadata.get('ekstern_id')
        sjekksum = metadata.get('sjekksum')
        avgiver_navn = metadata.get('avgiver_navn')
        avgiver_epost = metadata.get('avgiver_epost')
        koordinator_epost = metadata.get('koordinator_epost')
        arkiv_type = metadata.get('arkiv_type')
        arkivuttrekk_id = metadata.get('arkivuttrekk_id')
        storrelse = metadata.get('storrelse')

        return DataFromDatabase(invitasjon_id=invitasjon_id,
                                ekstern_id=ekstern_id,
                                sjekksum=sjekksum,
                                avgiver_navn=avgiver_navn,
                                avgiver_epost=avgiver_epost,
                                koordinator_epost=koordinator_epost,
                                arkiv_type=arkiv_type,
                                arkivuttrekk_id=arkivuttrekk_id,
                                storrelse=storrelse)
