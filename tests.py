"""CSC148 Assignment 1
    Test cases of every methods written by authors from course.py, criterion.py,
    survey.py, and grouper.py files.
"""
import course
import survey
import criterion
import grouper
import pytest
from typing import List, Set, FrozenSet

@pytest.fixture
def empty_course() -> course.Course:
    """Tests empty_course from example_tests.py"""
    return course.Course('csc148')


@pytest.fixture
def students() -> List[course.Student]:
    """Tests students from example_tests.py"""
    return [course.Student(1, 'Zoro'),
            course.Student(2, 'Aaron'),
            course.Student(3, 'Gertrude'),
            course.Student(4, 'Yvette')]


@pytest.fixture
def alpha_grouping(students_with_answers) -> grouper.Grouping:
    """Tests alpha_grouping from example_tests.py"""
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[3]]))
    grouping.add_group(grouper.Group([students_with_answers[1],
                                      students_with_answers[2]]))
    return grouping


@pytest.fixture
def greedy_grouping(students_with_answers) -> grouper.Grouping:
    """Tests greedy_grouping from example_tests.py"""
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[1],
                                      students_with_answers[3]]))
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[2]]))
    return grouping


@pytest.fixture
def window_grouping(students_with_answers) -> grouper.Grouping:
    """Tests window_grouping from example_tests.py"""
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[1]]))
    grouping.add_group(grouper.Group([students_with_answers[2],
                                      students_with_answers[3]]))
    return grouping


@pytest.fixture
def questions() -> List[survey.Question]:
    """Tests questions from example_tests.py"""
    return [survey.MultipleChoiceQuestion(1, 'why?', ['a', 'b']),
            survey.NumericQuestion(2, 'what?', -2, 4),
            survey.YesNoQuestion(3, 'really?'),
            survey.CheckboxQuestion(4, 'how?', ['a', 'b', 'c'])]


@pytest.fixture
def criteria(answers) -> List[criterion.Criterion]:
    """Tests criteria from example_tests.py"""
    return [criterion.HomogeneousCriterion(),
            criterion.HeterogeneousCriterion(),
            criterion.LonelyMemberCriterion()]


@pytest.fixture()
def weights() -> List[int]:
    """Tests weights from example_tests.py"""
    return [2, 5, 7]


@pytest.fixture
def answers() -> List[List[survey.Answer]]:
    """Tests answers from example_tests.py"""
    return [[survey.Answer('a'), survey.Answer('b'),
             survey.Answer('a'), survey.Answer('b')],
            [survey.Answer(0), survey.Answer(4),
             survey.Answer(-1), survey.Answer(1)],
            [survey.Answer(True), survey.Answer(False),
             survey.Answer(True), survey.Answer(True)],
            [survey.Answer(['a', 'b']), survey.Answer(['a', 'b']),
             survey.Answer(['a']), survey.Answer(['b'])]]


@pytest.fixture
def students_with_answers(students, questions, answers) -> List[course.Student]:
    """Tests students_with_answers from example_tests.py"""
    for i, student in enumerate(students):
        for j, question in enumerate(questions):
            student.set_answer(question, answers[j][i])
    return students


@pytest.fixture
def course_with_students(empty_course, students) -> course.Course:
    """Tests course_with_students from example_tests.py"""
    empty_course.enroll_students(students)
    return empty_course


@pytest.fixture
def course_with_students_with_answers(empty_course,
                                      students_with_answers) -> course.Course:
    """Tests course_with_students_with_answers from example_tests.py"""
    empty_course.enroll_students(students_with_answers)
    return empty_course


@pytest.fixture
def survey_(questions, criteria, weights) -> survey.Survey:
    """Tests survey_ from example_tests.py"""
    s = survey.Survey(questions)
    for i, question in enumerate(questions):
        if i:
            s.set_weight(weights[i-1], question)
        if len(questions)-1 != i:
            s.set_criterion(criteria[i], question)
    return s


@pytest.fixture
def group(students) -> grouper.Group:
    """Tests group from example_tests.py"""
    return grouper.Group(students)


def get_member_ids(grouping: grouper.Grouping) -> Set[FrozenSet[int]]:
    """Tests get_member_ids from example_tests.py"""
    member_ids = set()
    for group in grouping.get_groups():
        ids = []
        for member in group.get_members():
            ids.append(member.id)
        member_ids.add(frozenset(ids))
    return member_ids


def compare_groupings(grouping1: grouper.Grouping,
                      grouping2: grouper.Grouping) -> None:
    """Tests compare_groupings from example_tests.py"""
    assert get_member_ids(grouping1) == get_member_ids(grouping2)


