from pathlib import Path

import connexion
import logging
from flask_cors import CORS

from . import encoder, probes
from .globals import FLASK_ENV, PORT, GlobalObjects

app = None
logger = logging.getLogger(__name__)

def main(*args, **kwargs):
    global app
        
    app = connexion.FlaskApp(__name__, specification_dir=Path(__file__).parent.joinpath("swagger"))
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api(
        'swagger_v3.yaml', 
        arguments={'title': 'STAIoTCraft - PROJECT API'},
        pythonic_params=True
    )
    
    app.add_url_rule("/livez", view_func=probes.liveness_probe)
    app.add_url_rule("/readyz", view_func=probes.readiness_probe)

    CORS(app.app)

    GlobalObjects.getInstance().flask_app = app.app    

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    app.app.logger.setLevel(logging.INFO)

    return app
