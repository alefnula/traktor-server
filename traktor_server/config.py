from pathlib import Path

from traktor.config import ConfigField, Config as TraktorConfig


class Config(TraktorConfig):
    ENTRIES = {
        **TraktorConfig.ENTRIES,
        # Redis
        "redis_host": ConfigField(section="redis", option="host"),
        "redis_port": ConfigField(section="redis", option="port", type=int),
        "redis_db": ConfigField(section="redis", option="db", type=int),
        # Server
        "server_host": ConfigField(section="server", option="host"),
        "server_port": ConfigField(section="server", option="port", type=int),
        "server_url_prefix": ConfigField(
            section="server", option="url_prefix"
        ),
        "server_workers": ConfigField(
            section="server", option="workers", type=int
        ),
        "server_socket": ConfigField(section="server", option="socket"),
    }

    def __init__(self):
        # Path to the configuration file
        self.config_dir = (Path("~").expanduser() / ".traktor").absolute()

        # Redis
        self.redis_host = "127.0.0.1"
        self.redis_port = 6379
        self.redis_db = 1

        # Server
        self.server_host = "127.0.0.1"
        self.server_port = 8080
        self.server_url_prefix = None
        self.server_workers = 2
        self.server_socket = "/tmp/traktor.sock"

        super().__init__(config_file=self.config_dir / "traktor-server.ini")

    @property
    def redis_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @property
    def server_url(self):
        return f"{self.server_host}:{self.server_port}"

    @property
    def url_prefix(self):
        if self.server_url_prefix is None:
            return None
        else:
            return f"{self.server_url_prefix.strip('/')}"


config = Config()
