from gate import gate

class XOR (gate) :

    def __init__(self, input1 , input2 , output , gtype):
        gate.__init__(self, input1 , output , gtype)
        self.input2 = input2

    def calc(self):
        if self.input1 == self.input2 :
            self.output = 0
        else :
            self.output =1