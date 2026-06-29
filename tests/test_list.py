"""共有リンク一覧取得機能のユニットテスト（mock 利用）."""

from unittest.mock import MagicMock

from share.list.list import list_shared_links


def _make_link(path_lower, url, name):
    link = MagicMock()
    link.path_lower = path_lower
    link.url = url
    link.name = name
    return link


def _make_result(links, has_more=False, cursor=None):
    result = MagicMock()
    result.links = links
    result.has_more = has_more
    result.cursor = cursor
    return result


def test_list_shared_links_returns_empty_when_no_links():
    dbx = MagicMock()
    dbx.sharing_list_shared_links.return_value = _make_result([])

    result = list_shared_links(dbx)

    assert result == []
    dbx.sharing_list_shared_links.assert_called_once_with()


def test_list_shared_links_returns_single_link():
    link = _make_link("/foo.txt", "https://example.com/foo", "foo.txt")
    dbx = MagicMock()
    dbx.sharing_list_shared_links.return_value = _make_result([link])

    result = list_shared_links(dbx)

    assert result == [{"path": "/foo.txt", "url": "https://example.com/foo", "name": "foo.txt"}]


def test_list_shared_links_returns_multiple_links():
    links = [
        _make_link("/a.txt", "https://example.com/a", "a.txt"),
        _make_link("/b.txt", "https://example.com/b", "b.txt"),
    ]
    dbx = MagicMock()
    dbx.sharing_list_shared_links.return_value = _make_result(links)

    result = list_shared_links(dbx)

    assert len(result) == 2
    assert result[0] == {"path": "/a.txt", "url": "https://example.com/a", "name": "a.txt"}
    assert result[1] == {"path": "/b.txt", "url": "https://example.com/b", "name": "b.txt"}


def test_list_shared_links_follows_pagination():
    link1 = _make_link("/p1.txt", "https://example.com/p1", "p1.txt")
    link2 = _make_link("/p2.txt", "https://example.com/p2", "p2.txt")

    first_result = _make_result([link1], has_more=True, cursor="cursor_abc")
    second_result = _make_result([link2], has_more=False)

    dbx = MagicMock()
    dbx.sharing_list_shared_links.side_effect = [first_result, second_result]

    result = list_shared_links(dbx)

    assert len(result) == 2
    assert result[0]["path"] == "/p1.txt"
    assert result[1]["path"] == "/p2.txt"
    assert dbx.sharing_list_shared_links.call_count == 2
    dbx.sharing_list_shared_links.assert_called_with(cursor="cursor_abc")


def test_list_shared_links_dict_keys():
    link = _make_link("/doc.pdf", "https://example.com/doc", "doc.pdf")
    dbx = MagicMock()
    dbx.sharing_list_shared_links.return_value = _make_result([link])

    result = list_shared_links(dbx)

    assert set(result[0].keys()) == {"path", "url", "name"}
