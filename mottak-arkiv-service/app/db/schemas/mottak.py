from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.baseclass import Base


class TransferArchive(Base):
    id = Column(Integer, primary_key=True, index=True)
    obj = Column(UUID(as_uuid=True), index=True)
    title = Column(String)
    description = Column(String)
    object_name = Column(String)
    checksum = Column(String(64))
    creator_id = Column(Integer, ForeignKey('creators.id'))
    tester_id = Column(Integer, ForeignKey('testers.id'))
    coordinator_id = Column(Integer, ForeignKey('coordinators.id'))
    metadata_file_id = Column(Integer, ForeignKey('metadata_files.id'))

    creator = relationship("Creator")
    coordinator = relationship("Coordinator")
    tester = relationship("Tester")
    metadata_file = relationship("MetadataFile")

    def __repr__(self):
        return f"<TransferArchive id={self.id}, uuid={self.uuid}, title={self.title}>"


class Creator(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    organization = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"<Creator id={self.id}, name={self.name} email={self.email} >"


class Tester(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"<Tester id={self.id}, name={self.name} email={self.email} >"


class Coordinator(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"<Coordinator id={self.id}, name={self.name} email={self.email} >"


class MetadataFile(Base):
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    content = Column(Text)

    def __repr__(self):
        return f"<MetadataFile id={self.id}, type={self.type} content(50)={self.content[:50]} >"
