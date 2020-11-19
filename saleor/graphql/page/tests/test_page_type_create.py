import graphene

from ....page.error_codes import PageErrorCode
from ....page.models import PageType
from ...tests.utils import assert_no_permission, get_graphql_content

PAGE_TYPE_CREATE_MUTATION = """
    mutation PageTypeCreate($name: String, $slug: String, $addAttributes: [ID!]) {
        pageTypeCreate(input: {
            name: $name, slug: $slug, addAttributes: $addAttributes
        }) {
            pageType {
                id
                name
                slug
                attributes {
                    slug
                }
            }
            pageErrors {
                code
                field
                message
                attributes
            }
        }
    }
"""


def test_page_type_create_as_staff(
    staff_api_client,
    tag_page_attribute,
    author_page_attribute,
    permission_manage_page_types_and_attributes,
):
    # given
    staff_user = staff_api_client.user
    staff_user.user_permissions.add(permission_manage_page_types_and_attributes)

    name = "Test page type"
    slug = "test-page-type"

    attributes = [author_page_attribute, tag_page_attribute]

    variables = {
        "name": name,
        "slug": slug,
        "addAttributes": [
            graphene.Node.to_global_id("Attribute", attr.pk) for attr in attributes
        ],
    }

    # when
    response = staff_api_client.post_graphql(PAGE_TYPE_CREATE_MUTATION, variables)

    # then
    content = get_graphql_content(response)
    data = content["data"]["pageTypeCreate"]
    page_type_data = data["pageType"]
    errors = data["pageErrors"]

    assert not errors
    assert page_type_data["name"] == name
    assert page_type_data["slug"] == slug
    assert len(page_type_data["attributes"]) == 2
    assert {attr_data["slug"] for attr_data in page_type_data["attributes"]} == {
        attr.slug for attr in attributes
    }


def test_page_type_create_as_staff_no_perm(
    staff_api_client, tag_page_attribute, author_page_attribute
):
    # given
    name = "Test page type"
    slug = "test-page-type"

    attributes = [author_page_attribute, tag_page_attribute]

    variables = {
        "name": name,
        "slug": slug,
        "addAttributes": [
            graphene.Node.to_global_id("Attribute", attr.pk) for attr in attributes
        ],
    }

    # when
    response = staff_api_client.post_graphql(PAGE_TYPE_CREATE_MUTATION, variables)

    # then
    assert_no_permission(response)


def test_page_type_create_as_app(
    app_api_client, tag_page_attribute, permission_manage_page_types_and_attributes
):
    # given
    app = app_api_client.app
    app.permissions.add(permission_manage_page_types_and_attributes)

    name = "Test page type"
    slug = "test-page-type"

    variables = {
        "name": name,
        "slug": slug,
        "addAttributes": [
            graphene.Node.to_global_id("Attribute", tag_page_attribute.pk)
        ],
    }

    # when
    response = app_api_client.post_graphql(PAGE_TYPE_CREATE_MUTATION, variables)

    # then
    content = get_graphql_content(response)
    data = content["data"]["pageTypeCreate"]
    page_type_data = data["pageType"]
    errors = data["pageErrors"]

    assert not errors
    assert page_type_data["name"] == name
    assert page_type_data["slug"] == slug
    assert len(page_type_data["attributes"]) == 1
    assert page_type_data["attributes"][0]["slug"] == tag_page_attribute.slug


def test_page_type_create_as_app_no_perm(app_api_client, tag_page_attribute):
    # given
    name = "Test page type"
    slug = "test-page-type"

    variables = {
        "name": name,
        "slug": slug,
        "addAttributes": [
            graphene.Node.to_global_id("Attribute", tag_page_attribute.pk)
        ],
    }

    # when
    response = app_api_client.post_graphql(PAGE_TYPE_CREATE_MUTATION, variables)

    # then
    assert_no_permission(response)


