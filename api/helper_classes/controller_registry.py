class ControllerRegistry:
    def add_controller(self, controller):
        name = controller.__name__
        print(name)
        setattr(self, name, controller)
