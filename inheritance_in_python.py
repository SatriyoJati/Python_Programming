from abc import ABC, abstractmethod

class Config(ABC):
    @abstractmethod
    def get_salary(self):
        pass

class Configuration:
    def name_employee(self,name):
        return name

class Employee(Config):
    def __init__(self,configuration : Configuration , name):
        self.name = configuration.name_employee(name)
        self.age = "12"

    def get_salary(self):
        print("get the salary")

    def get_commision(self):
        print("get the commision")

class Exemployee(Employee):
    def __init__(self,configuration,name):
        super(Exemployee,self).__init__(configuration,name)

    def get_salary(self):
        print("get exemployee salary")
        print("separated two method into one")
        print(f"name of employee {self.name}")

c = Configuration()
e = Exemployee(c,"sarah")
e.get_salary()
