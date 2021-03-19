import csv
from neomodel import config, StructuredNode, StringProperty
from database.config import *

config.DATABASE_URL = 'bolt://{}:{}@{}:{}'.format(NEO4J_USER, NEO4J_PASSWORD, NEO4J_IP, NEO4J_PORT)


class Metric(StructuredNode):
    """
    A class to represent a Metric.

    Attributes
    ----------
    name : str
        name of the metric
    description : str
        description of the metric
   """

    name = StringProperty()
    description = StringProperty()


def create_from_csv(path: str):
    """
    Function to create metrics out of an csv file

    :param path: Path to the csv file
    :type path: int
    """

    with open(path) as csv_file:
        csv_reader_object = csv.reader(csv_file)
        for row in csv_reader_object:
            Metric.create({'name': row[0], 'description': row[1]})
        print(Metric.nodes.all())