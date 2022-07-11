from rest_framework import serializers
from .models import categories, Sentence

class latest_categoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = categories
        fields = (
            'id',
            'name',
        )

class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = (
            'id',
            'name',
        )

class get_categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = categories
        fields = (
            'id',
            'name',
            'description',
            'vol_list',
        )