class TestStudent:
    """Tests every methods inside Student Class"""
    def test_student_class(self) -> None:
        """Tests every methods inside Student Class"""
        s = course.Student(0, "Vincent")
        assert s.id == 0
        assert s.name == "Vincent"
        assert str(s) == "Vincent"
        q1 = survey.YesNoQuestion(1, "Do you like cs?")
        q2 = survey.YesNoQuestion(2, "Do you like math?")
        assert not s.has_answer(q1)
        assert not s.has_answer(q2)
        s.set_answer(q1, survey.Answer(False))
        s.set_answer(q2, survey.Answer(True))
        assert s.has_answer(q1)
        assert s.has_answer(q2)
        assert s.get_answer(q1) is not None
        assert s.get_answer(q2) is not None


class TestCourse:
    """Tests every methods inside Course Class"""
    def test_enroll_students(self) -> None:
        """Tests every methods inside Course Class"""
        c1 = course.Course("CSC148")
        c2 = course.Course("CSC165")
        s1 = course.Student(1, "A")
        s2 = course.Student(2, "B")
        c1.enroll_students([s1, s2])
        assert c1.students == [s1, s2]
        assert c1.get_students() == (s1, s2)
        c1.enroll_students([s1])
        assert c1.all_answered(survey.Survey([]))
        assert c2.all_answered(survey.Survey([]))


class TestQuestion:
    """Tests every methods inside Question Class"""
    def test_multiple_choice(self) -> None:
        """Tests MultipleChoiceQuestion"""
        m = survey.MultipleChoiceQuestion(0, "Choose one", ["A", "B", "C"])
        assert m.id == 0
        assert m.text == 'Choose one'
        assert 'Choose one' in str(m)
        assert 'A' in str(m)
        assert 'B' in str(m)
        assert 'C' in str(m)
        a1 = survey.Answer('A')
        a2 = survey.Answer('D')
        a3 = survey.Answer('B')
        assert m.validate_answer(a1)
        assert not m.validate_answer(a2)
        assert m.validate_answer(a3)
        assert m.get_similarity(a1, a1) == 1.0
        assert m.get_similarity(a1, a3) == 0.0

    def test_numeric(self) -> None:
        """Tests NumericQuestion"""
        m = survey.NumericQuestion(0, "what's my favorite number?", 5, 10)
        assert m.id == 0
        assert m.text == "what's my favorite number?"
        assert "what's my favorite number?" in str(m)
        assert '5' in str(m)
        assert '10' in str(m)
        a1 = survey.Answer(5)
        a2 = survey.Answer(19)
        a3 = survey.Answer(10)
        assert m.validate_answer(a1)
        assert not m.validate_answer(a2)
        assert m.validate_answer(a3)
        assert m.get_similarity(a1, a1) == 1.0
        assert m.get_similarity(a1, a3) == 0.0

    def test_yes_no(self) -> None:
        """Tests YesNoQuestion"""
        m = survey.YesNoQuestion(0, "Is the Earth round?")
        assert m.id == 0
        assert m.text == 'Is the Earth round?'
        assert 'Is the Earth round?' in str(m)
        a1 = survey.Answer(True)
        a2 = survey.Answer(1)
        a3 = survey.Answer(False)
        assert m.validate_answer(a1)
        assert not m.validate_answer(a2)
        assert m.validate_answer(a3)
        assert m.get_similarity(a1, a1) == 1.0
        assert m.get_similarity(a3, a3) == 1.0
        assert m.get_similarity(a1, a3) == 0.0
        assert m.get_similarity(a3, a1) == 0.0

    def test_checkbox(self) -> None:
        """Tests CheckboxQuestion"""
        m = survey.CheckboxQuestion(0, "Choose all that applies", \
                                    ["A", "B"])
        assert m.id == 0
        assert m.text == 'Choose all that applies'
        assert 'Choose all that applies' in str(m)
        assert 'A' in str(m)
        assert 'B' in str(m)
        a1 = survey.Answer(["A"])
        a2 = survey.Answer(1)
        a3 = survey.Answer(["A", "B"])
        assert m.validate_answer(a1)
        assert not m.validate_answer(a2)
        assert m.validate_answer(a3)
        assert m.get_similarity(a1, a1) == 1.0
        assert m.get_similarity(a3, a3) == 1.0


