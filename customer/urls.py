from django.urls import path
from customer import views

urlpatterns = [
    path("",views.LoginView.as_view(),name="login"),
    path("register",views.RegistrationView.as_view(),name="registeration"),
    path("home",views.HomeView.as_view(),name="home"),
    path("products/<int:id>",views.ProductDetailView.as_view(),name="product-detail"),
    path("products/<int:id>/carts/add",views.AddToCartView.as_view(),name="addtocart"),
    path("carts/all",views.MyCartView.as_view(),name="mycart"),
    path("carts/remove/<int:id>",views.CartitemRemoval,name="remove-product"),
    path("carts/placeorder/<int:cid>/<int:pid>",views.PlaceOrderView.as_view(),name="place-order")
]
