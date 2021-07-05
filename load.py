class ASDF:
    def __init__(self):
        self.true = [1,2,3,4]
        self.false = [5,6,7,8]

    def __iter__(self,type):
        if type:
            iter(self.true)
        elif type:
            iter(self.false)


if __name__=="__main__":
    a = ASDF()
    for i in iter(a,True):
        print(i)

    for i in a(False):
        print(i)