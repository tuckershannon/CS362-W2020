# -*- coding: utf-8 -*-
"""
Created on  January 19th 2020
@author: shannont
"""
import unittest
from unittest import TestCase
import classroom_manager


class TestStudent(TestCase):

    def setStudent(self):
        self.test_id = 229576
        self.first_name = "Tucker"
        self.last_name = "Shannon"
        self.student = classroom_manager.Student(self.test_id, self.first_name, self.last_name)

    def setAssignment(self):
        self.assignment = classroom_manager.Assignment("Assignment1", 100)

    def test_init_student(self):
        self.setStudent()

        self.assertEqual(self.test_id, self.student.id, "Wrong Student ID")
        self.assertEqual(self.first_name, self.student.first_name, "Wrong first name")
        self.assertEqual(self.last_name, self.student.last_name, "Wrong last name")
        self.assertIsNotNone(self.student.assignments, "Assignments not init")

    def test_get_full_name(self):
        self.setStudent()
        actualFullname = str(self.first_name + " " + self.last_name)

        self.assertEqual(actualFullname, self.student.get_full_name())

    def test_submit_assignment(self):
        self.setStudent()
        self.setAssignment()

        self.student.submit_assignment(self.assignment)
        self.assertEqual(self.student.assignments, [self.assignment])

    def test_get_assignments(self):
        self.setStudent()
        self.setAssignment()

        # check when no assignment is present
        self.assertEqual(self.student.get_assignments(), [])

        # check when one assignment is added
        self.student.submit_assignment(self.assignment)
        self.assertEqual(self.student.get_assignments(), [self.assignment])

        # check when another assignment is added
        self.student.submit_assignment(self.assignment)
        self.assertEqual(self.student.get_assignments(), [self.assignment, self.assignment])

    def test_get_assignment(self):
        self.setStudent()
        self.setAssignment()

        # check when no assignment is present
        self.assertIsNone(self.student.get_assignment("Assignment1"))

        # check when one assignment is added
        self.student.submit_assignment(self.assignment)

        addedAssignment = self.student.get_assignment("Assignment1")
        self.assertEqual(addedAssignment.name, self.assignment.name)

    def test_get_average(self):
        self.setStudent()
        self.setAssignment()

        # test with none
        self.assertEqual(self.student.get_average(), 0)

        self.assignment.grade = 60
        self.student.submit_assignment(self.assignment)

        # test the average with one
        self.assertEqual(self.student.get_average(), 60)

        self.assignment.grade = 80
        self.student.submit_assignment(self.assignment)

        # test the average with more than one
        self.assertEqual(self.student.get_average(), 80)

    def test_remove_assignment(self):
        self.setStudent()
        self.setAssignment()
        self.student.submit_assignment(self.assignment)

        # check to make sure the assignment was added properly
        self.assertEqual(self.student.get_assignment("Assignment1"),self.assignment)

        # now remove that assignment
        self.student.remove_assignment("Assignment1")

        # check to make sure it was removed
        self.assertIsNone(self.student.get_assignment("Assignment1"))





class TestAssignment(TestCase):


    def setAssignment(self):
        self.assignment = classroom_manager.Assignment("Assignment1", 100)

    def test_init_assignment(self):
        self.setAssignment()
        self.assertEqual(self.assignment.name,"Assignment1")
        self.assertEqual(self.assignment.max_score,100)
        self.assertEqual(self.assignment.grade,None)

    def test_assign_grade(self):
        self.setAssignment()
        self.assignment.assign_grade(99)

        # check to see if assignment was graded properly
        self.assertEqual(self.assignment.grade,99)

        # check to see if handles grade higher than max score
        self.assignment.assign_grade(101)
        self.assertEqual(self.assignment.grade, None)



