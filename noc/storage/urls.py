from django.urls import path
from.views import (
    ProductList, ProductDetail, ProductCreate, ProductUpdate,
    IncomeList, IncomeCreate, IncomeUpdate, IncomeDelete,
)


urlpatterns = [
    path('catalog/', ProductList.as_view(), name='product_list'),
    path('catalog/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('catalog/add', ProductCreate.as_view(), name='product_add'),
    path('catalog/<slug:slug>/update/', ProductUpdate.as_view(), name='product_update'),
    path('income/', IncomeList.as_view(), name='income_list'),
    path('income/add', IncomeCreate.as_view(), name='income_add'),
    path('income/<slug:slug>/update/', IncomeUpdate.as_view(), name='income_update'),
    path('income/<slug:slug>/delete/', IncomeDelete.as_view(template_name='storage/income_delete.html'), name='income_delete'),
    #path('expense/', ExpenseList.as_view(), name='expense_list'),
    #path('expense/<slug:slug>/update/', ExpenseUpdate.as_view(), name='expense_update'),
]
#<int:pk>
