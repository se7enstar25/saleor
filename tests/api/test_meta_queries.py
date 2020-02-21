import graphene

from tests.api.utils import assert_no_permission, get_graphql_content

PRIVATE_KEY = "private_key"
PRIVATE_VALUE = "private_vale"

PUBLIC_KEY = "key"
PUBLIC_VALUE = "value"


QUERY_SELF_PUBLIC_META = """
    {
        me{
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_me_as_customer(user_api_client):
    # given
    me = user_api_client.user
    me.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    me.save(update_fields=["meta"])

    # when
    response = user_api_client.post_graphql(QUERY_SELF_PUBLIC_META)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["me"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_me_as_staff(staff_api_client):
    # given
    me = staff_api_client.user
    me.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    me.save(update_fields=["meta"])

    # when
    response = staff_api_client.post_graphql(QUERY_SELF_PUBLIC_META)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["me"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_USER_PUBLIC_META = """
    query userMeta($id: ID!){
        user(id: $id){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_customer_as_staff(
    staff_api_client, permission_manage_users, customer_user
):
    # given
    customer_user.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    customer_user.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("User", customer_user.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_USER_PUBLIC_META, variables, [permission_manage_users]
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["user"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_customer_as_service_account(
    service_account_api_client, permission_manage_users, customer_user
):
    # given
    customer_user.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    customer_user.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("User", customer_user.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_USER_PUBLIC_META, variables, [permission_manage_users]
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["user"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_staff_as_other_staff(
    staff_api_client, permission_manage_staff, admin_user
):
    # given
    admin_user.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    admin_user.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("User", admin_user.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_USER_PUBLIC_META, variables, [permission_manage_staff]
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["user"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_staff_as_service_account(
    service_account_api_client, permission_manage_staff, admin_user
):
    # given
    admin_user.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    admin_user.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("User", admin_user.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_USER_PUBLIC_META, variables, [permission_manage_staff]
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["user"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_CHECKOUT_PUBLIC_META = """
    query checkoutMeta($token: UUID!){
        checkout(token: $token){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_checkout_as_anonymous_user(api_client, checkout):
    # given
    checkout.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    checkout.save(update_fields=["meta"])
    variables = {"token": checkout.pk}

    # when
    response = api_client.post_graphql(QUERY_CHECKOUT_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["checkout"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_other_customer_checkout_as_anonymous_user(
    api_client, checkout, customer_user
):
    # given
    checkout.user = customer_user
    checkout.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    checkout.save(update_fields=["user", "meta"])
    variables = {"token": checkout.pk}

    # when
    response = api_client.post_graphql(QUERY_CHECKOUT_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    assert not content["data"]["checkout"]


def test_query_public_meta_for_checkout_as_customer(user_api_client, checkout):
    # given
    checkout.user = user_api_client.user
    checkout.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    checkout.save(update_fields=["user", "meta"])
    variables = {"token": checkout.pk}

    # when
    response = user_api_client.post_graphql(QUERY_CHECKOUT_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["checkout"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_checkout_as_staff(
    staff_api_client, checkout, customer_user, permission_manage_checkouts
):
    # given
    checkout.user = customer_user
    checkout.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    checkout.save(update_fields=["user", "meta"])
    variables = {"token": checkout.pk}

    # when
    response = staff_api_client.post_graphql(
        QUERY_CHECKOUT_PUBLIC_META,
        variables,
        [permission_manage_checkouts],
        check_no_permissions=False,  # Remove after fix #5245
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["checkout"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_checkout_as_service_account(
    service_account_api_client, checkout, customer_user, permission_manage_checkouts
):
    # given
    checkout.user = customer_user
    checkout.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    checkout.save(update_fields=["user", "meta"])
    variables = {"token": checkout.pk}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_CHECKOUT_PUBLIC_META,
        variables,
        [permission_manage_checkouts],
        check_no_permissions=False,  # Remove after fix #5245
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["checkout"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_ORDER_BY_TOKEN_PUBLIC_META = """
    query orderMeta($token: UUID!){
        orderByToken(token: $token){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_order_by_token_as_anonymous_user(api_client, order):
    # given
    order.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    order.save(update_fields=["meta"])
    variables = {"token": order.token}

    # when
    response = api_client.post_graphql(QUERY_ORDER_BY_TOKEN_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["orderByToken"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_order_by_token_as_customer(user_api_client, order):
    # given
    order.user = user_api_client.user
    order.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    order.save(update_fields=["user", "meta"])
    variables = {"token": order.token}

    # when
    response = user_api_client.post_graphql(QUERY_ORDER_BY_TOKEN_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["orderByToken"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_order_by_token_as_staff(
    staff_api_client, order, customer_user, permission_manage_orders
):
    # given
    order.user = customer_user
    order.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    order.save(update_fields=["user", "meta"])
    variables = {"token": order.token}

    # when
    response = staff_api_client.post_graphql(
        QUERY_ORDER_BY_TOKEN_PUBLIC_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["orderByToken"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_order_by_token_as_service_account(
    service_account_api_client, order, customer_user, permission_manage_orders
):
    # given
    order.user = customer_user
    order.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    order.save(update_fields=["user", "meta"])
    variables = {"token": order.token}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_ORDER_BY_TOKEN_PUBLIC_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["orderByToken"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_ORDER_PUBLIC_META = """
    query orderMeta($id: ID!){
        order(id: $id){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_order_as_anonymous_user(api_client, order):
    # given
    variables = {"id": graphene.Node.to_global_id("Order", order.pk)}

    # when
    response = api_client.post_graphql(QUERY_ORDER_PUBLIC_META, variables)

    # then
    assert_no_permission(response)


def test_query_public_meta_for_order_as_customer(user_api_client, order):
    # given
    order.user = user_api_client.user
    order.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    order.save(update_fields=["user", "meta"])
    variables = {"id": graphene.Node.to_global_id("Order", order.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_ORDER_PUBLIC_META, variables)

    # then
    assert_no_permission(response)


def test_query_public_meta_for_order_as_staff(
    staff_api_client, order, customer_user, permission_manage_orders
):
    # given
    order.user = customer_user
    order.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    order.save(update_fields=["user", "meta"])
    variables = {"id": graphene.Node.to_global_id("Order", order.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_ORDER_PUBLIC_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["order"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_order_as_service_account(
    service_account_api_client, order, customer_user, permission_manage_orders
):
    # given
    order.user = customer_user
    order.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    order.save(update_fields=["user", "meta"])
    variables = {"id": graphene.Node.to_global_id("Order", order.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_ORDER_PUBLIC_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["order"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_DRAFT_ORDER_PUBLIC_META = """
    query draftOrderMeta($id: ID!){
        order(id: $id){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_draft_order_as_anonymous_user(api_client, draft_order):
    # given
    variables = {"id": graphene.Node.to_global_id("Order", draft_order.pk)}

    # when
    response = api_client.post_graphql(QUERY_DRAFT_ORDER_PUBLIC_META, variables)

    # then
    assert_no_permission(response)


def test_query_public_meta_for_draft_order_as_customer(user_api_client, draft_order):
    # given
    draft_order.user = user_api_client.user
    draft_order.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    draft_order.save(update_fields=["user", "meta"])
    variables = {"id": graphene.Node.to_global_id("Order", draft_order.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_DRAFT_ORDER_PUBLIC_META, variables)

    # then
    assert_no_permission(response)


def test_query_public_meta_for_draft_order_as_staff(
    staff_api_client, draft_order, customer_user, permission_manage_orders
):
    # given
    draft_order.user = customer_user
    draft_order.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    draft_order.save(update_fields=["user", "meta"])
    variables = {"id": graphene.Node.to_global_id("Order", draft_order.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_DRAFT_ORDER_PUBLIC_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["order"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_draft_order_as_service_account(
    service_account_api_client, draft_order, customer_user, permission_manage_orders
):
    # given
    draft_order.user = customer_user
    draft_order.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    draft_order.save(update_fields=["user", "meta"])
    variables = {"id": graphene.Node.to_global_id("Order", draft_order.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_ORDER_PUBLIC_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["order"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_FULFILLMENT_PUBLIC_META = """
    query fulfillmentMeta($token: UUID!){
        orderByToken(token: $token){
            fulfillments{
                metadata{
                    key
                    value
                }
          }
        }
    }
"""


def test_query_public_meta_for_fulfillment_as_anonymous_user(
    api_client, fulfilled_order
):
    # given
    fulfillment = fulfilled_order.fulfillments.first()
    fulfillment.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    fulfillment.save(update_fields=["meta"])
    variables = {"token": fulfilled_order.token}

    # when
    response = api_client.post_graphql(QUERY_FULFILLMENT_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["orderByToken"]["fulfillments"][0]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_fulfillment_as_customer(
    user_api_client, fulfilled_order
):
    # given
    fulfillment = fulfilled_order.fulfillments.first()
    fulfillment.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    fulfillment.save(update_fields=["meta"])
    fulfilled_order.user = user_api_client.user
    fulfilled_order.save(update_fields=["user"])
    variables = {"token": fulfilled_order.token}

    # when
    response = user_api_client.post_graphql(QUERY_FULFILLMENT_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["orderByToken"]["fulfillments"][0]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_fulfillment_as_staff(
    staff_api_client, fulfilled_order, customer_user, permission_manage_orders
):
    # given
    fulfillment = fulfilled_order.fulfillments.first()
    fulfillment.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    fulfillment.save(update_fields=["meta"])
    fulfilled_order.user = customer_user
    fulfilled_order.save(update_fields=["user"])
    variables = {"token": fulfilled_order.token}

    # when
    response = staff_api_client.post_graphql(
        QUERY_FULFILLMENT_PUBLIC_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["orderByToken"]["fulfillments"][0]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_fulfillment_as_service_account(
    service_account_api_client, fulfilled_order, customer_user, permission_manage_orders
):
    # given
    fulfillment = fulfilled_order.fulfillments.first()
    fulfillment.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    fulfillment.save(update_fields=["meta"])
    fulfilled_order.user = customer_user
    fulfilled_order.save(update_fields=["user"])
    variables = {"token": fulfilled_order.token}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_FULFILLMENT_PUBLIC_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["orderByToken"]["fulfillments"][0]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_ATTRIBUTE_PUBLIC_META = """
    query attributeMeta($id: ID!){
        attribute(id: $id){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_attribute_as_anonymous_user(api_client, color_attribute):
    # given
    color_attribute.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    color_attribute.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Attribute", color_attribute.pk)}

    # when
    response = api_client.post_graphql(QUERY_ATTRIBUTE_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["attribute"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_attribute_as_customer(user_api_client, color_attribute):
    # given
    color_attribute.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    color_attribute.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Attribute", color_attribute.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_ATTRIBUTE_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["attribute"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_attribute_as_staff(
    staff_api_client, color_attribute, permission_manage_products
):
    # given
    color_attribute.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    color_attribute.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Attribute", color_attribute.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_ATTRIBUTE_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["attribute"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_attribute_as_service_account(
    service_account_api_client, color_attribute, permission_manage_products
):
    # given
    color_attribute.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    color_attribute.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Attribute", color_attribute.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_ATTRIBUTE_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["attribute"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_CATEGORY_PUBLIC_META = """
    query categoryMeta($id: ID!){
        category(id: $id){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_category_as_anonymous_user(api_client, category):
    # given
    category.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    category.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Category", category.pk)}

    # when
    response = api_client.post_graphql(QUERY_CATEGORY_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["category"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_category_as_customer(user_api_client, category):
    # given
    category.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    category.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Category", category.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_CATEGORY_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["category"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_category_as_staff(
    staff_api_client, category, permission_manage_products
):
    # given
    category.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    category.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Category", category.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_CATEGORY_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["category"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_category_as_service_account(
    service_account_api_client, category, permission_manage_products
):
    # given
    category.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    category.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Category", category.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_CATEGORY_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["category"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_COLLECTION_PUBLIC_META = """
    query collectionMeta($id: ID!){
        collection(id: $id){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_collection_as_anonymous_user(api_client, collection):
    # given
    collection.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    collection.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Collection", collection.pk)}

    # when
    response = api_client.post_graphql(QUERY_COLLECTION_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["collection"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_collection_as_customer(user_api_client, collection):
    # given
    collection.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    collection.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Collection", collection.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_COLLECTION_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["collection"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_collection_as_staff(
    staff_api_client, collection, permission_manage_products
):
    # given
    collection.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    collection.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Collection", collection.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_COLLECTION_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["collection"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_collection_as_service_account(
    service_account_api_client, collection, permission_manage_products
):
    # given
    collection.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    collection.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Collection", collection.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_COLLECTION_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["collection"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_DIGITAL_CONTENT_PUBLIC_META = """
    query digitalContentMeta($id: ID!){
        digitalContent(id: $id){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_digital_content_as_anonymous_user(
    api_client, digital_content
):
    # given
    variables = {"id": graphene.Node.to_global_id("DigitalContent", digital_content.pk)}

    # when
    response = api_client.post_graphql(QUERY_DIGITAL_CONTENT_PUBLIC_META, variables)

    # then
    assert_no_permission(response)


def test_query_public_meta_for_digital_content_as_customer(
    user_api_client, digital_content
):
    # given
    digital_content.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    digital_content.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("DigitalContent", digital_content.pk)}

    # when
    response = user_api_client.post_graphql(
        QUERY_DIGITAL_CONTENT_PUBLIC_META, variables
    )

    # then
    assert_no_permission(response)


def test_query_public_meta_for_digital_content_as_staff(
    staff_api_client, digital_content, permission_manage_products
):
    # given
    digital_content.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    digital_content.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("DigitalContent", digital_content.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_DIGITAL_CONTENT_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["digitalContent"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_digital_content_as_service_account(
    service_account_api_client, digital_content, permission_manage_products
):
    # given
    digital_content.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    digital_content.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("DigitalContent", digital_content.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_DIGITAL_CONTENT_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["digitalContent"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_PRODUCT_PUBLIC_META = """
    query productsMeta($id: ID!){
        product(id: $id){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_product_as_anonymous_user(api_client, product):
    # given
    product.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    product.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Product", product.pk)}

    # when
    response = api_client.post_graphql(QUERY_PRODUCT_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["product"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_product_as_customer(user_api_client, product):
    # given
    product.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    product.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Product", product.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_PRODUCT_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["product"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_product_as_staff(
    staff_api_client, product, permission_manage_products
):
    # given
    product.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    product.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Product", product.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_PRODUCT_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["product"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_product_as_service_account(
    service_account_api_client, product, permission_manage_products
):
    # given
    product.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    product.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("Product", product.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_PRODUCT_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["product"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_PRODUCT_TYPE_PUBLIC_META = """
    query productTypeMeta($id: ID!){
        productType(id: $id){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_product_type_as_anonymous_user(api_client, product_type):
    # given
    product_type.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    product_type.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("ProductType", product_type.pk)}

    # when
    response = api_client.post_graphql(QUERY_PRODUCT_TYPE_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["productType"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_product_type_as_customer(user_api_client, product_type):
    # given
    product_type.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    product_type.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("ProductType", product_type.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_PRODUCT_TYPE_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["productType"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_product_type_as_staff(
    staff_api_client, product_type, permission_manage_products
):
    # given
    product_type.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    product_type.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("ProductType", product_type.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_PRODUCT_TYPE_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["productType"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_product_type_as_service_account(
    service_account_api_client, product_type, permission_manage_products
):
    # given
    product_type.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    product_type.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("ProductType", product_type.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_PRODUCT_TYPE_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["productType"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_PRODUCT_VARIANT_PUBLIC_META = """
    query productVariantMeta($id: ID!){
        productVariant(id: $id){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_product_variant_as_anonymous_user(api_client, variant):
    # given
    variant.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    variant.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("ProductVariant", variant.pk)}

    # when
    response = api_client.post_graphql(QUERY_PRODUCT_VARIANT_PUBLIC_META, variables)
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["productVariant"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_product_variant_as_customer(user_api_client, variant):
    # given
    variant.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    variant.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("ProductVariant", variant.pk)}

    # when
    response = user_api_client.post_graphql(
        QUERY_PRODUCT_VARIANT_PUBLIC_META, variables
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["productVariant"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_product_variant_as_staff(
    staff_api_client, variant, permission_manage_products
):
    # given
    variant.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    variant.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("ProductVariant", variant.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_PRODUCT_VARIANT_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["productVariant"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_product_variant_as_service_account(
    service_account_api_client, variant, permission_manage_products
):
    # given
    variant.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    variant.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("ProductVariant", variant.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_PRODUCT_VARIANT_PUBLIC_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["productVariant"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_SERVICE_ACCOUNT_PUBLIC_META = """
    query serviceAccountMeta($id: ID!){
        serviceAccount(id: $id){
            metadata{
                key
                value
            }
        }
    }
"""


def test_query_public_meta_for_service_account_as_anonymous_user(
    api_client, service_account
):
    # given
    variables = {"id": graphene.Node.to_global_id("ServiceAccount", service_account.pk)}

    # when
    response = api_client.post_graphql(QUERY_SERVICE_ACCOUNT_PUBLIC_META, variables)

    # then
    assert_no_permission(response)


def test_query_public_meta_for_service_account_as_customer(
    user_api_client, service_account
):
    # given
    variables = {"id": graphene.Node.to_global_id("ServiceAccount", service_account.pk)}

    # when
    response = user_api_client.post_graphql(
        QUERY_SERVICE_ACCOUNT_PUBLIC_META, variables
    )

    # then
    assert_no_permission(response)


def test_query_public_meta_for_service_account_as_staff(
    staff_api_client, service_account, permission_manage_service_accounts
):
    # given
    service_account.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    service_account.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("ServiceAccount", service_account.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_SERVICE_ACCOUNT_PUBLIC_META,
        variables,
        [permission_manage_service_accounts],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["serviceAccount"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


def test_query_public_meta_for_service_account_as_service_account(
    service_account_api_client, service_account, permission_manage_service_accounts
):
    # given
    service_account.store_value_in_metadata({PUBLIC_KEY: PUBLIC_VALUE})
    service_account.save(update_fields=["meta"])
    variables = {"id": graphene.Node.to_global_id("ServiceAccount", service_account.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_SERVICE_ACCOUNT_PUBLIC_META,
        variables,
        [permission_manage_service_accounts],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["serviceAccount"]["metadata"][0]
    assert metadata["key"] == PUBLIC_KEY
    assert metadata["value"] == PUBLIC_VALUE


QUERY_SELF_PRIVATE_META = """
    {
        me{
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_me_as_customer(user_api_client):
    # given

    # when
    response = user_api_client.post_graphql(QUERY_SELF_PRIVATE_META)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_me_as_staff_with_manage_customer(
    staff_api_client, permission_manage_users
):
    # given

    # when
    response = staff_api_client.post_graphql(
        QUERY_SELF_PRIVATE_META, None, [permission_manage_users]
    )

    # then
    assert_no_permission(response)


def test_query_private_meta_for_me_as_staff_with_manage_staff(
    staff_api_client, permission_manage_staff
):
    # given
    me = staff_api_client.user
    me.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    me.save(update_fields=["private_meta"])

    # when
    response = staff_api_client.post_graphql(
        QUERY_SELF_PRIVATE_META, None, [permission_manage_staff]
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["me"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_USER_PRIVATE_META = """
    query userMeta($id: ID!){
        user(id: $id){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_customer_as_staff(
    staff_api_client, permission_manage_users, customer_user
):
    # given
    customer_user.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    customer_user.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("User", customer_user.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_USER_PRIVATE_META, variables, [permission_manage_users]
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["user"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_customer_as_service_account(
    service_account_api_client, permission_manage_users, customer_user
):
    # given
    customer_user.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    customer_user.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("User", customer_user.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_USER_PRIVATE_META, variables, [permission_manage_users]
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["user"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_staff_as_other_staff(
    staff_api_client, permission_manage_staff, admin_user
):
    # given
    admin_user.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    admin_user.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("User", admin_user.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_USER_PRIVATE_META, variables, [permission_manage_staff]
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["user"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_staff_as_service_account(
    service_account_api_client, permission_manage_staff, admin_user
):
    # given
    admin_user.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    admin_user.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("User", admin_user.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_USER_PRIVATE_META, variables, [permission_manage_staff]
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["user"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_CHECKOUT_PRIVATE_META = """
    query checkoutMeta($token: UUID!){
        checkout(token: $token){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_checkout_as_anonymous_user(api_client, checkout):
    # given
    variables = {"token": checkout.pk}

    # when
    response = api_client.post_graphql(QUERY_CHECKOUT_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_other_customer_checkout_as_anonymous_user(
    api_client, checkout, customer_user
):
    # given
    checkout.user = customer_user
    checkout.save(update_fields=["user"])
    variables = {"token": checkout.pk}

    # when
    response = api_client.post_graphql(QUERY_CHECKOUT_PRIVATE_META, variables)
    content = get_graphql_content(response)

    # then
    assert not content["data"]["checkout"]


def test_query_private_meta_for_checkout_as_customer(user_api_client, checkout):
    # given
    checkout.user = user_api_client.user
    checkout.save(update_fields=["user"])
    variables = {"token": checkout.pk}

    # when
    response = user_api_client.post_graphql(QUERY_CHECKOUT_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_checkout_as_staff(
    staff_api_client, checkout, customer_user, permission_manage_checkouts
):
    # given
    checkout.user = customer_user
    checkout.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    checkout.save(update_fields=["user", "private_meta"])
    variables = {"token": checkout.pk}

    # when
    response = staff_api_client.post_graphql(
        QUERY_CHECKOUT_PRIVATE_META,
        variables,
        [permission_manage_checkouts],
        check_no_permissions=False,  # Remove after fix #5245
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["checkout"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_checkout_as_service_account(
    service_account_api_client, checkout, customer_user, permission_manage_checkouts
):
    # given
    checkout.user = customer_user
    checkout.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    checkout.save(update_fields=["user", "private_meta"])
    variables = {"token": checkout.pk}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_CHECKOUT_PRIVATE_META,
        variables,
        [permission_manage_checkouts],
        check_no_permissions=False,  # Remove after fix #5245
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["checkout"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_ORDER_BY_TOKEN_PRIVATE_META = """
    query orderMeta($token: UUID!){
        orderByToken(token: $token){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_order_by_token_as_anonymous_user(api_client, order):
    # given
    variables = {"token": order.token}

    # when
    response = api_client.post_graphql(QUERY_ORDER_BY_TOKEN_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_order_by_token_as_customer(user_api_client, order):
    # given
    order.user = user_api_client.user
    order.save(update_fields=["user"])
    variables = {"token": order.token}

    # when
    response = user_api_client.post_graphql(
        QUERY_ORDER_BY_TOKEN_PRIVATE_META, variables
    )

    # then
    assert_no_permission(response)


def test_query_private_meta_for_order_by_token_as_staff(
    staff_api_client, order, customer_user, permission_manage_orders
):
    # given
    order.user = customer_user
    order.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    order.save(update_fields=["user", "private_meta"])
    variables = {"token": order.token}

    # when
    response = staff_api_client.post_graphql(
        QUERY_ORDER_BY_TOKEN_PRIVATE_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["orderByToken"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_order_by_token_as_service_account(
    service_account_api_client, order, customer_user, permission_manage_orders
):
    # given
    order.user = customer_user
    order.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    order.save(update_fields=["user", "private_meta"])
    variables = {"token": order.token}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_ORDER_BY_TOKEN_PRIVATE_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["orderByToken"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_ORDER_PRIVATE_META = """
    query orderMeta($id: ID!){
        order(id: $id){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_order_as_anonymous_user(api_client, order):
    # given
    variables = {"id": graphene.Node.to_global_id("Order", order.pk)}

    # when
    response = api_client.post_graphql(QUERY_ORDER_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_order_as_customer(user_api_client, order):
    # given
    order.user = user_api_client.user
    order.save(update_fields=["user"])
    variables = {"id": graphene.Node.to_global_id("Order", order.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_ORDER_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_order_as_staff(
    staff_api_client, order, customer_user, permission_manage_orders
):
    # given
    order.user = customer_user
    order.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    order.save(update_fields=["user", "private_meta"])
    variables = {"id": graphene.Node.to_global_id("Order", order.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_ORDER_PRIVATE_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["order"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_order_as_service_account(
    service_account_api_client, order, customer_user, permission_manage_orders
):
    # given
    order.user = customer_user
    order.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    order.save(update_fields=["user", "private_meta"])
    variables = {"id": graphene.Node.to_global_id("Order", order.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_ORDER_PRIVATE_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["order"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_DRAFT_ORDER_PRIVATE_META = """
    query draftOrderMeta($id: ID!){
        order(id: $id){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_draft_order_as_anonymous_user(api_client, draft_order):
    # given
    variables = {"id": graphene.Node.to_global_id("Order", draft_order.pk)}

    # when
    response = api_client.post_graphql(QUERY_DRAFT_ORDER_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_draft_order_as_customer(user_api_client, draft_order):
    # given
    draft_order.user = user_api_client.user
    draft_order.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    draft_order.save(update_fields=["user", "private_meta"])
    variables = {"id": graphene.Node.to_global_id("Order", draft_order.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_DRAFT_ORDER_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_draft_order_as_staff(
    staff_api_client, draft_order, customer_user, permission_manage_orders
):
    # given
    draft_order.user = customer_user
    draft_order.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    draft_order.save(update_fields=["user", "private_meta"])
    variables = {"id": graphene.Node.to_global_id("Order", draft_order.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_DRAFT_ORDER_PRIVATE_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["order"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_draft_order_as_service_account(
    service_account_api_client, draft_order, customer_user, permission_manage_orders
):
    # given
    draft_order.user = customer_user
    draft_order.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    draft_order.save(update_fields=["user", "private_meta"])
    variables = {"id": graphene.Node.to_global_id("Order", draft_order.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_ORDER_PRIVATE_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["order"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_FULFILLMENT_PRIVATE_META = """
    query fulfillmentMeta($token: UUID!){
        orderByToken(token: $token){
            fulfillments{
                privateMetadata{
                    key
                    value
                }
          }
        }
    }
"""


def test_query_private_meta_for_fulfillment_as_anonymous_user(
    api_client, fulfilled_order
):
    # given
    variables = {"token": fulfilled_order.token}

    # when
    response = api_client.post_graphql(QUERY_FULFILLMENT_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_fulfillment_as_customer(
    user_api_client, fulfilled_order
):
    # given
    fulfilled_order.user = user_api_client.user
    fulfilled_order.save(update_fields=["user"])
    variables = {"token": fulfilled_order.token}

    # when
    response = user_api_client.post_graphql(QUERY_FULFILLMENT_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_fulfillment_as_staff(
    staff_api_client, fulfilled_order, customer_user, permission_manage_orders
):
    # given
    fulfillment = fulfilled_order.fulfillments.first()
    fulfillment.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    fulfillment.save(update_fields=["private_meta"])
    fulfilled_order.user = customer_user
    fulfilled_order.save(update_fields=["user"])
    variables = {"token": fulfilled_order.token}

    # when
    response = staff_api_client.post_graphql(
        QUERY_FULFILLMENT_PRIVATE_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["orderByToken"]["fulfillments"][0]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_fulfillment_as_service_account(
    service_account_api_client, fulfilled_order, customer_user, permission_manage_orders
):
    # given
    fulfillment = fulfilled_order.fulfillments.first()
    fulfillment.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    fulfillment.save(update_fields=["private_meta"])
    fulfilled_order.user = customer_user
    fulfilled_order.save(update_fields=["user"])
    variables = {"token": fulfilled_order.token}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_FULFILLMENT_PRIVATE_META,
        variables,
        [permission_manage_orders],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["orderByToken"]["fulfillments"][0]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_ATTRIBUTE_PRIVATE_META = """
    query attributeMeta($id: ID!){
        attribute(id: $id){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_attribute_as_anonymous_user(
    api_client, color_attribute
):
    # given
    variables = {"id": graphene.Node.to_global_id("Attribute", color_attribute.pk)}

    # when
    response = api_client.post_graphql(QUERY_ATTRIBUTE_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_attribute_as_customer(user_api_client, color_attribute):
    # given
    variables = {"id": graphene.Node.to_global_id("Attribute", color_attribute.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_ATTRIBUTE_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_attribute_as_staff(
    staff_api_client, color_attribute, permission_manage_products
):
    # given
    color_attribute.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    color_attribute.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("Attribute", color_attribute.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_ATTRIBUTE_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["attribute"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_attribute_as_service_account(
    service_account_api_client, color_attribute, permission_manage_products
):
    # given
    color_attribute.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    color_attribute.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("Attribute", color_attribute.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_ATTRIBUTE_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["attribute"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_CATEGORY_PRIVATE_META = """
    query categoryMeta($id: ID!){
        category(id: $id){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_category_as_anonymous_user(api_client, category):
    # given
    variables = {"id": graphene.Node.to_global_id("Category", category.pk)}

    # when
    response = api_client.post_graphql(QUERY_CATEGORY_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_category_as_customer(user_api_client, category):
    # given
    variables = {"id": graphene.Node.to_global_id("Category", category.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_CATEGORY_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_category_as_staff(
    staff_api_client, category, permission_manage_products
):
    # given
    category.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    category.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("Category", category.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_CATEGORY_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["category"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_category_as_service_account(
    service_account_api_client, category, permission_manage_products
):
    # given
    category.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    category.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("Category", category.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_CATEGORY_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["category"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_COLLECTION_PRIVATE_META = """
    query collectionMeta($id: ID!){
        collection(id: $id){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_collection_as_anonymous_user(api_client, collection):
    # given
    variables = {"id": graphene.Node.to_global_id("Collection", collection.pk)}

    # when
    response = api_client.post_graphql(QUERY_COLLECTION_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_collection_as_customer(user_api_client, collection):
    # given
    variables = {"id": graphene.Node.to_global_id("Collection", collection.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_COLLECTION_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_collection_as_staff(
    staff_api_client, collection, permission_manage_products
):
    # given
    collection.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    collection.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("Collection", collection.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_COLLECTION_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["collection"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_collection_as_service_account(
    service_account_api_client, collection, permission_manage_products
):
    # given
    collection.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    collection.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("Collection", collection.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_COLLECTION_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["collection"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_DIGITAL_CONTENT_PRIVATE_META = """
    query digitalContentMeta($id: ID!){
        digitalContent(id: $id){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_digital_content_as_anonymous_user(
    api_client, digital_content
):
    # given
    variables = {"id": graphene.Node.to_global_id("DigitalContent", digital_content.pk)}

    # when
    response = api_client.post_graphql(QUERY_DIGITAL_CONTENT_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_digital_content_as_customer(
    user_api_client, digital_content
):
    # given
    digital_content.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    digital_content.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("DigitalContent", digital_content.pk)}

    # when
    response = user_api_client.post_graphql(
        QUERY_DIGITAL_CONTENT_PRIVATE_META, variables
    )

    # then
    assert_no_permission(response)


def test_query_private_meta_for_digital_content_as_staff(
    staff_api_client, digital_content, permission_manage_products
):
    # given
    digital_content.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    digital_content.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("DigitalContent", digital_content.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_DIGITAL_CONTENT_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["digitalContent"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_digital_content_as_service_account(
    service_account_api_client, digital_content, permission_manage_products
):
    # given
    digital_content.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    digital_content.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("DigitalContent", digital_content.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_DIGITAL_CONTENT_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["digitalContent"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_PRODUCT_PRIVATE_META = """
    query productsMeta($id: ID!){
        product(id: $id){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_product_as_anonymous_user(api_client, product):
    # given
    variables = {"id": graphene.Node.to_global_id("Product", product.pk)}

    # when
    response = api_client.post_graphql(QUERY_PRODUCT_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_product_as_customer(user_api_client, product):
    # given
    variables = {"id": graphene.Node.to_global_id("Product", product.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_PRODUCT_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_product_as_staff(
    staff_api_client, product, permission_manage_products
):
    # given
    product.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    product.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("Product", product.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_PRODUCT_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["product"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_product_as_service_account(
    service_account_api_client, product, permission_manage_products
):
    # given
    product.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    product.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("Product", product.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_PRODUCT_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["product"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_PRODUCT_TYPE_PRIVATE_META = """
    query productTypeMeta($id: ID!){
        productType(id: $id){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_product_type_as_anonymous_user(
    api_client, product_type
):
    # given
    variables = {"id": graphene.Node.to_global_id("ProductType", product_type.pk)}

    # when
    response = api_client.post_graphql(QUERY_PRODUCT_TYPE_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_product_type_as_customer(user_api_client, product_type):
    # given
    variables = {"id": graphene.Node.to_global_id("ProductType", product_type.pk)}

    # when
    response = user_api_client.post_graphql(QUERY_PRODUCT_TYPE_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_product_type_as_staff(
    staff_api_client, product_type, permission_manage_products
):
    # given
    product_type.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    product_type.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("ProductType", product_type.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_PRODUCT_TYPE_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["productType"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_product_type_as_service_account(
    service_account_api_client, product_type, permission_manage_products
):
    # given
    product_type.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    product_type.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("ProductType", product_type.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_PRODUCT_TYPE_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["productType"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_PRODUCT_VARIANT_PRIVATE_META = """
    query productVariantMeta($id: ID!){
        productVariant(id: $id){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_product_variant_as_anonymous_user(api_client, variant):
    # given
    variant.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    variant.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("ProductVariant", variant.pk)}

    # when
    response = api_client.post_graphql(QUERY_PRODUCT_VARIANT_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_product_variant_as_customer(user_api_client, variant):
    # given
    variant.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    variant.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("ProductVariant", variant.pk)}

    # when
    response = user_api_client.post_graphql(
        QUERY_PRODUCT_VARIANT_PRIVATE_META, variables
    )

    # then
    assert_no_permission(response)


def test_query_private_meta_for_product_variant_as_staff(
    staff_api_client, variant, permission_manage_products
):
    # given
    variant.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    variant.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("ProductVariant", variant.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_PRODUCT_VARIANT_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["productVariant"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_product_variant_as_service_account(
    service_account_api_client, variant, permission_manage_products
):
    # given
    variant.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    variant.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("ProductVariant", variant.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_PRODUCT_VARIANT_PRIVATE_META,
        variables,
        [permission_manage_products],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["productVariant"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


QUERY_SERVICE_ACCOUNT_PRIVATE_META = """
    query serviceAccountMeta($id: ID!){
        serviceAccount(id: $id){
            privateMetadata{
                key
                value
            }
        }
    }
"""


def test_query_private_meta_for_service_account_as_anonymous_user(
    api_client, service_account
):
    # given
    variables = {"id": graphene.Node.to_global_id("ServiceAccount", service_account.pk)}

    # when
    response = api_client.post_graphql(QUERY_SERVICE_ACCOUNT_PRIVATE_META, variables)

    # then
    assert_no_permission(response)


def test_query_private_meta_for_service_account_as_customer(
    user_api_client, service_account
):
    # given
    variables = {"id": graphene.Node.to_global_id("ServiceAccount", service_account.pk)}

    # when
    response = user_api_client.post_graphql(
        QUERY_SERVICE_ACCOUNT_PRIVATE_META, variables
    )

    # then
    assert_no_permission(response)


def test_query_private_meta_for_service_account_as_staff(
    staff_api_client, service_account, permission_manage_service_accounts
):
    # given
    service_account.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    service_account.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("ServiceAccount", service_account.pk)}

    # when
    response = staff_api_client.post_graphql(
        QUERY_SERVICE_ACCOUNT_PRIVATE_META,
        variables,
        [permission_manage_service_accounts],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["serviceAccount"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE


def test_query_private_meta_for_service_account_as_service_account(
    service_account_api_client, service_account, permission_manage_service_accounts
):
    # given
    service_account.store_value_in_private_metadata({PRIVATE_KEY: PRIVATE_VALUE})
    service_account.save(update_fields=["private_meta"])
    variables = {"id": graphene.Node.to_global_id("ServiceAccount", service_account.pk)}

    # when
    response = service_account_api_client.post_graphql(
        QUERY_SERVICE_ACCOUNT_PRIVATE_META,
        variables,
        [permission_manage_service_accounts],
        check_no_permissions=False,
    )
    content = get_graphql_content(response)

    # then
    metadata = content["data"]["serviceAccount"]["privateMetadata"][0]
    assert metadata["key"] == PRIVATE_KEY
    assert metadata["value"] == PRIVATE_VALUE
