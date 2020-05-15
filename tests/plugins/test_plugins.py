from saleor.plugins.anonymize.plugin import AnonymizePlugin
from saleor.plugins.base_plugin import ConfigurationTypeField
from saleor.plugins.manager import get_plugins_manager
from tests.plugins.sample_plugins import PluginSample
from tests.plugins.utils import get_config_value


def test_update_config_items_keeps_bool_value(plugin_configuration, settings):
    settings.PLUGINS = ["tests.plugins.sample_plugins.PluginSample"]
    data_to_update = [
        {"name": "Username", "value": "new_admin@example.com"},
        {"name": "Use sandbox", "value": False},
    ]
    manager = get_plugins_manager()
    plugin_sample = manager.get_plugin(PluginSample.PLUGIN_ID)
    plugin_sample._update_config_items(data_to_update, plugin_sample.configuration)

    assert get_config_value("Use sandbox", plugin_sample.configuration) is False


def test_update_config_items_convert_to_bool_value():
    data_to_update = [
        {"name": "Username", "value": "new_admin@example.com"},
        {"name": "Use sandbox", "value": "false"},
    ]
    plugin_sample = PluginSample(
        configuration=PluginSample.DEFAULT_CONFIGURATION,
        active=PluginSample.DEFAULT_ACTIVE,
    )
    plugin_sample._update_config_items(data_to_update, plugin_sample.configuration)

    assert get_config_value("Use sandbox", plugin_sample.configuration) is False


def test_update_config_items_skips_new_keys_when_doesnt_exsit_in_conf_structure():
    data_to_update = [
        {"name": "New-field", "value": "content"},
    ]
    plugin_sample = PluginSample(
        configuration=PluginSample.DEFAULT_CONFIGURATION,
        active=PluginSample.DEFAULT_ACTIVE,
    )
    current_config = PluginSample.DEFAULT_CONFIGURATION

    plugin_sample._update_config_items(data_to_update, current_config)
    assert not all(
        [config_field["name"] == "New-field" for config_field in current_config]
    )


def test_update_config_items_adds_new_keys():
    data_to_update = [
        {"name": "New-field", "value": "content"},
    ]
    PluginSample.CONFIG_STRUCTURE["New-field"] = {
        "type": ConfigurationTypeField.STRING,
        "help_text": "New input field",
        "label": "New field",
    }
    plugin_sample = PluginSample(
        configuration=PluginSample.DEFAULT_CONFIGURATION,
        active=PluginSample.DEFAULT_ACTIVE,
    )
    current_config = PluginSample.DEFAULT_CONFIGURATION

    plugin_sample._update_config_items(data_to_update, current_config)
    assert any([config_field["name"] == "New-field" for config_field in current_config])


def test_save_plugin_configuration(plugin_configuration):
    cleaned_data = {"configuration": [{"name": "Username", "value": "new-username"}]}
    PluginSample.save_plugin_configuration(plugin_configuration, cleaned_data)
    plugin_configuration.refresh_from_db()
    configuration = plugin_configuration.configuration
    configuration_dict = {
        c_field["name"]: c_field["value"] for c_field in configuration
    }
    assert configuration_dict["Username"] == "new-username"


def test_save_plugin_configuration_adds_new_field(plugin_configuration):
    PluginSample.CONFIG_STRUCTURE["Token"] = {
        "type": ConfigurationTypeField.PASSWORD,
        "help_text": "New input field",
        "label": "New field",
    }
    cleaned_data = {"configuration": [{"name": "Token", "value": "token-data"}]}
    PluginSample.save_plugin_configuration(plugin_configuration, cleaned_data)
    plugin_configuration.refresh_from_db()
    configuration = plugin_configuration.configuration
    configuration_dict = {
        c_field["name"]: c_field["value"] for c_field in configuration
    }
    assert configuration_dict.get("Token") == "token-data"


def test_save_plugin_configuration_skips_new_field_when_doesnt_exsit_in_conf_structure(
    plugin_configuration,
):
    cleaned_data = {"configuration": [{"name": "Token", "value": "token-data"}]}
    PluginSample.save_plugin_configuration(plugin_configuration, cleaned_data)
    plugin_configuration.refresh_from_db()
    configuration = plugin_configuration.configuration
    configuration_dict = {
        c_field["name"]: c_field["value"] for c_field in configuration
    }
    assert not configuration_dict.get("Token")


def test_base_plugin__update_configuration_structure_when_old_config_is_empty(
    monkeypatch, plugin_configuration
):
    plugin_configuration.configuration = []
    plugin_configuration.save()
    PluginSample._update_configuration_structure(plugin_configuration.configuration)
    plugin_configuration.save()
    plugin_configuration.refresh_from_db()
    assert len(plugin_configuration.configuration) == len(
        PluginSample.DEFAULT_CONFIGURATION
    )


def test_base_plugin__update_configuration_structure_configuration_has_change(
    monkeypatch, plugin_configuration
):
    old_configuration = plugin_configuration.configuration.copy()
    config_structure = PluginSample.CONFIG_STRUCTURE
    config_structure["Private key"] = {
        "help_text": "Test",
        "label": "Test",
        "type": ConfigurationTypeField.STRING,
    }
    private_key_dict = {"name": "Private key", "value": "123457"}
    monkeypatch.setattr(
        PluginSample,
        "DEFAULT_CONFIGURATION",
        PluginSample.DEFAULT_CONFIGURATION + [private_key_dict],
    )
    PluginSample._update_configuration_structure(plugin_configuration.configuration)
    plugin_configuration.save()
    plugin_configuration.refresh_from_db()
    assert len(old_configuration) + 1 == len(plugin_configuration.configuration)
    old_configuration.append(private_key_dict)
    assert old_configuration == plugin_configuration.configuration


def test_base_plugin__append_config_structure_to_config(settings):
    settings.PLUGINS = ["tests.plugins.sample_plugins.PluginSample"]
    manager = get_plugins_manager()
    plugin = manager.get_plugin(PluginSample.PLUGIN_ID)
    config = [
        {"name": "Username", "value": "my_test_user"},
        {"name": "Password", "value": "my_password"},
    ]
    config_with_structure = [
        {
            "name": "Username",
            "value": "my_test_user",
            "type": "String",
            "help_text": "Username input field",
            "label": "Username",
        },
        {
            "name": "Password",
            "value": "my_password",
            "type": "Password",
            "help_text": "Password input field",
            "label": "Password",
        },
    ]
    plugin._append_config_structure(config)
    assert config == config_with_structure


def test_change_user_address_in_anonymize_plugin_reset_phone(address, settings):
    settings.PLUGINS = ["saleor.plugins.anonymize.plugin.AnonymizePlugin"]
    manager = get_plugins_manager()
    anonymize_plugin = manager.get_plugin(AnonymizePlugin.PLUGIN_ID)

    # ensure that phone is set
    assert address.phone

    new_address = anonymize_plugin.change_user_address(
        address=address, address_type=None, user=None, previous_value=address
    )
    assert not new_address.phone
