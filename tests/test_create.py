from unittest.mock import MagicMock

from share.create import create_shared_link


def test_create_shared_link():
    dbx = MagicMock()

    dbx.sharing_create_shared_link_with_settings.return_value.url = (
        "https://www.dropbox.com/s/test/example.txt"
    )

    result = create_shared_link(dbx, "/example.txt")

    assert result == "https://www.dropbox.com/s/test/example.txt"

    dbx.sharing_create_shared_link_with_settings.assert_called_once_with(
        "/example.txt"
    )