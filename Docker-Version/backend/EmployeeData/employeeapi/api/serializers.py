import abc
from collections import namedtuple
from rest_framework import serializers


class BaseEmployeeSerializer(serializers.Serializer):
    __metaclass__ = abc.ABCMeta

    id = serializers.IntegerField()
    name = serializers.CharField()
    contractTypeName = serializers.CharField()
    roleId = serializers.IntegerField()
    roleName = serializers.CharField(required=False, allow_null=True)
    roleDescription = serializers.CharField(required=False, allow_null=True)
    hourlySalary = serializers.IntegerField()
    monthlySalary = serializers.IntegerField()

    anualSalary = serializers.SerializerMethodField()

    @abc.abstractmethod
    def get_anualSalary(self, instance) -> int:
        """
        This method computes the anualsalary of the employee.
        """
        pass


class HourlyContractEmployeeSerializer(BaseEmployeeSerializer):
    def get_anualSalary(self, instance) -> int:
        return 120 * instance.hourlySalary * 12


class MontlyContractEmployeeSerializer(BaseEmployeeSerializer):
    def get_anualSalary(self, instance) -> int:
        return instance.monthlySalary * 12


class EmployeeSerializer(object):
    @classmethod
    def factory(cls, data):
        employee = namedtuple("Employee", data.keys())(*data.values())

        if data.get("contractTypeName") == "HourlySalaryEmployee":
            return HourlyContractEmployeeSerializer(employee)
        elif data.get("contractTypeName") == "MonthlySalaryEmployee":
            return MontlyContractEmployeeSerializer(employee)
        assert 0, "Bad Employee creation: " + data.get("contractTypeName")
