from django.forms import model_to_dict


def full_model_to_dict(model):
    converted_model = model_to_dict(model)
    converted_model["id"] = model.id
    return converted_model
