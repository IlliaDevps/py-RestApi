import sys
import os
import secrets
from datetime import datetime
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from blocklist import BLOCKLIST
from dotenv import load_dotenv

import redis
from rq import Queue

from db import db
import models


from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint



now = datetime.now()
message = f'{now:date %d:%m:%y: time : %H:%M:%S} Running and Logged!'
print(message, file = sys.stderr)
with open ('logs.txt', 'a') as file:
    print(message, file=file)

#---------------------------------------------------

def create_app(db_url=None):
    app = Flask (__name__)
    load_dotenv() #loading env variable from the file .env

    connection = redis.from_url(
        os.getenv('REDIS_URL')
    )
    app.queue = Queue('emails' ,  connection=connection)

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = "stores REST API"
    app.config ['API_VERSION']= "v1"
    app.config['OPENAPI_VERSION']= '3.0.3'
    app.config['OPENAPI_URL_PREFIX']= '/'
    app.config['OPENAPI_SWAGGER_UI_PATH']= '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URL', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app , db)
    api=Api(app)

    app.config['JWT_SECRET_KEY'] = '241792312309107685658846800634664924401'
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader #when ever we receive a WJT this functions runs and checks if the tocken is in the blocklist
    def check_if_token_in_blocklist(jtw_header, jtw_payload):
        return jtw_payload['jti'] in BLOCKLIST #if this retruns true then the request will be terminated and the user get an error which says the token has been revoked
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jtw_header, jtw_payload):
        return (jsonify(
            {
                'description': 'The token has been revoked',
                'error': 'Token_revoked'
            }
        ),401,
        )
    
    @jwt.needs_fresh_token_loader
    def token_non_fresh_callback(jtw_header, jtw_payload):
         return (jsonify(
            {
                'description': 'The token is not fresh',
                'error': 'fresh_token_requiered'
            }
        ),401,
        )  


    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # this probably should look in the DB and check if the user is admin
        if identity ==1 :
            return {'is_admin': True}
        return {'is_admin':False}


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({'message': 'The token has expired',  
                         'error':'token_expired'}), 
                          401,)
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({'message': 'Signature verification failed',  
                         'error':'invalid_token'}), 
                          401,)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({'description': 'Request does not contains an access token',  
                         'error':'authorization requiered'}), 
                          401,)
    

    


    

   # with app.app_context(): Since we will use Flask-Migrate to create our database tables, we no longer need AQLAlchemy to do it
   #      db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app



