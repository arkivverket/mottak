import xml.etree.ElementTree as ET

from app.domain.models.metadatafil import Metadatafil, ParsedMetadatafil


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
def _get_title(root: ET.Element, ns: dict) -> str:
    # Tittel = ARCHIVIST-ORGANIZATION + LABEL
    label = root.get('LABEL')
    try:
        agents = root.findall('mets:metsHdr/mets:agent', namespaces=ns)
        agent = [agent for agent in agents
                 if ("ARCHIVIST" == agent.get('ROLE') and
                     "ORGANIZATION" == agent.get('TYPE'))].pop()
        arch_org = agent.findtext('mets:name', namespaces=ns)
    except IndexError:
        arch_org = None

    return f'{arch_org} -- {label}'


def _get_kontaktperson(root: ET.Element, ns: dict) -> str:
    # Kontaktperson: Navn (e-post) SUBMITTER - INDIVIDUAL
    try:
        agents = root.findall('mets:metsHdr/mets:agent', namespaces=ns)
        agent = [agent for agent in agents
                 if ("ARCHIVIST" == agent.get('ROLE') and
                     "INDIVIDUAL" == agent.get('TYPE'))].pop()
        name = agent.findtext('mets:name', namespaces=ns)
        # Note is not a unique element. We have to search for the note containing email address
        email_list = [note for note in agent.findall('mets:note', namespaces=ns)
                      if '@' in note.text]
        if email_list:
            email = email_list.pop().text
        else:
            email = None
    except IndexError:
        name = None
        email = None

    return f"{name} ({email})"


def _get_arkivtype(root: ET.Element, ns: dict) -> str:
    # Arkivtype: DELIVERYSPECIFICATION
    try:
        altRecord_ids = root.findall('mets:metsHdr/mets:altRecordID', namespaces=ns)
        arkivtype = [alt for alt in altRecord_ids
                       if "DELIVERYSPECIFICATION" == alt.get('TYPE')].pop().text
        return arkivtype
    except IndexError:
        return 'None'


def _get_objekt_id(root: ET.Element):
    return root.get('OBJID')


# TODO Return float
def _format_size(size_bytes, unit="MB"):
    """
    Method that converts integers to common size units.
    Default unit is MB
    """
    convert = {
        "B": 1,
        "KB": 10**3,
        "MB": 10**6,
        "GB": 10**9,
        "TB": 10**12,
    }

    converted_size = size_bytes / convert[unit]
    return f"{converted_size} {unit}"


# TODO Return float
def _get_storrelse(root: ET.Element, ns: dict) -> str:
    # Størrelse: (METS FILE ID SIZE)
    files = root.findall('mets:fileSec/mets:fileGrp/mets:file', namespaces=ns)
    total_size = 0
    for file in files:
        total_size += int(file.get('SIZE'))
    return _format_size(total_size)


# TODO Dele opp i to metoder, _get_arkiv_startdato, _get_arkiv_sluttdato
def _get_tidsspenn(root: ET.Element, ns: dict) -> str:
    # Tidsspenn: (STARTDATE + ENDDATE)
    altRecord_ids = root.findall('mets:metsHdr/mets:altRecordID', namespaces=ns)
    startdate = None
    enddate = None
    for record in altRecord_ids:
        type_ = record.get('TYPE')
        if type_ == "STARTDATE":
            startdate = record.text
        elif type_ == "ENDDATE":
            enddate = record.text
    return f"{startdate} -- {enddate}"


def _get_avtalenummer(root: ET.Element, ns: dict) -> str:
    # Avtalenummer: SUBMISSSION AGREEMENT
    try:
        altRecord_ids = root.findall('mets:metsHdr/mets:altRecordID', namespaces=ns)
        avtalenummer = [alt for alt in altRecord_ids
                     if "SUBMISSIONAGREEMENT" == alt.get('TYPE')].pop().text
        return avtalenummer
    except IndexError:
        return 'None'


def get_parsedmetadatafil(metadatafil: Metadatafil) -> ParsedMetadatafil:
    """
    Method that parse the content (innhold) of a metadatfil
    and returns a object of type ParsedMetadatafil
    which contains information used for uploading an archive.
    """
    root = ET.fromstring(metadatafil.innhold)
    ns = _get_all_namespaces(root)

    parsed = ParsedMetadatafil(
        tittel=_get_title(root, ns),
        endret=metadatafil.endret,
        kontaktperson=_get_kontaktperson(root, ns),
        arkivtype=_get_arkivtype(root, ns),
        objekt_id=_get_objekt_id(root),
        storrelse=_get_storrelse(root, ns),
        tidsspenn=_get_tidsspenn(root, ns),
        avtalenummer=_get_avtalenummer(root, ns)
    )
    return parsed
