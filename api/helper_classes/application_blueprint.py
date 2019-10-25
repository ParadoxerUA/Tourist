from flask import Blueprint
from helper_classes.controller_registry import ControllerRegistry
from helper_classes.model_registry import ModelRegistry


class ApplicationBlueprint(Blueprint):
    def __init__(self, name, import_name, controllers_list, urls_dict, models_list=None):
        super().__init__(name, import_name)
        self.controllers_list = controllers_list
        self.models_list = models_list
        self.urls_dict = urls_dict
        self.controllers = None
        self.name = name

    def setup_urls(self):
        for rule, class_view in self.urls_dict.items():
            self.add_url_rule(rule, view_func=class_view)

    def setup_controllers(self):
        controller_registry = ControllerRegistry()
        
        for controller in self.controllers_list:
            controller_registry.add_controller(controller)
        self.controllers = controller_registry

    def setup_models(self):
        if self.models_list is not None:
            model_registrator = ModelRegistry()
            model_registrator.set_app_models(self.models_list)
