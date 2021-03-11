import json
import pathlib
import base64
import chevron
import markdown
import os
from uuid import UUID
from typing import List
from abc import ABC
from bs4 import BeautifulSoup


class MailgunEmail(ABC):
    def __init__(self, subject: str, to: List[str], sender: str, body_text: str, body_html: str):
        self.__subject = subject
        self.__to = to
        self.__from = sender
        self.__text = body_text
        self.__html = body_html

    def as_data(self):
        """
        Creates a dict adhering to Mailguns expected data structure
        :return: a dict following Mailguns eexpected data structure
        """
        return {'subject': self.__subject, 'to': self.__to, 'from': self.__from, 'text': self.__text,
                'html': self.__html}


class InvitasjonUploadUrl:
    """
    Creating invitasjon json object in expected structure for the archive-uploader
    """
    __url_prefix = 'dpldr://'

    def __init__(self, arkivuttrekk_obj_id: UUID, upload_url: str, invitasjon_ekstern_id: UUID, upload_type: str = 'tar'):
        self.reference = str(arkivuttrekk_obj_id)
        self.uploadUrl = upload_url
        self.uploadType = upload_type
        self.meta = {'invitasjonEksternId': str(invitasjon_ekstern_id)}

    def as_base64_url(self) -> str:
        """
        Base64 encodes the json object
        :return: a base64 encoded url as string
        """
        json_str = json.dumps(self.__dict__)
        json_bytes = json_str.encode('utf-8')
        base64_str = str(base64.b64encode(json_bytes), 'utf-8')
        return self.__url_prefix + base64_str


class InvitasjonEmail(MailgunEmail):
    """
    Template class for sending upload links through Mailgun.
    """

    __subject = "Invitasjon til opplastning"

    def __init__(self, mailgun_domain: str, to: List[str], arkivuttrekk_obj_id: UUID, arkivuttrekk_tittel: str,
                 upload_url: str):
        sender = f'Mottak Digitalarkivet <donotreply@{mailgun_domain}>'
        md_body = InvitasjonEmail.get_markdown_body(arkivuttrekk_obj_id, arkivuttrekk_tittel, upload_url)
        html_body = markdown.markdown(md_body, extensions=['markdown.extensions.tables'])
        txt_body = ''.join(BeautifulSoup(html_body, features="html.parser").find_all(text=True))
        super().__init__(self.__subject, to, sender, txt_body, html_body)

    @staticmethod
    def get_markdown_body(obj_id: UUID, tittel: str, upload_url: str) -> str:
        current_location = str(pathlib.Path(__file__).parent.absolute())
        invitasjon_template_file_path = os.path.join(current_location, 'bodies', 'invitasjon.md')
        with open(invitasjon_template_file_path, 'r') as f:
            return chevron.render(f, {'obj_id': obj_id, 'tittel': tittel, 'upload_url': upload_url})
