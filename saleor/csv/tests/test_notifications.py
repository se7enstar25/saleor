from unittest import mock

from django.core.files import File
from freezegun import freeze_time

from ...core.notify_events import AdminNotifyEvent
from ...core.utils import build_absolute_uri
from .. import ExportEvents, notifications
from ..models import ExportEvent
from ..notifications import get_default_export_payload


@freeze_time("2018-05-31 12:00:01")
@mock.patch("saleor.plugins.manager.PluginsManager.notify")
def test_send_export_download_link_notification(
    mocked_notify, site_settings, user_export_file, tmpdir, media_root
):
    # given
    file_mock = mock.MagicMock(spec=File)
    file_mock.name = "temp_file.csv"

    user_export_file.content_file = file_mock
    user_export_file.save()

    # when
    notifications.send_export_download_link_notification(user_export_file)

    # then
    expected_payload = get_default_export_payload(user_export_file)
    expected_payload["csv_link"] = build_absolute_uri(user_export_file.content_file.url)

    mocked_notify.assert_called_once_with(
        AdminNotifyEvent.CSV_PRODUCT_EXPORT_SUCCESS, expected_payload
    )

    assert ExportEvent.objects.filter(
        export_file=user_export_file,
        user=user_export_file.user,
        type=ExportEvents.EXPORTED_FILE_SENT,
    ).exists()


@freeze_time("2018-05-31 12:00:01")
@mock.patch("saleor.plugins.manager.PluginsManager.notify")
def test_send_export_failed_info(
    mocked_notify, site_settings, user_export_file, tmpdir, media_root
):
    # given
    file_mock = mock.MagicMock(spec=File)
    file_mock.name = "temp_file.csv"

    user_export_file.content_file = file_mock
    user_export_file.save()

    # when
    notifications.send_export_failed_info(user_export_file)

    # then
    expected_payload = get_default_export_payload(user_export_file)

    mocked_notify.assert_called_once_with(
        AdminNotifyEvent.CSV_EXPORT_FAILED, expected_payload
    )

    assert ExportEvent.objects.filter(
        export_file=user_export_file,
        user=user_export_file.user,
        type=ExportEvents.EXPORT_FAILED_INFO_SENT,
    )
