import os
import shutil
import sys
import time
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from watchdog.events import (DirCreatedEvent, FileCreatedEvent,
                             FileSystemEventHandler)
from watchdog.observers import Observer

from models import FileType as FileTypeModel

engine = create_engine(
    "sqlite:////home/yahyafazlani/code/projects/file-organizer/database.db")

session = Session(bind=engine)


class Handler(FileSystemEventHandler):
  def on_created(self, event: Union[FileCreatedEvent, DirCreatedEvent]):
    if not event.is_directory:
      file_path = event.src_path
      extension: str = os.path.splitext(file_path)[1]
      extension = extension.strip(".")

      file_type = session.query(FileTypeModel).filter(FileTypeModel.file_extension.is_(extension)).first()
      try:
        if file_type is not None:
          shutil.move(file_path, file_type.folder)
      except shutil.Error as e:
        print("An error occurred while moving the file. Please check if a file with the same name exists in the folder")


if __name__ == "__main__":
  path = sys.argv[1] if len(sys.argv) > 1 else '.'
  event_handler = Handler()
  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()

  try:
    while True:
      time.sleep(1)

  except KeyboardInterrupt:
    observer.stop()

  finally:
    observer.join()
