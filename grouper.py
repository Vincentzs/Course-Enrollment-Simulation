"""CSC148 Assignment 1

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Misha Schwartz, Mario Badr, Christine Murad, Diane Horton, Sophia Huynh
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Misha Schwartz, Mario Badr, Christine Murad, Diane Horton,
Sophia Huynh and Jaisie Sin

=== Module Description ===

This file contains classes that define different algorithms for grouping
students according to chosen criteria and the group members' answers to survey
questions. This file also contain a classe that describes a group of students as
well as a grouping (a group of groups).
"""
from __future__ import annotations
import random
from typing import TYPE_CHECKING, List, Any
from course import sort_students

if TYPE_CHECKING:
    from survey import Survey
    from course import Course, Student


def slice_list(lst: List[Any], n: int) -> List[List[Any]]:
    """
    Return a list containing slices of <lst> in order. Each slice is a
    list of size <n> containing the next <n> elements in <lst>.

    The last slice may contain fewer than <n> elements in order to make sure
    that the returned list contains all elements in <lst>.

    === Precondition ===
    n <= len(lst)

    >>> slice_list([3, 4, 6, 2, 3], 2) == [[3, 4], [6, 2], [3]]
    True
    >>> slice_list(['a', 1, 6.0, False], 3) == [['a', 1, 6.0], [False]]
    True
    """
    result = []
    length = len(lst)
    if n > 0:
        for i in range(0, length, n):
            result.append(lst[i: i + n])
    return result


def windows(lst: List[Any], n: int) -> List[List[Any]]:
    """
    Return a list containing windows of <lst> in order. Each window is a list
    of size <n> containing the elements with index i through index i+<n> in the
    original list where i is the index of window in the returned list.

    === Precondition ===
    n <= len(lst)

    >>> windows([3, 4, 6, 2, 3], 2) == [[3, 4], [4, 6], [6, 2], [2, 3]]
    True
    >>> windows(['a', 1, 6.0, False], 3) == [['a', 1, 6.0], [1, 6.0, False]]
    True
    """
    result = []
    length = len(lst)
    i = 0
    flag = False
    # if n == 1:
    #     for value in lst:
    #         result.append([value])
    # if n % 2 == 0:
    #     for i in range(0, length - 1, n - 1):
    #         result.append(lst[i: i + n])
    # else:
    #     for i in range(0, length - 2, n - 2):
    #         result.append(lst[i: i + n])
    while i < length and not flag:
        if n + i < length:
            result.append(lst[i: i + n])
            i += 1
        else:
            result.append(lst[i: length])
            flag = True
    return result


class Grouper:
    """
    An abstract class representing a grouper used to create a grouping of
    students according to their answers to a survey.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group

    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def __init__(self, group_size: int) -> None:
        """
        Initialize a grouper that creates groups of size <group_size>

        === Precondition ===
        group_size > 1
        """
        self.group_size = group_size

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """ Return a grouping for all students in <course> using the questions
        in <survey> to create the grouping.
        """
        raise NotImplementedError


class AlphaGrouper(Grouper):
    """
    A grouper that groups students in a given course according to the
    alphabetical order of their names.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group

    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """
        Return a grouping for all students in <course>.

        The first group should contain the students in <course> whose names come
        first when sorted alphabetically, the second group should contain the
        next students in that order, etc.

        All groups in this grouping should have exactly self.group_size members
        except for the last group which may have fewer than self.group_size
        members if that is required to make sure all students in <course> are
        members of a group.

        Hint: the sort_students function might be useful
        """
        grouping = Grouping()
        # sort好的list of student
        lst_students = sort_students(course.students, 'name')
        # sort好的student分成size大小的list of list of student
        groups = slice_list(lst_students, self.group_size)
        for group in groups:
            grouping.add_group(Group(group))
        return grouping


class RandomGrouper(Grouper):
    """
    A grouper used to create a grouping of students by randomly assigning them
    to groups.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group

    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """
        Return a grouping for all students in <course>.

        Students should be assigned to groups randomly.

        All groups in this grouping should have exactly self.group_size members
        except for one group which may have fewer than self.group_size
        members if that is required to make sure all students in <course> are
        members of a group.
        """
        grouping = Grouping()
        lst_students = course.students
        # random.shuffle mutates, no assignment
        random.shuffle(lst_students)
        groups = slice_list(lst_students, self.group_size)
        for group in groups:
            grouping.add_group(Group(group))
        return grouping


class GreedyGrouper(Grouper):
    """
    A grouper used to create a grouping of students according to their
    answers to a survey. This grouper uses a greedy algorithm to create
    groups.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group

    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def _max_score(self, lst_students: List[Student], survey: Survey) -> List:
        """Find the group of students with the most score
        (used for GreedyGrouper)
        """
        grouped_students = [lst_students[0]]
        lst_students.remove(lst_students[0])
        # Fails when half of students grouped => done
        while len(grouped_students) < self.group_size:
            score = 0
            i = 0
            # remaining students who are not grouped
            for j in range(len(lst_students)):
                grouped_students.append(lst_students[j])
                temp_score = survey.score_students(grouped_students)
                # find max score
                if temp_score > score:
                    score = temp_score
                    i = j
                grouped_students.remove(lst_students[j])
            # add the best match into a list
            grouped_students.append(lst_students[i])
            lst_students.remove(lst_students[i])
        return grouped_students

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """
        Return a grouping for all students in <course>.

        Starting with a tuple of all students in <course> obtained by calling
        the <course>.get_students() method, create groups of students using the
        following algorithm:

        1. select the first student in the tuple that hasn't already been put
           into a group and put this student in a new group.
        2. select the student in the tuple that hasn't already been put into a
           group that, if added to the new group, would increase the group's
           score the most (or reduce it the least), add that student to the new
           group.
        3. repeat step 2 until there are N students in the new group where N is
           equal to self.group_size.
        4. repeat steps 1-3 until all students have been placed in a group.

        In step 2 above, use the <survey>.score_students method to determine
        the score of each group of students.

        The final group created may have fewer than N members if that is
        required to make sure all students in <course> are members of a group.
        """
        grouping = Grouping()
        lst_students = list(course.get_students())
        while len(lst_students) > self.group_size:
            group = self._max_score(lst_students, survey)
            grouping.add_group(Group(group))
        grouping.add_group(Group(lst_students))
        return grouping


