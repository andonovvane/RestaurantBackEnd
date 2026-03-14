from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
from datetime import timedelta
from .models import Order, OrderItem
from .serializers import OrderSerializer
from user.permissions import CanManageOrders, IsStaff, IsCEO
from menuItems.models import MenuItem
from wineselection.models import Wine
from ingredients.models import Ingredient


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [CanManageOrders]

    def get_queryset(self):
        user = self.request.user
        if user.role == "client":
            return Order.objects.filter(client=user).order_by("-created_at")
        return super().get_queryset()


class OrderUpdateStatusView(APIView):
    permission_classes = [IsStaff]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {"error": "No status provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status == "completed":
            try:
                order.complete_order()
            except ValueError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            order.status = new_status
            order.save()

        return Response(OrderSerializer(order).data)


class OrderStatsView(APIView):
    permission_classes = [IsCEO]

    def get(self, request):
        period = request.query_params.get("period", "day")
        now = timezone.now()

        # Determine time range and grouping based on period
        if period == "day":
            start_date = now - timedelta(days=1)
            trunc_fn = TruncDay
        elif period == "week":
            start_date = now - timedelta(weeks=1)
            trunc_fn = TruncDay
        elif period == "month":
            start_date = now - timedelta(days=30)
            trunc_fn = TruncDay
        elif period == "year":
            start_date = now - timedelta(days=365)
            trunc_fn = TruncMonth
        else:
            return Response(
                {"error": "Invalid period. Choose from: day, week, month, year"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter completed orders within the period
        completed_orders = Order.objects.filter(
            status="completed",
            created_at__gte=start_date
        )

        # Total revenue
        total_revenue = OrderItem.objects.filter(
            order__in=completed_orders
        ).aggregate(
            total=Sum(F('price_at_order') * F('quantity'))
        )['total'] or 0

        # Total orders count
        total_orders = Order.objects.filter(created_at__gte=start_date).count()

        # Revenue over time (for line chart)
        revenue_over_time = completed_orders.annotate(
            period=trunc_fn('created_at')
        ).values('period').annotate(
            revenue=Sum('items__price_at_order'),
            orders=Count('id')
        ).order_by('period')

        # Most ordered menu items
        top_menu_items = OrderItem.objects.filter(
            order__in=completed_orders,
            item_type="menu_item"
        ).values('item_id').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:5]

        # Enrich menu items with names
        top_menu_items_data = []
        for item in top_menu_items:
            try:
                menu_item = MenuItem.objects.get(id=item['item_id'])
                top_menu_items_data.append({
                    "name": menu_item.name,
                    "category": menu_item.category,
                    "total_quantity": item['total_quantity']
                })
            except MenuItem.DoesNotExist:
                pass

        # Most ordered wines
        top_wines = OrderItem.objects.filter(
            order__in=completed_orders,
            item_type="wine"
        ).values('item_id').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:5]

        # Enrich wines with names
        top_wines_data = []
        for wine in top_wines:
            try:
                wine_obj = Wine.objects.get(id=wine['item_id'])
                top_wines_data.append({
                    "name": wine_obj.name,
                    "wine_type": wine_obj.wine_type,
                    "total_quantity": wine['total_quantity']
                })
            except Wine.DoesNotExist:
                pass

        # Orders by status breakdown
        status_breakdown = Order.objects.filter(
            created_at__gte=start_date
        ).values('status').annotate(
            count=Count('id')
        )

        # Peak hours
        peak_hours = completed_orders.extra(
            select={'hour': 'EXTRACT(hour FROM created_at)'}
        ).values('hour').annotate(
            count=Count('id')
        ).order_by('hour')

        # Low stock alerts
        low_stock_ingredients = Ingredient.objects.filter(
            stock_quantity__lte=10
        ).values('name', 'stock_quantity', 'unit')

        low_stock_wines = Wine.objects.filter(
            stock_of_wine__lte=5
        ).values('name', 'stock_of_wine')

        return Response({
            "period": period,
            "total_revenue": float(total_revenue),
            "total_orders": total_orders,
            "revenue_over_time": list(revenue_over_time),
            "top_menu_items": top_menu_items_data,
            "top_wines": top_wines_data,
            "status_breakdown": list(status_breakdown),
            "peak_hours": list(peak_hours),
            "low_stock_ingredients": list(low_stock_ingredients),
            "low_stock_wines": list(low_stock_wines),
        })