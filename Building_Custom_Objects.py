#Building custom Objects
'''
Everhing in pytojn is an bojects

you can create your won custom objects
existing type not adequatre
functions with insstance called methods

examples of methods:
upper(), lower(), split(), find(), append()
popo(), remove(), insert(), sort(), items, keys, values()
X.append()

string list dictionary

with underscores
__get__ special method in a class
'''

#Use Capital for Each Student
class Student:
    def __init__(self, first, last, courses = None):
        self.first_name = first
        self.last_name = last
        if courses == None:
            self.courses = []
        else:
            self.courses = courses

    def add_course(self, course):
        if course not in self.course:
            self.courses.append(course)
        else:
            print(f"{self.first_name} is already enrolled in the {course} course")
    def __str__(self):
        return f"{self.first_name},{self.last_name}, {self.courses}"


    def  find_in_file(self, filename):
        with open(file_name) as f:
            for line in f:
                #print(line.strip())
                first_name,last_name,course_d = Student.prep_record(line.strip())
                student_read_in = Student(first_name, last_name, course_d)
                if self == student_read_in: #doesnt really works
                    return True
            return False

    def add_to_file(self, filename):
        if self.find_in_file(filename):
            return "Record already exists"
        else:
            record_to_add = Student.prep_to_write(self.first_name, self.last_name\
            courses )
            with open(filename, "a+") as to_write:
                to_write.write(record_to_add+"\n")
            return "Record added"

    @staticmethod
    def prep_to_write(first_name, last_name, courses):
        full_name = first_name + ',' + last_name
        courses = ",".join(courses)
        return full_name+':'+courses

    @staticmethod
    def prep_record(line):
        line = line.split(":")
        first_name, last_name =line[0].split(",")
        print(line)
        course_details = line[1].split(",")
        return first_name, last_name, course_details

    def __eq__(self, other):
        self.first_name == other.first_name \
        and self.last_name == other.last_name

course_1 = ['python', 'rails','javascript']
course_2 = ['java', 'rails', 'c']

mashrur = Student("mashrur", "hossain")
print(mashrur)
