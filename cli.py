import sys
import time
from os import path
from shutil import rmtree

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from watchdog.observers import Observer

from models import FileType as FileTypeModel
from utils.folder import create_folder
from utils.handler import Handler
from utils.message import error, success

engine = create_engine(
    "sqlite:////home/yahyafazlani/code/projects/file-organizer/database.db")

session = Session(bind=engine)


@click.command(name="watch")
def start_watching():
  path = sys.argv[1] if len(sys.argv) > 1 else '.'
  event_handler = Handler(session)
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


@click.command(name="create")
@click.argument("extension", type=click.STRING)
@click.argument("folder_path", type=click.Path(exists=True, file_okay=False, resolve_path=True))
def create_filetype(extension, folder_path):
  extension = extension.strip(".")
  filetype = session.query(FileTypeModel).filter(
      FileTypeModel.file_extension.is_(extension)).first()

  if filetype is None:
    # `filetype` is no longer needed
    del filetype

    create_folder(folder_path)

    if not path.isdir(folder_path):
      error(f"'{folder_path}' is not a folder")

    new_filetype = FileTypeModel(file_extension=extension, folder=folder_path)
    session.add(new_filetype)
    session.commit()

    success("New filetype created")
    click.echo(
        f"Files ending with '.{extension}' will be moved to '{folder_path}'")

  else:
    error("Filetype already exists")


@click.command(name="delete")
@click.option("-df", "--delete-folder", type=bool, default=False)
@click.argument("extension")
@click.argument("folder_path", type=click.Path(exists=True, file_okay=False, resolve_path=True))
def delete_filetype(delete_folder, extension: str, folder_path):
  extension = extension.strip(".")
  filetype = session.query(FileTypeModel).filter(
      FileTypeModel.file_extension == extension).first()

  if filetype is not None:
    session.delete(filetype)
    session.commit()

    success("Filetype deleted")

    if delete_folder:
      try:
        rmtree(folder_path)
        success("Folder successfully deleted")
      except:
        error("An error occurred while deleting the folder")


@click.command(name="update")
@click.option("-m", "--move", type=bool, default=False)
@click.argument("extension")
@click.argument("new_folder_path", type=click.Path(exists=True, file_okay=False, resolve_path=True))
def update_filetype(extension: str, new_folder_path):
  extension = extension.strip(".")
  filetype = session.query(FileTypeModel).filter(
      FileTypeModel.file_extension == extension).first()

  if filetype is not None:
    create_folder(new_folder_path)

    filetype.folder = new_folder_path

    success("Filetype updated successfully")

  else:
    error("Filetype doesn't exist")


if __name__ == "__main__":
  start_watching()
  create_filetype()
  delete_filetype()
  update_filetype()
