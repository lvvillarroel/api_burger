from django.shortcuts import render
from rest_framework import status, viewsets, exceptions
from .models import Burger, Ingredient
from .serializers import BurgerSerializer, IngredientSerializer, BurgerIngredientSerializer
from rest_framework.response import Response
import json


class BurgerView(viewsets.ModelViewSet):
    queryset = Burger.objects.all()
    serializer_class = BurgerSerializer
    http_method_names = ['get', 'post', 'patch', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = BurgerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except Exception as e:
                return Response(data='Input inválido', status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            try:
                if int(pk) < 0:
                    raise ValueError
            except Exception as type_e:
                return Response(data='id invalido', status=status.HTTP_400_BAD_REQUEST)
            current_burger = self.get_object()
            serializer = BurgerSerializer(current_burger)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data='hamburguesa inexistente', status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        try:
            current_burger = self.get_object()
        except Exception as burger_e:
            return Response(data='Hamburguesa inexistente', status=status.HTTP_404_NOT_FOUND)
        kwargs['partial'] = True
        try:
            new_burger = self.update(request, *args, **kwargs)
            return Response(data=new_burger.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data='parámetros inválidos', status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            current_burger = self.get_object()
            self.perform_destroy(current_burger)
            return Response(data='hamburguesa eliminada', status=status.HTTP_200_OK)
        except Exception:
            return Response(data='hamburguesa inexistente', status=status.HTTP_404_NOT_FOUND)


class IngredientView(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ingredient = serializer.save()
            serializer.save(
                path='https://t2-burgerapi-ti.herokuapp.com/ingrediente/{}/'.format(ingredient.id))
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            try:
                if int(pk) < 0:
                    raise ValueError
            except Exception as type_e:
                return Response(data='id invalido', status=status.HTTP_400_BAD_REQUEST)
            current_ingredient = self.get_object()
            serializer = IngredientSerializer(current_ingredient)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data='ingrediente inexistente', status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            current_ingredient = self.get_object()
            for burger in Burger.objects.all():
                if current_ingredient in burger.ingredientes.all():
                    return Response(status=status.HTTP_409_CONFLICT, data='Ingrediente no se puede borrar, se encuentra presente en una hamburguesa')
            self.perform_destroy(current_ingredient)
            return Response(data='ingrediente eliminado', status=status.HTTP_200_OK)
        except Exception:
            return Response(data='ingrediente inexistente', status=status.HTTP_404_NOT_FOUND)


class BurgerIngredientView(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = BurgerIngredientSerializer
    http_method_names = ['put', 'delete']

    def update(self, request, *args, **kwargs):
        try:
            # Ver si existe el ingrediente
            try:
                current_ingredient = self.get_object()
            except Exception as ing_e:
                return Response(data='Ingrediente inexistente', status=status.HTTP_404_NOT_FOUND)

            # Ver si existe la hamburguesa
            try:
                current_burger = Burger.objects.get(
                    pk=kwargs['hamburguesa_pk'])
            except Exception as burger_e:
                return Response(data='Id de hamburguesa inválido', status=status.HTTP_400_BAD_REQUEST)

            # Ver si existe el ingrediente en la hamburguesa
            if current_ingredient in current_burger.ingredientes.all():
                return Response(data='ingrediente agregado', status=status.HTTP_201_CREATED)

            # Agregar el ingrediente a la hamburguesa
            current_burger.ingredientes.add(current_ingredient)
            return Response(data='ingrediente agregado', status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data='ingrediente inexistente', status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            current_ingredient = self.get_object()
            try:
                current_burger = Burger.objects.get(
                    pk=kwargs['hamburguesa_pk'])
            except Exception as burger_e:
                return Response(data='Id de hamburguesa inválido', status=status.HTTP_400_BAD_REQUEST)

            if not current_ingredient in current_burger.ingredientes.all():
                return Response(data='ingrediente inexistente en la hamburgesa', status=status.HTTP_404_NOT_FOUND)
            current_burger.ingredientes.remove(current_ingredient)
            return Response(data='ingrediente retirado', status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data='ingrediente inexistente', status=status.HTTP_404_NOT_FOUND)
