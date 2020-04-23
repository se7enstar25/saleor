import graphene
from django.core.exceptions import ValidationError

from ....account import models
from ....account.error_codes import AccountErrorCode
from ....core.permissions import AccountPermissions, get_permissions
from ...core.enums import PermissionEnum
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types.common import ServiceAccountError
from ...meta.deprecated.mutations import ClearMetaBaseMutation, UpdateMetaBaseMutation
from ...utils import get_user_or_service_account_from_context, requestor_is_superuser
from ..utils import can_manage_service_account, get_out_of_scope_permissions


class ServiceAccountInput(graphene.InputObjectType):
    name = graphene.String(description="Name of the service account.")
    is_active = graphene.Boolean(
        description="Determine if this service account should be enabled."
    )
    permissions = graphene.List(
        PermissionEnum,
        description="List of permission code names to assign to this service account.",
    )


class ServiceAccountTokenInput(graphene.InputObjectType):
    name = graphene.String(description="Name of the token.", required=False)
    service_account = graphene.ID(description="ID of service account.", required=True)


class ServiceAccountTokenCreate(ModelMutation):
    auth_token = graphene.types.String(
        description="The newly created authentication token."
    )

    class Arguments:
        input = ServiceAccountTokenInput(
            required=True, description="Fields required to create a new auth token."
        )

    class Meta:
        description = "Creates a new token."
        model = models.ServiceAccountToken
        permissions = (AccountPermissions.MANAGE_SERVICE_ACCOUNTS,)
        error_type_class = ServiceAccountError
        error_type_field = "service_account_errors"

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)
        data = data.get("input")
        cleaned_input = cls.clean_input(info, instance, data)
        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        cls._save_m2m(info, instance, cleaned_input)
        response = cls.success_response(instance)
        response.auth_token = instance.auth_token
        return response

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        service_account = cleaned_input.get("service_account")
        requestor = get_user_or_service_account_from_context(info.context)
        if not requestor_is_superuser(requestor) and not can_manage_service_account(
            requestor, service_account
        ):
            msg = "You can't manage this service account."
            code = AccountErrorCode.OUT_OF_SCOPE_SERVICE_ACCOUNT.value
            raise ValidationError({"service_account": ValidationError(msg, code=code)})
        return cleaned_input


class ServiceAccountTokenDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(description="ID of an auth token to delete.", required=True)

    class Meta:
        description = "Deletes an authentication token assigned to service account."
        model = models.ServiceAccountToken
        permissions = (AccountPermissions.MANAGE_SERVICE_ACCOUNTS,)
        error_type_class = ServiceAccountError
        error_type_field = "service_account_errors"

    @classmethod
    def clean_instance(cls, info, instance):
        service_account = instance.service_account
        requestor = get_user_or_service_account_from_context(info.context)
        if not requestor_is_superuser(requestor) and not can_manage_service_account(
            requestor, service_account
        ):
            msg = "You can't delete this service account token."
            code = AccountErrorCode.OUT_OF_SCOPE_SERVICE_ACCOUNT.value
            raise ValidationError({"id": ValidationError(msg, code=code)})


class ServiceAccountCreate(ModelMutation):
    auth_token = graphene.types.String(
        description="The newly created authentication token."
    )

    class Arguments:
        input = ServiceAccountInput(
            required=True,
            description="Fields required to create a new service account.",
        )

    class Meta:
        description = "Creates a new service account."
        model = models.ServiceAccount
        permissions = (AccountPermissions.MANAGE_SERVICE_ACCOUNTS,)
        error_type_class = ServiceAccountError
        error_type_field = "service_account_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        # clean and prepare permissions
        if "permissions" in cleaned_input:
            requestor = get_user_or_service_account_from_context(info.context)
            permissions = cleaned_input.pop("permissions")
            cleaned_input["permissions"] = get_permissions(permissions)
            cls.ensure_can_manage_permissions(requestor, permissions)
        return cleaned_input

    @classmethod
    def ensure_can_manage_permissions(cls, requestor, permission_items):
        """Check if requestor can manage permissions from input.

        Requestor cannot manage permissions witch he doesn't have.
        """
        if requestor_is_superuser(requestor):
            return
        permissions = get_out_of_scope_permissions(requestor, permission_items)
        if permissions:
            # add error
            error_msg = "You can't add permission that you don't have."
            code = AccountErrorCode.OUT_OF_SCOPE_PERMISSION.value
            params = {"permissions": permissions}
            raise ValidationError(
                {"permissions": ValidationError(error_msg, code=code, params=params)}
            )

    @classmethod
    def save(cls, info, instance, cleaned_input):
        instance.save()
        instance.tokens.create(name="Default")

    @classmethod
    def success_response(cls, instance):
        response = super().success_response(instance)
        response.auth_token = instance.tokens.get().auth_token
        return response


class ServiceAccountUpdate(ModelMutation):
    class Arguments:
        id = graphene.ID(
            description="ID of a service account to update.", required=True
        )
        input = ServiceAccountInput(
            required=True,
            description="Fields required to update an existing service account.",
        )

    class Meta:
        description = "Updates an existing service account."
        model = models.ServiceAccount
        permissions = (AccountPermissions.MANAGE_SERVICE_ACCOUNTS,)
        error_type_class = ServiceAccountError
        error_type_field = "service_account_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        requestor = get_user_or_service_account_from_context(info.context)
        if not requestor_is_superuser(requestor) and not can_manage_service_account(
            requestor, instance
        ):
            msg = "You can't manage this service account."
            code = AccountErrorCode.OUT_OF_SCOPE_SERVICE_ACCOUNT.value
            raise ValidationError({"id": ValidationError(msg, code=code)})

        # clean and prepare permissions
        if "permissions" in cleaned_input:
            permissions = cleaned_input.pop("permissions")
            cleaned_input["permissions"] = get_permissions(permissions)
            ServiceAccountCreate.ensure_can_manage_permissions(requestor, permissions)
        return cleaned_input


class ServiceAccountDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(
            description="ID of a service account to delete.", required=True
        )

    class Meta:
        description = "Deletes a service account."
        model = models.ServiceAccount
        permissions = (AccountPermissions.MANAGE_SERVICE_ACCOUNTS,)
        error_type_class = ServiceAccountError
        error_type_field = "service_account_errors"

    @classmethod
    def clean_instance(cls, info, instance):
        requestor = get_user_or_service_account_from_context(info.context)
        if not requestor_is_superuser(requestor) and not can_manage_service_account(
            requestor, instance
        ):
            msg = "You can't delete this service account."
            code = AccountErrorCode.OUT_OF_SCOPE_SERVICE_ACCOUNT.value
            raise ValidationError({"id": ValidationError(msg, code=code)})


class ServiceAccountUpdatePrivateMeta(UpdateMetaBaseMutation):
    class Meta:
        description = "Updates private metadata for a service account."
        permissions = (AccountPermissions.MANAGE_SERVICE_ACCOUNTS,)
        model = models.ServiceAccount
        public = False
        error_type_class = ServiceAccountError
        error_type_field = "service_account_errors"


class ServiceAccountClearPrivateMeta(ClearMetaBaseMutation):
    class Meta:
        description = "Clear private metadata for a service account."
        model = models.ServiceAccount
        permissions = (AccountPermissions.MANAGE_SERVICE_ACCOUNTS,)
        public = False
        error_type_class = ServiceAccountError
        error_type_field = "service_account_errors"
