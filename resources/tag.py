from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import TagSchema

blp = Blueprint('Tags', 'tags' , description = 'Operations on tags')