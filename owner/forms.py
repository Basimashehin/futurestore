from django import forms

class OrderUpdateForm(forms.Form):
    options=(
          ("dispatched","dispatched"),
           ("in_transit","in_transit") 
          )
    status=forms.ChoiceField(choices=options,widget=forms.Select(attrs={"class":"form-select"}))
    expected_delivery_date=forms.DateField(widget=forms.DateInput(attrs={"class":"form-control","type":"date"}))