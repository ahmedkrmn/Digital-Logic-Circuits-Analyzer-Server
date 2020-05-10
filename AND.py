from gate import gate

class AND(gate) :

    def __init__(self, input1 , input2 , output , gtype):
        gate.__init__(self, input1 , output , gtype)
        self.input2 = input2

    def calc(self):
        self.output = self.input1 and self.input2