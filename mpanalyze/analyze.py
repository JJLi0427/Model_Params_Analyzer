# Usage:
# calculate_parameters(model)

from typing import Optional
from .utils import save_parameters_to_json, start_http_server, make_analyze_dir
from .generate_cahrts import create_charts
from .get_params_dict import calculate_dict

def params_analyze(
    model: object, 
    name: Optional[str]=None,
    port: Optional[int]=None,
    save_dict: Optional[bool]=True,
    tree: Optional[bool]=True,
    treemap: Optional[bool]=True
):
    """
    Calculate the number of parameters in the model and their percentages.
    Draw a tree chart and a TreeMap chart to visualize the parameters.
    :param model: The model to analyze.
    :param name: The name of the model. If not specified, the directory name will be 'params_analyze'.
    :param port: The port to use for the HTTP server. If not specified, the browser will not be opened. Recommended only use in Debug mode. If you want to use in training, it will block the training process.
    :param save_dict: Whether to save the parameters to a JSON file. Default is True.
    :param tree: Whether to draw a tree chart. Default is True.
    :param treemap: Whether to draw a TreeMap chart. Default is True.
    """
    try:
        if save_dict == False and tree == False and treemap == False:
            print("Not saving any analyze file. Printing the parameters calculate dict instead.")
            param_dict = calculate_dict(model)
            print(param_dict)
            return
        else:
            dir = make_analyze_dir(name)
            param_dict = calculate_dict(model)
            if save_dict:
                save_parameters_to_json(param_dict, dir)
            if tree and treemap:
                create_charts(
                    param_dict, 
                    tree, 
                    treemap, 
                    dir
                )
                start_http_server(port)
    except Exception as e:
        print("Failed to calculate parameters: {}".format(e))