from ..core.permissions import (
    AccountPermissions,
    CheckoutPermissions,
    DiscountPermissions,
    OrderPermissions,
    PagePermissions,
    PaymentPermissions,
    ProductPermissions,
    ShippingPermissions,
    SitePermissions,
)


class WebhookEventAsyncType:
    ANY = "any_events"

    CATEGORY_CREATED = "category_created"
    CATEGORY_UPDATED = "category_updated"
    CATEGORY_DELETED = "category_deleted"

    ORDER_CREATED = "order_created"
    ORDER_CONFIRMED = "order_confirmed"
    ORDER_FULLY_PAID = "order_fully_paid"
    ORDER_UPDATED = "order_updated"
    ORDER_CANCELLED = "order_cancelled"
    FULFILLMENT_CANCELED = "fulfillment_canceled"
    ORDER_FULFILLED = "order_fulfilled"

    DRAFT_ORDER_CREATED = "draft_order_created"
    DRAFT_ORDER_UPDATED = "draft_order_updated"
    DRAFT_ORDER_DELETED = "draft_order_deleted"

    SALE_CREATED = "sale_created"
    SALE_UPDATED = "sale_updated"
    SALE_DELETED = "sale_deleted"

    INVOICE_REQUESTED = "invoice_requested"
    INVOICE_DELETED = "invoice_deleted"
    INVOICE_SENT = "invoice_sent"

    FULFILLMENT_CREATED = "fulfillment_created"

    CUSTOMER_CREATED = "customer_created"
    CUSTOMER_UPDATED = "customer_updated"

    COLLECTION_CREATED = "collection_created"
    COLLECTION_UPDATED = "collection_updated"
    COLLECTION_DELETED = "collection_deleted"

    PRODUCT_CREATED = "product_created"
    PRODUCT_UPDATED = "product_updated"
    PRODUCT_DELETED = "product_deleted"

    PRODUCT_VARIANT_CREATED = "product_variant_created"
    PRODUCT_VARIANT_UPDATED = "product_variant_updated"
    PRODUCT_VARIANT_DELETED = "product_variant_deleted"

    PRODUCT_VARIANT_OUT_OF_STOCK = "product_variant_out_of_stock"
    PRODUCT_VARIANT_BACK_IN_STOCK = "product_variant_back_in_stock"

    CHECKOUT_CREATED = "checkout_created"
    CHECKOUT_UPDATED = "checkout_updated"

    NOTIFY_USER = "notify_user"

    PAGE_CREATED = "page_created"
    PAGE_UPDATED = "page_updated"
    PAGE_DELETED = "page_deleted"

    TRANSLATION_CREATED = "translation_created"
    TRANSLATION_UPDATED = "translation_updated"

    DISPLAY_LABELS = {
        ANY: "Any events",
        CATEGORY_CREATED: "Category created",
        CATEGORY_UPDATED: "Category updated",
        CATEGORY_DELETED: "Category deleted",
        ORDER_CREATED: "Order created",
        ORDER_CONFIRMED: "Order confirmed",
        ORDER_FULLY_PAID: "Order paid",
        ORDER_UPDATED: "Order updated",
        ORDER_CANCELLED: "Order cancelled",
        ORDER_FULFILLED: "Order fulfilled",
        DRAFT_ORDER_CREATED: "Draft order created",
        DRAFT_ORDER_UPDATED: "Draft order updated",
        DRAFT_ORDER_DELETED: "Draft order deleted",
        SALE_CREATED: "Sale created",
        SALE_UPDATED: "Sale updated",
        SALE_DELETED: "Sale deleted",
        INVOICE_REQUESTED: "Invoice requested",
        INVOICE_DELETED: "Invoice deleted",
        INVOICE_SENT: "Invoice sent",
        CUSTOMER_CREATED: "Customer created",
        CUSTOMER_UPDATED: "Customer updated",
        COLLECTION_CREATED: "Collection created",
        COLLECTION_UPDATED: "Collection updated",
        COLLECTION_DELETED: "Collection deleted",
        PRODUCT_CREATED: "Product created",
        PRODUCT_UPDATED: "Product updated",
        PRODUCT_DELETED: "Product deleted",
        PRODUCT_VARIANT_CREATED: "Product variant created",
        PRODUCT_VARIANT_UPDATED: "Product variant updated",
        PRODUCT_VARIANT_DELETED: "Product variant deleted",
        PRODUCT_VARIANT_OUT_OF_STOCK: "Product variant stock changed",
        PRODUCT_VARIANT_BACK_IN_STOCK: "Product variant back in stock",
        CHECKOUT_CREATED: "Checkout created",
        CHECKOUT_UPDATED: "Checkout updated",
        FULFILLMENT_CREATED: "Fulfillment_created",
        FULFILLMENT_CANCELED: "Fulfillment_cancelled",
        NOTIFY_USER: "Notify user",
        PAGE_CREATED: "Page Created",
        PAGE_UPDATED: "Page Updated",
        PAGE_DELETED: "Page Deleted",
        TRANSLATION_CREATED: "Create translation",
        TRANSLATION_UPDATED: "Update translation",
    }

    CHOICES = [
        (ANY, DISPLAY_LABELS[ANY]),
        (CATEGORY_CREATED, DISPLAY_LABELS[CATEGORY_CREATED]),
        (CATEGORY_UPDATED, DISPLAY_LABELS[CATEGORY_UPDATED]),
        (CATEGORY_DELETED, DISPLAY_LABELS[CATEGORY_DELETED]),
        (ORDER_CREATED, DISPLAY_LABELS[ORDER_CREATED]),
        (ORDER_CONFIRMED, DISPLAY_LABELS[ORDER_CONFIRMED]),
        (ORDER_FULLY_PAID, DISPLAY_LABELS[ORDER_FULLY_PAID]),
        (ORDER_UPDATED, DISPLAY_LABELS[ORDER_UPDATED]),
        (ORDER_CANCELLED, DISPLAY_LABELS[ORDER_CANCELLED]),
        (ORDER_FULFILLED, DISPLAY_LABELS[ORDER_FULFILLED]),
        (DRAFT_ORDER_CREATED, DISPLAY_LABELS[DRAFT_ORDER_CREATED]),
        (DRAFT_ORDER_UPDATED, DISPLAY_LABELS[DRAFT_ORDER_UPDATED]),
        (DRAFT_ORDER_DELETED, DISPLAY_LABELS[DRAFT_ORDER_DELETED]),
        (SALE_CREATED, DISPLAY_LABELS[SALE_CREATED]),
        (SALE_UPDATED, DISPLAY_LABELS[SALE_UPDATED]),
        (SALE_DELETED, DISPLAY_LABELS[SALE_DELETED]),
        (INVOICE_REQUESTED, DISPLAY_LABELS[INVOICE_REQUESTED]),
        (INVOICE_DELETED, DISPLAY_LABELS[INVOICE_DELETED]),
        (INVOICE_SENT, DISPLAY_LABELS[INVOICE_SENT]),
        (CUSTOMER_CREATED, DISPLAY_LABELS[CUSTOMER_CREATED]),
        (CUSTOMER_UPDATED, DISPLAY_LABELS[CUSTOMER_UPDATED]),
        (COLLECTION_CREATED, DISPLAY_LABELS[COLLECTION_CREATED]),
        (COLLECTION_UPDATED, DISPLAY_LABELS[COLLECTION_UPDATED]),
        (COLLECTION_DELETED, DISPLAY_LABELS[COLLECTION_DELETED]),
        (PRODUCT_CREATED, DISPLAY_LABELS[PRODUCT_CREATED]),
        (PRODUCT_UPDATED, DISPLAY_LABELS[PRODUCT_UPDATED]),
        (PRODUCT_DELETED, DISPLAY_LABELS[PRODUCT_DELETED]),
        (PRODUCT_VARIANT_CREATED, DISPLAY_LABELS[PRODUCT_VARIANT_CREATED]),
        (PRODUCT_VARIANT_UPDATED, DISPLAY_LABELS[PRODUCT_VARIANT_UPDATED]),
        (PRODUCT_VARIANT_DELETED, DISPLAY_LABELS[PRODUCT_VARIANT_DELETED]),
        (PRODUCT_VARIANT_OUT_OF_STOCK, DISPLAY_LABELS[PRODUCT_VARIANT_OUT_OF_STOCK]),
        (PRODUCT_VARIANT_BACK_IN_STOCK, DISPLAY_LABELS[PRODUCT_VARIANT_BACK_IN_STOCK]),
        (CHECKOUT_CREATED, DISPLAY_LABELS[CHECKOUT_CREATED]),
        (CHECKOUT_UPDATED, DISPLAY_LABELS[CHECKOUT_UPDATED]),
        (FULFILLMENT_CREATED, DISPLAY_LABELS[FULFILLMENT_CREATED]),
        (FULFILLMENT_CANCELED, DISPLAY_LABELS[FULFILLMENT_CANCELED]),
        (NOTIFY_USER, DISPLAY_LABELS[NOTIFY_USER]),
        (PAGE_CREATED, DISPLAY_LABELS[PAGE_CREATED]),
        (PAGE_UPDATED, DISPLAY_LABELS[PAGE_UPDATED]),
        (PAGE_DELETED, DISPLAY_LABELS[PAGE_DELETED]),
        (TRANSLATION_CREATED, DISPLAY_LABELS[TRANSLATION_CREATED]),
        (TRANSLATION_UPDATED, DISPLAY_LABELS[TRANSLATION_UPDATED]),
    ]

    ALL = [event[0] for event in CHOICES]

    PERMISSIONS = {
        CATEGORY_CREATED: ProductPermissions.MANAGE_PRODUCTS,
        CATEGORY_UPDATED: ProductPermissions.MANAGE_PRODUCTS,
        CATEGORY_DELETED: ProductPermissions.MANAGE_PRODUCTS,
        ORDER_CREATED: OrderPermissions.MANAGE_ORDERS,
        ORDER_CONFIRMED: OrderPermissions.MANAGE_ORDERS,
        ORDER_FULLY_PAID: OrderPermissions.MANAGE_ORDERS,
        ORDER_UPDATED: OrderPermissions.MANAGE_ORDERS,
        ORDER_CANCELLED: OrderPermissions.MANAGE_ORDERS,
        ORDER_FULFILLED: OrderPermissions.MANAGE_ORDERS,
        DRAFT_ORDER_CREATED: OrderPermissions.MANAGE_ORDERS,
        DRAFT_ORDER_DELETED: OrderPermissions.MANAGE_ORDERS,
        DRAFT_ORDER_UPDATED: OrderPermissions.MANAGE_ORDERS,
        SALE_CREATED: DiscountPermissions.MANAGE_DISCOUNTS,
        SALE_UPDATED: DiscountPermissions.MANAGE_DISCOUNTS,
        SALE_DELETED: DiscountPermissions.MANAGE_DISCOUNTS,
        INVOICE_REQUESTED: OrderPermissions.MANAGE_ORDERS,
        INVOICE_DELETED: OrderPermissions.MANAGE_ORDERS,
        INVOICE_SENT: OrderPermissions.MANAGE_ORDERS,
        CUSTOMER_CREATED: AccountPermissions.MANAGE_USERS,
        CUSTOMER_UPDATED: AccountPermissions.MANAGE_USERS,
        COLLECTION_CREATED: ProductPermissions.MANAGE_PRODUCTS,
        COLLECTION_UPDATED: ProductPermissions.MANAGE_PRODUCTS,
        COLLECTION_DELETED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_CREATED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_UPDATED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_DELETED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_VARIANT_CREATED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_VARIANT_UPDATED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_VARIANT_DELETED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_VARIANT_BACK_IN_STOCK: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_VARIANT_OUT_OF_STOCK: ProductPermissions.MANAGE_PRODUCTS,
        CHECKOUT_CREATED: CheckoutPermissions.MANAGE_CHECKOUTS,
        CHECKOUT_UPDATED: CheckoutPermissions.MANAGE_CHECKOUTS,
        FULFILLMENT_CREATED: OrderPermissions.MANAGE_ORDERS,
        FULFILLMENT_CANCELED: OrderPermissions.MANAGE_ORDERS,
        NOTIFY_USER: AccountPermissions.MANAGE_USERS,
        PAGE_CREATED: PagePermissions.MANAGE_PAGES,
        PAGE_UPDATED: PagePermissions.MANAGE_PAGES,
        PAGE_DELETED: PagePermissions.MANAGE_PAGES,
        TRANSLATION_CREATED: SitePermissions.MANAGE_TRANSLATIONS,
        TRANSLATION_UPDATED: SitePermissions.MANAGE_TRANSLATIONS,
    }


