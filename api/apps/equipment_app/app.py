from helper_classes.application_blueprint import ApplicationBlueprint
from .controllers import controllers
from .models import models

app = ApplicationBlueprint('equipment', __name__, controllers, models_list=models)
