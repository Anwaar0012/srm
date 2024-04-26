from django.contrib import admin
from django.urls import path
from .views import InvoiceListView, createInvoice, view_PDF,get_details_customer,get_product_rate,create_recovery,recovery_list,generate_invoice_excel_report

app_name = 'invoice'
urlpatterns = [
    path('', InvoiceListView.as_view(), name="invoice-list"),
    path('invoice/create/', createInvoice, name="invoice-create"),
    path('invoice-detail/<id>', view_PDF, name='invoice-detail'),
    # path('invoice-download/<id>', generate_PDF, name='invoice-download'),
    path('create-recovery/<id>', create_recovery, name='create-recovery'),
    path('recovery-list/',recovery_list, name='recovery-list'),
    path('get-customer-details/<str:shop_name>/', get_details_customer, name='get_customer_details'),
    path('get-product-rate/<str:product_name>/', get_product_rate, name='get_product_rate'),
    path('gen-report-invoice/', generate_invoice_excel_report, name='generate_invoice_report'),


]
