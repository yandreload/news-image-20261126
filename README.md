# The World in One Day — Thursday 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/yandreload/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/yandreload/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Entry for the make.fun bounty
[Sum up 26 November's world news in one image](https://make.fun/bounty/news-image-20261126)
($100 USDC, 50 paid places, closes Sat 28 Nov 2026 07:00 WIB).

## The image

A 1024×1024 newspaper front page, "THE WORLD IN ONE DAY", summing up
Thursday 26 November 2026 in six stories plus an "also today" ticker:

- **Lead — North Korea:** Kim Jong Un orders wider deployment of
  tactical nuclear weapons and declares the North's nuclear status
  "absolutely inviolable" (KCNA, reported Thursday).
- **Trade:** Trump unveils new tariffs on 14 partners — China up to
  40%, the EU 15% — aimed at factory overcapacity.
- **Ukraine:** Kyiv says it struck a Russian air base, damaging
  five planes.
- **U.S. courts:** a second judge blocks Trump's birthright
  citizenship order.
- **Egypt:** a fuel tanker crash ignites a huge fire near Cairo,
  killing at least 30.
- **Culture:** Duran Duran guitarist Andy Taylor dies at 65.
- **Also today:** Norway's court voids oil licences; Kenya's last
  Ebola patient goes home; Gukesh–Sindarov chess Game 2 drawn;
  Thanksgiving in the US.

Every story is dated on the image or in [SOURCES.md](SOURCES.md).

## How it is built

- `generate.py` — the build tool (Python 3 + Pillow). It draws the
  whole front page from the fixed story text in the file and writes
  `entry.png`. Run it to rebuild the image.
- `entry.png` — the committed entry image, 1024×1024, under 1 MiB.
- `main.py` — the entrypoint (Python 3.13, standard library only). It
  copies `entry.png` to `/output/entry.png`. No network, no
  randomness: two runs write identical bytes.

## Run it

```sh
python3 generate.py   # rebuild entry.png from the story text
python3 main.py       # writes /output/entry.png
```

## Verify

```sh
python3 main.py && sha256sum /output/entry.png
python3 main.py && sha256sum /output/entry.png   # same hash
python3 -c "from PIL import Image; im = Image.open('/output/entry.png'); print(im.size, im.format)"
```

## License

MIT — see [LICENSE](LICENSE).
