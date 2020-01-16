from rest_framework import serializers
from .models import Case


class CaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'name', 'data']
