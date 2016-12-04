#! encoding:utf8

### 描述器來建立@property

## 1.
class Homework(object):
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self,value):
        if not (0<=value<=100):
            raise ValueError('Grade must be between 0 and 100')
        self._grade = value

galileo = Homework()
galileo.grade = 95

## 2. 問題是當要設置一個人不同科目的分數時，工作會變得繁瑣。
class Exam(object):
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0<=value<=100):
            raise ValueError('Grade must be between 0 and 100')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self,value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self,value):
        self._check_grade(value)
        self._math_grade = value

### 3.

class Grade(object):
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value

class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

# exam = Exam()
# exam.writing_grade = 40
# Exam.__dict__['writing_grade'].__set__(exam, 40)

first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 100
print('Writing', first_exam.writing_grade)
print('Science', first_exam.science_grade)
second_exam = Exam()
second_exam.writing_grade = 75
print 'Second:{},is right'.format(second_exam.writing_grade)
print 'First:{}, is wrong'.format(first_exam.writing_grade)

## 4. 會有記憶體洩漏問題 (不懂!!!)

class Grade(object):
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None: return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value



## 5.最終解法

from weakref import WeakKeyDictionary

class Grade(object):
    def __init__(self):
        self._values = WeakKeyDictionary()
    def __get__(self, instance, instance_type):
        if instance is None: return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value

class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print('First ', first_exam.writing_grade, 'is right')
print('Second', second_exam.writing_grade, 'is right')
