from helper_classes.application_blueprint import ApplicationBlueprint
from .urls import urls
from .controllers import controllers
from .models import models

app = ApplicationBlueprint('user', __name__, controllers, urls_dict=urls, models_list=models)
