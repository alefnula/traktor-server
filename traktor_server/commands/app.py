import typer
from pathlib import Path

from console_tea.commands.config import app as config_app

from traktor_server.config import config


app = typer.Typer(name="traktor-server", help="Traktor server.")


# Add tea subcommands
app.add_typer(config_app)


@app.callback()
def callback(
    config_path: Path = typer.Option(
        default=None,
        help="Path to the configuration.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
):
    if config_path is not None:
        config.config_path = config_path

    config.load()


@app.command()
def runserver():
    """Run development server."""
    from django.core.management import execute_from_command_line

    execute_from_command_line(
        ["traktor-server", "runserver", config.server_url]
    )


@app.command()
def gunicorn():
    """Run gunicorn server."""
    from gunicorn.app import base
    from traktor_server import wsgi

    class TraktorApplication(base.BaseApplication):
        def __init__(self, application, **kwargs):
            self.options = kwargs
            self.application = application
            super().__init__()

        def load_config(self):
            config_dict = {
                key: value
                for key, value in self.options.items()
                if key in self.cfg.settings and value is not None
            }
            for key, value in config_dict.items():
                self.cfg.set(key.lower(), value)

        def init(self, parser, opts, args):
            pass

        def load(self):
            return self.application

    options = {
        "bind": f"0.0.0.0:{config.server_port}",
        "workers": config.server_workers,
    }
    TraktorApplication(wsgi.application, **options).run()


@app.command(hidden=True)
def shell():
    """Run IPython shell with loaded configuration and models."""
    try:
        from IPython import embed
        from traktor.config import config
        from traktor.engine import engine
        from traktor.models import Project, Task, Entry

        embed(
            user_ns={
                "config": config,
                "engine": engine,
                "Project": Project,
                "Task": Task,
                "Entry": Entry,
            },
            colors="neutral",
        )
    except ImportError:
        typer.secho("IPython is not installed", color=typer.colors.RED)
