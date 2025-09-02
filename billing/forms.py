from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, InvoiceItem, Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','email','phone','address']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'customer': forms.Select(attrs={'class':'form-select'}),
            'number': forms.TextInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'due_date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-select'}),
            'discount_type': forms.Select(attrs={'class':'form-select'}),
            'discount_value': forms.NumberInput(attrs={'class':'form-control'}),
            'tax_rate': forms.NumberInput(attrs={'class':'form-control'}),
            'shipping': forms.NumberInput(attrs={'class':'form-control'}),
            'attachment': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'notes': forms.Textarea(attrs={'class':'form-control','rows':3}),
        }

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['title','description','quantity','unit_price']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class':'form-control'}),
        }

InvoiceItemFormSet = inlineformset_factory(
    Invoice, InvoiceItem,
    form=InvoiceItemForm,
    fields=('title','description','quantity','unit_price'),
    extra=0,
    can_delete=True
)



# InvoiceItemFormSet = inlineformset_factory(
#     Invoice, InvoiceItem, form=InvoiceItemForm,
#     fields=['title','description','quantity','unit_price'],
#     extra=1, can_delete=True, min_num=1, validate_min=True
# )
