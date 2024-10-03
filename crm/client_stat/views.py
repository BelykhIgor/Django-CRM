from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from ads.models import Ads
from contracts.models import Contracts
from customers.models import Customers
from leads.models import Leads
from products.models import Products
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger("logger_info")

class ClientStatView(LoginRequiredMixin, View):
    login_url = 'user_auth:login'
    def get(self, request):
        logger.info("Start Client statistics")
        if request.user.is_authenticated:
            user = request.user  # Текущий пользователь
            groups = user.groups.all()
            group_names = [group.name for group in groups]
            logger.info(f"User is_authenticated - user: {request.user}, groups: {group_names}")
            products_count = Products.objects.count()
            advertisements_count = Ads.objects.count()
            leads_count = Leads.objects.count()
            customers_count = Customers.objects.count()
            total_ads_budget = Ads.objects.aggregate(Sum('advertising_budget'))['advertising_budget__sum'] or 0
            total_contract_amount = Contracts.objects.aggregate(Sum('amount'))['amount__sum'] or 0
            ratio = round(total_contract_amount / total_ads_budget, 2) if total_ads_budget != 0 else 0

            logger.info(f"statistics data:\n"
                        f"products_count - {products_count}\n"
                        f"advertisements_count - {advertisements_count}\n"
                        f"leads_count - {leads_count}\n"
                        f"customers_count - {customers_count}\n"
                        f"total_ads_budget - {total_ads_budget}\n"
                        f"total_contract_amount - {total_contract_amount}\n"
                        f"ratio - {ratio}"
                        )
            context = {
                'group_names': group_names,
                'products_count': products_count,
                'advertisements_count': advertisements_count,
                'leads_count': leads_count,
                'customers_count': customers_count,
                'total_ads_budget': total_ads_budget,
                'total_contract_amount': total_contract_amount,
                'ratio': ratio,

            }
            return render(request, 'client_stat/index.html', context)
