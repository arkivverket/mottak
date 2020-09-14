from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Enum, BigInteger
from sqlalchemy import func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.baseclass import Base


class Arkivuttrekk(Base):
    """This is the class that represents an archive that is being processed in mottak."""
    id = Column(Integer(), autoincrement=True, nullable=False, primary_key=True, unique=True)
    obj_id = Column(UUID(as_uuid=True), nullable=False, index=True, unique=True)
    status = Column(Enum('Invitert', 'Under behandling', 'Avvist', 'Sent til bevaring', name='arkivuttrekk_status_type', create_type=True), nullable=False, index=True)
    type = Column(Enum('Noark3', 'Noark5', 'Fagsystem', name='arkivvuttrekk_type_type', create_type=True))
    tittel = Column(String(), nullable=False)
    beskrivelse = Column(String(), nullable=False)
    sjekksum = Column(String(length=64), nullable=False)
    avgiver_navn = Column(String(), nullable=False)
    avgiver_epost = Column(String(), nullable=False)
    koordinator_epost = Column(String(), nullable=False)
    opprettet = Column(DateTime(), server_default=func.now(), nullable=False)
    endret = Column(DateTime(), server_default=func.now(), onupdate=func.current_timestamp(), nullable=False)

    invitasjoner = relationship('Invitasjon', backref='arkivuttrekk')
    lokasjoner = relationship('Lokasjon', backref='arkivuttrekk')
    metadatafiler = relationship('Metadatafil', backref='arkivuttrekk')
    overforingspakker = relationship('Overforingspakke', backref='arkivuttrekk')
    testere = relationship('Tester', backref='arkivuttrekk')


class Invitasjon(Base):
    """An invitation. When we send an invitation to upload we create such an object and connect it to an archive.
    Not sure if we should create more than one if we send out several invitations.
    Perhaps it should contain a reference to the actual invitation being sent.
    """
    id = Column(Integer(), autoincrement=True, nullable=False, primary_key=True, unique=True)
    arkiv_id = Column(Integer(), ForeignKey('arkivuttrekk.id'), nullable=False, unique=True)
    status = Column(Enum('Sent', 'Feilet', name='status_type', create_type=True), nullable=False)
    opprettet = Column(DateTime(), server_default=func.now(), nullable=False)


class Lokasjon(Base):
    """ Location class. When we unpack an archive we create an object describing where it was unpacked.
    Note that we assume that everything is unpacked into the same storage account.
    """
    id = Column(Integer(), autoincrement=True, nullable=False, primary_key=True, unique=True)
    arkiv_id = Column(Integer(), ForeignKey('arkivuttrekk.id'), nullable=False, unique=False)
    kontainer = Column(String(), nullable=False, unique=False)
    generasjon = Column(Integer(), nullable=False, unique=False)

    # add a constraint so arkiv.id + generasjon is unique

    __table_args__ = (
        UniqueConstraint('arkiv_id', 'generasjon', name='arkiv_id_generasjon_uc'),
    )


class Metadatafil(Base):
    """The metadata file which contains the METS file which is used as a basis for the
    archive. If we move away from METS we should change the ENUM field to support other file types."""
    id = Column(Integer(), autoincrement=True, nullable=False, primary_key=True, unique=True)
    arkiv_id = Column(Integer(), ForeignKey('arkivuttrekk.id'), nullable=False, unique=True)
    type = Column(Enum('xml/mets', name='metadatatype', create_type=True), nullable=False, unique=False)
    innhold = Column(Text(), nullable=False)
    filnavn = Column(String(), nullable=False)
    opprettet = Column(DateTime(), server_default=func.now(), nullable=False)


class Overforingspakke(Base):
    """When we accept an upload we create a 'overforingspakke' object that points to the object which
    contains the tar file."""
    id = Column(Integer(), autoincrement=True, nullable=False, primary_key=True, unique=True)
    arkiv_id = Column(Integer(), ForeignKey('arkivuttrekk.id'), nullable=False, unique=True)
    navn = Column(String(), nullable=False)
    storrelse = Column(BigInteger(), nullable=False)
    status = Column(Enum('OK', 'Avbrutt', 'Feilet', name='status_type', create_type=True), nullable=False)


class Tester(Base):
    """ The tester which is assigned to testing an archive. Identified by email. """
    id = Column(Integer(), autoincrement=True, nullable=False, primary_key=True, unique=True)
    arkiv_id = Column(Integer(), ForeignKey('arkivuttrekk.id'), nullable=False, unique=False)
    epost = Column(String(), nullable=False)
