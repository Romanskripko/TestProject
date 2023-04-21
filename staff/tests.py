import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest.mock import patch
from rest_framework import status
from rest_framework.reverse import reverse

from staff.models import Employee, Department, director_position


class EmployeeTestCase(TestCase):
    def setUp(self) -> None:
        self.department_1 = Department.objects.create(name='TestDepartment')
        self.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.url = reverse('employee-list')
        self.employee_1 = Employee.objects.create(
            name='SomeName',
            photo=self.image,
            position='some_position',
            salary='150000',
            age=20,
            department=self.department_1)
        self.employee_2 = Employee.objects.create(
            name='SomeName',
            photo=self.image,
            position=director_position,
            salary='150000',
            age=20,
            department=self.department_1)
        self.user = get_user_model().objects.create_user(username='admin', password='admin')
        self.client.force_login(user=self.user)

    def test_get_list_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        print(response.data)

    @patch('rest_framework.serializers.ImageField.to_internal_value')
    def test_create_ok(self, mock_image_clean):
        mock_image_clean.return_value = self.image
        response = self.client.post(
            self.url,
            data={
                'name': 'SomeName',
                'photo': self.image,
                'position': 'some_position',
                'salary': '150000',
                'age': 20,
                'department': self.department_1.pk
            }
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 3)

    @patch('rest_framework.serializers.ImageField.to_internal_value')
    def test_create_second_director(self, mock_image_clean):
        mock_image_clean.return_value = self.image
        response = self.client.post(
            self.url,
            data={
                'name': 'SomeName',
                'photo': self.image,
                'position': director_position,
                'salary': '150000',
                'age': 20,
                'department': self.department_1.pk
            }
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['msg'][0], f'{director_position} for this department already exists')

    def test_delete_employee_ok(self):
        url = reverse('employee-detail', kwargs={'pk': self.employee_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 1)


class DepartmentTestCase(TestCase):
    def setUp(self) -> None:
        self.department_1 = Department.objects.create(name='TestDepartment')
        self.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.url = reverse('departments')
        self.employee_1 = Employee.objects.create(
            name='SomeName',
            photo=self.image,
            position='some_position',
            salary='150000',
            age=20,
            department=self.department_1)
        self.employee_2 = Employee.objects.create(
            name='ImportantName',
            photo=self.image,
            position=director_position,
            salary='150000',
            age=20,
            department=self.department_1)
        self.result = [
            {
                'id': self.department_1.id,
                'name': self.department_1.name,
                'employees_count': 2,
                'salary_count': '300000.00',
                'director': 'ImportantName'
            }
        ]

    def test_get_list_ok(self):
        response = self.client.get(self.url)
        print(response.data)
        self.assertEqual(response.data, self.result)
