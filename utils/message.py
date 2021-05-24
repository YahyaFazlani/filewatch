import click

def success(output, bold=True):
  click.secho(output, fg="green", bold=bold)

def error(output, bold=True):
  click.secho(output, fg="red", err=True)