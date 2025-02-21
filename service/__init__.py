import os
import logging
import sys
from flask import Flask
from flask_cors import CORS
from service import config
from service.common import log_handlers
from service.models import db, Account, init_db
from service.routes import app

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Initialize CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Apply CORS for all routes and allow any origin

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    init_db(app)  # Make our database tables
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

app.logger.info("Service initialized!")

# Import routes after initialization to avoid circular imports
from service import routes, models  # noqa: F401 E402
