from django.urls import path
from api.views import CategoryView,ProductView,CategoryDetailView,ProductDetailView,CartsView,CartDetailView
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("category",CategoryView,basename="category")
router.register("products",ProductView,basename="product")
router.register("cart",CartsView,basename="cart")
router.register("cart/<int:pk>",CartDetailView,basename="cartdetail")

urlpatterns = [
    path("category/<int:id>",CategoryDetailView.as_view(),name='categorydetail'),
    path("products/<int:id>",ProductDetailView.as_view(), name='productdetail')

]+router.urls