import json

from tests.utils import get_graphql_content

from saleor.graphql.core.utils import snake_to_camel_case

from saleor.graphql.core.utils import snake_to_camel_case


def assert_no_permission(response):
    content = get_graphql_content(response)
    assert 'errors' in content
    assert content['errors'][0]['message'] == 'You do not have permission to perform this action'


def get_multipart_request_body(query, variables, file, file_name):
    """Create request body for multipart GraphQL requests.

    Multipart requests are different than standard GraphQL requests, because
    of additional 'operations' and 'map' keys.
    """
    return {
        'operations': json.dumps({'query': query, 'variables': variables}),
        'map': json.dumps({file_name: ['variables.file']}), file_name: file}


def convert_dict_keys_to_camel_case(d):
    """Changes dict fields from d[field_name] to d[fieldName].

    Useful when dealing with dict data such as address that need to be parsed
    into graphql input.
    """
    data = {}
    for k, v in d.items():
        new_key = snake_to_camel_case(k)
        data[new_key] = d[k]
    return data
