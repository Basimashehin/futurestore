from django.shortcuts import render,redirect
from owner.models import Orders
from owner.forms import OrderUpdateForm
from django.core.mail import send_mail

# Create your views here.
from django.views.generic import TemplateView,ListView,DetailView

class AdminDashBoardView(TemplateView):
    template_name="dashboard.html"
     
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        cnt=Orders.objects.filter(status="order_placed").count()
        print("here",cnt)
        context["count"]=cnt
        return context

class OrdersListView(ListView):
    model=Orders
    context_object_name="orders"
    template_name="admin-listorder.html"

    def get_queryset(self):
        return Orders.objects.filter(status="order_placed")


class OrderDetailView(DetailView):
    model=Orders
    template_name="order-details.html"
    pk_url_kwarg="id"
    context_object_name="order"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        form=OrderUpdateForm()
        context["form"]=form
        return context
    def post(self,request,*args,**kwargs):
        order=self.get_object()
        form=OrderUpdateForm(request.POST)
        if form.is_valid():
            order.status=form.cleaned_data.get("status")
            order.expected_delivery_date=form.cleaned_data.get("expected_delivery_date")
            dt=form.cleaned_data.get("expected_delivery_date")
            order.save()
            send_mail("order delivery update futurestore",
            f"your order will be delivered on {dt}",
            "basimak95@gmail.com",
            ["bijila47@gmail.com"]
            )
            return redirect("dashboard")
        else:
            return render(request,self.template_name)





