class A:
    def __init__(self,name):
        self.name = name
    def get_name(self):
        return self.name

class B:
    def __init__(self,type_name):
        self.type_name = type_name
    def get_type(self):
        return self.type_name

class C(A,B):
    def __init__(self,name,type_name):
        A.__init__(self,name)
        B.__init__(self,type_name)
    def say_hello(self):
        return f'I am {self.get_name()}, a proud {self.type_name}.'

if __name__ == '__main__':
    c = C('Leo', 'Lion')
    print(c.say_hello())