from pyecharts import options as opts
from pyecharts.charts import Tree, TreeMap, Page

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
                if key not in [
                    'params', 
                    'percentage', 
                    'params.sum', 
                    'percentage.sum'
                ]:
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
            result.append(
                {
                    "name": name, 
                    "value": value_sum, 
                    "children": children
                }
            )
    return result


def create_charts(
    param_dict: dict,
    tree: bool=True,
    treemap: bool=True,
    dir: str=None
):
    """
    Draw a tree chart and a TreeMap chart to visualize the parameters.
    :param param_dict: The dictionary containing the parameters and their percentages.
    :param tree: Whether to draw a tree chart. Default is True.
    :param treemap: Whether to draw a TreeMap chart. Default is True.
    :param dir: The directory to save the charts HTML file.
    """
    page = Page()
    full_path = f"{dir}/params_chart.html"
    
    # Convert the parameter dictionary to a tree
    if tree:
        tree_data = [dict_to_tree("Model", param_dict)]
        # Create a Tree chart
        tree = (
            Tree(init_opts=opts.InitOpts(width="1920px", height="1080px"))
            .add(
                "", 
                tree_data, 
                collapse_interval=2,
                initial_tree_depth=2,
                label_opts=opts.LabelOpts(font_size=24)
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Model Parameters")
            )
        )        
        page.add(tree)
        
    if treemap:
        TreeMap_data = dict_to_TreeMap(param_dict) 
        # Create a TreeMap chart
        treemap = (
            TreeMap(init_opts=opts.InitOpts(width="1920px", height="1080px"))
            .add(
                "", 
                TreeMap_data, 
                label_opts=opts.LabelOpts(
                    is_show=True, 
                    position="inside", 
                    font_size=24
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Portion Map")
            )
        )
        page.add(treemap)
        
    # Render the chart
    page.render(full_path)