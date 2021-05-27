import os
from utils.message import success, error


def create_folder(path):
  if not os.path.exists(path):
    os.mkdir(path)
    success("New folder created")