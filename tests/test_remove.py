import argparse
from types import SimpleNamespace
from unittest.mock import Mock

from share import remove


def _args(filepath: str) -> argparse.Namespace:
    return argparse.Namespace(filepath=filepath)


def test_to_dropbox_path_keeps_posix_path():
    assert remove._to_dropbox_path("/docs/report.txt") == "/docs/report.txt"


def test_to_dropbox_path_converts_windows_separator():
    assert remove._to_dropbox_path(r"\docs\report.txt") == "/docs/report.txt"


def test_remove_shared_link_returns_1_when_not_authenticated(monkeypatch, capsys):
    monkeypatch.setattr(remove, "get_client", lambda: None)

    result = remove.remove_shared_link(_args("/docs/report.txt"))

    assert result == 1
    assert "認証情報が見つかりません" in capsys.readouterr().out


def test_remove_shared_link_revokes_first_found_link(monkeypatch, capsys):
    dbx = SimpleNamespace()
    response = SimpleNamespace(links=[SimpleNamespace(url="https://dbx.example/shared")])
    dbx.sharing_list_shared_links = Mock(return_value=response)
    dbx.sharing_revoke_shared_link = Mock()
    monkeypatch.setattr(remove, "get_client", lambda: dbx)

    result = remove.remove_shared_link(_args("/docs/report.txt"))

    assert result == 0
    dbx.sharing_list_shared_links.assert_called_once_with(
        path="/docs/report.txt",
        direct_only=True,
    )
    dbx.sharing_revoke_shared_link.assert_called_once_with(
        url="https://dbx.example/shared",
    )
    assert "共有を無事に停止しました" in capsys.readouterr().out


def test_remove_shared_link_returns_1_when_link_is_not_found(monkeypatch, capsys):
    dbx = SimpleNamespace()
    dbx.sharing_list_shared_links = Mock(
        return_value=SimpleNamespace(links=[]),
    )
    dbx.sharing_revoke_shared_link = Mock()
    monkeypatch.setattr(remove, "get_client", lambda: dbx)

    result = remove.remove_shared_link(_args("/docs/report.txt"))

    assert result == 1
    dbx.sharing_revoke_shared_link.assert_not_called()
    assert "共有リンクが見つかりません" in capsys.readouterr().out


def test_remove_shared_link_returns_1_when_dropbox_api_fails(monkeypatch, capsys):
    dbx = SimpleNamespace()
    dbx.sharing_list_shared_links = Mock(side_effect=RuntimeError("api error"))
    dbx.sharing_revoke_shared_link = Mock()
    monkeypatch.setattr(remove, "get_client", lambda: dbx)

    result = remove.remove_shared_link(_args("/docs/report.txt"))

    assert result == 1
    dbx.sharing_revoke_shared_link.assert_not_called()
    assert "エラーが発生しました: api error" in capsys.readouterr().out
