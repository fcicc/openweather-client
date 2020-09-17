# entry point for uWSGI
from src.server import create_app
app = create_app()