class WebhookEventSyncType:
    PAYMENT_LIST_GATEWAYS = "payment_list_gateways"
    PAYMENT_AUTHORIZE = "payment_authorize"
    PAYMENT_CAPTURE = "payment_capture"
    PAYMENT_REFUND = "payment_refund"
    PAYMENT_VOID = "payment_void"
    PAYMENT_CONFIRM = "payment_confirm"
    PAYMENT_PROCESS = "payment_process"

    SHIPPING_LIST_METHODS_FOR_CHECKOUT = "shipping_list_methods_for_checkout"
    CHECKOUT_FILTER_SHIPPING_METHODS = "checkout_filter_shipping_methods"
    ORDER_FILTER_SHIPPING_METHODS = "order_filter_shipping_methods"

    DISPLAY_LABELS = {
        PAYMENT_AUTHORIZE: "Authorize payment",
        PAYMENT_CAPTURE: "Capture payment",
        PAYMENT_CONFIRM: "Confirm payment",
        PAYMENT_LIST_GATEWAYS: "List payment gateways",
        PAYMENT_PROCESS: "Process payment",
        PAYMENT_REFUND: "Refund payment",
        PAYMENT_VOID: "Void payment",
        SHIPPING_LIST_METHODS_FOR_CHECKOUT: "Shipping list methods for checkout",
        ORDER_FILTER_SHIPPING_METHODS: "Filter order shipping methods",
        CHECKOUT_FILTER_SHIPPING_METHODS: "Filter checkout shipping methods",
    }

    CHOICES = [
        (PAYMENT_AUTHORIZE, DISPLAY_LABELS[PAYMENT_AUTHORIZE]),
        (PAYMENT_CAPTURE, DISPLAY_LABELS[PAYMENT_CAPTURE]),
        (PAYMENT_CONFIRM, DISPLAY_LABELS[PAYMENT_CONFIRM]),
        (PAYMENT_LIST_GATEWAYS, DISPLAY_LABELS[PAYMENT_LIST_GATEWAYS]),
        (PAYMENT_PROCESS, DISPLAY_LABELS[PAYMENT_PROCESS]),
        (PAYMENT_REFUND, DISPLAY_LABELS[PAYMENT_REFUND]),
        (PAYMENT_VOID, DISPLAY_LABELS[PAYMENT_VOID]),
        (
            SHIPPING_LIST_METHODS_FOR_CHECKOUT,
            DISPLAY_LABELS[SHIPPING_LIST_METHODS_FOR_CHECKOUT],
        ),
        (ORDER_FILTER_SHIPPING_METHODS, DISPLAY_LABELS[ORDER_FILTER_SHIPPING_METHODS]),
        (
            CHECKOUT_FILTER_SHIPPING_METHODS,
            DISPLAY_LABELS[CHECKOUT_FILTER_SHIPPING_METHODS],
        ),
    ]

    ALL = [event[0] for event in CHOICES]

    PAYMENT_EVENTS = [
        PAYMENT_AUTHORIZE,
        PAYMENT_CAPTURE,
        PAYMENT_CONFIRM,
        PAYMENT_LIST_GATEWAYS,
        PAYMENT_PROCESS,
        PAYMENT_REFUND,
        PAYMENT_VOID,
    ]

    PERMISSIONS = {
        PAYMENT_AUTHORIZE: PaymentPermissions.HANDLE_PAYMENTS,
        PAYMENT_CAPTURE: PaymentPermissions.HANDLE_PAYMENTS,
        PAYMENT_CONFIRM: PaymentPermissions.HANDLE_PAYMENTS,
        PAYMENT_LIST_GATEWAYS: PaymentPermissions.HANDLE_PAYMENTS,
        PAYMENT_PROCESS: PaymentPermissions.HANDLE_PAYMENTS,
        PAYMENT_REFUND: PaymentPermissions.HANDLE_PAYMENTS,
        PAYMENT_VOID: PaymentPermissions.HANDLE_PAYMENTS,
        SHIPPING_LIST_METHODS_FOR_CHECKOUT: ShippingPermissions.MANAGE_SHIPPING,
        ORDER_FILTER_SHIPPING_METHODS: OrderPermissions.MANAGE_ORDERS,
        CHECKOUT_FILTER_SHIPPING_METHODS: CheckoutPermissions.MANAGE_CHECKOUTS,
    }


