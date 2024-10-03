from django.urls import path

from contracts.views import ContractList, CreateContractView, DetailContractView, ContractEditView, ContractDeleteView

app_name = "contracts"

urlpatterns = [
    path("", ContractList.as_view(), name="contract_list"),
    path("new/", CreateContractView.as_view(), name="create_contract"),
    path("<int:pk>/", DetailContractView.as_view(), name="contract_detail"),
    path("<int:pk>/edit/", ContractEditView.as_view(), name="contract_edit"),
    path("<int:pk>/delete/", ContractDeleteView.as_view(), name="contract_delete"),
]