import pandas as pd
import functools

class REGenerator(object):
    """This class ecnapsulates the functionality required to select content for Referring Expressions (RE) in an NLG system."""

    def __init__(self, dom_file):
        """
        Initialise an RE Generator

        :param dom_file: path to a csv file containing a representation of domain entities, attribtues and values. Referents are indexed by their row number (from 0), each row specifies their values of particular attributes. Top row is the attribute names.
        :type dom_file: str
        """
        self._dom_file = dom_file
        self.domain = pd.read_csv(open(self.domain_file, 'r', encoding='utf-8'))

    @property
    def domain_file(self):
        """
        Get the filepath to the domain associated with this REGenerator.
        :return: the file
        :rtype: str
        """
        return self._dom_file

    @property
    def attributes(self):
        """
        Get the attributes read from the domain file.
        :return: the attributes
        :rtype: list
        """
        return list(self.domain)

    def properties_of(self, referent_id):
        """
        Get the properties of a particular referent.
        :param referent_id: the referent ID (i.e. its row in the domain)
        :type referent_id: int
        :return: the properties of this referent, represented as (attribute, value) pairs.
        :rtype: list
        """
        return [(a, self.domain[a][referent_id]) for a in self.attributes]

    def __compare(self, p1, p2):
        """
        This method compares two properties (attribue-value pairs) and determines their relative
        order. This method is what determines which properties will be considered first.
        Currently, this method prioritises properties by the preference order of attributes,
        which is determined by the order in which attributes are listed in the first row of the
        domain file.

        :param p1: a property, consisting of an attribute and a value
        :type p1: tuple
        :param p2: a property, consisting of an attribute and a value
        :type p2: tuple
        :return: a number indicating the comparison
        :rtype: int
        """
        return self.attributes.index(p1[0]) - self.attributes.index(p2[0])


    def is_true_of(self, attribute, value, entity_id):
        """
        Check whether a property (attribute-value pair) is true of some entity.
        :param attribute: the attribute
        :type attribute: str
        :param value: the value
        :type value: object
        :param entity_id: the referent
        :type entity_id: int
        :return: true if the referent has this property
        :rtype: bool
        """
        if attribute in self.domain:
            return value in self.domain[attribute][entity_id]
        return False

    def __excludes(self, att, val, distractors):
        """
        Check if a property (attribute + value) excludes any entities, i.e. if there are any entities
        that do not have this property
        :param att: the attribute
        :type att: str
        :param val: the value
        :type val: object
        :param distractors: the set of distractors
        :type distractors: set
        :return: the subset of distractors which are excluded by this property
        :rtype: set
        """
        excluded = set([d for d in distractors if val not in self.domain[att][d]])
        return excluded

    def __pick_property(self, properties):
        """
        Generator function. Pops the next avalable property in an ordered list and returns it.
        :param properties: the list of properties
        :type properties: list
        :return: the next property (an attribute-value pair)
        :rtype: tuple
        """
        while properties:
            yield properties.pop()

    def make_re(self, referent_id):
        """
        Make a referring expression for a specific referent. This procedure
        will pick properties one by one, check if they exclude any distratcors, and include
        them in the description if they do, updating the remaining distractor set in the process.
        The procedure terminates when either there are no properties left, or
        all distractors have been excluded.

        :param referent_id: The intended referent
        :type referent_id: int
        :return: The description, a set of proeprties (attribute-value pairs)
        :rtype: set

        """
        #Check if the referent requested is in the domain
        if not self.domain.index.contains(referent_id):
            raise RuntimeError('Referent ' + str(referent_id) + ' is not in the domain')

        description = set() #init empty description, as a set
        distractors = set(list(self.domain.index)) #init distractor set
        distractors.remove(referent_id)

        #pull out the properties for this referent
        #properties are (a,v) pairs
        properties = self.properties_of(referent_id)

        #sort the properties by some heuristic...
        properties = sorted(properties, key=functools.cmp_to_key(self.__compare), reverse = True)

        while len(distractors) > 0:
            try:
                p = next(self.__pick_property(properties)) #next property
                excl = self.__excludes(p[0], p[1], distractors) #which distractors are excluded?

                if excl:
                    description.add(p) #add property if some distractors are excluded
                    distractors -= excl #remove excluded distractors

            except StopIteration: #break if there's no more properties left
                break

        return description


if __name__ == '__main__':
    reg = REGenerator('domain_ex.csv')
    description = reg.make_re(0)
    print(description)


