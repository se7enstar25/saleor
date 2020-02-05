import binascii
from typing import TYPE_CHECKING, Type, Union

import graphene
import graphene_django_optimizer as gql_optimizer
from django.core.exceptions import ValidationError
from graphene import ObjectType

from ....core.utils import generate_unique_slug

if TYPE_CHECKING:
    # flake8: noqa
    from django.db.models import Model


def clean_seo_fields(data):
    """Extract and assign seo fields to given dictionary."""
    seo_fields = data.pop("seo", None)
    if seo_fields:
        data["seo_title"] = seo_fields.get("title")
        data["seo_description"] = seo_fields.get("description")


def snake_to_camel_case(name):
    """Convert snake_case variable name to camelCase."""
    if isinstance(name, str):
        split_name = name.split("_")
        return split_name[0] + "".join(map(str.capitalize, split_name[1:]))
    return name


def str_to_enum(name):
    """Create an enum value from a string."""
    return name.replace(" ", "_").replace("-", "_").upper()


def validate_image_file(file, field_name):
    """Validate if the file is an image."""
    if not file.content_type.startswith("image/"):
        raise ValidationError(
            {field_name: ValidationError("Invalid file type", code="invalid")}
        )


def from_global_id_strict_type(
    global_id: str, only_type: Union[ObjectType, str], field: str = "id"
) -> str:
    """Resolve a node global id with a strict given type required."""
    try:
        _type, _id = graphene.Node.from_global_id(global_id)
    except (binascii.Error, UnicodeDecodeError) as exc:
        raise ValidationError(
            {
                field: ValidationError(
                    "Couldn't resolve to a node: %s" % global_id, code="not_found"
                )
            }
        ) from exc

    if str(_type) != str(only_type):
        raise ValidationError(
            {field: ValidationError(f"Must receive a {only_type} id", code="invalid")}
        )
    return _id


def get_node_optimized(qs, lookup, info):
    qs = qs.filter(**lookup)
    qs = gql_optimizer.query(qs, info)
    return qs[0] if qs else None


def validate_slug_and_generate_if_needed(
    instance: Type["Model"],
    slugable_field: str,
    cleaned_input: dict,
    slug_field_name: str = "slug",
) -> dict:
    """Validate slug from input and generate in create mutation if is not given."""
    # update mutation - just check if slug value is not empty
    # we use _state.adding to checking if instance is saved because if pk has default
    # value it is set before save
    if not instance._state.adding:  # type: ignore
        validate_slug_value(cleaned_input)
        return cleaned_input

    # create mutation - generate slug if slug value is empty
    slug = cleaned_input.get(slug_field_name)
    if not slug and slugable_field in cleaned_input:
        slug = generate_unique_slug(instance, cleaned_input[slugable_field])
        cleaned_input[slug_field_name] = slug
    return cleaned_input


def validate_slug_value(cleaned_input, slug_field_name: str = "slug"):
    if slug_field_name in cleaned_input:
        slug = cleaned_input[slug_field_name]
        if not slug:
            raise ValidationError(
                f"{slug_field_name.capitalize()} value cannot be blank."
            )
