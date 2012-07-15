def get_app_name_for_model(model):
    return model.__module__.split('.')[-2]