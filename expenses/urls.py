from django.urls import path
from . import views


urlpatterns =[
    path('', views.ExpenseApiview.as_view(), name='expenses'),
    path('<int:id>', views.ExpenseApiview.as_view(), name='expense')
]