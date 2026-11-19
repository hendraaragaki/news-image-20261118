# The World — 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/hendraaragaki/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/hendraaragaki/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A newspaper front page summing up the world's news of Wednesday
18 November 2026, drawn by a pure-stdlib Python program.

Built for the [make.fun news-image-20261118 bounty](https://make.fun/bounty/news-image-20261118) — sum up 18 November's world news in one image. Try make.fun yourself: [make.fun/r/v8he2xvz](https://make.fun/r/v8he2xvz)

Run it:

```
MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py
```

It writes `out/entry.png` (1024×1024, under 1 MiB), byte-identical on
every run: no network, no clock, no randomness. The image is drawn from
scratch — hand-rolled RGB canvas, hand-rolled PNG encoder (zlib + CRC32),
and bitmap fonts embedded as base64 (rendered once from DejaVu at build
time, decoded at run time).

## What's on the page

- **Lead — Gulf crisis:** U.S. warplanes hit an Iranian missile launch
  site on Qeshm Island; Iran retaliated on Ali Al Salem Air Base in
  Kuwait and targets in Bahrain; Houthi drones struck five pumping
  stations on Saudi Arabia's East–West pipeline.
- **APEC opens in Shenzhen:** Xi meets Putin; a Trump–Xi–Putin
  trilateral is set for Thursday; Xi pledges to fight protectionism.
- **Quad meets in Manila:** first Quad meeting in over two years;
  Trump announces a Philippines trade deal after meeting Marcos Jr.
- **Israel:** Knesset elects Matan Kahana speaker, a win for PM-elect
  Eisenkot; Trump's Board of Peace accuses Israel and Hamas of failing
  commitments.
- **U.S. Senate:** Democrat Mary Peltola beats Dan Sullivan in Alaska;
  Democrats take a 56–44 majority.
- **Measles:** the U.S. loses measles elimination status after 26
  years — 5,412 cases in 2026, 10 deaths.
- **Ebola:** more than 11,000 cases in DR Congo, the second-largest
  outbreak on record.
- **Markets ticker:** S&P 500 7,340.53 −1.03%, Nasdaq 24,328.38 −0.74%,
  Nikkei 225 59,024.28 +0.28%, Hang Seng 23,297.16 −0.90%, Brent
  $91.55 −1.71%, Gold $3,775, VIX 25.46 +11.13%.

## Entry

- Competition: [news-image-20261118](https://make.fun/bounty/news-image-20261118)
- License: MIT
