from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from contracts.models import Contracts
from customers.models import Customers
from leads.models import Leads
from products.models import Products
from django.db.models import Sum
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from ads.forms import CreateAdsForm
from ads.models import Ads
import logging

logger = logging.getLogger("logger_info")


class AdsListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    Представление для отображения списка рекламных кампаний.

    Это представление наследуется от ListView и отображает список всех объектов модели Ads.
    Пользователь должен быть авторизован для доступа к этому представлению.
    """
    login_url = 'user_auth:login'
    template_name = "ads/ads-list.html"
    model = Ads
    context_object_name = "ads"
    permission_required = "ads.view_ads"

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос для отображения списка рекламных кампаний.

        Логирует запрос и вызывает родительский метод get для рендеринга страницы.
        """
        logger.info(f"Пользователь {request.user} запросил список рекламных компаний.")
        return super().get(request, *args, **kwargs)


class AdsCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Представление для создания новой рекламной кампании.

    Пользователь должен быть авторизован для создания нового объекта Ads.
    """
    login_url = 'user_auth:login'
    template_name = "ads/ads-create.html"
    form_class = CreateAdsForm
    model = Ads
    context_object_name = "ads"
    success_url = reverse_lazy("ads:ads_list")
    permission_required = "ads.add_ads"

    def form_valid(self, form):
        """
        Обрабатывает успешную валидацию формы.

        Логирует создание новой рекламной кампании.
        """
        logger.info(f"Пользователь {self.request.user} создал новую рекламную компанию: {form.instance.title}")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Обрабатывает неудачную валидацию формы.

        Логирует ошибки, возникшие при создании новой рекламной кампании.
        """
        logger.warning(f"Не удалось создать рекламную компанию. Ошибки: {form.errors}")
        return super().form_invalid(form)


class AdsDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """
    Представление для отображения детальной информации о рекламной кампании.

    Пользователь должен быть авторизован для просмотра детальной информации.
    """
    login_url = 'user_auth:login'
    model = Ads
    template_name = "ads/ads-detail.html"
    context_object_name = "ads"
    permission_required = "ads.view_ads"

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос для получения детальной информации о рекламной кампании.

        Логирует запрос детальной информации и вызывает родительский метод get.
        """
        logger.info(f"Пользователь {request.user} запросил детальную информацию об рекламной компании.")
        return super().get(request, *args, **kwargs)


class AdsEditView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования рекламной кампании.

    Пользователь должен быть авторизован для редактирования существующей рекламной кампании.
    """
    login_url = 'user_auth:login'
    model = Ads
    form_class = CreateAdsForm
    template_name = "ads/ads-edit.html"
    context_object_name = 'ads'
    permission_required = "ads.change_ads"

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного редактирования кампании.
        """
        return reverse_lazy('ads:ads_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        """
        Обрабатывает успешную валидацию формы.

        Логирует обновление рекламной кампании.
        """
        logger.info(f"Пользователь {self.request.user} обновил рекламную компанию: {form.instance.title}")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Обрабатывает успешную валидацию формы.

        Логирует обновление рекламной кампании.
        """
        logger.warning(f"Не удалось обновить рекламную компанию. Ошибки: {form.errors}")
        return super().form_invalid(form)


class AdsDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """
    Обрабатывает неудачную валидацию формы.

    Логирует ошибки, возникшие при обновлении рекламной кампании.
    """
    login_url = 'user_auth:login'
    model = Ads
    template_name = "ads/ads-delete.html"
    context_object_name = "ads"
    success_url = reverse_lazy("ads:ads_list")
    permission_required = "ads.delete_ads"

    def delete(self, request, *args, **kwargs):
        """
        Обрабатывает удаление рекламной кампании.

        Логирует удаление рекламной кампании и вызывает родительский метод delete.
        """
        ads = self.get_object()
        logger.info(f"Пользователь {request.user} удалил рекламную компанию: {ads.title} (ID: {ads.id})")
        return super().delete(request, *args, **kwargs)


class AdsStatisticView(View):
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
