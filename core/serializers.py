from rest_framework import serializers
from .models import Case


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'case_type', 'data']
        read_only_fields = ['name']
        create_only_fields = ['case_type']
