from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from materials.models import Course, Lesson, Enrollment, Module
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@example')
        self.teacher = User.objects.create(email='teacher@example.com', role='teacher')
        self.teacher2 = User.objects.create(email='teacher2@example.com', role='teacher')
        self.student = User.objects.create(email='student@example.com', role='student')
        self.course = Course.objects.create(title='Test Course', description='Test Course', owner=self.teacher)

    def test_create_course_teacher(self):
        """ Проверяем создание курса преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:course-list')
        data = {'title': 'Test Course New'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_create_course_student(self):
        """ Проверяем создание курса студентом. """

        self.client.force_authenticate(user=self.student)
        url = reverse('materials:course-list')
        data = {'title': 'Test Course Student'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})

    def test_retrieve_course(self):
        """ Проверяем просмотр информации о курсе преподавателем - владельцем курса. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:course-detail', args={self.course.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Course')

    def test_retrieve_course_no_owner(self):
        """ Проверяем просмотр курса преподавателем - не владельцем. """

        self.client.force_authenticate(user=self.teacher2)
        url = reverse('materials:course-detail', args={self.course.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "No Course matches the given query."})

    def test_course_update(self):
        """ Проверяем обновление курса преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:course-detail', args=(self.course.pk,))
        data = {'title': 'Test Course Update'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Test Course Update')

    def test_course_delete(self):
        """ Проверяем удаление курса преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        """ Проверяем просмотр списка всех курсов. """

        self.client.force_authenticate(user=self.student)
        url = reverse('materials:course-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "title": self.course.title,
                    "description": self.course.description,
                    "owner": self.course.owner.pk,
                    "count_modules": 0,
                    "modules": [],
                    'is_enrolled': False
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class ModuleTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@example')
        self.teacher = User.objects.create(email='teacher@example.com', role='teacher')
        self.teacher2 = User.objects.create(email='teacher2@example.com', role='teacher')
        self.student = User.objects.create(email='student@example.com', role='student')
        self.course = Course.objects.create(title='Test Course', description='Test Course', owner=self.teacher)
        self.module = Module.objects.create(title='Test Module', description='Test Module', course=self.course,
                                            owner=self.teacher)

    def test_create_module_teacher(self):
        """ Проверяем создание модуля преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:module-list')
        data = {'title': 'Test Module New', 'course': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.all().count(), 2)

    def test_create_module_student(self):
        """ Проверяем создание модуля студентом. """

        self.client.force_authenticate(user=self.student)
        url = reverse('materials:module-list')
        data = {'title': 'Test Module Student'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})

    def test_retrieve_module(self):
        """ Проверяем просмотр информации о модуле преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:module-detail', args={self.module.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Module')

    def test_module_update(self):
        """ Проверяем обновление модуля преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:module-detail', args=(self.module.pk,))
        data = {'title': 'Test Module Update'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Test Module Update')

    def test_module_delete(self):
        """ Проверяем удаление модуля преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:module-detail', args=(self.module.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Module.objects.all().count(), 0)

    def test_module_list(self):
        """ Проверяем просмотр списка модулей. """

        self.client.force_authenticate(user=self.student)
        url = reverse('materials:module-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.module.pk,
                    "title": self.module.title,
                    "description": self.module.description,
                    "course": self.course.pk,
                    "owner": self.module.owner.pk,
                    "count_lessons": 0
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonTestCase(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create(email='teacher@example.com', role='teacher')
        self.student = User.objects.create(email='student@example.com', role='student')
        self.course = Course.objects.create(title='Test Course', description='Test Course', owner=self.teacher)
        self.module = Module.objects.create(title='Test Module', description='Test Module', course=self.course,
                                            owner=self.teacher)
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Lesson', module=self.module,
                                            owner=self.teacher)

    def test_create_lesson_teacher(self):
        """ Проверяем создание урока преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:lesson-list')
        data = {'title': 'Test Lesson New', 'module': self.module.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_module_student(self):
        """ Проверяем создание урока студентом. """

        self.client.force_authenticate(user=self.student)
        url = reverse('materials:lesson-list')
        data = {'title': 'Test Lesson Student', 'module': self.module.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})

    def test_retrieve_lesson(self):
        """ Проверяем просмотр информации об уроке преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:lesson-detail', args={self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Lesson')

    def test_lesson_update(self):
        """ Проверяем обновление урока преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:lesson-detail', args=(self.lesson.pk,))
        data = {'title': 'Test Lesson Update'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Test Lesson Update')

    def test_lesson_delete(self):
        """ Проверяем удаление урока преподавателем. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:lesson-detail', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """ Проверяем просмотр списка уроков. """

        self.client.force_authenticate(user=self.student)
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "module": self.module.pk,
                    "owner": self.lesson.owner.pk,
                    "video": self.lesson.video,
                    "image": self.lesson.image
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class EnrollmentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@example.com')
        self.teacher = User.objects.create(email='teacher@example.com', role='teacher')
        self.student = User.objects.create(email='student@example.com', role='student')
        self.course = Course.objects.create(title='Test Course', description='Test Course', owner=self.teacher)
        self.enrollment = Enrollment(course=self.course, student=self.student)

    def test_create_enrollment(self):
        """ Проверяем зачисление на курс пользователя - студента. """

        self.client.force_authenticate(user=self.student)
        url = reverse('materials:enrollment-create')
        data = {'course': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Enrollment.objects.filter(student=self.student, course=self.course).exists())

    def test_create_enrollment_any_user(self):
        """ Проверяем зачисление на курс пользователя не являющегося студентом. """

        self.client.force_authenticate(user=self.user)
        url = reverse('materials:enrollment-create')
        data = {'course': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас нет доступа к этому ресурсу.'})

    def test_create_enrollment_teacher(self):
        """ Проверяем зачисление на курс преподавателя. """

        self.client.force_authenticate(user=self.teacher)
        url = reverse('materials:enrollment-create')
        data = {'course': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})

    def test_create_enrollment_delete(self):
        """ Проверяем отчисление студента с курса. """

        self.client.force_authenticate(user=self.student)
        self.enrollment = Enrollment(course=self.course, student=self.student)
        self.enrollment.save()

        url = reverse('materials:enrollment-create')
        data = {'course': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Вы отчислились с курса'})
