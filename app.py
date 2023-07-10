import sys
from datetime import datetime
from flask import Flask
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint



now = datetime.now()
message = f'{now:date %d:%m:%y: time : %H:%M:%S} Running and Logged!'
print(message, file = sys.stderr)
with open ('logs.txt', 'a') as file:
    print(message, file=file)

#---------------------------------------------------


app = Flask (__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['API_TITLE'] = "stores REST API"
app.config ['API_VERSION']= "v1"
app.config['OPENAPI_VERSION']= '3.0.3'
app.config['OPENAPI_URL_PREFIX']= '/'
app.config['OPENAPI_SWAGGER_UI_PATH']= '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api=Api(app)
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)



