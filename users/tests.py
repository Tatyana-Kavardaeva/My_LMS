from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User


class TestUserTestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create(email='admin@test.com', password='1234', role='admin')
        self.teacher_user = User.objects.create(email='teacher@test.com', password='1234', role='teacher')
        self.student_user = User.objects.create(email='student@test.com', password='1234', role='student')

    def test_create_user(self):
        """ Проверяем создание пользователя. """

        data = {'email': 'user2@test.com', 'password': '1234', 'role': 'student'}
        url = reverse('users:users-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)

    def test_create_user_invalid_email(self):
        """ Проверяем создание пользователя с невалидным email """

        url = reverse('users:users-list')
        data = {'email': 'invalidemail', 'password': '1234', 'role': 'student'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['Введите правильный адрес электронной почты.']})

    def test_create_two_admin(self):
        """ Проверяем создание второго администратора """

        url = reverse('users:users-list')
        data = {'email': 'adsmin2@test.com', 'password': '<PASSWORD>', 'role': 'admin'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': ["Ошибка выбора роли. Выберите 'преподаватель' или 'студент'"]})

    def test_list_users_as_admin(self):
        """ Проверяем доступ администратора к просмотру списка пользователей. """

        self.client.force_authenticate(user=self.admin_user)
        url = reverse('users:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_as_teacher(self):
        """ Проверяем доступ к просмотру списка пользователей преподавателем. """

        self.client.force_authenticate(user=self.teacher_user)
        url = reverse('users:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_as_student(self):
        """ Проверяем доступ к просмотру списка пользователей студентом. """

        self.client.force_authenticate(user=self.student_user)
        url = reverse('users:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user(self):
        """ Проверяем просмотр информации о пользователе администратором. """

        self.client.force_authenticate(user=self.admin_user)
        url = reverse('users:users-detail', args={self.student_user.pk})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('email'), self.student_user.email)

    def test_update_user(self):
        """ Проверяем обновление пользователя администратором. """

        self.client.force_authenticate(user=self.admin_user)
        url = reverse('users:users-detail', args=(self.student_user.pk,))
        data = {'first_name': 'Иван'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('first_name'), 'Иван')

    def test_delete_user(self):
        """ Проверяем удаление пользователя администратором """

        self.client.force_authenticate(user=self.admin_user)
        url = reverse('users:users-detail', args=(self.teacher_user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
