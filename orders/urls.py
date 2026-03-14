from django.urls import path
from orders.views import OrderListCreateView, OrderUpdateStatusView, OrderStatsView

urlpatterns = [
    path('', OrderListCreateView.as_view()),
    path('<int:pk>/status/', OrderUpdateStatusView.as_view()),
    path('stats/', OrderStatsView.as_view()),
]