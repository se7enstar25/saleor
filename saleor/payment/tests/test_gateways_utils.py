import warnings

import pytest

from ..gateways.utils import get_supported_currencies
from ..interface import GatewayConfig


@pytest.fixture
def gateway_config():
    return GatewayConfig(
        gateway_name="Dummy",
        auto_capture=True,
        supported_currencies=[],
        connection_params={"secret-key": "dummy"},
    )


def test_get_supported_currencies(gateway_config):
    # given
    gateway_config.supported_currencies = ["PLN", "USD"]

    # when
    currencies = get_supported_currencies(gateway_config, "Test")

    # then
    assert currencies == ["PLN", "USD"]


def test_get_supported_currencies_default_currency(gateway_config):
    # when
    with warnings.catch_warnings(record=True) as warns:
        currencies = get_supported_currencies(gateway_config, "Test")

        expected_warning = (
            "Default currency used for Test. "
            "DEFAULT_CURRENCY setting is deprecated, "
            "please configure supported currencies for this gateway."
        )
        assert any([str(warning.message) == expected_warning for warning in warns])

    # then
    assert currencies == ["USD"]
