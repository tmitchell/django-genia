"""genia/utils.py

Helper functions and other misc code that is shared
"""

def get_app_name_for_model(model):
    """Extract the app name from a model class

        :param model: Generational model
        :type app_name: Django Model
        :return: App name containing model
        :rtype: String
    """
    return model.__module__.split('.')[-2]