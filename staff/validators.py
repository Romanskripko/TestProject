from rest_framework.exceptions import ValidationError

from staff.models import director_position


class UniqueDirectorValidator:
    requires_context = True

    def __call__(self, attrs, serializer):
        if attrs['position'] == director_position and attrs['department'].employees.filter(position='Директор').exists():
            raise ValidationError({'msg': f'{director_position} for this department already exists'})
