from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Invoice, InvoiceItem, Customer
from .forms import InvoiceForm, InvoiceItemFormSet, CustomerForm

# Utility: simple invoice number generator
def next_invoice_number():
    last = Invoice.objects.order_by('-id').first()
    nxt = (last.id + 1) if last else 1
    return f"INV-{nxt:05d}"

# Quick customer create
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer created!")
            return redirect('invoice_create')
    else:
        form = CustomerForm()
    return render(request, 'billing/customer_form.html', {'form': form})

def invoice_list(request):
    q = request.GET.get('q','').strip()
    invoices = Invoice.objects.select_related('customer').all().order_by('-id')
    if q:
        invoices = invoices.filter(
            Q(number__icontains=q) |
            Q(customer__name__icontains=q) |
            Q(status__icontains=q)
        )
    return render(request,'billing/invoice_list.html',{'invoices':invoices,'q':q})

def invoice_create(request):
    if request.method=='POST':
        form = InvoiceForm(request.POST, request.FILES)
        formset = InvoiceItemFormSet(request.POST, prefix='items')
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            formset.instance = invoice
            formset.save()
            invoice.update_totals()
            messages.success(request,"Invoice created successfully!")
            return redirect('invoice_list')
    else:
        form = InvoiceForm(initial={'number': next_invoice_number()})
        formset = InvoiceItemFormSet(prefix='items')

    return render(request,'billing/invoice_form.html',{'form':form,'formset':formset})

def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method=='POST':
        form = InvoiceForm(request.POST, request.FILES, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, instance=invoice, prefix='items')
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            formset.instance = invoice
            formset.save()
            invoice.update_totals()
            messages.success(request,"Invoice updated successfully!")
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice, prefix='items')

    return render(request,'billing/invoice_form.html',{'form':form,'formset':formset,'invoice':invoice})
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice.objects.select_related('customer'), pk=pk)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})

def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    messages.success(request, "Invoice deleted!")
    return redirect('invoice_list')
