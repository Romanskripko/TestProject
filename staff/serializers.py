from rest_framework import serializers

from staff.models import Department, Employee
from staff.validators import UniqueDirectorValidator


class DepartmentSerializer(serializers.ModelSerializer):
    employees_count = serializers.IntegerField(read_only=True)
    salary_count = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    director = serializers.CharField(read_only=True)

    class Meta:
        model = Department
        fields = ('id', 'name', 'employees_count', 'salary_count', 'director')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name', 'photo', 'position', 'salary', 'age', 'department')
        validators = (UniqueDirectorValidator(), )
