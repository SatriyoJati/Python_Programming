class Student:

    def __init__(self, first, last, courses=None):
        self.first_name = first
        self.last_name =last




class StudentAthlete(Student):

    def __init__(self,first,last,course=None, sport=None):
        #super().__int__(self,first,last,courses=None)
        self.sport= sport
