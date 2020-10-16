import xml.etree.ElementTree as ET
from datetime import date
from uuid import UUID

from app.domain.models.Arkivuttrekk import Arkivuttrekk, ArkivuttrekkStatus, ArkivuttrekkType


def _recursive_ns(elem: ET.Element, ns: dict) -> dict:
    """
    Method that returns a dictionary containing the namespaces used
    when parsing an METS XML.
    """
    if elem.tag[0] == "{":
        uri, ignore, tag = elem.tag[1:].partition("}")
    else:
        uri = None
        tag = elem.tag
    # Only add tag and uri if both are unique
    if tag not in ns and uri not in ns.values():
        ns[tag] = uri

    # Check children of elem and update with unique tag:uri
    for child in elem:
        ns.update(_recursive_ns(child, ns))
    return ns


def _get_all_namespaces(root: ET.Element) -> dict:
    """
    Method that returns a dictionary containing the namespaces used
    when parsing an METS XML.
    """
    ns = _recursive_ns(root, {})
    return ns


# TODO Error handling of missing XML nodes, applies to all functions below
def _get_objekt_id(root: ET.Element) -> UUID:
    uuid_str = root.get('OBJID')
    return UUID(uuid_str[5:])


def _str2ArkivuttrekkType(arkivuttrekk_str: str) -> ArkivuttrekkType:
    """
    Method that converts a str to a ArkivuttrekkType Enum value or returns a ValueError
    """
    if "Noark" in arkivuttrekk_str and "5" in arkivuttrekk_str:
        return ArkivuttrekkType.NOARK5
    if "Noark" in arkivuttrekk_str and "3" in arkivuttrekk_str:
        return ArkivuttrekkType.NOARK3
    if "Fagsystem" in arkivuttrekk_str:
        return ArkivuttrekkType.FAGSYSTEM
    return 'None'


# TODO Finn ut om arkiv type ser ut som her eller som i ArkivuttrekkType Enum.verdier
# "Noark 5 - Sakarkiv" --> "Noark5"
def _get_arkivtype(root: ET.Element, ns: dict) -> str:
    # Arkivtype: DELIVERYSPECIFICATION
    try:
        altRecord_ids = root.findall('mets:metsHdr/mets:altRecordID', namespaces=ns)
        arkivtype = [alt for alt in altRecord_ids
                     if "DELIVERYSPECIFICATION" == alt.get('TYPE')].pop().text
    except IndexError:
        return 'None'
    else:
        return _str2ArkivuttrekkType(arkivtype)


def _get_title(root: ET.Element, ns: dict) -> str:
    # Tittel = ARCHIVIST-ORGANIZATION + LABEL
    label = root.get('LABEL')
    try:
        agents = root.findall('mets:metsHdr/mets:agent', namespaces=ns)
        agent = [agent for agent in agents
                 if ("ARCHIVIST" == agent.get('ROLE') and
                     "ORGANIZATION" == agent.get('TYPE'))].pop()
    except IndexError:
        arch_org = None
    else:
        arch_org = agent.findtext('mets:name', namespaces=ns)
    return f'{arch_org} -- {label}'


def _get_checksum(root: ET.Element, ns: dict) -> str:
    files = root.find('mets:fileSec/mets:fileGrp/mets:file', namespaces=ns)
    return files.get('CHECKSUM')


def _get_avgiver_navn(root: ET.Element, ns: dict) -> str:
    try:
        agents = root.findall('mets:metsHdr/mets:agent', namespaces=ns)
        agent = [agent for agent in agents
                 if ("ARCHIVIST" == agent.get('ROLE') and
                     "INDIVIDUAL" == agent.get('TYPE'))].pop()
    except IndexError:
        return 'None'
    else:
        return agent.findtext('mets:name', namespaces=ns)


def _get_avgiver_epost(root: ET.Element, ns: dict) -> str:
    try:
        agents = root.findall('mets:metsHdr/mets:agent', namespaces=ns)
        agent = [agent for agent in agents
                 if ("ARCHIVIST" == agent.get('ROLE') and
                     "INDIVIDUAL" == agent.get('TYPE'))].pop()
    except IndexError:
        return 'None'
    else:
        email_list = [note for note in agent.findall('mets:note', namespaces=ns)
                      if '@' in note.text]
        return email_list.pop().text if email_list else 'None'


def _get_arkiv_startdato(root: ET.Element, ns: dict) -> date:
    altRecord_ids = root.findall('mets:metsHdr/mets:altRecordID', namespaces=ns)
    for altRecord in altRecord_ids:
        if altRecord.get('TYPE') == "STARTDATE":
            date_ = altRecord.text
            return date.fromisoformat(date_)
    return None


def _get_arkiv_sluttdato(root: ET.Element, ns: dict) -> date:
    altRecord_ids = root.findall('mets:metsHdr/mets:altRecordID', namespaces=ns)
    for altRecord in altRecord_ids:
        if altRecord.get('TYPE') == "ENDDATE":
            date_ = altRecord.text
            return date.fromisoformat(date_)
    return None


def _convert_2_megabytes(size_bytes) -> float:
    """
    Method that converts bytes to MB
    """
    MB = 10 ** 6
    converted_size = float(size_bytes / MB)
    return converted_size


def _get_storrelse(root: ET.Element, ns: dict) -> float:
    # Størrelse: (METS FILE ID SIZE)
    files = root.findall('mets:fileSec/mets:fileGrp/mets:file', namespaces=ns)
    total_bytes = 0
    for file in files:
        total_bytes += int(file.get('SIZE'))
    return _convert_2_megabytes(total_bytes)


def _get_avtalenummer(root: ET.Element, ns: dict) -> str:
    # Avtalenummer: SUBMISSSION AGREEMENT
    try:
        altRecord_ids = root.findall('mets:metsHdr/mets:altRecordID', namespaces=ns)
        avtalenummer = [alt for alt in altRecord_ids
                        if "SUBMISSIONAGREEMENT" == alt.get('TYPE')].pop().text
        return avtalenummer
    except IndexError:
        return 'None'


def create_arkivuttrekk_from_parsed_innhold(metadatafil_id: int, innhold: str) -> Arkivuttrekk:
    """
    Method that parse the content (innhold) of a metadatfil
    and returns a domain object of type Arkivuttrekk.
    """
    root = ET.fromstring(innhold)
    ns = _get_all_namespaces(root)

    arkivuttrekk = Arkivuttrekk(
        obj_id=_get_objekt_id(root),
        status=ArkivuttrekkStatus.UNDER_OPPRETTING,
        type_=_get_arkivtype(root, ns),
        tittel=_get_title(root, ns),
        sjekksum_sha256=_get_checksum(root, ns),
        avgiver_navn=_get_avgiver_navn(root, ns),
        avgiver_epost=_get_avgiver_epost(root, ns),
        metadatafil_id=metadatafil_id,
        arkiv_startdato=_get_arkiv_startdato(root, ns),
        arkiv_sluttdato=_get_arkiv_sluttdato(root, ns),
        storrelse=_get_storrelse(root, ns),
        avtalenummer=_get_avtalenummer(root, ns)
    )
    return arkivuttrekk
