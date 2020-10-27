import json
import base64
from typing import List
from uuid import UUID


class InvitasjonMelding:
    __url_prefix = 'dpldr://'

    def __init__(self, arkivuttrekk_obj_id: UUID, upload_url: str, invitasjon_uuid: UUID, upload_type: str = 'tar'):
        self.reference = str(arkivuttrekk_obj_id)
        self.upload_url = upload_url
        self.upload_type = upload_type
        self.meta = {'invitasjon_uuid': str(invitasjon_uuid)}

    def as_base64_url(self):
        json_str = json.dumps(self.__dict__)
        print(json_str)
        json_bytes = json_str.encode('utf-8')
        base64_str = str(base64.b64encode(json_bytes), 'utf-8')
        return self.__url_prefix + base64_str
