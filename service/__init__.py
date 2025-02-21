import sys
from flask import Flask
from service import config
from service.common import log_handlers
from flask_cors import CORS  # <-- Added this import

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Initialize CORS
CORS(app)  # <-- Added this line to enable CORS

# Import the routes after the Flask app is created
from service import routes, models  # noqa: F401 E402

from service.common import error_handlers, cli_commands  # noqa: F401 E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # make our database tables
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

app.logger.info("Service initialized!")