class WindowGrouper(Grouper):
    """
    A grouper used to create a grouping of students according to their
    answers to a survey. This grouper uses a window search algorithm to create
    groups.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group

    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """
        Return a grouping for all students in <course>.

        Starting with a tuple of all students in <course> obtained by calling
        the <course>.get_students() method, create groups of students using the
        following algorithm:

        1. Get the windows of the list of students who have not already been
           put in a group.
        2. For each window in order, calculate the current window's score as
           well as the score of the next window in the list. If the current
           window's score is greater than or equal to the next window's score,
           make a group out of the students in current window and start again at
           step 1. If the current window is the last window, compare it to the
           first window instead.

        In step 2 above, use the <survey>.score_students to determine the score
        of each window (list of students).

        In step 1 and 2 above, use the windows function to get the windows of
        the list of students.

        If there are any remaining students who have not been put in a group
        after repeating steps 1 and 2 above, put the remaining students into a
        new group.
        """
        grouping = Grouping()
        student_list = list(course.get_students())
        if len(student_list) <= self.group_size:
            grouping.add_group(Group(student_list))
            return grouping
        while len(student_list) > 0:
            student_windows = windows(student_list, self.group_size)
            i = 0
            flag = False
            while i + 1 < len(student_windows) and not flag:
                score1 = survey.score_students(student_windows[i])
                score2 = survey.score_students(student_windows[i+1])
                if score1 >= score2:
                    flag = True
                else:
                    i += 1
            group = Group(student_windows[i])
            grouping.add_group(group)
            for member in student_windows[i]:
                student_list.remove(member)
        return grouping


class Group:
    """
    A group of one or more students

    === Private Attributes ===
    _members: a list of unique students in this group

    === Representation Invariants ===
    No two students in _members have the same id
    """

    _members: List[Student]

    def __init__(self, members: List[Student]) -> None:
        """ Initialize a group with members <members> """
        self._members = members

    def __len__(self) -> int:
        """ Return the number of members in this group """
        return len(self._members)

    def __contains__(self, member: Student) -> bool:
        """
        Return True iff this group contains a member with the same id
        as <member>.
        """
        member_id = []
        for member_ in self._members:
            member_id.append(member_.id)
        if member.id in member_id:
            return True
        return False

    def __str__(self) -> str:
        """
        Return a string containing the names of all members in this group
        on a single line.

        You can choose the precise format of this string.
        """
        name = ''
        for member in self._members:
            name += member.name
        return name

    def get_members(self) -> List[Student]:
        """ Return a list of members in this group. This list should be a
        shallow copy of the self._members attribute.
        """
        copy = []
        for member in self._members:
            copy.append(member)
        return copy


class Grouping:
    """
    A collection of groups

    === Private Attributes ===
    _groups: a list of Groups

    === Representation Invariants ===
    No group in _groups contains zero members
    No student appears in more than one group in _groups
    """

    _groups: List[Group]

    def __init__(self) -> None:
        """ Initialize a Grouping that contains zero groups """
        self._groups = []

    def __len__(self) -> int:
        """ Return the number of groups in this grouping """
        return len(self._groups)

    def __str__(self) -> str:
        """
        Return a multi-line string that includes the names of all of the members
        of all of the groups in <self>. Each line should contain the names
        of members for a single group.

        You can choose the precise format of this string.
        """
        groups_ = self._groups
        name = ''
        for i in range(len(groups_)):
            name += 'Group :' + str(i) + 'Members: '
            for member in groups_[i].get_members():
                # if len(groups_) == i:
                #     name += 'Members: ' + member.name
                # # only add \n at the last member
                # else:s
                name += member.name
            name += '\n'
        return name

    def add_group(self, group: Group) -> bool:
        """
        Add <group> to this grouping and return True.

        Iff adding <group> to this grouping would violate a representation
        invariant don't add it and return False instead.
        """
        ori_group_id = []
        group_id = []
        # Don't put len(self._groups) == 0 in the if below.Check rep. inv.
        if len(group) == 0:
            return False
        else:
            for group_ in self._groups:
                for member in group_.get_members():
                    ori_group_id.append(member.id)
            for member in group.get_members():
                group_id.append(member.id)
        for member_id in group_id:
            if member_id in ori_group_id:
                return False
        self._groups.append(group)
        return True

    def get_groups(self) -> List[Group]:
        """ Return a list of all groups in this grouping.
        This list should be a shallow copy of the self._groups
        attribute.
        """
        copy = []
        if len(self._groups) != 0:
            for group in self._groups:
                copy.append(group)
        return copy


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'random',
                                                  'survey',
                                                  'course']})
