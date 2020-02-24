# CS362 Assignment 4
# Classroom Manager

#Student class
class Student:
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.assignments = []

    def get_full_name(self):
        return str(self.first_name + " " + self.last_name)

    def submit_assignment(self, assignment):
        self.assignments.append(assignment)


    def get_assignments(self):

        return self.assignments

    def get_assignment(self, name):
        for a in self.assignments:
            if a.name == name:
                return a
        return None

    def get_average(self):
        sum_grades = 0
        total_assignments = 0
        for a in self.assignments:
            if a.grade != None:
                sum_grades = sum_grades + a.grade
                total_assignments = total_assignments + 1

        if sum_grades == 0:
            average = 0
        else:
            average = sum_grades/total_assignments

        return average

    def remove_assignment(self, name):
        for a in self.assignments:
            if a.name == name:
                self.assignments.remove(a)
                del name

#Assignment class
class Assignment:
    def __init__(self, name, max_score):
        self.name = name
        self.max_score = max_score
        self.grade = None

    def assign_grade(self, grade):
        self.grade = grade
        if grade >= self.max_score:
            self.grade = None
