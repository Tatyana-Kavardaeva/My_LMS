from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from materials.models import Course, Lesson, Enrollment, Module
from tests.models import Test, Question, Answer, StudentAnswer, TestResult
from users.models import User


class TestTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@example')
        self.teacher = User.objects.create(email='teacher@example.com', role='teacher')
        self.student = User.objects.create(email='student@example.com', role='student')
        self.course = Course.objects.create(title='Test Course', description='Test Course', owner=self.teacher)
        self.test = Test.objects.create(title='Test', course=self.course, owner=self.teacher)
        self.question = Question.objects.create(text='Test Question', test=self.test, owner=self.teacher)
        self.answer = Answer.objects.create(text='Test Answer', question=self.question, owner=self.teacher)
        self.answer2 = Answer.objects.create(text='Test Answer2', question=self.question, owner=self.teacher)
        self.student_answer = StudentAnswer.objects.create(question=self.question, student=self.student, answer=self.answer)

    def test_create_test_teacher(self):
        """ Проверяем создание теста преподавателем """
        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:test-list')
        data = {
            'title': 'Test New',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Test.objects.all().count(), 2)

    def test_create_test_student(self):
        """ Проверяем создание теста студентом """

        self.client.force_authenticate(user=self.student)
        url = reverse('tests:test-list')
        data = {
            'title': 'Test Student',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})

    def test_retrieve_test(self):
        """ Проверяем просмотр информации о тесте преподавателем """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:test-detail', args={self.test.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test')

    def test_test_update(self):
        """ Проверяем обновление теста преподавателем """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:test-detail', args=(self.test.pk,))
        data = {'title': 'Test Update'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Test Update')

    def test_test_delete(self):
        """ Проверяем удаление теста преподавателем """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:test-detail', args=(self.test.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Test.objects.all().count(), 0)

class StudentAnswerTestCase(APITestCase):

    def setUp(self):
        self.teacher = User.objects.create(email='teacher@example.com', role='teacher')
        self.student = User.objects.create(email='student@example.com', role='student')
        self.course = Course.objects.create(title='Test Course', description='Test Course', owner=self.teacher)
        self.test = Test.objects.create(title='Test', course=self.course, owner=self.teacher)
        self.question = Question.objects.create(text='Test Question', test=self.test, owner=self.teacher)
        self.answer = Answer.objects.create(text='Test Answer', question=self.question, owner=self.teacher)
        self.student_answer = StudentAnswer.objects.create(question=self.question, student=self.student,
                                                           answer=self.answer)

    def test_student_answer_create(self):
        """ Проверяет ответ на вопрос студентом """

        self.client.force_authenticate(user=self.student)
        url = reverse('tests:student-answer-create')
        data = {
            'question': self.question.pk,
            'answer': self.answer.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_answer_create(self):
        """ Проверяет ответ на вопрос преподавателем """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:student-answer-create')
        data = {
            'question': self.question.pk,
            'answer': self.answer.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})


class TestResultTestCase(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create(email='teacher@example.com', role='teacher')
        self.student = User.objects.create(email='student@example.com', role='student')
        self.course = Course.objects.create(title='Test Course', description='Test Course', owner=self.teacher)
        self.test = Test.objects.create(title='Test', course=self.course, owner=self.teacher)
        self.question = Question.objects.create(text='Test Question', test=self.test, owner=self.teacher)
        self.answer = Answer.objects.create(text='Test Answer', question=self.question, owner=self.teacher)
        self.student_answer = StudentAnswer.objects.create(question=self.question, student=self.student,
                                                           answer=self.answer)
        self.result = TestResult.objects.create(test=self.test, student=self.student)

    def test_result_create(self):
        """ Проверяет создание результата тестирования студентом """
        self.client.force_authenticate(user=self.student)
        url = reverse('tests:results')
        data = {
            'test': self.question.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_result_create_teacher(self):
        """ Проверяет создание результата тестирования преподавателем """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:results')
        data = {
            'test': self.question.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})

    def test_result_detail(self):
        """ Проверяет просмотр результата тестирования студентом, проходившим тест """

        self.client.force_authenticate(user=self.student)
        url = reverse('tests:results-detail', args=(self.result.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_result_detail_any_student(self):
        """ Проверяет просмотр результата тестирования студентом, не проходившим тест """

        self.student2 = User.objects.create(email='student2@example.com', role='student')
        self.client.force_authenticate(user=self.student2)

        url = reverse('tests:results-detail', args=(self.result.pk,))
        response = self.client.get(url)
        print(response.json())
        print(response.status_code)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас нет доступа к этому результату.'})
