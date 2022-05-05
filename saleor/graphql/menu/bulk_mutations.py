import graphene

from ...core.permissions import MenuPermissions
from ...menu import models
from ..core.mutations import ModelBulkDeleteMutation
from ..core.types import MenuError, NonNullList
from .types import Menu, MenuItem


class MenuBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = NonNullList(
            graphene.ID, required=True, description="List of menu IDs to delete."
        )

    class Meta:
        description = "Deletes menus."
        model = models.Menu
        object_type = Menu
        permissions = (MenuPermissions.MANAGE_MENUS,)
        error_type_class = MenuError
        error_type_field = "menu_errors"

    @classmethod
    def bulk_action(cls, info, queryset):
        menus = list(queryset)
        queryset.delete()
        for menu in menus:
            info.context.plugins.menu_deleted(menu)


class MenuItemBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = NonNullList(
            graphene.ID, required=True, description="List of menu item IDs to delete."
        )

    class Meta:
        description = "Deletes menu items."
        model = models.MenuItem
        object_type = MenuItem
        permissions = (MenuPermissions.MANAGE_MENUS,)
        error_type_class = MenuError
        error_type_field = "menu_errors"

    @classmethod
    def bulk_action(cls, info, queryset):
        menu_items = list(queryset)
        queryset.delete()
        for menu_item in menu_items:
            info.context.plugins.menu_item_deleted(menu_item)
