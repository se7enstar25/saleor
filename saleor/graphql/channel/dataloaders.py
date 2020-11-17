from ...channel.models import Channel
from ..checkout.dataloaders import CheckoutByIdLoader, CheckoutLineByIdLoader
from ..core.dataloaders import DataLoader
from ..order.dataloaders import OrderByIdLoader, OrderLineByIdLoader


class ChannelByIdLoader(DataLoader):
    context_key = "channel_by_id"

    def batch_load(self, keys):
        channels = Channel.objects.in_bulk(keys)
        return [channels.get(channel_id) for channel_id in keys]


class ChannelBySlugLoader(DataLoader):
    context_key = "channel_by_slug"

    def batch_load(self, keys):
        channels = Channel.objects.in_bulk(keys, field_name="slug")
        return [channels.get(slug) for slug in keys]


class ChannelByCheckoutLineIDLoader(DataLoader):
    context_key = "channel_by_checkout_line"

    def batch_load(self, keys):
        def channel_by_lines(checkout_lines):
            checkout_ids = [line.checkout_id for line in checkout_lines]

            def channels_by_checkout(checkouts):
                channel_ids = [checkout.channel_id for checkout in checkouts]

                return ChannelByIdLoader(self.context).load_many(channel_ids)

            return (
                CheckoutByIdLoader(self.context)
                .load_many(checkout_ids)
                .then(channels_by_checkout)
            )

        return (
            CheckoutLineByIdLoader(self.context).load_many(keys).then(channel_by_lines)
        )


class ChannelByOrderLineIdLoader(DataLoader):
    context_key = "channel_by_orderline"

    def batch_load(self, keys):
        def channel_by_lines(order_lines):
            order_ids = [line.order_id for line in order_lines]

            def channels_by_checkout(orders):
                channel_ids = [order.channel_id for order in orders]

                return ChannelByIdLoader(self.context).load_many(channel_ids)

            return (
                OrderByIdLoader(self.context)
                .load_many(order_ids)
                .then(channels_by_checkout)
            )

        return OrderLineByIdLoader(self.context).load_many(keys).then(channel_by_lines)
