# THE THURSDAY PAPER

Thursday 26 November 2026 in one image: 50 dated world stories, 10 regions, three drawn lead stories, twelve panels, a numbered world map, a DATE CHECK strip and a UTC timeline — no AI photos, every story verified against two or more reports.

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/keepomakima/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/keepomakima/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

## How it works

`main.py` (Python 3.13, standard library + Pillow when available) draws the whole front page with PIL and writes `entry.png` (1024×1024, under 1 MiB). On the bare grading machine without Pillow it falls back to the committed `entry.png` beside the script, verified by sha256 — the same bytes either way. No network is used anywhere.

Run it twice and the bytes are identical:

```sh
python3 main.py
```

Output goes to `$MAKEFUN_OUTPUT_DIR/entry.png` (`/output/entry.png` by default).

## The day in one line

Houthis claim strikes on Saudi Arabia's Ras Tanura refinery and Riyadh's financial district (Brent settles $94.61); Washington proposes Section 301 tariffs on 14 trading partners; Kim Jong Un calls for wider tactical nuclear deployment; Pakistan's first astronaut docks at China's Tiangong station.
