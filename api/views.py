from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.response import Response
from api.serializers import ProductSerializer,CategorySerializer,CartSerializer,OrderSerializer,ReviewSerializers
from owner.models import Products,Categories,Carts,Orders,Reviews
from rest_framework import authentication,permissions
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User

# Create your views here.

class CategoryView(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def create(self,request,*args,**kwargs):
        serializer=CategorySerializer(data=request.data)
        user=request.user
        print(user)
        if serializer.is_valid():
            if user.is_superuser:
                serializer.save()
                return Response(data=serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response({"msg":"only admin can add category"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=True)
    def add_product(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        category = Categories.objects.get(id=id)
        user = request.user
        serializer = ProductSerializer(data=request.data,context={"category": category})
        print(request.user)
        if serializer.is_valid():
            if user.is_superuser == 1:
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": "only admin can add products"},
                                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=True)
    def get_products(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        print(request.user)
        category = Categories.objects.get(id=id)
        products = category.products_set.all()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True)
    def get_reviews(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        product = Products.objects.get(id=id)
        reviews = product.review_set.all()
        serializer = ReviewSerializers(reviews, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def post_review(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        product = Products.objects.get(id=id)
        user = request.user
        serializer = ReviewSerializers(data=request.data, context={"user": user, "product": product})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        print(request.user)
        category=Categories.objects.get(id=id)
        serializer=CategorySerializer(category)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        category=Categories.objects.get(id=id)
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            category.category_name=serializer.validated_data.get("category_name")
            category.is_active=serializer.validated_data.get("is_active")
            category.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        category=Categories.objects.get(id=id)
        serializer=CategorySerializer(category)
        category.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)


class ProductView(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        return Response(data={"msg":"no access"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    @action(methods=["post"], detail=True)
    def add_to_cart(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        product = Products.objects.get(id=id)
        user = request.user
        serializer = CartSerializer(data=request.data, context={"user": user, "product": product})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ProductDetailView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        product =Products.objects.get(id=id)
        serializer=ProductSerializer(product)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class CartsView(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Carts.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return Response(data={"msg":"no access"})

    @action(methods=["post"], detail=True)
    def place_order(self, request, *args, **kwargs):
        cart_id = kwargs.get("pk")
        cart = Carts.objects.get(id=cart_id)
        product = cart.product
        user = request.user
        serializer = OrderSerializer(data=request.data, context={"user": user, "product": product, "cart": cart})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailView(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Carts.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        id=kwargs.get("cid")
        cart = Carts.objects.filter(id=id,user=request.user)
        serializer = CartSerializer(cart,)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return Response(data={"msg": "no access"})





