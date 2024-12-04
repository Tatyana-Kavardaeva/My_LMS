from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from materials.models import Course
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
        self.student_answer = StudentAnswer.objects.create(question=self.question, student=self.student,
                                                           answer=self.answer)

    def test_create_test_teacher(self):
        """ Проверяем создание теста преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:test-list')
        data = {'title': 'Test New'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Test.objects.all().count(), 2)

    def test_create_test_student(self):
        """ Проверяем создание теста студентом. """

        self.client.force_authenticate(user=self.student)
        url = reverse('tests:test-list')
        data = {'title': 'Test Student'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})

    def test_create_test_with_an_invalid_title(self):
        """ Проверяем создание теста с невалидным названием. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:test-list')
        data = {'title': 'Крипта'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Использованы запрещенные слова']})

    def test_retrieve_test(self):
        """ Проверяем просмотр информации о тесте преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:test-detail', args={self.test.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test')

    def test_test_update(self):
        """ Проверяем обновление теста преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:test-detail', args=(self.test.pk,))
        data = {'title': 'Test Update'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Test Update')

    def test_test_delete(self):
        """ Проверяем удаление теста преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:test-detail', args=(self.test.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Test.objects.all().count(), 0)

    def test_list_test(self):
        """ Проверяем просмотр теста преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:test-list')
        response = self.client.get(url)
        data = response.json()
        result = {
                    "count": 1,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": self.test.pk,
                            "title": self.test.title,
                            "description": self.test.description,
                            "course": self.test.course.pk,
                            # "completed_at": self.test.completed_at,
                            "owner": self.test.owner.pk,
                            "questions": [
                                {
                                    "id": self.question.pk,
                                    "text": self.question.text,
                                    "test": self.question.test.pk,
                                    "answers": [
                                        {
                                            "pk": self.answer.pk,
                                            "text": self.answer.text,
                                            "is_correct": self.answer.is_correct,
                                            "question": self.answer.question.pk,
                                        },
                                        {
                                            "pk": self.answer2.pk,
                                            "text": self.answer2.text,
                                            "is_correct": self.answer2.is_correct,
                                            "question": self.answer2.question.pk,
                                        }
                                    ]
                                }
                                    ]
                                }
                            ]
                        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


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
        """ Проверяем ответ на вопрос студентом. """

        self.client.force_authenticate(user=self.student)
        url = reverse('tests:student-answer-create')
        data = {'question': self.question.pk, 'answer': self.answer.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_answer_create(self):
        """ Проверяем ответ на вопрос преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:student-answer-create')
        data = {'question': self.question.pk, 'answer': self.answer.pk}
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
        """ Проверяем создание результата тестирования студентом. """
        self.client.force_authenticate(user=self.student)
        url = reverse('tests:results')
        data = {'test': self.question.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_result_create_teacher(self):
        """ Проверяем создание результата тестирования преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('tests:results')
        data = {'test': self.question.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})

    def test_result_detail(self):
        """ Проверяем просмотр результата тестирования студентом, проходившим тест. """

        self.client.force_authenticate(user=self.student)
        url = reverse('tests:results-detail', args=(self.result.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_result_detail_any_student(self):
        """ Проверяем просмотр результата тестирования студентом, не проходившим тест. """

        self.student2 = User.objects.create(email='student2@example.com', role='student')
        self.client.force_authenticate(user=self.student2)
        url = reverse('tests:results-detail', args=(self.result.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас нет доступа к этому результату.'})
