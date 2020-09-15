import typer
from tea_console.console import command
from tea_django.commands.db import dump, load


app = typer.Typer(name="db")


# Mount dump and load
command(app, name="dump")(dump)
command(app, name="load")(load)
