"""現在共有しているファイルの一覧を取得する。"""


def list_shared_links(dbx) -> list[dict]:
    """Dropbox の共有リンクを全件返す。

    Args:
        dbx: dropbox.Dropbox インスタンス

    Returns:
        {"path": str, "url": str, "name": str} のリスト
    """
    links = []
    result = dbx.sharing_list_shared_links()
    while True:
        for link in result.links:
            links.append({
                "path": link.path_lower,
                "url": link.url,
                "name": link.name,
            })
        if not result.has_more:
            break
        result = dbx.sharing_list_shared_links(cursor=result.cursor)
    return links
