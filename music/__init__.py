"""Initialize Flask app."""

from pathlib import Path
from flask import Flask, render_template

import music.adapters.repository as repo
from music.adapters.memory_repository import MemoryRepository, populate

def create_app(test_config=None):
    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('music') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()

    # Fill the content of the repository from the CSV files.
    populate(data_path, repo.repo_instance)

    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

    return app
