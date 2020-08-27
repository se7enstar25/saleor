import logging

from ...celeryconf import app
from ...core.taxes import TaxError
from ...order.events import external_notification_event
from ...order.models import Order
from . import AvataxConfiguration, api_post_request

logger = logging.getLogger(__name__)


@app.task(
    autoretry_for=(TaxError,), retry_backoff=60, retry_kwargs={"max_retries": 5},
)
def api_post_request_task(transaction_url, data, config, order_id):
    config = AvataxConfiguration(**config)
    order = Order.objects.filter(id=order_id).first()
    if not order:
        logger.error(
            "Unable to send the order %s to Avatax. Order doesn't exist.", order_id
        )
        return
    response = api_post_request(transaction_url, data, config)

    msg = f"Order sent to Avatax. Order ID: {order.token}"
    if not response or "error" in response:
        msg = "Unable to send order to Avatax."

    external_notification_event(order=order, user=None, message=msg, parameters=None)
    if not response:
        raise TaxError
