from rest_framework import serializers
from .models import Case, Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'case', 'name', 'file']


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'case_type', 'data']
        read_only_fields = ['name']
        create_only_fields = ['case_type']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'data':
                value = {**instance.data, **value}

            setattr(instance, attr, value)

        instance.save()
        return instance
