import os
import time
import json
import webbrowser
import http.server
import socketserver

def make_analyze_dir(dir_name: str):
    """
    Make directories to save the charts and JSON file.
    :param dir_name: The name of the directory to save the charts and JSON file.
    """
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        if dir_name is not None:
            os.makedirs(f"{dir_name}_mpanalyze_{timestamp}", exist_ok=True)
        os.makedirs(f"mpanalyze_{timestamp}", exist_ok=True)
    except Exception as e:
        print("Failed to create directories: {}".format(e))
        
    return f"{dir_name}_params_analyze" if dir_name is not None else "params_analyze"


def save_parameters_to_json(param_dict: dict, dir: str):
    """
    Save the parameters and their percentages to a JSON file.
    :param param_dict: The dictionary containing the parameters and their percentages.
    """
    full_path = f"{dir}/model_params.json"
    try:
        with open(full_path, 'w') as f:
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
            print("Starting HTTP server...If in training, it will block the training process.")
            Handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", port), Handler) as httpd:
                webbrowser.open_new_tab('http://localhost:{}/params_analyze/model_parameters.html'.format(port))
                httpd.serve_forever()
    except Exception as e:
        print("Failed to start HTTP server: {}".format(e))