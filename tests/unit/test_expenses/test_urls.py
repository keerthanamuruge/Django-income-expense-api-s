from django.urls import reverse, resolve

from expenses.views import ExpenseListApiView, ExpenseDetailApiView


class TestExpenseUrls:

    def test_expenses_get_and_post_urls(self):
        url = reverse('expenses')
        assert resolve(url).func.cls == ExpenseListApiView

    def test_expense_detail_url(self):
        url = reverse('expense', kwargs={
            'id': 1
        })
        assert resolve(url).func.cls == ExpenseDetailApiView
