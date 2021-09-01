from django.urls import path

from lotracker.views.info import InfoView
from lotracker.views.filter_set import FilterSetListCreateAPIView, FilterSetUpdateDeleteAPIView
from lotracker.views.filter_set_lot import FilterSetLotListAPIView, MarkAsReadView, MarkAllAsReadView
from lotracker.views.lot import LotListAPIView, FilterDataAPIView, LotDetailAPIView, SuggestAPIView, \
    AddToFavouriteAPIView, FavouriteLotsListAPIView
from lotracker.views.organization import OrganizationDetailAPIView, OrganizationListAPIView
from lotracker.views.product import ProductListAPIView

urlpatterns = [
    path('info/', InfoView.as_view(), name='info'),
    path('lots/', LotListAPIView.as_view(), name='lot-list'),
    path('lots/<int:pk>/', LotDetailAPIView.as_view(), name='lot-detail'),
    path('lots/<int:pk>/favourite/', AddToFavouriteAPIView.as_view(), name='lot-favourite'),
    path('products/', ProductListAPIView.as_view(), name='organization-list'),
    path('organizations/', OrganizationListAPIView.as_view(), name='organization-list'),
    path('organizations/<int:pk>/', OrganizationDetailAPIView.as_view(), name='organization-detail'),
    path('filter_data/', FilterDataAPIView.as_view(), name='filter-data'),
    path('favourites/', FavouriteLotsListAPIView.as_view(), name='favourite-list'),
    path('suggest/', SuggestAPIView.as_view(), name='suggest'),
    path('filter_sets/', FilterSetListCreateAPIView.as_view(), name='filter-sets-list'),
    path('filter_sets/<int:pk>/', FilterSetUpdateDeleteAPIView.as_view(), name='filter-sets-detail'),
    path('filter_sets_lots/', FilterSetLotListAPIView.as_view(), name='filter-sets-lots-detail'),
    path('filter_sets_lots/<int:pk>/mark_as_read/', MarkAsReadView.as_view(), name='filter-sets-lots-mark-as-read'),
    path('filter_sets_lots/mark_as_read/', MarkAllAsReadView.as_view(), name='filter-sets-lots-mark-all-as-read'),
]
