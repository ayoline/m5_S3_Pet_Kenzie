from rest_framework import generics
from .models import Animal
from .serializers import AnimalSerializer


class AnimalView(generics.ListCreateAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


class AnimalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    lookup_url_kwarg = "animal_id"
