from gate import gate

class OR (gate) :

    def __init__(self, input1 , input2 , output , gtype):
        gate.__init__(self, input1 , output , gtype)
        self.input2 = input2

    def calc(self):
        self.output = self.input1 or self.input2