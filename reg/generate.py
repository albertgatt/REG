import pandas as pd
import functools

class REGenerator(object):

    def __init__(self, dom_file):
        self._dom_file = dom_file
        self.domain = pd.read_csv(open(self.domain_file, 'r', encoding='utf-8'))

    @property
    def domain_file(self):
        return self._dom_file

    @property
    def attributes(self):
        return list(self.domain)

    def properties_of(self, referent_id):
        return [(a, self.domain[a][referent_id]) for a in self.attributes]

    def __compare(self, p1, p2):
        return self.attributes.index(p1[0]) - self.attributes.index(p2[0])


    def is_true_of(self, attribute, value, entity_id):
        if attribute in self.domain:
            return value in self.domain[attribute][entity_id]
        return False

    def __excludes(self, att, val, distractors):
        '''Check if a property excludes any distractors in a particular set'''
        excluded = set([d for d in distractors if val not in self.domain[att][d]])
        return excluded

    def __pick_property(self, properties):
        while properties:
            yield properties.pop()

    def make_re(self, referent_id):
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


