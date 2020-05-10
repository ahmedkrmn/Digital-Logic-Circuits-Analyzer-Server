from gate import gate

class NOT (gate) :

    def calc(self):
        if self.input1 == 1 :
            self.output = 0
        elif self.input1 == 0:
            self.output = 1