class TestAnswer:
    """Tests every methods inside Answer class"""
    def test_eq(self) -> None:
        """Tests special method __eq__"""
        a1 = survey.Answer('Donkey')
        a2 = survey.Answer('Donkey')
        assert a1 == a2

    def test_multiple_choice(self) -> None:
        """Tests MultipleChoiceQuestion"""
        q1 = survey.MultipleChoiceQuestion(0, "just choose", ["A", "B", "C"])
        assert not survey.Answer(1).is_valid(q1)
        assert survey.Answer("C").is_valid(q1)

    def test_numeric(self) -> None:
        """Tests NumericQuestion"""
        q1 = survey.NumericQuestion(0, "what's my favorite number?", 5, 10)
        assert not survey.Answer(1).is_valid(q1)
        assert survey.Answer(5).is_valid(q1)

    def test_yes_no(self) -> None:
        """Tests YesNoQuestion"""
        q1 = survey.YesNoQuestion(0, "Is the Earth round?")
        assert not survey.Answer(1).is_valid(q1)
        assert survey.Answer(True).is_valid(q1)

    def test_checkbox(self) -> None:
        """Tests CheckboxQuestion"""
        q1 = survey.CheckboxQuestion(0, "just choose",
                                     ["A", "B", "C", "D", "E", "F"])
        assert not q1.validate_answer(survey.Answer(1))
        assert not q1.validate_answer(survey.Answer("E"))


class TestCriterion:
    """Tests every methods inside Criterion class"""
    def test_homo_mc(self) -> None:
        """Tests homogeneous multiple choice questions"""
        c = criterion.HomogeneousCriterion()
        q = survey.MultipleChoiceQuestion(0, "just choose", ["A", "B", "C"])
        a1 = survey.Answer("A")
        a2 = survey.Answer("B")
        assert c.score_answers(q, [a1]) == 1.0
        assert c.score_answers(q, [a1, a2]) == 0

    def test_hetero_mc(self) -> None:
        """Tests heterogeneous multiple choice questions"""
        c = criterion.HeterogeneousCriterion()
        q = survey.MultipleChoiceQuestion(0, "just choose", ["A", "B", "C"])
        a1 = survey.Answer("A")
        a2 = survey.Answer("B")
        assert c.score_answers(q, [a1]) == 0.0
        assert c.score_answers(q, [a1, a2]) == 1

    def test_lonely_mc(self) -> None:
        """Tests lonely member multiple choice questions"""
        c = criterion.LonelyMemberCriterion()
        q = survey.MultipleChoiceQuestion(0, "just choose", ["A", "B", "C"])
        a1 = survey.Answer("A")
        a2 = survey.Answer("B")
        assert q.get_similarity(a1, a1) != 0.0
        assert c.score_answers(q, [a1]) == 0.0
        assert c.score_answers(q, [a1, a2]) == 0.0
        assert c.score_answers(q, [a1, a1, a1]) == 1.0

    def test_homo_numeric(self) -> None:
        """Tests homogeneous numeric questions"""
        c = criterion.HomogeneousCriterion()
        q = survey.NumericQuestion(0, "what's my favorite number?", 2, 8)
        a1 = survey.Answer(2)
        a2 = survey.Answer(5)
        assert c.score_answers(q, [a1]) == 1.0
        assert c.score_answers(q, [a1, a2]) == 0.5

    def test_hetero_numeric(self) -> None:
        """Tests heterogeneous numeric questions"""
        c = criterion.HeterogeneousCriterion()
        q = survey.NumericQuestion(0, "what's my favorite number?", 2, 8)
        a1 = survey.Answer(2)
        a2 = survey.Answer(5)
        assert c.score_answers(q, [a1]) == 0.0
        assert c.score_answers(q, [a1, a2]) == 0.5

    def test_lonely_numeric(self) -> None:
        """Tests lonley member numeric questions"""
        c = criterion.LonelyMemberCriterion()
        q = survey.NumericQuestion(0, "Is the Earth round?", 2, 8)
        a1 = survey.Answer(2)
        a2 = survey.Answer(5)
        assert c.score_answers(q, [a1, a2]) == 0.0
        assert c.score_answers(q, [a1, a1, a1]) == 1


class TestGroup:
    """Tests every methods inside Group class"""
    def test_group(self) -> None:
        """Tests every methods inside Group class"""
        g = grouper.Group([])
        students = [course.Student(i, "Student" + str(i)) for i in range(5)]
        assert g.get_members() == []
        assert len(g) == 0
        assert students[0] not in g
        g = grouper.Group(students)
        assert len(g) == 5
        for i in range(5):
            assert students[i] in g
            assert students[i].name in str(g)
        assert isinstance(g.get_members(), list)
        assert len(g.get_members()) == 5


class TestGrouping:
    """Tests every methods inside Grouping class"""
    def test_grouping(self) -> None:
        """Tests every methods inside Grouping class"""
        group1 = grouper.Group([course.Student(i, "Student" + str(i))
                                for i in range(3)])
        grouping = grouper.Grouping()
        grouping.add_group(group1)
        assert "\n" in str(grouping)
        assert "Student0" in str(grouping)
        assert "Student1" in str(grouping)
        assert "Student2" in str(grouping)
        assert len(grouping) == 1
        assert grouping.get_groups() == grouping.get_groups()


