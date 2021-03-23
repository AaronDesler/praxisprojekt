# external endpoints
from flask import Flask, render_template, request

import core

app = Flask(__name__, static_url_path='',
            template_folder='../frontend/templates', static_folder='../frontend/static')


@app.route('/', methods=["GET"])
def index():
    """
    API endpoint to display main page view

    :return: the rendered html main page
    """
    return render_template("index.html")


@app.route('/component', methods=["GET"])
def component():
    """
    API endpoint to display component page view

    :return: the rendered html component page
    """
    return render_template("component.html")


@app.route('/process', methods=["GET"])
def process():
    """
    API endpoint to display component page view

    :return: the rendered html process page
    """
    return core.error_handler(500, "Noch nicht umgesetzt")


@app.route("/component/overview", methods=["GET"])
def get_component_overview():
    """
    API Endpoint returning all components for the Index site
    :receives None
    :return: a JSON object containing a list of components
    """

    components = core.get_component_list()

    return components


@app.route("/component/delete", methods=["POST"])
def do_component_delete():
    """
    API Endpoint to delete a specific component

    :return: a JSON object with the success of the deletion
    """
    x = request.data
    if request.is_json:
        try:
            result = core.delete_component(request.json)

            return result, 200

        except:
            return "Internal Error", 500
    else:
        return "No JSON body was transferred", 400


@app.route('/component/view', methods=["POST"])
def component_view_route():
    """
    API endpoint to use the function from the Core-Module to view components
    """

    if request.is_json:
        try:
            return core.get_component(request.json), 200
        except:
            return "Internal Error", 500
    else:
        return core.error_handler(400, "No JSON body was transferred")


@app.route('/component/create_edit', methods=["POST"])
def component_create_edit_route():
    """
    Use function from the Core-Module to create or edit components (Original function is located in component_handler.py
    """

    if request.is_json:
        return core.create_edit_component(request.json), 200
    else:
        return core.error_handler(400, "No JSON body was transferred")
