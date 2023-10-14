from rest_framework.views import Request, Response, APIView, status
from .models import Pet
from .serializers import PetSerializer
from groups.models import Group
from traits.models import Trait
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):
    def get(self, req: Request) -> Response:
        group_param = req.query_params.get("group", None)
        trait_param = req.query_params.get("trait", None)

        pets = Pet.objects.all()

        if group_param:
            pets = pets.filter(group__name__iexact=group_param)

        if trait_param:
            pets = pets.filter(traits__name__iexact=trait_param).distinct()

        result = self.paginate_queryset(pets, req)
        serializer = PetSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, req: Request) -> Response:
        serializer = PetSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        recieve_group = serializer.validated_data.pop("group")
        recieve_trait = serializer.validated_data.pop("traits")
        group = Group.objects.filter(
            scientific_name__iexact=recieve_group["scientific_name"]
        ).first()
        if not group:
            group = Group.objects.create(**recieve_group)
        pet = Pet.objects.create(**serializer._validated_data, group=group)
        for traits_data in recieve_trait:
            trait = Trait.objects.filter(name__iexact=traits_data["name"]).first()
            if not trait:
                trait = Trait.objects.create(**traits_data)
            trait.pets.add(pet)
        serializer = PetSerializer(pet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PetDetailView(APIView):
    def get(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def patch(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, pk=pet_id)
        serializer = PetSerializer(data=req.data, partial=True)
        serializer.is_valid(raise_exception=True)
        receive_group = serializer.validated_data.pop("group", None)
        receive_traits = serializer.validated_data.pop("traits", None)

        if receive_group:
            group = Group.objects.filter(
                scientific_name__iexact=receive_group["scientific_name"]
            ).first()
            if not group:
                group = Group.objects.create(**receive_group)
            pet.group = group
        if receive_traits:
            trait_to_add = []
            for trait_data in receive_traits:
                trait = Trait.objects.filter(name__iexact=trait_data["name"]).first()
                if not trait:
                    trait = Trait.objects.create(**trait_data)
                trait_to_add.append(trait)
            pet.traits.set(trait_to_add)
        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)
        pet.save()
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def delete(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, pk=pet_id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
