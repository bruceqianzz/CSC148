"""Assignment 2: Organization Hierarchy
You must NOT use list.sort() or sorted() in your code.

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the entities
in an organization's hierarchy.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Sophia Huynh
"""
from __future__ import annotations
from typing import List, Optional, Union, TextIO, Tuple


# TODO: === TASK 1 ===
# Complete the merge() function and the Employee and Organization classes
# according to their docstrings.
# Go through client_code.py to find additional methods that you must
# implement.
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.

# You must NOT use list.sort() or sorted() in your code.
# Write and make use of the merge() function instead.


def merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Pre-condition: <lst1> and <lst2> are both sorted.

    >>> merge([1, 2, 5], [3, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """
    # TODO Task 1: Complete the merge() function.
    output = []
    while len(lst1) != 0 and len(lst2) != 0:
        if lst1[0] < lst2[0]:
            output.append(lst1[0])
            lst1 = lst1[1:]
        else:
            output.append(lst2[0])
            lst2 = lst2[1:]
    output.extend(lst1)
    output.extend(lst2)
    return output


class Employee:
    """An Employee: an employee in an organization.

    === Public Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.

    === Private Attributes ===
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - eid > 0
    - Within an organization, each eid only appears once. Two Employees cannot
      share the same eid.
    - salary > 0
    - 0 <= rating <= 100
    """
    eid: int
    name: str
    position: str
    salary: float
    rating: int
    _superior: Optional[Employee]
    _subordinates: List[Employee]

    # === TASK 1 ===
    def __init__(self, eid: int, name: str, position: str,
                 salary: float, rating: int) -> None:
        """Initialize this Employee with the ID <eid>, name <name>,
        position <position>, salary <salary> and rating <rating>.

        >>> e = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e.eid
        1
        >>> e.rating
        50
        """
        # TODO Task 1: Complete the __init__ method.
        self.eid = eid
        self.name = name
        self.position = position
        self.salary = salary
        self.rating = rating
        self._superior = None
        self._subordinates = []

    def __lt__(self, other: Employee) -> bool:
        """Return True iff <other> is an Employee and this Employee's eid is
        less than <other>'s eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1 < e2
        True
        """
        # TODO Task 1: Complete the __lt__ method.
        return self.eid < other.eid

    def __gt__(self, other: Employee) -> bool:
        """Return True iff <other> is an Employee and this Employee's eid is
        greater than <other>'s eid."""

        return self.eid > other.eid

    def __eq__(self, other: Employee) -> bool:
        """Return True iff <other> is an Employee and this Employee's eid is
        equal to <other>'s eid."""

        return self.eid == other.eid

    def get_direct_subordinates(self) -> List[Employee]:
        """Return a list of the direct subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].name
        'Emma Ployee'
        """
        # TODO Task 1: Complete the get_direct_subordinates method.
        return self._subordinates[:]

    def get_all_subordinates(self) -> List[Employee]:
        """Return a list of all of the subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_all_subordinates()[0].name
        'Emma Ployee'
        >>> e3.get_all_subordinates()[1].name
        'Sue Perior'
        """
        # TODO Task 1: Complete the get_all_subordinates method.
        output = self._subordinates
        if self._subordinates == []:
            return []
        else:
            for sub in self._subordinates:
                output = merge(output, sub.get_all_subordinates())
        return output

    def get_organization_head(self) -> Employee:
        """Return the head of the organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_organization_head().name
        'Bigg Boss'
        """
        # TODO Task 1: Complete the get_organization_head method.
        if self._superior is None:
            return self
        else:
            return self._superior.get_organization_head()

    def get_superior(self) -> Optional[Employee]:
        """Returns the superior of this Employee or None if no superior exists.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_superior() is None
        True
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().name
        'Sue Perior'
        """
        # TODO Task 1: Complete the get_superior method.
        return self._superior

    # Task 1: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def become_subordinate(self, superior: Union[Employee, None]) -> None:
        """Set this Employee's superior to <superior> and becomes a direct
        subordinate of <superior>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().eid
        2
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.become_subordinate(None)
        >>> e1.get_superior() is None
        True
        >>> e2.get_direct_subordinates()
        []
        """
        # TODO Task 1: Complete the become_subordinate method.
        if self._superior is not None:
            self._superior._subordinates.remove(self)
        self._superior = superior
        if superior is not None:
            superior._subordinates = merge(superior._subordinates, [self])

    def remove_subordinate_id(self, eid: int) -> None:
        """Remove the subordinate with the eid <eid> from this Employee's list
        of direct subordinates.

        Does NOT change the employee with eid <eid>'s superior.

        Pre-condition: This Employee has a subordinate with eid <eid>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e2.remove_subordinate_id(1)
        >>> e2.get_direct_subordinates()
        []
        >>> e1.get_superior() is e2
        True
        """
        # TODO Task 1: Complete the remove_subordinate_id method.
        for sub in self._subordinates:
            if sub.eid == eid:
                self._subordinates.remove(sub)

    def add_subordinate(self, subordinate: Employee) -> None:
        """Add <subordinate> to this Employee's list of direct subordinates.

        Does NOT change subordinate's superior.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e2.add_subordinate(e1)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.get_superior() is None
        True
        """
        # TODO Task 1: Complete the add_subordinate method.
        self._subordinates = merge(self._subordinates, [subordinate])

    def get_employee(self, eid: int) -> Optional[Employee]:
        """Returns the employee with ID <eid> or None if no such employee exists
        as a subordinate of this employee.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_employee(1) is e1
        True
        >>> e1.get_employee(1) is e1
        True
        >>> e2.get_employee(3) is None
        True
        """
        # TODO Task 1: Complete the get_employee method.
        if self.eid == eid:
            return self
        else:
            for sub in self._subordinates:
                a1 = sub.get_employee(eid)
                if a1 is not None:
                    return a1
        return None

    def get_employees_paid_more_than(self, amount: float) -> List[Employee]:
        """Get all subordinates of this employee that have a salary higher than
        <amount> (including this employee, if this employee's salary is higher
        than <amount>).

        Employees must be returned in increasing order of eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> more_than_10000 = e3.get_employees_paid_more_than(10000)
        >>> len(more_than_10000) == 2
        True
        >>> more_than_10000[0].name
        'Sue Perior'
        >>> more_than_10000[1].name
        'Bigg Boss'
        """
        # TODO Task 1: Complete the get_employees_paid_more_than method.
        total = []
        if self.salary > amount:
            total.append(self)
        for sub in self.get_all_subordinates():
            if sub.salary > amount:
                total = merge(total, [sub])
        return total

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 1. Write their headers and bodies below.
    def get_higher_paid_employees(self) -> List[Employee]:
        """Return a list of employee who has higher salary
        then this employee"""
        leader = self.get_organization_head()
        staff = leader.get_all_subordinates()
        staff = merge(staff, [leader])
        output = []
        for i in staff:
            if i.salary > self.salary:
                output.append(i)
        return output

    def get_closest_common_superior(self, eid: int) -> Employee:
        """get the closest common superior for two employee"""
        lst1 = []
        a1 = self
        while a1 is not None:
            lst1.append(a1)
            a1 = a1._superior
        lst2 = []
        boss = self.get_organization_head()
        if boss.eid == eid or self == boss:
            return boss
        else:
            e = boss.get_employee(eid)
            while e is not None:
                lst2.append(e)
                e = e._superior
        for i in lst1:
            if i in lst2:
                return i

    # === TASK 2 ===
    def get_department_name(self) -> str:
        """Returns the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_name()
        ''
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e1.become_subordinate(e2)
        >>> e1.get_department_name()
        'Department'
        """
        # TODO Task 2: Complete the get_department_name method.
        if self._superior is None:
            return ""
        else:
            return self._superior.get_department_name()

    def get_position_in_hierarchy(self) -> str:
        """Returns a string that describes the Employee's position in the
        organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_position_in_hierarchy()
        'Worker, Department, Company'
        >>> e2.get_position_in_hierarchy()
        'Manager, Department, Company'
        >>> e3.get_position_in_hierarchy()
        'CEO, Company'
        """
        # TODO Task 2: Complete the get_position_in_hierarchy method.
        output = "{}".format(self.position)
        if self._superior is None:
            return output
        else:
            a1 = self._superior
            while a1 is not None:
                if isinstance(a1, Leader):
                    output += ", {}".format(a1.get_department_name())
                a1 = a1._superior
        return output

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 2.
    def get_department_employees(self) -> List[Employee]:
        """Return a list of employee who are in the same
        department with this current employee
        Pre-condition: self.current_employee is a Leader.
        """
        output = self.get_all_subordinates()
        output = merge(output, [self])
        return output

    # === TASK 3 ===
    # Task 3: Helper methods
    #         While not called by the client_code, this method may be helpful
    #         to you and will be tested. You can (and should) call this in
    #         the other methods that you implement.
    def get_department_leader(self) -> Optional[Employee]:
        """Return the leader of this Employee's department. If this Employee is
        not in a department, return None.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_leader() is None
        True
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_department_leader().name
        'Sue Perior'
        >>> e2.get_department_leader().name
        'Sue Perior'
        """
        # TODO Task 3: Complete the get_department_leader method.
        if self.get_department_name() == "":
            return None
        else:
            a1 = self
            if a1._superior is None:
                return a1
            else:
                while a1._superior is not None and \
                        self.get_department_name() == \
                        a1._superior.get_department_name():
                    a1 = a1._superior
            return a1

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 3.
    def change_department_leader(self) -> Employee:
        """Change this current employee to the department leader"""
        leader = self.get_department_leader()
        if leader is None or leader == self:
            return self.get_organization_head()
        self._superior._subordinates.remove(self)
        new = Leader(self.eid, self.name, self.position,\
                     self.salary, self.rating, leader.get_department_name())
        tmp1 = self._subordinates[:]
        for sub in tmp1:
            sub.become_subordinate(new)
        new.become_subordinate(leader._superior)
        if new._superior is not None:
            new._superior._subordinates.remove(leader)
        new_lead = Employee(leader.eid, leader.name,\
                            leader.position, leader.salary, leader.rating)
        tmp2 = leader._subordinates[:]
        for sub in tmp2:
            sub.become_subordinate(new_lead)
        new_lead.become_subordinate(new)
        if new._superior is not None:
            return new.get_organization_head()
        return new

    def become_leader(self, department_name: str) -> Leader:
        """Let a employee become a leader"""
        new = Leader(self.eid, self.name, self.position,\
                     self.salary, self.rating, department_name)
        if self._superior is not None:
            self._superior._subordinates.remove(self)
            new.become_subordinate(self._superior)
        tmp = self._subordinates[:]
        for i in tmp:
            i.become_subordinate(new)
        return new

    # Part 4: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def get_highest_rated_subordinate(self) -> Employee:
        """Return the subordinate of this employee with the highest rating.

        Pre-condition: This Employee has at least one subordinate.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Sue Perior'
        >>> e1.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Emma Ployee'
        """
        # TODO Task 4: Complete the get_highest_rated_subordinate method.
        output = self._subordinates[0]
        for i in self._subordinates:
            if i.rating > output.rating:
                output = i
        return output

    def swap_up(self) -> Employee:
        """Swap this Employee with their superior. Return the version of this
        Employee that is contained in the Organization (i.e. if this Employee
        becomes a Leader, the new Leader version is returned).

        Pre-condition: self is not the head of the Organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> new_e1 = e1.swap_up()
        >>> isinstance(new_e1, Leader)
        True
        >>> new_e2 = new_e1.get_direct_subordinates()[0]
        >>> isinstance(new_e2, Employee)
        True
        >>> new_e1.position
        'Manager'
        >>> new_e1.eid
        1
        >>> e3.get_direct_subordinates()[0] is new_e1
        True
        """
        change = True
        new_leader = None
        tmp1 = self.get_direct_subordinates()
        if not isinstance(self, Leader):
            if not isinstance(self._superior, Leader):
                old = self._superior
                self.become_subordinate(old._superior)
                a0 = old._subordinates[:]
                for i in tmp1:
                    i.become_subordinate(old)
                for j in a0:
                    j.become_subordinate(self)
                old.become_subordinate(self)
                self.position, self.salary, old.position, old.salary = \
                    old.position, old.salary, self.position, self.salary
            else:
                new_leader = Leader(self.eid, self.name, \
                                    self._superior.position,\
                                    self._superior.salary, self.rating,
                                    self._superior.get_department_name())
                new_employee = Employee(self._superior.eid,\
                                        self._superior.name,\
                                        self.position, self.salary,
                                        self._superior.rating)
                if self._superior._superior is not None:
                    self._superior._superior._subordinates.\
                        remove(self._superior)
                new_leader.become_subordinate(self._superior.get_superior())
                new_employee.become_subordinate(new_leader)
                a0 = self._superior.get_direct_subordinates()[:]
                a0.remove(self)
                for i in a0:
                    i.become_subordinate(new_leader)
                for j in tmp1:
                    j.become_subordinate(new_employee)
                change = False
        if isinstance(self, Leader):
            if not isinstance(self._superior, Leader):
                new_leader = Employee(self.eid, self.name,\
                                        self._superior.position,\
                                        self._superior.salary,\
                                        self.rating)
                new_employee = Leader(self._superior.eid,\
                                    self._superior.name, self.position,\
                                    self.salary, self._superior.rating,\
                                    self.get_department_name())
                new_leader.become_subordinate(self._superior._superior)
                new_employee.become_subordinate(new_leader)
                if self._superior._superior is not None:
                    self._superior._superior.\
                        _subordinates.remove(self._superior)
                a0 = self._superior.get_direct_subordinates()[:]
                a0.remove(self)
                for i in a0:
                    i.become_subordinate(new_leader)
                for j in tmp1:
                    j.become_subordinate(new_employee)
                change = False
            else:
                old_one = self._superior
                self.become_subordinate(old_one._superior)
                a0 = old_one._subordinates[:]
                for i in tmp1:
                    i.become_subordinate(old_one)
                for j in a0:
                    j.become_subordinate(self)
                old_one.become_subordinate(self)
                self.position, self.salary, old_one.position, old_one.salary = \
                    old_one.position, old_one.salary, self.position, self.salary
                a1 = self.get_department_name()
                a2 = old_one.get_department_name()
                self.become_leader(a2)
                old_one.become_leader(a1)
        if change:
            return self
        return new_leader


    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 4.
    def obtain_subordinates(self, ids: List[int]) -> Employee:
        """Put all the staff of the id in list as a subordinate of the
        current employee"""
        for id_ in ids:
            boss = self.get_organization_head()
            i = boss.get_employee(id_)
            if i is None:
                pass
            elif i == boss:
                new = i.get_highest_rated_subordinate()
                new.become_subordinate(None)
                tmp = i._subordinates[:]
                for sub in tmp:
                    sub.become_subordinate(new)
                i.become_subordinate(self)
                i._subordinates = []
            else:
                tmp = i._subordinates[:]
                for sub in tmp:
                    sub.become_subordinate(i._superior)
                i.become_subordinate(self)
                i._subordinates = []
        return self.get_organization_head()


class Organization:
    """An Organization: an organization containing employees.

    === Private Attributes ===
    _head:
        The head of the organization.

    === Representation Invariants ===
    - _head is either an Employee (or subclass of Employee) or None (if there
      are no Employees).
    - No two Employees in an Organization have the same eid.
    """
    _head: Optional[Employee]

    # === TASK 1 ===
    def __init__(self, head: Optional[Employee] = None) -> None:
        """Initialize this Organization with the head <head>.

        >>> o = Organization()
        >>> o.get_head() is None
        True
        """
        # TODO Task 1: Complete the __init__ method.
        self._head = head

    def get_head(self) -> Optional[Employee]:
        """Return the head of this organization"""
        return self._head

    def get_employee(self, eid: int) -> Optional[Employee]:
        """
        Return the employee with id <eid>. If no such employee exists, return
        None.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> o.add_employee(e1)
        >>> o.get_employee(1) is e1
        True
        >>> o.get_employee(2) is None
        True
        """
        # TODO Task 1: Complete the get_employee method.
        if self._head is None:
            return None
        return self._head.get_employee(eid)

    def add_employee(self, employee: Employee, superior_id: int = None) -> None:
        """Add <employee> to this organization as the subordinate of the
        employee with id <superior_id>.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.get_head() is e2
        True
        >>> o.add_employee(e1, 2)
        >>> o.get_employee(1) is e1
        True
        >>> e1.get_superior() is e2
        True
        """
        # TODO Task 1: Complete the add_employee method.
        if superior_id is None:
            if self._head is None:
                self._head = employee
            else:
                self._head.become_subordinate(employee)
                self._head = employee
        else:
            s = self.get_employee(superior_id)
            employee.become_subordinate(s)

    def get_average_salary(self, position: Optional[str] = None) -> float:
        """Returns the average salary of all employees in the organization with
        the position <position>.

        If <position> is None, this returns the average salary of all employees.

        If there are no such employees, return 0.0

        >>> o = Organization()
        >>> o.get_average_salary()
        0.0
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.add_employee(e1, 2)
        >>> o.get_average_salary()
        15000.0
        """
        # TODO Task 1: Complete the get_average_salary method.
        if self._head is None:
            return 0.0
        l = self._head.get_all_subordinates()
        l = merge(l, [self._head])
        total = 0
        amount = 0
        if position is None:
            for i in l:
                total += i.salary
                amount += 1
            return total / amount
        else:
            for i in l:
                if i.position == position:
                    total += i.salary
                    amount += 1
            if amount == 0:
                return 0.0
            return total / amount

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 1.
    def get_next_free_id(self) -> int:
        """
        To return the next free id that is available to use, that there
        is no duplicate id in this organization
        >>> o = Organization()
        >>> e1 = Employee(0, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(1, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e1)
        >>> o.add_employee(e2, 0)
        >>> o.get_next_free_id()
        2
        """
        id_ = 1
        while self.get_employee(id_):
            id_ += 1
        return id_

    def get_employees_with_position(self, position: str) -> List:
        """
        return a list of employee who are in the given position
        """
        l = self._head.get_all_subordinates()
        l = merge(l, [self._head])
        output = []
        for i in l:
            if i.position == position:
                output.append(i)
        return output

    # === TASK 3 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 3.
    def set_head(self, new: Employee) -> None:
        """Set the head of this organization when some employee is promoted"""
        self._head = new

    # === TASK 4 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 4.
    def fire_employee(self, eid: int) -> None:
        """fire selected employee from the organization"""
        i = self.get_employee(eid)
        if i is None:
            return
        else:
            if i == self._head:
                if i.get_direct_subordinates() == []:
                    self._head = None
                    return
                new = self._head.get_highest_rated_subordinate()
                new.become_subordinate(None)
                staffs = i.get_direct_subordinates()[:]
                for i in staffs:
                    i.become_subordinate(new)
                self._head = new
            else:
                staffs = i.get_direct_subordinates()[:]
                for sub in staffs:
                    sub.become_subordinate(i.get_superior())
                i.become_subordinate(None)

    def fire_lowest_rated_employee(self) -> None:
        """ fire the lowest rated employee from the organization"""
        staffs = self._head.get_all_subordinates()
        staffs.append(self._head)
        output = staffs[0]
        for i in staffs[1:]:
            if i.rating < output.rating:
                output = i
            elif i.rating == output.rating:
                if i.eid < output.eid:
                    output = i
        self.fire_employee(output.eid)

    def fire_under_rating(self, rating: int) -> None:
        """fir all the employees lower than the given rating"""
        staffs = self._head.get_all_subordinates()
        staffs.append(self._head)
        fire_list = []
        for staff in staffs:
            if staff.rating < rating:
                fire_list.append(staff)
        new_list = []
        for i in fire_list:
            flag = True
            j = 0
            while j < len(new_list) and flag:
                if new_list[j].rating > i.rating:
                    flag = False
                elif new_list[j].rating == i.rating and new_list[j].eid > i.eid:
                    flag = False
                else:
                    j += 1
            new_list.insert(j, i)
        for i in new_list:
            self.fire_employee(i.eid)

    def promote_employee(self, eid: int) -> None:
        """promote an employee based on his rating """
        employee = self.get_employee(eid)
        if employee is None:
            return
        while employee.get_superior() is not None and\
                employee.rating >= employee.get_superior().rating:
            employee = employee.swap_up()
        if employee.get_superior() is None:
            self._head = employee


# === TASK 2: Leader ===
# TODO: Complete the Leader class and its methods according to their docstrings.
#       You will also need to revisit Organization and Employee to implement
#       additional methods.
#       Go through client_code.py to find additional methods that you must
#       implement.
#
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.
#
# After the completion of Task 2, you should be able to run organization_ui.py,
# though not all of the buttons will work.


class Leader(Employee):
    """A subclass of Employee. The leader of a department in an organization.

    === Private Attributes ===
    _department_name:
        The name of the department this Leader is the head of.

    === Inherited Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - All Employee RIs are inherited.
    - Department names are unique within an organization.
    """
    _department_name: str

    # === TASK 2 ===
    def __init__(self, eid: int, name: str, position: str, salary: float,
                 rating: int, department: str) -> None:
        """Initialize this Leader with the ID <eid>, name <name>, position
        <position>, salary <salary>, rating <rating>, and department name
        <department>.

        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e2.name
        'Sue Perior'
        >>> e2.get_department_name()
        'Department'
        """
        # TODO Task 2: Complete the __init__ method.
        Employee.__init__(self, eid, name, position, salary, rating)
        self._department_name = department

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 2.
    #       There may also be Employee methods that you'll need to override.
    def get_department_name(self) -> str:
        """Returns the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string."""
        return self._department_name

    def get_position_in_hierarchy(self) -> str:
        """Returns a string that describes the Employee's position in the
        organization.
        """
        output = "{}, {}".format(self.position, self._department_name)
        if self._superior is None:
            return output
        else:
            a1 = self._superior
            while a1 is not None:
                if isinstance(a1, Leader):
                    output += ", {}".format(a1.get_department_name())
                a1 = a1.get_superior()
        return output

    # === TASK 3 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 3. If there are no methods there, consider if you need to
    #       override any of the Task 3 Employee methods.
    def become_employee(self) -> Employee:
        """make a Leader becomes an employee"""
        new = Employee(self.eid, self.name,\
                       self.position, self.salary, self.rating)
        if self._superior is not None:
            self.get_superior().remove_subordinate_id(self.eid)
        new.become_subordinate(self._superior)
        tmp = self._subordinates[:]
        for i in tmp:
            i.become_subordinate(new)
        return new

    def become_leader(self, department_name: str) -> Leader:
        """change the department name if this employee is a Leader"""
        self._department_name = department_name
        return self


    # === TASK 4 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 4. If there are no methods there, consider if you need to
    #       override any of the Task 4 Employee methods.


# === TASK 5 ===
# TODO: Complete the create_department_salary_tree() function according to
#       its docstrings and the specifications in the assignment handout.
#
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.

class DepartmentSalaryTree:
    """A DepartmentSalaryTree: A tree representing the salaries of departments.
    The salaries considered only consist of employees directly in a department
    and not in any of their subdepartments.

    Do not change this class.

    === Public Attributes ===
    department_name:
        The name of the department that this DepartmentSalaryTree represents.
    salary:
        The average salary of the department that this DepartmentSalaryTree
        represents.
    subdepartments:
        The subdepartments of the department that this DepartmentSalaryTree
        represents.
    """
    department_name: str
    salary: float
    subdepartments: [DepartmentSalaryTree]

    def __init__(self, department_name: str, salary: float,
                 subdepartments: List[DepartmentSalaryTree]) -> None:
        """Initialize this DepartmentSalaryTree with the department name
        <department_name>, salary <salary>, and the subdepartments
        <subdepartments>.

        >>> d = DepartmentSalaryTree('Department', 30000, [])
        >>> d.department_name
        'Department'
        """
        self.department_name = department_name
        self.salary = salary
        self.subdepartments = subdepartments[:]

    # def pr(self, depth = 1):
    #     if self.subdepartments == []:
    #         print("{}{}/{}".format("   " * depth, \
    #         self.department_name, self.salary))
    #         return
    #     print("{}{}/{}".format("   "*depth,self.department_name,self.salary))
    #     for i in self.subdepartments:
    #         i.pr(depth+1)
    #     return


def _helper_for_create_tree(staff: Employee) -> Tuple[Employee, List[Employee]]:
    """helper method 1"""
    department = staff.get_department_name()
    staffs = staff.get_all_subordinates()
    output = [staff]
    for i in staffs:
        if i.get_department_name() == department:
            output = merge(output, [i])
    salary = 0
    for i in output:
        salary += i.salary
    average = salary / len(output)
    output = DepartmentSalaryTree(staff.get_department_name(), average, [])
    new = Employee(1, "a", "a", 1, 1)
    for sub in staff.get_direct_subordinates():
        new.add_subordinate(sub)
    lst = _helper2(new)
    return output, lst


def _helper2(staff: Employee) -> List:
    """helper method 2"""
    lst = []
    if isinstance(staff, Leader):
        return [staff]
    elif staff.get_direct_subordinates() == []:
        return []
    for sub in staff.get_direct_subordinates():
        lst = merge(lst, _helper2(sub))
    return lst


def _helper3(func: Callable) -> DepartmentSalaryTree:
    """helper method 3"""
    if func[1] == []:
        return func[0]
    output = func[0]
    for sub in func[1]:
        output.subdepartments.append(_helper3(_helper_for_create_tree(sub)))
    return output


def create_department_salary_tree(organization: Organization) -> \
        Optional[DepartmentSalaryTree]:
    """Return the DepartmentSalaryTree corresponding to <organization>.

    If <organization> has no departments, return None.

    Pre-condition: If there is at least one department in <organization>,
    then the head of <organization> is also a Leader.

    >>> o = Organization()
    >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
    >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
    >>> o.add_employee(e2)
    >>> o.add_employee(e1, 2)
    >>> o.add_employee(e3)
    >>> dst = create_department_salary_tree(o)
    >>> dst.department_name
    'Company'
    >>> dst.salary
    50000.0
    >>> dst.subdepartments[0].department_name
    'Department'
    >>> dst.subdepartments[0].salary
    15000.0
    """
    # TODO Task 5: Complete the create_department_salary_tree function.
    header = organization.get_head()
    if header is None or not isinstance(header, Leader):
        return None
    else:
        return _helper3(_helper_for_create_tree(header))


# === TASK 6 ===
# TODO: Complete the create_organization_from_file() function according to
#       its docstrings and the specifications in the assignment handout.
#
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.

def create_organization_from_file(file: TextIO) -> Organization:
    """Return the Organization represented by the information in <file>.

    >>> o = create_organization_from_file(open('employees.txt'))
    >>> o.get_head().name
    'Alice'
    """
    # TODO Task 6: Complete the create_organization_from_file function.
    alls = []
    line = file.readline()
    org = None
    while line:
        line = line.strip().split(",")
        if line[5] == "":
            org = Organization(Leader(int(line[0]), line[1], line[2], \
                                    int(line[3]), int(line[4]), line[6]))
        elif alls == []:
            alls.append(line)
        else:
            i = 0
            while i < len(alls) and line[0] > alls[i][0]:
                i += 1
            alls.insert(i, line)
        line = file.readline().strip()
    s = alls[:]
    while s:
        for j in alls:
            if len(j) == 7 and org.get_employee(int(j[5])):
                staff = Leader(int(j[0]), j[1], j[2],\
                               int(j[3]), int(j[4]), j[6])
                org.add_employee(staff, int(j[5]))
                s.remove(j)
            elif len(j) == 6 and org.get_employee(int(j[5])):
                staff = Employee(int(j[0]), j[1],\
                                 j[2], int(j[3]), int(j[4]))
                org.add_employee(staff, int(j[5]))
                s.remove(j)
            else:
                pass
        alls = s
    return org


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'doctest', 'typing',
                                   '__future__'],
        'max-args': 7})


# e1 = Leader(1,"Alice","CEO",250000,20,"1level")
# e2 = Leader(3,"Alice","CEO",250000,20,"3level")
# e3 = Leader(7,"Alice","CEO",250000,20,"2level")
# e4 = Employee(4, "a", "e", 1,1)
# e5 = Employee(2, "a", "e", 1,1)
# e6 = Employee(10, "a", "e", 1,1)
# e4.become_subordinate(e1)
# e5.become_subordinate(e1)
# e3.become_subordinate(e1)
# e2.become_subordinate(e4)
# e6.become_subordinate(e4)
# o = Organization(e1)
# a = create_department_salary_tree(o)
# a.pr()new
