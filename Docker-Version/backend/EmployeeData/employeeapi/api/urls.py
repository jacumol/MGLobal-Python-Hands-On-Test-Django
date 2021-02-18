from django.urls import path
from employeeapi.api.views import EmployeeListAPIView

urlpatterns = [
    path("employees/", 
        EmployeeListAPIView.as_view(), name="employee-list"),
]