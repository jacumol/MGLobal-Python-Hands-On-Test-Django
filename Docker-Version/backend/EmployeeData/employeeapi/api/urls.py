from django.urls import path
from employeeapi.api.views import EmployeeListAPIView, EmployeeDetailAPIView

urlpatterns = [
    path("employees/", EmployeeListAPIView.as_view(), name="employee-list"),
    path(
        "employees/<int:pk>/", EmployeeDetailAPIView.as_view(), name="employee-detail"
    ),
]
