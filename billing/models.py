from django.db import models
from django.utils import timezone
from decimal import Decimal

class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name or f"Customer #{self.pk}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='invoices')
    number = models.CharField(max_length=20, unique=True)
    date = models.DateField(default=timezone.now)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    discount_type = models.CharField(max_length=10, choices=[('percent','Percent'), ('amount','Amount')], default='percent')
    discount_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))  # percent or flat
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))  # percent
    shipping = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    notes = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='invoices/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_totals(self):
        items = self.items.all()
        sub = sum((item.quantity * item.unit_price for item in items), start=Decimal('0.00'))

        # discount
        if self.discount_type == 'percent':
            discount = (sub * (self.discount_value / Decimal('100'))) if self.discount_value else Decimal('0.00')
        else:
            discount = self.discount_value or Decimal('0.00')

        taxable_base = sub - discount
        tax = (taxable_base * (self.tax_rate / Decimal('100'))) if self.tax_rate else Decimal('0.00')
        grand = taxable_base + tax + (self.shipping or Decimal('0.00'))

        self.subtotal = sub.quantize(Decimal('0.01'))
        self.total = grand.quantize(Decimal('0.01'))
        self.save(update_fields=['subtotal', 'total'])

    def __str__(self):
        return f"{self.number} - {self.customer}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        self.line_total = (self.quantity * self.unit_price).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
        # After saving an item, update the invoice totals:
        self.invoice.update_totals()

    def __str__(self):
        return f"{self.title} ({self.quantity} x {self.unit_price})"
