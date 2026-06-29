"""共有リンク発行機能（担当: Daito）."""

from __future__ import annotations


def create_shared_link(dbx, file_path: str) -> str:
    """Dropbox上のファイルに対して共有リンクを発行する。"""
    metadata = dbx.sharing_create_shared_link_with_settings(file_path)
    return metadata.url


def add_create_parser(subparsers) -> None:
    """share create サブコマンドを登録する。"""
    parser = subparsers.add_parser(
        "create",
        help="Dropbox上のファイルの共有リンクを発行する",
    )
    parser.add_argument(
        "file_path",
        help="共有リンクを発行するDropbox上のファイルパス",
    )
    parser.set_defaults(func=cmd_create)


def cmd_create(args) -> int:
    """share create のハンドラ。"""
    from share.client import get_client

    dbx = get_client()
    url = create_shared_link(dbx, args.file_path)

    print(f"共有リンクを発行しました: {url}")
    return 0
