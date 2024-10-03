from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DeleteView,
    CreateView,
    UpdateView,
    DetailView
)

from customers.forms import CustomersCreateForm
from customers.models import Customers
import logging

logger = logging.getLogger("logger_info")

class CustomersListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    Представление для отображения списка клиентов.

    Пользователь должен быть авторизован для просмотра списка всех активных клиентов.
    """
    login_url = 'user_auth:login'
    template_name = "customers/customers-list.html"
    model = Customers
    context_object_name = "customers"
    permission_required = "customers.view_customers"

    def get(self, request, *args, **kwargs):
        """
        Записывает информацию о запросе пользователя и вызывает стандартный метод отображения списка клиентов.
        """
        logger.info(f"Пользователь {request.user} запросил список активных клиентов.")
        return super().get(request, *args, **kwargs)


class CreateCustomersView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Представление для создания нового клиента.

    Пользователь должен быть авторизован для создания нового клиента.
    """
    login_url = 'user_auth:login'
    model = Customers
    form_class = CustomersCreateForm
    template_name = "customers/customers-create.html"
    context_object_name = "customers"
    success_url = reverse_lazy("customers:customers_list")
    permission_required = "customers.add_customers"

    def form_valid(self, form):
        """
        Обрабатывает успешную валидацию формы и записывает событие создания клиента в логи.
        """
        customer = form.save(commit=False)
        customer.save()
        logger.info(f"Пользователь {self.request.user} создал активного клиента: {customer}")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Обрабатывает неудачную валидацию формы и записывает ошибки в логи.
        """
        logger.warning(f"Не удалось создать активного клиента. Ошибки: {form.errors}")
        return super().form_invalid(form)


class CustomersDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """
    Представление для отображения детальной информации о клиенте.

    Пользователь должен быть авторизован для просмотра детальной информации о клиенте.
    """
    login_url = 'user_auth:login'
    model = Customers
    template_name = "customers/customers-detail.html"
    context_object_name = "customers"
    permission_required = "customers.view_customers"

    def get(self, request, *args, **kwargs):
        """
        Записывает информацию о запросе пользователя на просмотр деталей клиента.
        """
        logger.info(f"Пользователь {request.user} запросил детальную информацию активном клиенте.")
        return super().get(request, *args, **kwargs)


class CustomersEditView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования информации о клиенте.

    Пользователь должен быть авторизован для обновления данных клиента.
    """
    login_url = 'user_auth:login'
    model = Customers
    form_class = CustomersCreateForm
    template_name = "customers/customers-edit.html"
    context_object_name = "customers"
    permission_required = "customers.change_customers"

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного редактирования клиента.
        """
        return reverse_lazy('customers:customers_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        """
        Обрабатывает успешную валидацию формы и записывает событие обновления клиента в логи.
        """
        logger.info(f"Пользователь {self.request.user} обновил данные активного клиента: {form.instance.title}")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Обрабатывает неудачную валидацию формы и записывает ошибки в логи.
        """
        logger.warning(f"Не удалось обновить данные активного клиента. Ошибки: {form.errors}")
        return super().form_invalid(form)


class CustomersDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """
    Представление для удаления клиента.

    Пользователь должен быть авторизован для удаления клиента.
    """
    login_url = 'user_auth:login'
    model = Customers
    template_name = "customers/customers-delete.html"
    context_object_name = "customers"
    success_url = reverse_lazy("customers:customers_list")
    permission_required = "customers.delete_customers"

    def delete(self, request, *args, **kwargs):
        """
        Записывает событие удаления клиента в логи перед его удалением.
        """
        customers = self.get_object()
        logger.info(f"Пользователь {request.user} удалил активного клиента: {customers.title} (ID: {customers.id})")
        return super().delete(request, *args, **kwargs)