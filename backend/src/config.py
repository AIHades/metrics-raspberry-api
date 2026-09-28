import os
from pathlib import Path


class Settings:
    @property
    def base_dir(self):
        base_dir = Path(__file__).parent.parent.parent
        return base_dir

    @property
    def frontend_dir(self):
        return os.path.join(self.base_dir, "frontend")

    @property
    def templates_dir(self):
        return os.path.join(self.frontend_dir, "templates")

    @property
    def static_dir(self):
        return os.path.join(self.frontend_dir, "static")

settings = Settings()