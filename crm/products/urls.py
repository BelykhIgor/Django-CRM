from django.urls import path

from products.views import (
    ProductsListView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,
    CreateProductView,
)

app_name = "products"

urlpatterns = [
    path('', ProductsListView.as_view(), name='product_list'),
    path('new/', CreateProductView.as_view(), name='create_product'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_edit'),
]