SUBSCRIBABLE_EVENTS = [
    WebhookEventAsyncType.CATEGORY_CREATED,
    WebhookEventAsyncType.CATEGORY_UPDATED,
    WebhookEventAsyncType.CATEGORY_DELETED,
    WebhookEventAsyncType.ORDER_CREATED,
    WebhookEventAsyncType.ORDER_UPDATED,
    WebhookEventAsyncType.ORDER_CONFIRMED,
    WebhookEventAsyncType.ORDER_FULLY_PAID,
    WebhookEventAsyncType.ORDER_FULFILLED,
    WebhookEventAsyncType.ORDER_CANCELLED,
    WebhookEventAsyncType.DRAFT_ORDER_CREATED,
    WebhookEventAsyncType.DRAFT_ORDER_UPDATED,
    WebhookEventAsyncType.DRAFT_ORDER_DELETED,
    WebhookEventAsyncType.PRODUCT_CREATED,
    WebhookEventAsyncType.PRODUCT_UPDATED,
    WebhookEventAsyncType.PRODUCT_DELETED,
    WebhookEventAsyncType.PRODUCT_VARIANT_DELETED,
    WebhookEventAsyncType.PRODUCT_VARIANT_CREATED,
    WebhookEventAsyncType.PRODUCT_VARIANT_UPDATED,
    WebhookEventAsyncType.PRODUCT_VARIANT_BACK_IN_STOCK,
    WebhookEventAsyncType.PRODUCT_VARIANT_OUT_OF_STOCK,
    WebhookEventAsyncType.SALE_CREATED,
    WebhookEventAsyncType.SALE_UPDATED,
    WebhookEventAsyncType.SALE_DELETED,
    WebhookEventAsyncType.INVOICE_REQUESTED,
    WebhookEventAsyncType.INVOICE_DELETED,
    WebhookEventAsyncType.INVOICE_SENT,
    WebhookEventAsyncType.FULFILLMENT_CREATED,
    WebhookEventAsyncType.FULFILLMENT_CANCELED,
    WebhookEventAsyncType.CUSTOMER_CREATED,
    WebhookEventAsyncType.CUSTOMER_UPDATED,
    WebhookEventAsyncType.COLLECTION_CREATED,
    WebhookEventAsyncType.COLLECTION_UPDATED,
    WebhookEventAsyncType.COLLECTION_DELETED,
    WebhookEventAsyncType.CHECKOUT_CREATED,
    WebhookEventAsyncType.CHECKOUT_UPDATED,
    WebhookEventAsyncType.PAGE_CREATED,
    WebhookEventAsyncType.PAGE_UPDATED,
    WebhookEventAsyncType.PAGE_DELETED,
    WebhookEventAsyncType.TRANSLATION_CREATED,
    WebhookEventAsyncType.TRANSLATION_UPDATED,
]
