from unittest.mock import patch

import graphene
import pytest

ATTRIBUTE_VALUE_DELETE_MUTATION = """
    mutation updateChoice($id: ID!) {
        attributeValueDelete(id: $id) {
            attributeValue {
                name
                slug
            }
        }
    }
"""


@patch("saleor.attribute.signals.delete_from_storage.delay")
def test_delete_attribute_value(
    delete_from_storage_mock,
    staff_api_client,
    color_attribute,
    pink_attribute_value,
    permission_manage_product_types_and_attributes,
):
    # given
    value = color_attribute.values.get(name="Red")
    query = ATTRIBUTE_VALUE_DELETE_MUTATION
    node_id = graphene.Node.to_global_id("AttributeValue", value.id)
    variables = {"id": node_id}

    # when
    staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_product_types_and_attributes]
    )

    # then
    with pytest.raises(value._meta.model.DoesNotExist):
        value.refresh_from_db()
    delete_from_storage_mock.assert_not_called()


@patch("saleor.attribute.signals.delete_from_storage.delay")
def test_delete_file_attribute_value(
    delete_from_storage_mock,
    staff_api_client,
    file_attribute,
    permission_manage_product_types_and_attributes,
):
    # given
    value = file_attribute.values.first()
    file_url = value.file_url
    query = ATTRIBUTE_VALUE_DELETE_MUTATION
    node_id = graphene.Node.to_global_id("AttributeValue", value.id)
    variables = {"id": node_id}

    # when
    staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_product_types_and_attributes]
    )

    # then
    with pytest.raises(value._meta.model.DoesNotExist):
        value.refresh_from_db()
    delete_from_storage_mock.assert_called_once_with(file_url)
