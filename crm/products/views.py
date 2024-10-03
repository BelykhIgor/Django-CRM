from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView
)

from products.forms import CreateProductForm
from products.models import Products
import logging

logger = logging.getLogger("logger_info")


class ProductsListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    Представление для отображения списка продуктов.

    Пользователь должен быть авторизован для просмотра списка продуктов.
    """
    login_url = 'user_auth:login'
    template_name = "products/products-list.html"
    model = Products
    context_object_name = "products"
    permission_required = "products.view_products"

    def get(self, request, *args, **kwargs):
        """
        Логирует запрос на получение списка продуктов.
        """
        logger.info(f"Пользователь {request.user} запросил список продуктов.")
        return super().get(request, *args, **kwargs)


class CreateProductView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Представление для создания нового продукта.

    Пользователь должен быть авторизован для создания продукта.
    """
    login_url = 'user_auth:login'
    model = Products
    form_class = CreateProductForm
    template_name = "products/products-create.html"
    context_object_name = "product"
    success_url = reverse_lazy("products:product_list")
    permission_required = "products.add_products"

    def form_valid(self, form):
        """
        Логирует успешное создание продукта.
        """
        logger.info(f"Пользователь {self.request.user} создал новый продукт: {form.instance.title}")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Логирует ошибки при неудачной попытке создания продукта.
        """
        logger.warning(f"Не удалось создать продукт. Ошибки: {form.errors}")
        return super().form_invalid(form)


class ProductDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """
    Представление для отображения детальной информации о продукте.

    Пользователь должен быть авторизован для просмотра детальной информации о продукте.
    """
    login_url = 'user_auth:login'
    model = Products
    template_name = "products/products-detail.html"
    context_object_name = "product"
    permission_required = "products.view_products"

    def get(self, request, *args, **kwargs):
        """
        Логирует запрос на получение детальной информации о продукте.
        """
        logger.info(f"Пользователь {request.user} запросил детальную информацию об продукте.")
        return super().get(request, *args, **kwargs)


class ProductUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования существующего продукта.

    Пользователь должен быть авторизован для редактирования продукта.
    """
    login_url = 'user_auth:login'
    model = Products
    form_class = CreateProductForm
    template_name = "products/products-edit.html"
    context_object_name = "product"
    success_url = reverse_lazy('products:product_list')
    permission_required = "products.change_products"

    def form_valid(self, form):
        """
        Логирует успешное обновление продукта.
        """
        logger.info(f"Пользователь {self.request.user} обновил продукт: {form.instance.title}")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Логирует ошибки при неудачной попытке обновления продукта.
        """
        logger.warning(f"Не удалось обновить продукт. Ошибки: {form.errors}")
        return super().form_invalid(form)


class ProductDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """
    Представление для удаления продукта.

    Пользователь должен быть авторизован для удаления продукта.
    """
    login_url = 'user_auth:login'
    model = Products
    template_name = "products/products-delete.html"
    context_object_name = "product"
    success_url = reverse_lazy('products:product_list')
    permission_required = "products.delete_products"

    def delete(self, request, *args, **kwargs):
        """
        Логирует событие удаления продукта.
        """
        product = self.get_object()
        logger.info(f"Пользователь {request.user} удалил продукт: {product.title} (ID: {product.id})")
        return super().delete(request, *args, **kwargs)

