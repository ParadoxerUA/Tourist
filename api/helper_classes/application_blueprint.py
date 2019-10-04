from flask import Blueprint
from helper_classes.controller_registry import ControllerRegistry


class ApplicationBlueprint(Blueprint):
    def __init__(self, name, import_name, controllers_list, urls_dict):
        super().__init__(name, import_name)
        self.controllers_list = controllers_list
        self.urls_dict = urls_dict

    def setup_urls(self):
        for rule, class_view in self.urls_dict.items():
            view_name = class_view.__class__.__name__
            self.add_url_rule(rule, view_func=class_view.as_view(view_name))

    def setup_controllers(self):
        controller_registry = ControllerRegistry()
        
        for controller in self.controllers_list:
            controller_registry.add_controller(controller)

        self.controllers = controller_registry
