from os import path
from utils.folder import create_folder

import click
from shutil import rmtree
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import FileType as FileTypeModel
from utils.message import success, error

engine = create_engine(
    "sqlite:////home/yahyafazlani/code/projects/file-organizer/database.db")

session = Session(bind=engine)


@click.command(name="create")
@click.argument("extension")
@click.argument("folder")
def create_filetype(extension: str, folder):
  extension = extension.strip(".")
  filetype = session.query(FileTypeModel).filter(
      FileTypeModel.file_extension.is_(extension)).first()

  if filetype is None:
    # `filetype` is no longer needed
    del filetype

    folder_path = path.abspath(folder)

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
@click.argument("folder")
def delete_filetype(delete_folder, extension: str, folder):
  extension = extension.strip(".")
  filetype = session.query(FileTypeModel).filter(
      FileTypeModel.file_extension == extension).first()

  if filetype is not None:
    session.delete(filetype)
    session.commit()

    success("Filetype deleted")

    if delete_folder:
      folder_path = path.abspath(folder)
      try:
        rmtree(folder_path)
        success("Folder successfully deleted")
      except:
        error("An error occurred while deleting the folder")


@click.command(name="update")
@click.argument("extension")
@click.argument("new_folder")
def update_filetype(extension: str, new_folder):
  extension = extension.strip(".")
  filetype = session.query(FileTypeModel).filter(
      FileTypeModel.file_extension == extension).first()

  if filetype is not None:
    new_folder_path = path.abspath(new_folder)

    create_folder(new_folder_path)

    filetype.folder = new_folder_path

    success("Filetype updated successfully")

  else:
    error("Filetype doesn't exist")


if __name__ == "__main__":
  create_filetype()
  delete_filetype()
  update_filetype()
