from person import Person, Status
import numpy as np
import math
import random
from typing import List

class Population:
    def __init__(self, size: int, positionnal_variance: float, 
                 radius_neighbors: float, nb_infected: int, immunity_prob: float):
        """Class that aggregates a list of persons

        Args:
            size (int): nb of persons in our population
            positionnal_variance (float): variance of positions between persons
            radius_neighbors (float): distance that tell if a person is a neighbor or not of another person
            nb_infected (int): nb of people infected at the creation of the population
            immunity_prob (float): among all healthy persons, probability to be immune 
        """
        self.size = size
        self.positionnal_variance = positionnal_variance
        self.radius_neighbors = radius_neighbors
        self.nb_infected = nb_infected
        self.immunity_prob = immunity_prob
        self.persons: List[Person] = []
    
    def get_person_by_id(self, id_to_retrieve: int) -> Person:
        """Function to access a person thanks to its id

        Args:
            id_to_retrieve (int): id of the person we want to return

        Returns:
            Person: person we want to retrieve
        """
        for person in self.persons:
            if id_to_retrieve == person.id:
                return person
    
    def generate_list_of_persons(self) -> List[Person]:
        """Function that creates a population of multiple persons, based on class attributes

        Returns:
            List[Person]: all persons of the population
        """
        all_population = []
        mu, sigma = 0, math.sqrt(self.positionnal_variance)
        all_possible_x = np.random.normal(mu, sigma, self.size)
        all_possible_y = np.random.normal(mu, sigma, self.size)
        persons_infected_ids = [random.randint(0, self.size) for _ in range(self.nb_infected)]
        for i in range(self.size):
            position_x = all_possible_x[i]
            position_y = all_possible_y[i]
            if i in persons_infected_ids:
                person = Person(i, position_x, position_y, Status.SICK, self.radius_neighbors)
            else:
                is_immune = np.random.choice([True, False], p=[self.immunity_prob, 1-self.immunity_prob])
                if is_immune:
                    person = Person(i, position_x, position_y, Status.IMMUNE, self.radius_neighbors)
                else:
                    person = Person(i, position_x, position_y, Status.HEALTHY, self.radius_neighbors)
            all_population.append(person)
        
        self.persons = all_population

    def neighbors_attribution(self):
        """
        Function that assigns to each person its list of neighbors
        """
        for person in self.persons:
            person.genererate_list_of_neighbors(self.persons)
    
    def __str__(self) -> str:
        infos = {}
        infos["nb_persons"] = self.size
        infos["nb_infected_start"] = self.nb_infected
        for status in (list(Status)):
            infos[f"current_{status.value}"]=0
            for person in self.persons:
                if status.value == person.status:
                    infos[f"current_{status.value}"]+=1
        return str(infos)
        
pop = Population(size = 10, 
                 positionnal_variance = 2, 
                 radius_neighbors = 1, 
                 nb_infected = 2, 
                 immunity_prob = 0.5)
pop.generate_list_of_persons()
pop.neighbors_attribution()
print(np.random.choice([0,1], p=[0.8, 0.2]))
for person in pop.persons:
    print("for")
    print(person)

print(pop)