"""共有リンク削除コマンド."""

from __future__ import annotations

import argparse
from pathlib import Path, PureWindowsPath

from share.client import get_client


def _to_dropbox_path(filepath: str) -> str:
    """OSごとの差を吸収してDropbox API用のパスへ変換する."""
    path = Path(filepath).expanduser()
    path_text = str(path)
    if "\\" in path_text:
        return PureWindowsPath(path_text).as_posix()
    return path.as_posix()


def remove_shared_link(args: argparse.Namespace) -> int:
    """指定されたファイルの共有リンクを削除する."""
    print("----------------------------------------")
    print("共有停止コマンドが呼び出されました")
    print(f" 対象ファイル: {args.filepath}")
    print("----------------------------------------")

    target_path = _to_dropbox_path(args.filepath)
    dbx = get_client()
    if dbx is None:
        print("認証情報が見つかりません。先にログインしてください。")
        return 1

    try:
        print(f"Dropbox上の {target_path} のリンクを検索中...")
        response = dbx.sharing_list_shared_links(
            path=target_path,
            direct_only=True,
        )

        if not response.links:
            print("共有リンクが見つかりません。")
            return 1

        shared_url = response.links[0].url
        dbx.sharing_revoke_shared_link(url=shared_url)
        print("共有を無事に停止しました！")
        return 0
    except Exception as exc:
        print(f"エラーが発生しました: {exc}")
        return 1


def add_remove_parser(subparsers) -> None:
    """``share remove`` サブコマンドを登録する."""
    parser = subparsers.add_parser("remove", help="Dropbox の共有リンクを削除する")
    parser.add_argument("filepath", help="共有リンクを削除する Dropbox 上のファイルパス")
    parser.set_defaults(func=remove_shared_link)
