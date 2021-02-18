from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from employeeapi.api.serializers import EmployeeSerializer
from employeeapi.api.utils import EmployeeDataGetter


class EmployeeListAPIView(APIView):
    def get(self, request):
        response = EmployeeDataGetter.get_api_data()
        if type(response) is dict:
            return Response(response, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        employees = [EmployeeSerializer.factory(t) for t in response.json()]
        data = []
        for employee in employees:
            try:
                data.append(employee.data)
            except AttributeError as e:
                continue
            except:
                Response(
                    {"message": "Unknown error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(data, status=status.HTTP_200_OK)


class EmployeeDetailAPIView(APIView):
    def get(self, request, pk):
        response = EmployeeDataGetter.get_api_data()
        if type(response) is dict:
            return Response(response, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        employees = [
            EmployeeSerializer.factory(t) for t in response.json() if t.get("id") == pk
        ]

        if len(employees) == 1:
            employee = employees[0]
        elif len(employees) == 0:
            return Response(
                {"message": "Resource not found"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            # http_418 is a joke, hope you don't take it seriously!
            return Response(
                {"message": "Multiple objects Returned"},
                status=status.HTTP_418_IM_A_TEAPOT,
            )
        try:
            data = employee.data
        except AttributeError as e:
            return Response(
                {"message": "Resource not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(data, status=status.HTTP_200_OK)
