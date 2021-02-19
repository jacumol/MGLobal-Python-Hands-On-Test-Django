from logging import exception
from unittest.mock import patch, MagicMock
from rest_framework.test import APITestCase
from rest_framework import status
import requests
from django.urls import reverse

from employeeapi.api.serializers import (
    EmployeeSerializer,
    HourlyContractEmployeeSerializer,
    MontlyContractEmployeeSerializer,
)


class EmployeeSerializerTestCase(APITestCase):
    def setUp(self) -> None:
        self.hourly_employee_dict = {
            "id": 1,
            "name": "Sub1",
            "contractTypeName": "HourlySalaryEmployee",
            "roleId": 1,
            "roleName": "Administrator",
            "roleDescription": None,
            "hourlySalary": 10000.0,
            "monthlySalary": 10000.0,
        }
        self.monthly_employee_dict = {
            "id": 1,
            "name": "Sub2",
            "contractTypeName": "MonthlySalaryEmployee",
            "roleId": 1,
            "roleName": "Administrator",
            "roleDescription": None,
            "hourlySalary": 10000.0,
            "monthlySalary": 10000.0,
        }

    def test_check_class_factory(self):
        employee_obj = EmployeeSerializer.factory(self.hourly_employee_dict)
        self.assertIsInstance(employee_obj, HourlyContractEmployeeSerializer)

        employee_obj = EmployeeSerializer.factory(self.monthly_employee_dict)
        self.assertIsInstance(employee_obj, MontlyContractEmployeeSerializer)

    def test_anual_salary_computation(self):
        employee_obj = EmployeeSerializer.factory(self.hourly_employee_dict)
        salary = self.hourly_employee_dict["hourlySalary"] * 120 * 12
        self.assertEqual(employee_obj.data["anualSalary"], salary)

        employee_obj = EmployeeSerializer.factory(self.monthly_employee_dict)
        salary = self.hourly_employee_dict["monthlySalary"] * 12
        self.assertEqual(employee_obj.data["anualSalary"], salary)


class EmployeeListAPIViewTestCase(APITestCase):
    list_url = reverse("employee-list")
    # detail_url = reverse("employee-detail")

    def setUp(self) -> None:
        self.hourly_employee_dict = {
            "id": 1,
            "name": "Sub1",
            "contractTypeName": "HourlySalaryEmployee",
            "roleId": 1,
            "roleName": "Administrator",
            "roleDescription": None,
            "hourlySalary": 10000.0,
            "monthlySalary": 10000.0,
        }
        self.monthly_employee_dict = {
            "id": 2,
            "name": "Sub2",
            "contractTypeName": "MonthlySalaryEmployee",
            "roleId": 2,
            "roleName": "Administrator",
            "roleDescription": None,
            "hourlySalary": 10000.0,
            "monthlySalary": 10000.0,
        }

    @patch("employeeapi.api.utils.EmployeeDataGetter.get_api_data")
    def test_employee_list(self, get_api_data):
        data = [self.hourly_employee_dict, self.monthly_employee_dict]
        get_api_data.return_value = data
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    @patch("employeeapi.api.utils.EmployeeDataGetter.get_api_data")
    def test_employee_detail(self, get_api_data):
        data = [self.hourly_employee_dict, self.monthly_employee_dict]
        get_api_data.return_value = data
        response = self.client.get(reverse("employee-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(self.hourly_employee_dict["name"], response.data["name"])

    @patch("employeeapi.api.utils.EmployeeDataGetter.get_api_data")
    def test_unknown_employee_detail(self, get_api_data):
        data = [self.hourly_employee_dict, self.monthly_employee_dict]
        get_api_data.return_value = data
        response = self.client.get(reverse("employee-detail", kwargs={"pk": 3}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("requests.get")
    def test_bad_timeout_response_employee_list(self, get):
        get.side_effect = requests.exceptions.Timeout
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data["message"], "Timeout error")

    @patch("requests.get")
    def test_bad_too_many_redirect_response_employee_list(self, get):
        get.side_effect = requests.exceptions.TooManyRedirects
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data["message"], "Too many redirects error")

    @patch("requests.get")
    def test_bad_unknown_response_employee_list(self, get):
        get.side_effect = ZeroDivisionError
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data["message"], "Unknown error")
