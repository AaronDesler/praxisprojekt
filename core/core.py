from typing import Dict, Any, Union

import database
import processing


def get_component_list() -> str:
    """Calls the get_compontent_list method and converts the output to JSON

    Returns:
        str: A JSON formatted compontent list
    """
    component_list_dict = database.get_component_list()
    output_json = processing.dict_to_json(component_list_dict)

    return output_json


def create_edit_component(input_object: Union[Dict[str, Any], str]) -> str:
    """
    Receives a JSON object in the form defined under JSON_objects_defitnions.py for either editing a component or creating a new component
    The answer is also a JSON object, only containing the success state, which is True or False
    
    :param input_object: JSON object containing all component attributes (special information to differentiate edit or create is contained in the UID, which is either -1 or the original UID
    :type input_object: str
    :return A JSON object containing the success state, which is True or False
    """

    data_dict = processing.json_to_dict(input_object)

    if data_dict["uid"] == "-1":
        result_dict = database.add_component(data_dict)
        return processing.dict_to_json(result_dict)
    else:
        result_dict = database.update_component(data_dict)
        return processing.dict_to_json(result_dict)


def get_component(input_object: str) -> str:
    """
    Receives a JSON object in the form defined under JSON_objects_defitnions.py for getting/viewing a component.
    It returns another JSON object, sturctured as described in docu/JSON_objects_definitions.py
    which is retreived from the component_handler.

    :param input_object: JSON object containing the component uid
    :type input_object: str
    :return: Returns a JSON object, sturctured as described in docu/JSON_objects_definitions.py
    """

    data_dict = processing.json_to_dict(input_object)
    component_dict = database.get_component(data_dict)
    output_json = processing.dict_to_json(component_dict)

    return output_json


def delete_component(input_object: str) -> str:
    """Calls the delete_component method and returns whether successful or not in JSON Format

    Args:
        data (str): String in JSON Format

    Returns:
        (str): String in JSON Format

    :param input_object:
    """

    data_dict = processing.json_to_dict(input_object)
    result_dict = database.delete_component(data_dict)
    output_json = processing.dict_to_json(result_dict)

    return output_json