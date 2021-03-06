# pylint: skip-file
import json
from datetime import datetime

from django.utils.timezone import get_default_timezone
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, BigInteger, String, Text, DateTime, ARRAY, VARCHAR
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LocalDateTime(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value, engine):
        if value is not None:
            return value

    def process_result_value(self, value, engine):
        if value is not None:
            return datetime(value.year, value.month, value.day,
                            value.hour, value.minute, value.second,
                            value.microsecond, tzinfo=get_default_timezone())

class JSONEncodedDict(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class UserEntity(Base):
    __tablename__ = 'user_entity'
    id = Column(BigInteger, primary_key=True)
    source_interface_id = Column(BigInteger)
    source_identifier = Column(String)
    subject_id = Column(BigInteger, ForeignKey('subject.id'))
    date_created = Column(LocalDateTime)
    date_deleted = Column(LocalDateTime)
    properties = JSONEncodedDict()
    password = Column(String)

    subject = relationship('Subject')

class Subject(Base):
    __tablename__ = 'subject'
    id = Column(BigInteger, primary_key=True)
    subject_type = Column(Text)
    properties = Column(JSONEncodedDict)
    settings = Column(JSONEncodedDict)
    username = Column(String)
    last_modified = Column(LocalDateTime)
    role_ids = ARRAY(BigInteger)
    group_ids = ARRAY(BigInteger)

class Zaak(Base):
    __tablename__ = 'zaak'
    id = Column(BigInteger, primary_key=True)
    zaaktype_id = Column(BigInteger)
    pid = Column(BigInteger)
    onderwerp = Column(String)
    resultaat = Column(String)
    created = Column(LocalDateTime)
    registratiedatum = Column(LocalDateTime)
    status = Column(String)

class ObjectData(Base):
    __tablename__ = 'object_data'
    uuid = Column(UUID, primary_key=True)
    object_id = Column(BigInteger)
    object_class = Column(String)
    properties = Column(JSONEncodedDict)

class Logging(Base):
    __tablename__ = 'logging'
    id = Column(BigInteger, primary_key=True)
    zaak_id = Column(BigInteger)
    event_type = Column(String)
    onderwerp = Column(String)
    event_data = Column(JSONEncodedDict)
    created = Column(LocalDateTime)
    created_by = Column(String)

class File(Base):
    __tablename__ = 'file'
    id = Column(BigInteger, primary_key=True)
    filestore_id = Column(BigInteger, ForeignKey('filestore.id'))
    case_id = Column(BigInteger)
    version = Column(BigInteger)
    date_created = Column(LocalDateTime)
    created_by = Column(String)
    name = Column(String)

    filestore = relationship('Filestore')

class Filestore(Base):
    __tablename__ = 'filestore'
    id = Column(BigInteger, primary_key=True)
    uuid = Column(UUID)
    original_name = Column(String)
    mimetype = Column(String)
    date_created = Column(LocalDateTime)

class CaseStatus(Base):
    __tablename__ = 'zaaktype_status'
    id = Column(BigInteger, primary_key=True)
    fase = Column(String)
