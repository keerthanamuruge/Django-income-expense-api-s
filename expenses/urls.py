from django.urls import path
from . import views
from .views import ExpenseListApiView, ExpenseDetailApiView

urlpatterns =[
    path('', views.ExpenseListApiView.as_view(), name='expenses'),
    path('<int:id>', views.ExpenseDetailApiView.as_view(), name='expense')
]