def test_page_type_create_unique_slug_generated(
    staff_api_client,
    tag_page_attribute,
    author_page_attribute,
    permission_manage_page_types_and_attributes,
):
    """Ensure that unique slug is generated when slug is not given."""

    # given
    staff_user = staff_api_client.user
    staff_user.user_permissions.add(permission_manage_page_types_and_attributes)

    name_1 = "Test page type"
    name_2 = "test page type"
    slug = "test-page-type"

    page_type = PageType.objects.create(name=name_1, slug=slug)

    attributes = [author_page_attribute, tag_page_attribute]

    variables = {
        "name": name_2,
        "addAttributes": [
            graphene.Node.to_global_id("Attribute", attr.pk) for attr in attributes
        ],
    }

    # when
    response = staff_api_client.post_graphql(PAGE_TYPE_CREATE_MUTATION, variables)

    # then
    content = get_graphql_content(response)
    data = content["data"]["pageTypeCreate"]
    page_type_data = data["pageType"]
    errors = data["pageErrors"]

    assert not errors
    assert PageType.objects.count() == 2
    assert page_type_data["id"] != graphene.Node.to_global_id("PageType", page_type.pk)
    assert page_type_data["name"] == name_2
    assert page_type_data["slug"] == "test-page-type-2"
    assert len(page_type_data["attributes"]) == 2
    assert {attr_data["slug"] for attr_data in page_type_data["attributes"]} == {
        attr.slug for attr in attributes
    }


def test_page_type_create_duplicated_slug(
    staff_api_client,
    tag_page_attribute,
    author_page_attribute,
    permission_manage_page_types_and_attributes,
):
    """Ensure that unique errors is raised when page type with given slug exists."""

    # given
    staff_user = staff_api_client.user
    staff_user.user_permissions.add(permission_manage_page_types_and_attributes)

    name_1 = "Test page type"
    name_2 = "test page type"
    slug = "test-page-type"

    PageType.objects.create(name=name_1, slug=slug)

    attributes = [author_page_attribute, tag_page_attribute]

    variables = {
        "name": name_2,
        "slug": slug,
        "addAttributes": [
            graphene.Node.to_global_id("Attribute", attr.pk) for attr in attributes
        ],
    }

    # when
    response = staff_api_client.post_graphql(PAGE_TYPE_CREATE_MUTATION, variables)

    # then
    content = get_graphql_content(response)
    data = content["data"]["pageTypeCreate"]
    page_type_data = data["pageType"]
    errors = data["pageErrors"]

    assert not page_type_data
    assert len(errors) == 1
    assert errors[0]["code"] == PageErrorCode.UNIQUE.name
    assert errors[0]["field"] == "slug"


def test_page_type_create_not_valid_attributes(
    staff_api_client,
    tag_page_attribute,
    color_attribute,
    size_attribute,
    permission_manage_page_types_and_attributes,
):
    # given
    staff_user = staff_api_client.user
    staff_user.user_permissions.add(permission_manage_page_types_and_attributes)

    name = "Test page type"
    slug = "test-page-type"

    attributes = [color_attribute, tag_page_attribute, size_attribute]

    variables = {
        "name": name,
        "slug": slug,
        "addAttributes": [
            graphene.Node.to_global_id("Attribute", attr.pk) for attr in attributes
        ],
    }

    # when
    response = staff_api_client.post_graphql(PAGE_TYPE_CREATE_MUTATION, variables)

    # then
    content = get_graphql_content(response)
    data = content["data"]["pageTypeCreate"]
    page_type_data = data["pageType"]
    errors = data["pageErrors"]

    assert not page_type_data
    assert len(errors) == 1
    assert errors[0]["code"] == PageErrorCode.INVALID.name
    assert errors[0]["field"] == "addAttributes"
    assert set(errors[0]["attributes"]) == {
        graphene.Node.to_global_id("Attribute", attr.pk)
        for attr in [color_attribute, size_attribute]
    }
