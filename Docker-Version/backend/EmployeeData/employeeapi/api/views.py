from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from employeeapi.api.serializers import EmployeeSerializer


class EmployeeListAPIView(APIView):
    def get(self, request):
        DATA_API_URL = "http://masglobaltestapi.azurewebsites.net/api/Employees"
        response = requests.get(DATA_API_URL)
        # print(response)
        # print(response.text)
        # print(response.json())
        # print(response.status_code)
        employees = [EmployeeSerializer.factory(t) for t in response.json()]
        print(employees)
        r = []
        for employee in employees:
            if employee.is_valid():
                r.append(employee.validated_data)
            else:
                print(employee.errors)

        return Response(r, status=status.HTTP_200_OK)


class EmployeeDetailAPIView(APIView):
    pass