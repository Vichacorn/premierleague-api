import sys
import os
from config import OPENAPI_AUTOGEN_DIR

if not os.path.exists(OPENAPI_AUTOGEN_DIR):
    print("Folder '{}' not found.  "
          "Execute openapi-generator to generate it, "
          "e.g.,".format(OPENAPI_AUTOGEN_DIR))
    print()
    print("  "
          "java -jar openapi-generator-cli-3.3.4.jar"
          " generate -i openapi/premier-league-api.yaml"
          " -o {} -g python-flask".format(OPENAPI_AUTOGEN_DIR))
    print()
    exit(1)

sys.path.append(OPENAPI_AUTOGEN_DIR)

import connexion
from openapi_server import encoder

app = connexion.App(__name__,)
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi/premier-league-api.yaml')
app.run(port=8080,debug=True)
