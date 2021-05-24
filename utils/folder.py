from os import mkdir, path
from utils.message import success, error


def create_folder(path):
  if not path.exists(path):
    try:
      mkdir(path)
      success("New folder created")
    except FileNotFoundError as e:
      error(f"A file or folder with the name {e.filename} does not exist")
