from rest_framework import serializers
from .models import Animal, Sex
from groups.models import Group
from traits.models import Trait
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from rest_framework.exceptions import PermissionDenied


class AnimalSerializer(serializers.ModelSerializer):
    sex = serializers.ChoiceField(
        choices=Sex.choices,
        default=Sex.DEFAULT,
    )
    age_in_human_years = serializers.SerializerMethodField()
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def get_age_in_human_years(self, obj: Animal):
        return obj.convert_dog_age_to_human_years()

    class Meta:
        model = Animal
        fields = [
            "name",
            "age",
            "weight",
            "sex",
            "age_in_human_years",
            "group",
            "traits",
        ]

    def create(self, validated_data: dict):
        group_data = validated_data.pop("group")
        group_obj, _ = Group.objects.get_or_create(**group_data)

        traits_list = []
        traits = validated_data.pop("traits")
        for trait in traits:
            obj, _ = Trait.objects.get_or_create(**trait)
            traits_list.append(obj)

        animal_obj = Animal.objects.create(**validated_data, group=group_obj)
        animal_obj.traits.set(traits_list)

        return animal_obj

    def update(self, instance: Animal, validated_data: dict):
        UNAUTHORIZED_KEYS = ["group", "traits", "sex"]
        errors = {}

        for key, value in validated_data.items():
            if key in UNAUTHORIZED_KEYS:
                errors.update({f"{key}": f"You can not update {key} property."})
            else:
                setattr(instance, key, value)

        if len(errors):
            raise PermissionDenied(errors)
           
        instance.save()

        return instance
