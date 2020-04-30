from django.urls import path, include
from rest_framework_nested import routers
from . import views


router = routers.SimpleRouter()
router.register(r'hamburguesa', views.BurgerView)
router.register(r'ingrediente', views.IngredientView)

burgers_router = routers.NestedSimpleRouter(
    router, r'hamburguesa', lookup='hamburguesa')
burgers_router.register(r'ingrediente', views.BurgerIngredientView)
urlpatterns = [
    path('', include(router.urls)),
    path('', include(burgers_router.urls)),
]
