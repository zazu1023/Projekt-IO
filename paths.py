import os
import sys
from pathlib import Path


def app_base_path() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def resource_path(relative: str) -> str:
    return str(app_base_path() / relative)


def configure_kivy_resources() -> None:
    from kivy.resources import resource_add_path

    resource_add_path(str(app_base_path()))


def get_db_path() -> str:
    if os.name == 'nt':
        base = Path(os.environ.get('APPDATA', Path.home()))
    else:
        base = Path.home() / '.local' / 'share'

    db_dir = base / 'StudentPlanner'
    db_dir.mkdir(parents=True, exist_ok=True)
    return str(db_dir / 'student_planner.db')
