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
    def get_anualSalary(self, instance):
        """
            This method computes the anualsalary of the employee.
        """
        pass


class HourlyContractEmployeeSerializer(BaseEmployeeSerializer):
    
    def get_anualSalary(self, instance):
        return 120 * instance.hourlySalary * 12


class MontlyContractEmployeeSerializer(BaseEmployeeSerializer):
    
    def get_anualSalary(self, instance):
        return instance.monthlySalary * 12


class EmployeeSerializer(object):

    @classmethod
    def factory(cls, data):
        del data["id"]
        employee = namedtuple("Employee", data.keys())(*data.values())
        if data["contractTypeName"] == "HourlySalaryEmployee": 
            return HourlyContractEmployeeSerializer(employee)
            # return HourlyContractEmployeeSerializer(data=data)
        elif data["contractTypeName"] == "MonthlySalaryEmployee":
            return MontlyContractEmployeeSerializer(employee)
            # return MontlyContractEmployeeSerializer(data=data)
        # if "HourlySalaryEmployee" in data: 
        #     return HourlyContractEmployeeSerializer(data)
        # elif "MonthlySalaryEmployee" in data:
        #     return MontlyContractEmployeeSerializer(data)
        assert 0, "Bad Employee creation: " + type