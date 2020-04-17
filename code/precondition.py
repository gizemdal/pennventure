# Preconditions

precondition_id = 0 # unique precondition id, assigned by creation order

class Precondition(object):
    
    def __init__(self, condition_context, elems):
        global precondition_id
        self.context = condition_context
        self.elems = elems
        self.id = precondition_id
        precondition_id += 1

    def __eq__(self, other):
        return self.id == other.id

    def create_precondition_tuple(self):
        return (self.context, self.elems)
