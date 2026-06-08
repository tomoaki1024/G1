"""コマンドラインのエントリポイント（土台）.

各サブコマンドの中身は担当者が実装する。
"""

import argparse
import sys

def remove_shared_link(args: argparse.Namespace) -> int:
    print("----------------------------------------")
    print(f"共有停止コマンドが呼び出されました")
    print(f" 対象ファイル: {args.filepath}")
    print("----------------------------------------")

    target_path = args.filepath

    # get_client() もらったら消す
    if True:
        print("開発中 認証コード合流待ちです。")
        return 0

    # 
    try:
        # dbx = get_client() 

        # 2. ファイルパスから共有リンクのURLを探す
        print(f"Dropbox上の {target_path} のリンクを検索中...")
        response = dbx.sharing_list_shared_links(path=target_path, direct_only=True)
        
        if not response.links:
            print("共有リンクが見つかりません。")
            return 1
            
        shared_url = response.links[0].url

        # 3. リンクを削除する
        dbx.sharing_revoke_shared_link(url=shared_url)
        print("共有を無事に停止しました！")
        return 0

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1

    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="share", description="Dropbox 共有リンク発行ツール")
    sub = parser.add_subparsers(dest="command", required=True)

    # TODO(担当者): 各サブコマンドを追加し、set_defaults(func=...) でハンドラを紐づける
    # 例) sub.add_parser("auth", help="Dropbox 認証を行う").set_defaults(func=cmd_auth)
    parser_remove = sub.add_parser("remove", help="共有を停止する")
    parser_remove.add_argument("filepath", help="共有を停止するファイルのパス")
    parser_remove.set_defaults(func=remove_shared_link)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
