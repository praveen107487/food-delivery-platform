from app.order.models.order import Order
from app.order.models.order_status_history import OrderStatusHistory
from app.order.schemas import (
    OrderDetailsResponse,
    OrderSummaryResponse,
    OrderTimelineResponse,
)


class OrderMapper:
    @staticmethod
    def to_summary_response(order: Order) -> OrderSummaryResponse:
        return OrderSummaryResponse.model_validate(order)

    @staticmethod
    def to_details_response(order: Order) -> OrderDetailsResponse:
        return OrderDetailsResponse.model_validate(order)

    @staticmethod
    def to_timeline_response(
        history: list[OrderStatusHistory],
    ) -> list[OrderTimelineResponse]:
        return [OrderTimelineResponse.model_validate(item) for item in history]
