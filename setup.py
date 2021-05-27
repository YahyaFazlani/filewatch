from setuptools import setup

setup(
  name="filewatch",
  version="1.0",
  py_modules=["filewatch"],
  install_requires=["click", "watchdog", "sqlalchemy"],
  entry_points={
    "console_scripts": [
      "filewatch = cli:cli"
    ]
  }
)