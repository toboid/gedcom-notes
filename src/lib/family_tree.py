from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from gedcom.parser import Parser

from .individual import Individual


class FamilyTree:
    def __init__(self, gedcom_file_path):
        self.gedcom = Parser()
        self.gedcom.parse_file(gedcom_file_path)

        self.individuals = []
        self.families = []
        self.other = []

        for element in self.gedcom.get_root_child_elements():
            if isinstance(element, IndividualElement):
                self.individuals.append(Individual(element, self.gedcom))
            elif isinstance(element, FamilyElement):
                self.families.append(element)
            else:
                self.other.append(element)

    def find(self, search):
        search_items = [f'{key}={value}' for key, value in search.items()]
        search_string = ':'.join(search_items)

        print(search_string)

        for individual in self.individuals:
            if individual.criteria_match(search_string):
                return individual

    def get_ancestors(self, individual):
        return [Individual(a, self.gedcom) for a in self.gedcom.get_ancestors(individual.individual_element)]
