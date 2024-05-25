def calculate_parameters_and_percentages(model: object):
    """
    Calculate the number of parameters in the model and their percentages.
    :param model: The model to analyze.
    """
    param_dict = {}
    total_params = 0

    for name, param in model.named_parameters():
        if param.requires_grad:
            num_params = param.numel()
            total_params += num_params

            # Split the name by '.' and create nested dictionaries
            keys = name.split('.')
            sub_dict = param_dict
            for key in keys[:-1]:
                if key not in sub_dict:
                    sub_dict[key] = {}
                sub_dict = sub_dict[key]

            # Add the parameter count and percentage to the innermost dictionary
            sub_dict[keys[-1]] = {'params': num_params, 'percentage': num_params / total_params * 100}

    return param_dict, total_params


def add_sums(sub_dict: dict):
    """
    Get the sum of the parameters and percentages in the dictionary.
    :param sub_dict: The dictionary to calculate the sum.
    """
    params_sum = 0
    percentage_sum = 0
    for key, value in sub_dict.items():
        if isinstance(value, dict):
            if 'params' in value and 'percentage' in value:
                params_sum += value['params']
                percentage_sum += value['percentage']
            else:
                value = add_sums(value)
                params_sum += value.get('params.sum', 0)
                percentage_sum += value.get('percentage.sum', 0)
    sub_dict['params.sum'] = params_sum
    sub_dict['percentage.sum'] = percentage_sum
    return sub_dict

def calculate_dict(model):
    """
    Get the dictionary of parameters and their percentages.
    :param model: The model to analyze.
    """
    param_dict, _ = calculate_parameters_and_percentages(model)
    param_dict = add_sums(param_dict)
    return param_dict