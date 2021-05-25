from os import mkdir, path
from utils.message import success, error


def create_folder(path):
  mkdir(path)
  success("New folder created")
