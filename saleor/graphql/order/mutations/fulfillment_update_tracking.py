import graphene

from ....core.permissions import OrderPermissions
from ....order.actions import fulfillment_tracking_updated
from ....order.notifications import send_fulfillment_update
from ...app.dataloaders import get_app_promise
from ...core.mutations import BaseMutation
from ...core.types import OrderError
from ...plugins.dataloaders import get_plugin_manager_promise
from ..types import Fulfillment, Order
from .order_fulfill import FulfillmentUpdateTrackingInput


class FulfillmentUpdateTracking(BaseMutation):
    fulfillment = graphene.Field(
        Fulfillment, description="A fulfillment with updated tracking."
    )
    order = graphene.Field(
        Order, description="Order for which fulfillment was updated."
    )

    class Arguments:
        id = graphene.ID(required=True, description="ID of a fulfillment to update.")
        input = FulfillmentUpdateTrackingInput(
            required=True, description="Fields required to update a fulfillment."
        )

    class Meta:
        description = "Updates a fulfillment for an order."
        permissions = (OrderPermissions.MANAGE_ORDERS,)
        error_type_class = OrderError
        error_type_field = "order_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        fulfillment = cls.get_node_or_error(info, data.get("id"), only_type=Fulfillment)
        tracking_number = data.get("input").get("tracking_number") or ""
        fulfillment.tracking_number = tracking_number
        fulfillment.save()
        order = fulfillment.order
        app = get_app_promise(info.context).get()
        manager = get_plugin_manager_promise(info.context).get()
        fulfillment_tracking_updated(
            fulfillment,
            info.context.user,
            app,
            tracking_number,
            manager,
        )
        input_data = data.get("input", {})
        notify_customer = input_data.get("notify_customer")
        if notify_customer:
            send_fulfillment_update(order, fulfillment, manager)
        return FulfillmentUpdateTracking(fulfillment=fulfillment, order=order)
