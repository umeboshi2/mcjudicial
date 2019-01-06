from datetime import datetime, date

from sqlalchemy import Column, ForeignKey

# column types
from sqlalchemy import Integer, Unicode
from sqlalchemy import Boolean, Date
from sqlalchemy import PickleType
from sqlalchemy import Enum
# from sqlalchemy import DateTime

from sqlalchemy.orm import relationship
# from sqlalchemy.orm import backref

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint
from hornstone.alchemy import Base
from hornstone.alchemy import TimeStampMixin

####################################
# Data Types                      ##
####################################
CourtName = Enum('sct', 'coa', 'trial',
                 name='mc_courtname_enum')

####################################
#  Tables                         ##
####################################


class Case(Base, TimeStampMixin):
    __tablename__ = 'mc_cases'
    id = Column(Integer, primary_key=True)
    court = Column(CourtName)
    docket_num = Column(Unicode(20))
    link = Column(Unicode(50))
    name = Column(Unicode)
    date = Column(Date)
    has_brief = Column(Boolean(name='has_brief'))
    has_video = Column(Boolean(name='has_video'))
    UniqueConstraint(docket_num, date, link)
    def __repr__(self):
        return "<Case({}): {}>".format(self.docket_num, self.name)


class CaseDetail(Base, TimeStampMixin):
    __tablename__ = "mc_case_details"
    id = Column(Integer, ForeignKey('mc_cases.id'),
                primary_key=True)
    content = Column(PickleType)


Case.details = relationship(CaseDetail, uselist=False)
