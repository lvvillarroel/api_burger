from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from .models import Burger, Ingredient


class BurgerIngredientSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'burger_pk': 'burger__pk',
    }

    class Meta:
        model = Ingredient
        fields = ('path',)


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'nombre', 'descripcion')


class BurgerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Burger
        fields = ('id', 'nombre', 'precio',
                  'descripcion', 'imagen', 'ingredientes')
    ingredientes = BurgerIngredientSerializer(many=True, read_only=True)