class TestSurvey:
    """Tests every methods inside Survey class"""
    def test_survey(self) -> None:
        q1 = survey.YesNoQuestion(0, "Is the Earth round?")
        s = survey.Survey([])
        assert len(s) == 0
        assert q1 not in s
        assert str(s) is not None
        assert len(s.get_questions()) == 0
        assert s.get_questions() == []
        assert isinstance(s._get_criterion(q1), criterion.HomogeneousCriterion)
        assert isinstance(s._get_weight(q1), int)
        assert s.score_students(students) == 0
        grouping = grouper.Grouping()
        assert s.score_grouping(grouping) == 0
        assert not s.set_weight(5, q1)
        assert s._get_weight(q1) == 1


class TestSlicingAndWindows:
    """Tests the helper functions of slice_list and windows in grouper.py"""
    def test_slice_list(self) -> None:
        """Tests slice_list helper function"""
        assert grouper.slice_list([], 2) == []
        assert grouper.slice_list([1, 2, 3], 100) == [[1, 2, 3]]
        assert grouper.slice_list([1, 2, 3], 2) == [[1, 2], [3]]

    def test_windows(self) -> None:
        """Tests windows helper function"""
        assert grouper.windows([], 2) == []
        assert grouper.windows([1, 2, 3, 4, 5], 100) == [[1, 2, 3, 4, 5]]
        assert grouper.windows([1, 2, 3], 2) == [[1, 2], [2, 3]]


def grouping_to_list_of_list(grouping_: grouper.Grouping) -> list:
    """used for converting from grouper.Grouping to list for easier
    comparison"""
    r = []
    for g in grouping_.get_groups():
        r.append(sorted([x.id for x in g.get_members()]))
    r.sort()
    return r


def grouping_to_list_of_list_flatten(grouping: grouper.Grouping) -> list:
    """used for converting from grouper.Grouping to list for easier
    comparison"""
    r = []
    for g in grouping.get_groups():
        r.extend([x.id for x in g.get_members()])
    r.sort()
    return r


class TestGrouper:
    """Tests every classes inside grouper.py"""
    def test_max_score(self) -> None:
        """Tests GreedyGrouper's helper method"""
        students = [course.Student(i, "Student" + str(i)) for i in range(5)]
        questions = [survey.NumericQuestion(i, "What's my favorite number?" +
                                            str(i), 2, 8) for i in range(5)]
        s = survey.Survey(questions)
        answers = [1, 0, 0, 3, 4] * 5
        i = 0
        for q in questions:
            for stu in students:
                stu.set_answer(q, survey.Answer(2 + answers[i]))
                i += 1

        c = course.Course("CSC148")
        c.enroll_students(students)
        grouper_ = grouper.GreedyGrouper(1)._max_score(students, s)
        grouping1 = grouper.GreedyGrouper(1).make_grouping(c, s).get_groups()
        grouping2 = grouping1[0].get_members()
        assert grouper_ == grouping2

    def test_Grouper(self) -> None:
        """Tests every grouper class, AlphaGrouper,
        RandomGrouper, GreedyGrouper, and WindowGrouper
        """
        students = [course.Student(i, "Student" + str(i)) for i in range(5)]
        questions = [survey.NumericQuestion(i, "What's my favorite number?" +
                                            str(i), 2, 8) for i in range(5)]
        s = survey.Survey(questions)

        answers = [1, 0, 0, 3, 4] * 5
        i = 0
        for q in questions:
            for stu in students:
                stu.set_answer(q, survey.Answer(2 + answers[i]))
                i += 1

        c = course.Course("CSC148")
        c.enroll_students(students)

        grouping1 = grouper.AlphaGrouper(1).make_grouping(c, s)
        assert len(grouping1) == 5
        assert grouping_to_list_of_list(grouping1) == [[0], [1], [2], [3], [4]]

        grouping1 = grouper.RandomGrouper(1).make_grouping(c, s)
        assert len(grouping1) == 5
        assert grouping_to_list_of_list_flatten(grouping1) == [0, 1, 2, 3, 4]

        grouping1 = grouper.GreedyGrouper(1).make_grouping(c, s)
        assert len(grouping1) == 5
        assert grouping_to_list_of_list(grouping1) == [[0], [1], [2], [3], [4]]

        grouping1 = grouper.WindowGrouper(1).make_grouping(c, s)
        assert len(grouping1) == 5
        assert grouping_to_list_of_list(grouping1) == [[0], [1], [2], [3], [4]]


if __name__ == '__main__':
    pytest.main(['tests.py'])
