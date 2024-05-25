# Usage:
# calculate_parameters(model)

import os
import json
import webbrowser
import http.server
import socketserver

from typing import Optional
from pyecharts import options as opts
from pyecharts.charts import Tree, TreeMap, Page

from .utils import dict_to_tree, dict_to_TreeMap


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


def create_charts(param_dict: dict):
    """
    Draw a tree chart and a TreeMap chart to visualize the parameters.
    :param param_dict: The dictionary containing the parameters and their percentages.
    """
    # Convert the parameter dictionary to a tree
    tree_data = [dict_to_tree("Model", param_dict)]
    TreeMap_data = dict_to_TreeMap(param_dict)
    
    page = Page() 
    
    # Create a Tree chart
    tree = (
        Tree(init_opts=opts.InitOpts(width="1920px", height="1080px"))
        .add(
            "", 
            tree_data, 
            collapse_interval=2,
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Model Parameters"))
    )

    # Create a TreeMap chart
    treemap = (
        TreeMap(init_opts=opts.InitOpts(width="1920px", height="1080px"))
        .add(
            "", 
            TreeMap_data, 
            label_opts=opts.LabelOpts(is_show=True, position="inside"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Portion Map"))
    )

    # Combine the charts using Grid
    page.add(tree)
    page.add(treemap)
    # Render the chart
    
    page.render("./params_analyze/model_parameters.html")


def save_parameters_to_json(param_dict: dict):
    """
    Save the parameters and their percentages to a JSON file.
    :param param_dict: The dictionary containing the parameters and their percentages.
    """
    try:
        with open('./params_analyze/model_params.json', 'w') as f:
            json.dump(param_dict, f, indent=4)
    except IOError as e:
        print("Failed to save parameters to JSON: {}".format(e))


def start_http_server(port: int):
    """
    Start an HTTP server to serve the charts.
    :param port: The port to use for the HTTP server. If not specified, the browser will not be opened.
    """
    try:
        if port is not None:
            Handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", port), Handler) as httpd:
                webbrowser.open_new_tab('http://localhost:{}/params_analyze/model_parameters.html'.format(port))
                httpd.serve_forever()
    except Exception as e:
        print("Failed to start HTTP server: {}".format(e))


def calculate_parameters(model: object, port: Optional[int]=None):
    """
    Calculate the number of parameters in the model and their percentages.
    Draw a tree chart and a TreeMap chart to visualize the parameters.
    :param model: The model to analyze.
    :param port: The port to use for the HTTP server. If not specified, the browser will not be opened. Recommended only use in Debug mode. If you want to use in training, it will block the training process.
    """
    try:
        os.makedirs("params_analyze", exist_ok=True)
        param_dict, _ = calculate_parameters_and_percentages(model)
        param_dict = add_sums(param_dict)
        create_charts(param_dict)
        save_parameters_to_json(param_dict)
        start_http_server(port)
    except Exception as e:
        print("Failed to calculate parameters: {}".format(e))