from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from django.views import View
from .models import LineItem, Invoice,Recovery
from .forms import LineItemFormset, InvoiceForm, RecoveryForm
from myapp.models import Product, Shop
from django.utils import timezone


import pdfkit

class InvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.all().order_by("-id")
        context = {
            "invoices":invoices,
        }

        return render(self.request, 'invoice/invoice-list.html', context)
    
    def post(self, request):        
        # import pdb;pdb.set_trace()
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))

        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)
        # import pdb;pdb.set_trace()
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)

        return redirect('invoice:invoice-list')

def createInvoice(request):
    """
    Invoice Generator page it will have Functionality to create new invoices, 
    this will be protected view, only admin has the authority to read and make
    changes here.
    """

    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)
        
        if form.is_valid():
            
            
            invoice = Invoice.objects.create(customer=form.data["customer"],
                    customer_email=form.data["customer_email"],
                    billing_address = form.data["billing_address"],
                    date=form.data["date"],
                    due_date=form.data['due_date'],
                    message=form.data["message"],
                    salesperson=form.data["salesperson"],
                    manager=form.data["manager"],
                    sale_types=form.data['sale_types'],
                    routing=form.data["routing"],
                    paid_amount=form.data["paid_amount"],
                    # balance=form.data["balance"]
                    )
            # invoice.save()
            
        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            for form in formset:
                service = form.cleaned_data.get('service')
                description = form.cleaned_data.get('description')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if service and quantity and rate:
                    amount = Decimal(str(rate)) * Decimal(str(quantity))  # Convert rate and quantity to Decimal objects
                    # amount = float(rate)*float(quantity)
                    total += amount
                    LineItem(customer=invoice,
                            service=service,
                            description=description,
                            quantity=quantity,
                            rate=rate,
                            amount=amount).save()
                    print(total)
            invoice.total_amount = total
            invoice.save()
            # Calculate and update the balance
            # invoice.balance = Decimal(str(invoice.total_amount)) - invoice.paid_amount
            # invoice.balance = invoice.total_amount - Decimal(invoice.paid_amount)
            # invoice.save()
            
            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('/invoice/')
    context = {
        "title" : "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, 'invoice/invoice-create.html', context)


def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    lineitem = invoice.lineitem_set.all()

    # Get the current date
    # current_date = timezone.now()

    # Extract day, month, and year components from the due_date
    invoice_date = invoice.date
    day = invoice_date.day
    month = invoice_date.month
    year = invoice_date.year


    context = {
        "company": {
            "name": "Sh.A.Rehman Traders",
            "address" :"Main Bazaar Piplan (Mianwali)",
            "phone": "03006084456",
            # "email": "asad@gmail.com",
        },
        "invoice_id": f"{invoice.id}{day}{month}{year}",
        "invoice_total": invoice.total_amount,
        "customer": invoice.customer,
        "customer_email": invoice.customer_email,
        "date": invoice_date,
        "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "Sale_Type":invoice.sale_types,
        "lineitem": lineitem,

    }
    return render(request, 'invoice/pdf_template.html', context)

def generate_PDF(request, id):
    # Use False instead of output path to save pdf to a variable
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\wkhtmltopdf.exe')
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice:invoice-detail', args=[id])), False, configuration=config)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response

# def get_recovery_data(request, id):
    
#     invoice = get_object_or_404(Invoice, id=id)
#     data = {
#         'invoice_id': invoice.id,
#         'customer': invoice.customer,
#         'total_amount': invoice.customer,
#         'date': invoice.date.strftime('%Y-%m-%d')
#     }
#     return HttpResponse(json.dumps(data), content_type='application/json')

# def create_recovery(request,id):
#     invoice = get_object_or_404(Invoice, id=id)
#     data = {
#         'invoice_id': invoice.id,
#         'customer': invoice.customer,
#         'total_amount': invoice.customer,
#         'date': invoice.date.strftime('%Y-%m-%d')
#     }
#     return HttpResponse(json.dumps(data), content_type='application/json')
    
    # if request.method == 'POST':

    #     form = RecoveryForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('success_url')  # Replace 'success_url' with the URL to redirect to after successful form submission
    # else:
    #     form = RecoveryForm()
    # return render(request, 'invoice/recovery_form.html', {'form': form})

# def create_recovery(request, id):
#     print("Enter the create_recovery")
#     invoice = get_object_or_404(Invoice, id=id)
#     print("outside the post method")
#     if request.method == 'POST':
#         print("came in post ")
#         form = RecoveryForm(request.POST)
#         if form.is_valid():
#             print("came into form validation")

#             new_paid_amount = form.cleaned_data['new_paid_amount']
#             current_balance = invoice.total_amount - new_paid_amount

#             # Print out values for debugging
#             print("New Paid Amount:", new_paid_amount)
#             print("Current Balance:", current_balance)
#             print("Updated Date:", form.cleaned_data['updated_date'])

#             recovery = Recovery(
#                 customer_name=invoice.customer,
#                 total_amount=invoice.total_amount,
#                 date=invoice.date,
#                 balance=invoice.balance,
#                 updated_date=form.cleaned_data['updated_date'],
#                 new_paid_amount=new_paid_amount,
#                 current_balance=current_balance
#             )
#             recovery.save()
#             print(" data saved")
#     else:
#         form = RecoveryForm()
#         print("using else statiement")

#     data = {
#         'invoice_id': invoice.id,
#         'customer': invoice.customer,
#         'total_amount': invoice.total_amount,
#         'date': invoice.date.strftime('%Y-%m-%d'),
#         'balance': invoice.balance,
#         'form': form,
#     }
#     return render(request, 'invoice/recovery_form.html', data)




# class Recovery(View):
#     def get(self, *args, **kwargs):
#         invoices = Invoice.objects.all().order_by("-id")
#         context = {
#             "invoices":invoices,
#         }

#         return render(self.request, 'invoice/invoice-list.html', context)
    


# def change_status(request):
#     return redirect('invoice:invoice-list')

def view_404(request,  *args, **kwargs):

    return redirect('invoice:invoice-list')

from django.http import JsonResponse


# def get_details_customer(request, shop_name):
#     shop = Shop.objects.get(id=shop_name)
#     data = {
#         'name': shop.name,
#         'address': shop.address,
#         'owner_number': shop.owner_number,
#         'owner_cnic': shop.owner_cnic,
#     }
#     return JsonResponse(data)


def get_details_customer(request, shop_name):
    try:
        shop = Shop.objects.get(name=shop_name)
        data = {
            'name': shop.name,
            'address': shop.address,
            'owner_number': shop.owner_number,
            'owner_cnic': shop.owner_cnic,
        }
        return JsonResponse(data)
    except Shop.DoesNotExist:
        return JsonResponse({'error': 'Shop not found'}, status=404)

# Showing httpresponse when i hit /invoice/get_details_customer/zulfiqarali in browser  
# def get_details_customer(request, shop_name):
#     try:
#         shop = get_object_or_404(Shop, name=shop_name)
#         data = {
#             'name': shop.name,
#             'address': shop.address,
#             'owner_number': shop.owner_number,
#             'owner_cnic': shop.owner_cnic,
#         }
#         return HttpResponse(json.dumps(data), content_type='application/json')
#     except Http404:
#         return HttpResponse(json.dumps({'error': 'Shop not found'}), status=404, content_type='application/json')

    
def get_product_rate(request, product_name):
    try:
        product = Product.objects.get(product_name=product_name)
        data = {
            'rate': product.price,  # Assuming 'price' is the rate field
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
from django.db import transaction
from django.db.models import F

def create_recovery(request, id):
     thank=False
     invoice = get_object_or_404(Invoice, id=id)
     if request.method=="POST":
        customer = invoice.customer
        total_amount = invoice.total_amount
        total_amount= Decimal(total_amount)
        date = invoice.date.strftime('%Y-%m-%d')
        balance = invoice.balance
        # existing_balance=Decimal(balance)
        existing_paid_amount=Invoice.paid_amount
        new_paid_amount_str = request.POST.get('new_paid_amount', '')
        # Convert new_paid_amount to Decimal
        new_paid_amount = Decimal(new_paid_amount_str)
        current_balance = invoice.total_amount - new_paid_amount
        recovery = Recovery(customer_name=customer, total_amount=total_amount, date=date, balance=balance,new_paid_amount=new_paid_amount,current_balance=current_balance)
        recovery.save()
        # Update the invoice's paid_amount field by adding new_paid_amount to it
        # with transaction.atomic():
        #     Invoice.objects.filter(id=id).update(
        #         paid_amount=F('paid_amount') + new_paid_amount,
        #         # previous_balance=F('balance'),
        #         # balance=F('current_balance'),
        #     )
        # with transaction.atomic():
        #         Invoice.objects.filter(id=id).update(paid_amount=F('paid_amount') + new_paid_amount)
        # # with transaction.atomic():
        # #         Invoice.objects.filter(id=id).update(previous_balance=F('previous_balance') + balance)
        # with transaction.atomic():
        #         Invoice.objects.filter(id=id).update(balance=F('balance') + current_balance)

        thank=True
     
     return render(request, 'invoice/recovery_form.html', {'thank':thank,'invoice_id': id})