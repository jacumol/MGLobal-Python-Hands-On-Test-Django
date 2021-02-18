from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from employeeapi.api.serializers import EmployeeSerializer

DATA_API_EMPLOYEES_URL = "http://masglobaltestapi.azurewebsites.net/api/Employees/"
class EmployeeListAPIView(APIView):
    
    def get(self, request):
        response = requests.get(DATA_API_EMPLOYEES_URL)
        employees = [EmployeeSerializer.factory(t) for t in response.json()]
        r = []
        for employee in employees:
            # print(employee.data)
            r.append(employee.data)

            # if employee.is_valid():
            #     print(employee.validated_data)
            #     r.append(employee.validated_data)
            # else:
            #     print(employee.errors)

        return Response(r, status=status.HTTP_200_OK)


class EmployeeDetailAPIView(APIView):
    def get(self, request, pk):
        response = requests.get(DATA_API_EMPLOYEES_URL)
        employees = [EmployeeSerializer.factory(t) for t in response.json() if t["id"]==pk]
        if len(employees) == 1:
            employee = employees[0] 
        return Response(employee.data, status=status.HTTP_200_OK)