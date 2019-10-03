from flask import Blueprint
from .urls import add_urls

smoke_app = Blueprint('smoke_app', __name__)

add_urls(smoke_app)
