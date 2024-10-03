from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from leads.forms import CreateLeadsForm
from leads.models import Leads
import logging

logger = logging.getLogger("logger_info")


class LeadsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Представление для отображения списка потенциальных клиентов.

    Пользователь должен быть авторизован для просмотра списка потенциальных клиентов.
    """
    login_url = 'user_auth:login'
    template_name = "leads/leads-list.html"
    model = Leads
    context_object_name = "leads"
    permission_required = "leads.view_leads"

    def get(self, request, *args, **kwargs):
        """
        Логирует запрос на получение списка потенциальных клиентов и возвращает стандартный метод отображения списка.
        """
        logger.info(f"Пользователь {request.user} запросил список потенциальных клиентов.")
        return super().get(request, *args, **kwargs)


class CreateLeadsView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Представление для создания нового потенциального клиента.

    Пользователь должен быть авторизован для создания нового потенциального клиента.
    """
    login_url = 'user_auth:login'
    template_name = "leads/leads-create.html"
    form_class = CreateLeadsForm
    model = Leads
    context_object_name = "leads"
    success_url = reverse_lazy("leads:leads_list")
    permission_required = "leads.add_leads"

    def form_valid(self, form):
        """
        Логирует успешное создание потенциального клиента.
        """
        logger.info(f""
                    f"Пользователь {self.request.user} "
                    f"создал нового потенциального клиента: "
                    f"{form.instance.first_name}{form.instance.last_name}")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Логирует ошибки при неудачной попытке создания потенциального клиента.
        """
        logger.warning(f"Не удалось создать потенциального клиента. Ошибки: {form.errors}")
        return super().form_invalid(form)


class DetailLeadsView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """
    Представление для отображения детальной информации о потенциальном клиенте.

    Пользователь должен быть авторизован для просмотра детальной информации о клиенте.
    """
    login_url = 'user_auth:login'
    model = Leads
    template_name = "leads/leads-detail.html"
    context_object_name = "leads"
    permission_required = "leads.view_leads"

    def get(self, request, *args, **kwargs):
        """
        Логирует запрос на получение детальной информации о потенциальном клиенте.
        """
        logger.info(f"Пользователь {request.user} запросил детальную информацию об потенциальном клиенте.")
        return super().get(request, *args, **kwargs)


class UpdateLeadsView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    Представление для обновления информации о потенциальном клиенте.

    Пользователь должен быть авторизован для обновления информации о клиенте.
    """
    login_url = 'user_auth:login'
    model = Leads
    form_class = CreateLeadsForm
    template_name = "leads/leads-edit.html"
    context_object_name = 'leads'
    permission_required = "leads.change_leads"

    def form_valid(self, form):
        """
        Логирует успешное обновление данных потенциального клиента.
        """
        logger.info(
            f"Пользователь {self.request.user} обновил данные потенциального клиента: "
            f"{form.instance.first_name}, "
            f"{form.instance.last_name}",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Логирует ошибки при неудачном обновлении данных клиента.
        """
        logger.warning(f"Не удалось обновить рекламную данные потенциального клиента. Ошибки: {form.errors}")
        return super().form_invalid(form)

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного обновления клиента.
        """
        return reverse_lazy('leads:detail_leads', kwargs={'pk': self.object.pk})


class DeleteLeadsView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """
    Представление для удаления потенциального клиента.

    Пользователь должен быть авторизован для удаления клиента.
    """
    login_url = 'user_auth:login'
    model = Leads
    template_name = "leads/leads-delete.html"
    context_object_name = "leads"
    success_url = reverse_lazy("leads:leads_list")
    permission_required = "leads.delete_leads"

    def delete(self, request, *args, **kwargs):
        """
        Логирует событие удаления клиента перед его удалением.
        """
        leads = self.get_object()
        logger.info(f"Пользователь {request.user} удалил потенциального клиента: {leads.first_name} (ID: {leads.id})")
        return super().delete(request, *args, **kwargs)
