from node import Node

class Expression(Node):
    def __init__(self, name):
        self.name = name
        super().__init__()
        
    def __str__(self):
        return f"'{self.name}'"

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self,otherNode):
        if otherNode == None:
            return False
        else:
            return self.name == otherNode.name
        
    def __lt__(self, otherNode):
        if otherNode == None:
            raise TypeError("'<' not supported between instances of 'Expression' and 'NoneType'")
        if self.name == otherNode.name:
            return self.name < otherNode.name
        return self.name < otherNode.name