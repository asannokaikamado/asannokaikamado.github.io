"""img/menu/ の写真から、index.html のお弁当カルーセル部分を作り直します。

使い方（リポジトリのフォルダで実行）:
    python tools/update_gallery.py

写真のファイル名のルール:
    料理名(S).jpg / 料理名(M).jpg … サイズの印つきで表示
    料理名.jpg                    … サイズの印なしで表示
並び順は料理名の順（同じ料理は S → M の順）です。
index.html の <!-- gallery:start --> と <!-- gallery:end --> の間だけを書き換えます。
"""
import html
import re
import struct
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MENU_DIR = ROOT / "img" / "menu"
INDEX = ROOT / "index.html"
START, END = "<!-- gallery:start -->", "<!-- gallery:end -->"
EAGER_COUNT = 3  # 最初に見えている枚数（この枚数までは遅延読み込みしない）
SIZE_PATTERN = re.compile(r"^(?P<name>.+?)\s*[(（](?P<size>[SMＳＭsm])[)）]$")
SIZE_ORDER = {"S": 0, "M": 1, None: 0}


def jpeg_size(path):
    """JPEGファイルの横幅・高さを読み取る（追加ライブラリ不要）。"""
    data = path.read_bytes()
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker == 0xFF or marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2 if marker != 0xFF else 1
            continue
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height, width = struct.unpack(">HH", data[i + 5:i + 9])
            return width, height
        length = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + length
    raise ValueError(f"{path.name}: 画像のサイズを読み取れませんでした")


def parse_name(path):
    stem = unicodedata.normalize("NFC", path.stem)
    m = SIZE_PATTERN.match(stem)
    if not m:
        return stem, None
    size = unicodedata.normalize("NFKC", m.group("size")).upper()
    return m.group("name"), size


def build_items():
    photos = [p for p in MENU_DIR.iterdir() if p.suffix.lower() in (".jpg", ".jpeg")]
    entries = []
    for path in photos:
        name, size = parse_name(path)
        entries.append((unicodedata.normalize("NFKC", name), SIZE_ORDER[size], name, size, path))
    entries.sort(key=lambda e: (e[0], e[1]))

    lines = []
    for index, (_, _, name, size, path) in enumerate(entries):
        width, height = jpeg_size(path)
        size_label = f"（{size}サイズ）" if size else ""
        badge = f'<span class="size size-{size.lower()}">{size}サイズ</span>' if size else ""
        lazy = ' loading="lazy"' if index >= EAGER_COUNT else ""
        src = html.escape(f"img/menu/{path.name}".replace(" ", "%20"))
        lines += [
            '          <li class="sl-card"><figure>',
            f'            <img src="{src}" alt="{html.escape(name)}のお弁当{size_label}"'
            f' width="{width}" height="{height}"{lazy} decoding="async">',
            f"            <figcaption>{html.escape(name)}{badge}</figcaption>",
            "          </figure></li>",
        ]
    return lines, len(entries)


def main():
    # Windows のコンソールでも日本語のメッセージを表示できるようにする
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    text = INDEX.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit(f"index.html に {START} と {END} が見つかりません")
    lines, count = build_items()
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    new_text = head + START + "\n" + "\n".join(lines) + "\n          " + END + tail
    INDEX.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"カルーセルを更新しました（{count}枚）")


if __name__ == "__main__":
    main()
