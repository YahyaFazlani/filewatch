import os
import shutil
from typing import Union

from models import FileType as FileTypeModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from watchdog.events import (DirCreatedEvent, FileCreatedEvent,
                             FileSystemEventHandler)


class Handler(FileSystemEventHandler):

  def __init__(self, session: Session) -> None:
    self.session = session

  def on_created(self, event: Union[FileCreatedEvent, DirCreatedEvent]):
    if event.is_directory:
      print(f"Directory created - {event.src_path}")

    if not event.is_directory:
      print(f"File created - {event.src_path}")

      file_path = event.src_path
      extension: str = os.path.splitext(file_path)[1]
      extension = extension.strip(".")

      file_type = self.session.query(FileTypeModel).filter(
          FileTypeModel.file_extension.is_(extension)).first()

      try:
        if file_type is not None:
          new_file_path = os.path.join(file_type.folder, file_path)

          shutil.move(file_path, file_type.folder)
          print(f"File moved - {os.path.relpath(file_path)}")
      except shutil.Error as e:
        print("An error occurred while moving the file. Please check if a file with the same name exists in the folder")
