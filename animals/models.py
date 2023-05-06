from django.db import models
from math import log


class Sex(models.TextChoices):
    MALE = "Macho"
    FEMALE = "Femea"
    DEFAULT = "Não informado"


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()

    sex = models.CharField(
        max_length=15,
        choices=Sex.choices,
        default=Sex.DEFAULT,
    )

    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="animals",
    )

    traits = models.ManyToManyField(
        "traits.Trait",
        related_name="animals",
    )

    def convert_dog_age_to_human_years(self):
        human_age = 16 * log(self.age) + 31
        return human_age
