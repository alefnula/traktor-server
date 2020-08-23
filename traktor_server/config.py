from traktor.config import ConfigField, Config as TraktorConfig


class Config(TraktorConfig):
    ENTRIES = {
        **TraktorConfig.ENTRIES,
        "server_host": ConfigField(section="server", option="host"),
        "server_port": ConfigField(section="server", option="port", type=int),
        "server_workers": ConfigField(
            section="server", option="workers", type=int
        ),
    }

    def __init__(self):
        self.server_host = "127.0.0.1"
        self.server_port = 8080
        self.server_workers = 2

        super().__init__()

    @property
    def server_url(self):
        return f"{self.server_host}:{self.server_port}"


config = Config()
