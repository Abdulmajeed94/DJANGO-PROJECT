from rest_framework import serializers

from .models import Reviewes


class ReviewesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviewes
        fields = '__all__'
