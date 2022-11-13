from owner.models import Carts
def cart_count(request):
    cnt=Carts.objects.filter(user=request.user,status="in_cart").count()
    return{"cnt":cnt}