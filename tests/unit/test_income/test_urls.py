from django.urls import reverse, resolve

from incomesource.views import IncomelistApiView, IncomeDetailApiView


class TestExpenseUrls:

    def test_expenses_get_and_post_urls(self):
        url = reverse('income')
        assert resolve(url).func.cls == IncomelistApiView

    def test_expense_detail_url(self):
        url = reverse('income_detail', kwargs={
            'id': 1
        })
        assert resolve(url).func.cls == IncomeDetailApiView
