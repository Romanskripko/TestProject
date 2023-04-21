from django.db import models
from django.db.models import Count, Sum, Subquery, OuterRef

director_position = 'Директор'


class Employee(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    photo = models.ImageField(upload_to='employees')
    position = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=9, decimal_places=2)
    age = models.PositiveIntegerField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='employees')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

        constraints = [
            models.UniqueConstraint(fields=['department', 'position'],
                                    condition=models.Q(position=director_position),
                                    name='staff.Employee.unique_director_for_department')
        ]

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def get_full_list(cls):
        return cls.objects.all().annotate(
            employees_count=Count('employees'),
            salary_count=Sum('employees__salary'),
            director=Subquery(
                Employee.objects.filter(
                    department=OuterRef('pk'),
                    position=director_position
                ).values('name')[:1]),
        ).order_by('id')

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'
