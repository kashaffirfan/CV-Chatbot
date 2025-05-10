from rest_framework import serializers
from .models import CV
import os

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ['id', 'file', 'uploaded_at', 'extracted_text', 'name', 'content']
        read_only_fields = ['uploaded_at', 'extracted_text', 'content']

    def create(self, validated_data):
        # Get the file name without extension and use it as the name
        file_obj = validated_data.get('file')
        if file_obj and not validated_data.get('name'):
            name = os.path.splitext(file_obj.name)[0]
            validated_data['name'] = name
        return super().create(validated_data)