#Working with Files


file_name = "data.txt"

def prep_record(line):
    line = line.split(":")
    first_name, last_name =line[0].split(",")
    print(line)
    course_details = line[1].split(",")
    return first_name, last_name, course_details

def prep_to_write(first_name, last_name, courses):
    full_name = first_name + ',' + last_name
    courses = ",".join(courses)
    return full_name+':'+courses

with open(file_name) as f:
    for line in f:
        print(line.strip())
        rist_name,last_name,coruse_d =prep_record(line)
