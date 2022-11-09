from django.urls import path
from . import views


urlpatterns =[
    path('', views.IncomelistApiView.as_view(), name='income'),
    path('<int:id>', views.IncomeDetailApiView.as_view(), name='income_detail')
]