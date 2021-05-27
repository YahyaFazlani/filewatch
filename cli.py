import shutil
import time
from os import path, listdir, environ
from shutil import rmtree
from dotenv import load_dotenv
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from watchdog.observers import Observer

from models import FileType as FileTypeModel
from utils.folder import create_folder
from utils.handler import Handler
from utils.message import error, success

load_dotenv()

DB_URI = environ.get("DB_URI", "sqlite:///database.db")
engine = create_engine(DB_URI)

session = Session(bind=engine)


@click.group()
def cli():
  pass


@cli.command(name="start")
@click.option("-p", "--path", required=False, default=".", type=click.Path(exists=True, file_okay=False, resolve_path=True), help="path to watch from")
def start_watching(path):
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


@cli.command(name="create")
@click.argument("extension", type=click.STRING)
@click.argument("folder_path", type=click.Path(file_okay=False, resolve_path=True))
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


@cli.command(name="delete")
@click.option("-df", "--delete-folder", type=bool, default=False)
@click.argument("extension")
def delete_filetype(delete_folder, extension: str):
  extension = extension.strip(".")
  filetype = session.query(FileTypeModel).filter(
      FileTypeModel.file_extension == extension).first()

  if filetype is None:
    error(f"No filetype named '{extension}'")
    return

  folder_path = filetype.folder

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


@cli.command(name="update")
@click.option("-m", "--move", type=bool, default=False)
@click.argument("extension")
@click.argument("new_folder_path", type=click.Path(file_okay=False, resolve_path=True))
def update_filetype(extension: str, new_folder_path, move: bool):
  extension = extension.strip(".")
  filetype = session.query(FileTypeModel).filter(
      FileTypeModel.file_extension == extension).first()

  if filetype is not None:
    if filetype.folder == new_folder_path:
      error("New folder same as old folder")
      return

    create_folder(new_folder_path)

    if move:
      click.echo("Moving files...")
      files_to_move = listdir(filetype.folder)

      try:
        for file in files_to_move:
          shutil.move(path.join(filetype.folder, file), new_folder_path)
        success("Files moved")
        shutil.rmtree(filetype.folder)
        success("Deleted old folder")
      except:
        error("An error occurred while moving the files")

    filetype.folder = new_folder_path
    session.commit()

    success("Filetype updated successfully")

  else:
    error("Filetype doesn't exist")


if __name__ == "__main__":
  cli()
