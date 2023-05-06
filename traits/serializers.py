from rest_framework import serializers
from .models import Trait


class TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trait
        fields = [
            "id",
            "name",
        ]
