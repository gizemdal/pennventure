# NPC
from character import Character

# Multiclass classifier: trained to classify interactions
class MulticlassPerceptron(object):

    def __init__(self, data):
        self.interactions = {}
        # first get the labels
        for (x, y) in data:
            # categories
            info = { 'friendly': 0.0, 'romantic': 0.0, 'hostile': 0.0, 'neutral': 0.0 }
            self.interactions[y] = info
        iterations = 20
        for i in range(iterations):
            for d in data:
                c = self.classify(d[0])
                if c != d[1]:
                    self.interactions[c]['friendly'] -= d[0][0]
                    self.interactions[d[1]]['friendly'] += d[0][0]
                    self.interactions[c]['romantic'] -= d[0][1]
                    self.interactions[d[1]]['romantic'] += d[0][1]
                    self.interactions[c]['hostile'] -= d[0][2]
                    self.interactions[d[1]]['hostile'] += d[0][2]
                    self.interactions[c]['neutral'] -= d[0][3]
                    self.interactions[d[1]]['neutral'] += d[0][3]

    def classify(self, instance):
        l = ""
        maxDot = - float('inf')
        for label in self.interactions:
            friendly = instance[0] * self.interactions[label]['friendly']
            romantic = instance[1] * self.interactions[label]['romantic']
            hostile = instance[2] * self.interactions[label]['hostile']
            neutral = instance[3] * self.interactions[label]['neutral']
            sum = friendly + romantic + hostile + neutral
            if sum > maxDot:
                maxDot = sum
                l = label
        return l

class NPC(Character):

    def __init__(self, name="", location=None):
        super(NPC, self).__init__(name, location)