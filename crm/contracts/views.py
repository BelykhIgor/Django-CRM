from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from contracts.forms import ContractCreateForm
from contracts.models import Contracts
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ContractList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    Представление для отображения списка контрактов.

    Это представление отображает все объекты модели Contracts.
    Доступ к нему разрешен только авторизованным пользователям.
    """
    login_url = 'user_auth:login'
    template_name = "contracts/contracts-list.html"
    model = Contracts
    context_object_name = "contracts"
    permission_required = "contracts.view_contracts"


class CreateContractView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Представление для создания нового контракта.

    Пользователь должен быть авторизован для
    создания нового объекта модели Contracts.
    В поле manager автоматически записывается текущий пользователь.
    """
    login_url = 'user_auth:login'
    model = Contracts
    template_name = "contracts/contracts-create.html"
    form_class = ContractCreateForm
    context_object_name = "contracts"
    success_url = reverse_lazy("contracts:contract_list")
    permission_required = "contracts.add_contracts"

    def form_valid(self, form):
        """
        Обрабатывает успешную валидацию формы.

        Назначает текущего пользователя как менеджера
        контракта перед сохранением формы.
        """
        if self.request.user.is_authenticated:
            form.instance.manager = self.request.user
        else:
            return redirect('login')

        return super().form_valid(form)


class DetailContractView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """
    Представление для отображения детальной информации о контракте.

    Пользователь должен быть авторизован для просмотра детальной
    информации о выбранном контракте.
    """
    login_url = 'user_auth:login'
    model = Contracts
    template_name = "contracts/contracts-detail.html"
    context_object_name = "contracts"
    permission_required = "contracts.view_contracts"


class ContractEditView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования контракта.

    Пользователь должен быть авторизован для редактирования
    существующего контракта. Название контракта нельзя изменить при редактировании.
    """
    login_url = 'user_auth:login'
    model = Contracts
    template_name = "contracts/contracts-edit.html"
    form_class = ContractCreateForm
    context_object_name = "contracts"
    permission_required = "contracts.change_contracts"

    def form_valid(self, form):
        """
        Обрабатывает успешную валидацию формы.

        Оставляет название контракта неизменным при редактировании.
        """
        form.instance.title = self.get_object().title
        return super().form_valid(form)

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного редактирования контракта.
        """
        return reverse_lazy('contracts:contract_detail', kwargs={'pk': self.object.pk})


class ContractDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """
    Представление для удаления контракта.

    Пользователь должен быть авторизован для удаления существующего контракта.
    """
    login_url = 'user_auth:login'
    model = Contracts
    template_name = "contracts/contracts-delete.html"
    context_object_name = "contracts"
    success_url = reverse_lazy("contracts:contract_list")
    permission_required = "contracts.delete_contracts"
