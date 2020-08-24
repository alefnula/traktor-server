from pathlib import Path

from traktor.config import ConfigField, Config as TraktorConfig


class Config(TraktorConfig):
    ENTRIES = {
        **TraktorConfig.ENTRIES,
        "server_host": ConfigField(section="server", option="host"),
        "server_port": ConfigField(section="server", option="port", type=int),
        "server_workers": ConfigField(
            section="server", option="workers", type=int
        ),
        "server_socket": ConfigField(section="server", option="socket"),
    }

    def __init__(self):
        # Path to the configuration file
        self.config_dir = (Path("~").expanduser() / ".traktor").absolute()

        self.server_host = "127.0.0.1"
        self.server_port = 8080
        self.server_workers = 2
        self.server_socket = "/tmp/traktor.sock"

        super().__init__(config_file=self.config_dir / "traktor-server.ini")

    @property
    def server_url(self):
        return f"{self.server_host}:{self.server_port}"


config = Config()
