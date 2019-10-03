from helper_classes.application_blueprint import ApplicationBlueprint
from .urls import urls
from .controllers import controllers

smoke_app = ApplicationBlueprint('smoke_app', __name__, controllers, urls)
