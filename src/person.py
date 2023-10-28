import json
from enum import Enum
from typing import List

DAYS_BEFORE_HEALING = 7

class Status(Enum):
    """
    Class that defines all possible Status for a person
    """
    HEALTHY = "HEALTHY"
    SICK = "SICK"
    DEAD = "DEAD"
    IMMUNE = "IMMUNE" 

class NeighbourhoodArea:
    def __init__(self, position_x: float, position_y: float, radius: float):
        """Class that defines the area that represents neighborood of a person

        Args:
            position_x (float): position on x axis of the person
            position_y (float): position on y axis of the person
            radius (float): radius to define area
        """
        self.x_min = position_x - radius
        self.y_min = position_y - radius
        self.x_max = position_x + radius
        self.y_max = position_y + radius

class Person:
    def __init__(self, 
                 id: int, 
                 position_x: float, 
                 position_y: float, 
                 initial_status: Status, 
                 radius_neighbors: float):
        """Class that defines a person

        Args:
            id (int): id of the person (unique)
            position_x (float): position on x axis of the person
            position_y (float): position on y axis of the person
            initial_status (Status): initial status given at the beginning of the simulation
            radius_neighbors (float): radius that defines the area of the persons's neighborhood
        """
        self.id = id
        self.position_x = position_x
        self.position_y = position_y
        self.status: str = initial_status.value
        self.consecutive_days_seek = 0
        self.neighborood_area = NeighbourhoodArea(self.position_x, 
                                                  self.position_y, 
                                                  radius_neighbors)
        self.neighbors: List[int] = []
    
    def update_status(self):
        """Function that updates the status of a person
        """
        if (self.status == Status.SICK.value) and (self.consecutive_days_seek >= DAYS_BEFORE_HEALING):
            self.status = Status.IMMUNE.value
    
    def next_epoch(self):
        """Function that defines the next state of a person
        """
        if (self.status == Status.SICK.value):
            self.consecutive_days_seek += 1 
    
    def genererate_list_of_neighbors(self, list_of_persons):
        """Function that creates the list of neighbors of a person

        Args:
            list_of_persons (List[Person]): list of persons representing a population
        """
        for person in list_of_persons:
            if (self.neighborood_area.x_max > person.position_x) \
                and (self.neighborood_area.x_min < person.position_x) \
                and (self.neighborood_area.y_max > person.position_y) \
                and (self.neighborood_area.y_min < person.position_y) \
                and (self.id != person.id):
                self.neighbors.append(person.id)
     
    def __str__(self) -> str:
        """Representation of a person

        Returns:
            str: arguments of a person on a dict format
        """
        args_to_skip = ["neighborood_area"]
        arguments = {key : value for key, value in self.__dict__.items() if key not in args_to_skip}
        return str(arguments)
