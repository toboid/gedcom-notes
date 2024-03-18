from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from gedcom.parser import Parser
import gedcom.tags


class Individual:
    def __init__(self, individual_element, gedcom):
        self.individual_element = individual_element
        self.gedcom = gedcom

    def __getattr__(self, attr):
        return getattr(self.individual_element, attr)

    def get_display_name(self):
        return ' '.join(self.individual_element.get_name()).title()

    def get_birth_date(self):
        dt, *_ = self.get_birth_data()
        return dt

    def get_date_of_birth(self):
        dt, _, _ = self.get_birth_data()
        return dt

    def get_place_of_birth(self):
        _, place, _ = self.get_birth_data()
        return place

    def get_date_of_death(self):
        dt, _, _ = self.get_death_data()
        return dt

    def get_place_of_death(self):
        _, place, _ = self.get_death_data()
        return place

    def get_parents(self):
        parents = self.gedcom.get_parents(self.individual_element)
        return map(lambda p: Individual(p, self.gedcom), parents)

    def get_children(self):
        all_children = []
        for family in self.gedcom.get_families(self.individual_element):
            children = map(lambda f: Individual(f, self.gedcom),
                           self.gedcom.get_family_members(family, gedcom.tags.GEDCOM_TAG_CHILD))
            all_children.extend(list(children))
        return all_children

    def get_partners(self):
        family_parents = []
        for family in self.gedcom.get_families(self.individual_element):
            parents = map(lambda f: Individual(f, self.gedcom),
                          self.gedcom.get_family_members(family, 'PARENTS'))
            family_parents.extend(list(parents))
        return filter(lambda p: p.get_pointer() != self.individual_element.get_pointer(), family_parents)
        # return family_parents


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
