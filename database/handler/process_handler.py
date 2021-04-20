from neomodel import config, StructuredNode, StringProperty, UniqueIdProperty, \
    RelationshipTo, relationship, db
from datetime import datetime

from core.success_handler import success_handler
from database.handler.relationships import RelationshipProcessComponent, RelationshipProcessMetric
import database.handler.component_handler as component_handler
import database.handler.metric_handler as metric_handler
import database.handler.reformatter as reformatter
import database.handler.queries as queries
from database.config import *

config.DATABASE_URL = 'bolt://{}:{}@{}:{}'.format(NEO4J_USER, NEO4J_PASSWORD, NEO4J_IP, NEO4J_PORT)


class Process(StructuredNode):
    """
    A class to represent a Process.

    Attributes
    ----------
    uid : str
        process id
    name : str
        name of the process
    responsible_person : str
        name of the responsible person
    description : str
        description of the process
    creation_timestamp : str
        timestamp of creation time
    last_timestamp : str
        timestamp of last update
    includesComponent : relationship
        relationship to component
    hasMetric : relationship
        relationship to metric
    """

    uid = UniqueIdProperty()
    name = StringProperty()
    responsible_person = StringProperty()
    description = StringProperty()
    creation_timestamp = StringProperty()
    last_timestamp = StringProperty()

    hasComponent = RelationshipTo(component_handler.Component, "includes", model=RelationshipProcessComponent)
    hasMetric = RelationshipTo(metric_handler.Metric, "targets", model=RelationshipProcessMetric)


def get_process_list() -> dict:
    """
    Function to retrieve a list of all processes

    :return: List of processes in a dict
    """
    output_dict = success_handler()

    query = queries.get_process_list()
    result, meta = db.cypher_query(query)
    output_dict["process"] = result[0][0]

    return output_dict


def get_process(input_dict: dict) -> dict:
    """
    Function to retrieve a single process

    :param input_dict: process uid
    :type input_dict: dict
    :return: process dict
    """
    output_dict = success_handler()

    query = queries.get_process(input_dict["uid"])
    result, meta = db.cypher_query(query)
    output_dict["process"], output_dict["target_metrics"] = reformatter.reformat_process(result[0])

    return output_dict


def add_process(input_dict: dict) -> dict:
    """
    Function to add a single process

    :param input_dict: process as a dictionary
    :type input_dict: dict
    :return: Status dict
    """

    output = Process(
        name=input_dict["process"]["name"],
        responsible_person=input_dict["process"]["responsible_person"],
        creation_timestamp=str(datetime.now()),
        last_timestamp=str(datetime.now()),
        description=input_dict["process"]["description"])

    output.save()

    for metric in input_dict["target_metrics"]:
        output.hasMetric.connect(metric_handler.Metric.nodes.get(name=metric),
                                 {"value": input_dict["target_metrics"][metric]})

    output_dict = success_handler()
    output_dict["process_uid"] = output.uid

    return output_dict


def update_process(input_dict: dict) -> dict:
    """
    Function to edit a single process

    :param input_dict: process as a dictionary
    :type input_dict: dict
    :return: Status dict
    """
    uid = input_dict["process"]["uid"]

    query = queries.update_process(uid, input_dict["process"]["name"], input_dict["process"]["responsible_person"],
                                   input_dict["process"]["description"], str(datetime.now()))
    db.cypher_query(query)

    for metric in input_dict["target_metrics"]:
        query = queries.update_process_metric(uid, metric, input_dict["target_metrics"][metric])
        db.cypher_query(query)

    return success_handler()


def delete_process(input_dict: dict) -> dict:
    """
    Function to delete a single process

    :param input_dict: Identifier
    :type input_dict: dict
    :return: Status dict
    """

    query = queries.delete_process(input_dict["uid"])
    db.cypher_query(query)

    return success_handler()


def add_process_reference(input_dict: dict) -> dict:
    """
    Function to add a process reference (to a component included in the respective process)

    :param input_dict: a dictionary containing process uid, component id and weight
    :type input_dict: dict
    :return: Status dict
    """

    process = Process.nodes.get(uid=input_dict['process_uid'])
    component = component_handler.Component.nodes.get(uid=input_dict['component_uid'])

    process.hasComponent.connect(component, {"weight": input_dict["weight"]})

    return success_handler()


def update_process_reference(input_dict: dict) -> dict:
    """
    Function to edit a process reference (to a component included in the respective process)

    :param input_dict: process uid and an old and new weight
    :type input_dict: dict
    :return: Status dict
    """

    process = Process.nodes.get(uid=input_dict['uid'])

    component_list = process.hasComponent.all()

    for component in component_list:
        rel = process.hasComponent.relationship(component)
        if rel.weight == input_dict['old_weight']:
            rel.weight = input_dict['new_weight']
            rel.save()

    return success_handler()


def delete_process_reference(input_dict: dict) -> dict:
    """
    Function to delete a process reference (to a component not longer in the respective process)

    :param input_dict: a dictionary including the process uid and a weight
    :type input_dict: dict
    :return: Status dict
    """

    db.cypher_query('Match (n: Process {uid: "' + input_dict['uid'] +
                    '"})-[r: includes {weight: ' + str(input_dict['weight']) + '}] -() Delete r')

    return success_handler()
