from django.urls import path, include
from rest_framework_nested import routers
from . import views


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'hamburguesa/?', views.BurgerView)
router.register(r'ingrediente/?', views.IngredientView)

burgers_router = routers.NestedSimpleRouter(
    router, r'hamburguesa/?', lookup='hamburguesa', trailing_slash=False)
burgers_router.register(r'ingrediente/?', views.BurgerIngredientView)
urlpatterns = [
    path('', include(router.urls)),
    path('', include(burgers_router.urls)),
]
