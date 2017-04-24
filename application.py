import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

from app import create_app
application = create_app()

if __name__ == "main":
    application.run(debug=True)
