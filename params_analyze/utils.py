def dict_to_tree(name, param_dict):
    """
    Make a tree from a dictionary.
    :param name: The name of the root node.
    :param param_dict: The dictionary to convert to a tree.
    """
    children = []
    for key, value in param_dict.items():
        if key not in [
            'params', 
            'percentage', 
            'params.sum', 
            'percentage.sum', 
        ]:
            if isinstance(value, dict):
                children.append(dict_to_tree(key, value))
            else:
                children.append({"name": f"{key}: {value}"})
    return {"name": name, "children": children}

def dict_to_TreeMap(param_dict):
    """
    Make a TreeMap from a dictionary.
    :param param_dict: The dictionary to convert to a TreeMap.
    """
    result = []
    for name, value in param_dict.items():
        if isinstance(value, dict):
            children = []
            for key, subvalue in value.items():
                if key not in ['params', 'percentage', 'params.sum', 'percentage.sum']:
                    if isinstance(subvalue, dict):
                        children.extend(dict_to_TreeMap({key: subvalue}))
                    else:
                        children.extend({"name": f"{key}: {subvalue}", "value": subvalue})
            if 'params.sum' in value:
                value_sum = value['params.sum']
            elif 'params' in value:
                value_sum = value['params']
            else:
                value_sum = 0
            result.append({"name": name, "value": value_sum, "children": children})
    return result