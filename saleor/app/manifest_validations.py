from collections import defaultdict
from typing import Dict, Iterable, List

from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.db.models import Value
from django.db.models.functions import Concat

from ..core.permissions import (
    get_permissions,
    get_permissions_enum_list,
    split_permission_codename,
)
from .error_codes import AppErrorCode
from .types import AppExtensionTarget, AppExtensionType, AppExtensionView
from .validators import AppURLValidator

T_ERRORS = Dict[str, List[ValidationError]]


AVAILABLE_APP_EXTENSION_CONFIGS = {
    AppExtensionType.DETAILS: {
        AppExtensionView.PRODUCT: [
            AppExtensionTarget.CREATE,
            AppExtensionTarget.MORE_ACTIONS,
        ]
    },
    AppExtensionType.OVERVIEW: {
        AppExtensionView.PRODUCT: [
            AppExtensionTarget.CREATE,
            AppExtensionTarget.MORE_ACTIONS,
        ]
    },
}


def _clean_app_url(url):
    url_validator = AppURLValidator()
    url_validator(url)


def clean_manifest_url(manifest_url):
    try:
        _clean_app_url(manifest_url)
    except (ValidationError, AttributeError):
        msg = "Enter a valid URL."
        code = AppErrorCode.INVALID_URL_FORMAT.value
        raise ValidationError({"manifest_url": ValidationError(msg, code=code)})


def clean_permissions(
    required_permissions: List[str], saleor_permissions: Iterable[Permission]
) -> List[Permission]:
    missing_permissions = []
    all_permissions = {perm[0]: perm[1] for perm in get_permissions_enum_list()}
    for perm in required_permissions:
        if not all_permissions.get(perm):
            missing_permissions.append(perm)
    if missing_permissions:
        error_msg = "Given permissions don't exist."
        code = AppErrorCode.INVALID_PERMISSION.value
        params = {"permissions": missing_permissions}
        raise ValidationError(error_msg, code=code, params=params)

    permissions = [all_permissions[perm] for perm in required_permissions]
    permissions = split_permission_codename(permissions)
    return [p for p in saleor_permissions if p.codename in permissions]


def clean_manifest_data(manifest_data):
    errors: T_ERRORS = defaultdict(list)

    validate_required_fields(manifest_data, errors)
    try:
        _clean_app_url(manifest_data["tokenTargetUrl"])
    except (ValidationError, AttributeError):
        errors["tokenTargetUrl"].append(
            ValidationError(
                "Incorrect format.",
                code=AppErrorCode.INVALID_URL_FORMAT.value,
            )
        )

    saleor_permissions = get_permissions().annotate(
        formated_codename=Concat("content_type__app_label", Value("."), "codename")
    )
    try:
        app_permissions = clean_permissions(
            manifest_data.get("permissions", []), saleor_permissions
        )
    except ValidationError as e:
        errors["permissions"].append(e)
        app_permissions = []

    manifest_data["permissions"] = app_permissions

    if not errors:
        clean_extensions(manifest_data, app_permissions, errors)

    if errors:
        raise ValidationError(errors)


def _clean_extension_permissions(extension, app_permissions, errors):
    permissions_data = extension.get("permissions", [])
    try:
        extension_permissions = clean_permissions(permissions_data, app_permissions)
    except ValidationError as e:
        e.params["label"] = extension.get("label")
        errors["extensions"].append(e)
        return

    if len(extension_permissions) != len(permissions_data):
        errors["extensions"].append(
            ValidationError(
                "Extension permission must be listed in App's permissions.",
                code=AppErrorCode.OUT_OF_SCOPE_PERMISSION.value,
            )
        )

    extension["permissions"] = extension_permissions


def _validate_configuration(extension, errors):

    available_config_for_type = AVAILABLE_APP_EXTENSION_CONFIGS.get(
        extension["type"], {}
    )
    available_config_for_type_and_view = available_config_for_type.get(
        extension["view"], []
    )

    if extension["target"] not in available_config_for_type_and_view:
        msg = (
            "Incorrect configuration of app extension for fields: view, type and "
            "target."
        )
        errors["extensions"].append(
            ValidationError(
                msg,
                code=AppErrorCode.INVALID.value,
            )
        )


def clean_extensions(manifest_data, app_permissions, errors):
    extensions = manifest_data.get("extensions", [])
    enum_map = [
        (AppExtensionView, "view"),
        (AppExtensionType, "type"),
        (AppExtensionTarget, "target"),
    ]
    for extension in extensions:
        for extension_enum, key in enum_map:
            if extension[key] in [code.upper() for code, _ in extension_enum.CHOICES]:
                extension[key] = getattr(extension_enum, extension[key])
            else:
                errors["extensions"].append(
                    ValidationError(
                        f"Incorrect value for field: {key}",
                        code=AppErrorCode.INVALID.value,
                    )
                )

        try:
            _clean_app_url(extension["url"])
        except (ValidationError, AttributeError):
            errors["extensions"].append(
                ValidationError(
                    "Incorrect value for field: url.",
                    code=AppErrorCode.INVALID_URL_FORMAT.value,
                )
            )
        _validate_configuration(extension, errors)
        _clean_extension_permissions(extension, app_permissions, errors)


def validate_required_fields(manifest_data, errors):
    manifest_required_fields = {"id", "version", "name", "tokenTargetUrl"}
    extension_required_fields = {
        "label",
        "url",
        "view",
        "type",
        "target",
    }
    manifest_missing_fields = manifest_required_fields.difference(manifest_data)
    if manifest_missing_fields:
        [
            errors[missing_field].append(
                ValidationError("Field required.", code=AppErrorCode.REQUIRED.value)
            )
            for missing_field in manifest_missing_fields
        ]

    app_extensions_data = manifest_data.get("extensions", [])
    for extension in app_extensions_data:
        extension_fields = set(extension.keys())
        missing_fields = extension_required_fields.difference(extension_fields)
        if missing_fields:
            errors["extensions"].append(
                ValidationError(
                    "Missing required fields for app extension: %s."
                    % ", ".join(missing_fields),
                    code=AppErrorCode.REQUIRED.value,
                )
            )
