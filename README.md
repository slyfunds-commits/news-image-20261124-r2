# Tuesday 24 November 2026 in one picture — full day, 38 stories, 9 regions

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/slyfunds-commits/news-image-20261124-r2/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/slyfunds-commits/news-image-20261124-r2/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Entry for the [make.fun bounty "Sum up 24 November's world news in one image"](https://make.fun/bounty/news-image-20261124) — round 2. One 1024×1024 image summing up Tuesday 24 November 2026: 38 stories across 9 regions, with four drawn lead scenes (Wall Street's rally fading, the fourth tanker burning in the Strait of Hormuz, Huawei's conviction in Brooklyn, Champions League matchday 5) and a DATE CHECK footer naming what was left out because it happened on another day.

Round 1 was invalid (the grader's run exited 1: it sets `MAKEFUN_OUTPUT_DIR` to a directory that does not exist yet and the program opened the file without creating it). Round 2 fixes that with `os.makedirs(MAKEFUN_OUTPUT_DIR, exist_ok=True)` before writing, tested against a fresh non-existent directory.

## How to run

```sh
python3 main.py            # writes entry.png in this directory
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png (dir created if missing)
```

Stdlib only (Python 3.13, `zlib` + `struct` for the PNG, no Pillow, no third-party imports, hand-authored 5×7 bitmap font). Deterministic: two runs produce identical bytes.

## The 38 stories (all Tuesday 24 November 2026, event or first report)

**Leads** — US markets: Nasdaq −2.0% to 23,604, S&P −1.0% to 7,168, Dow +0.2% to 49,678; Nvidia −8.3% to $151.37 a day after +31.5%; Asia: Nikkei +3.9% to 58,654, KOSPI +7.5% · Strait of Hormuz: a 4th tanker hits a mine and burns (Iran says Tue), 3 tankers ablaze earlier the same day · Huawei convicted by a Brooklyn jury on 10 of 12 counts — deceiving banks over Iran business, stealing trade secrets · Champions League: Galatasaray 1–0 Aston Villa, Bodø/Glimt 1–0 LASK, Arsenal 1–1 Borussia Dortmund, Man City 2–2 Napoli, Real Madrid 5–1 PSV (all FT).

**North America** — Trump tariff-probe findings due (Section 301, 16 partners) · US consumer confidence 103.3, best since Jan 2025 · Trump orders federal executions expedited · States sue Musk firms over Grok sexualised images · US drone helped catch El Chapo Isidro (revealed Tue).

**Europe** — Serbia school shooting in Kragujevac: 2 staff hurt, 17-year-old arrested · Sweden to vote 30 Nov on Kristersson staying PM · NATO vows space defence · 490,000 Russian war dead reported, 1,000 suicides · Pelicot shocked at nude photos promoting a book.

**Middle East** — Gaza: 6 killed in Israeli strikes; 1,675 dead since 10 Oct · Riyadh finance-district tower targeted in a "terrorist attack" · Iraq PM takes over Kurdistan border crossings after an oil-smuggling probe · Oxfam: Gaza a "toxic land".

**Asia** — China probes Politburo member Chen Jining (4th since 2025) · China extends its gallium/germanium/antimony export pause to 27 Jan 2027 · China death sentence for spying official Ma · North Korea threatens to close its Swiss diplomatic office.

**South Asia** — Nepal 5.3 quake, felt in 5 nations, no casualties · Hasina seeks return; Dhaka says come as prisoner · Bangladesh mass typhoid vaccination · India army searches after Himalayan flood.

**Africa** — ~175 migrants missing after a boat is lost off Senegal · Sudan RSF splinter defects to the army in Khartoum · Tripoli demands answers from Kyiv.

**Latin America & Caribbean** — Brazil GDP forecast cut to 1.9% · Bukele names 3 Salvadoran soldiers killed in a Haiti blast · Hippo Cove reopens after Hurricane Fiona.

**Oceania** — Australia FM Wong warns US–China rivalry is straining conflict safeguards.

**World** — UK sanctions the Houthis + 4 figures · Reuters poll: S&P seen at 8,150 by end-2027 · Thai court upholds opposition MP verdict · Indonesia candy-factory bodies found · Pope Francis diary visions.

Sources: AP, Reuters, AFP, Xinhua, Anadolu. Press time: 24 Nov 2026, 22:00 UTC.

## License

MIT — see [LICENSE](LICENSE).
