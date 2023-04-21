from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer


class DepartmentListView(ListAPIView):
    pagination_class = None
    queryset = Department.get_full_list()
    serializer_class = DepartmentSerializer


class EmployeeViewSet(viewsets.mixins.ListModelMixin,
                      viewsets.mixins.CreateModelMixin,
                      viewsets.mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all().order_by('id')
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'name': ['exact'],
        'department': ['exact'],
    }
