from decimal import Decimal
from django.db import models
import datetime
# Create your models here.
class Invoice(models.Model):
    customer = models.CharField(max_length=100)
    customer_email = models.TextField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    message = models.TextField(default= "this is a default message.")
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    salesperson = models.CharField(max_length=100, blank=True, null=True)
    manager = models.CharField(max_length=100, blank=True, null=True)
    routing = models.CharField(max_length=255, blank=True, null=True)
    paid_amount=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    balance=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    previous_balance=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    # current_balance=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    sale_types = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False)
    

    def save(self, *args, **kwargs):
        if isinstance(self.total_amount, str):
            self.total_amount = Decimal(self.total_amount)
        if isinstance(self.paid_amount, str):
            self.paid_amount = Decimal(self.paid_amount)

        # Calculate balance if both total_amount and paid_amount are not None
        if self.total_amount is not None and self.paid_amount is not None:
            self.balance = self.total_amount - self.paid_amount

        super().save(*args, **kwargs)



    def __str__(self):
        return str(self.customer)
    
    def get_status(self):
        return self.status
    
    
    

    # def save(self, *args, **kwargs):
        # if not self.id:             
        #     self.due_date = datetime.datetime.now()+ datetime.timedelta(days=15)
        # return super(Invoice, self).save(*args, **kwargs)

class LineItem(models.Model):
    customer = models.ForeignKey(Invoice,on_delete=models.CASCADE, blank=True, null=True)
    service = models.TextField()
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.customer)
    
class Recovery(models.Model):
    customer_name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    updated_date = models.DateField(auto_now=True)
    new_paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    

        
    def __str__(self):
        return f"Recovery for {self.customer_name} on {self.date}"
   