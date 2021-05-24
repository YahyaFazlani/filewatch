from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class FileType(Base):
  __tablename__ = "filetypes"

  file_extension = Column(String, primary_key=True)
  folder = Column(String, unique=True)

  def __repr__(self) -> str:
    return "<FileType file_extension='%' folder='%'>" % (self.file_extension, self.folder)
