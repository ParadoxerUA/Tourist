def register_controllers():
    from .smoke_controller import SmokeController
    controllers = [SmokeController]
    controller_object = lambda: None
    for controller in controllers:
        setattr(controller_object, 'smoke', controller)

    return controller_object
