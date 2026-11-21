# The World in One Page — Saturday 21 November 2026

A one-day world-news front page for the make.fun news-image bounty.
The program draws a single 1024×1024 newspaper front page that sums
up the world's news of **Saturday 21 November 2026**: five stories in
separate panels, plus a ticker of shorter items from the same day.

## The five stories

1. **M6.9 quake shakes Peru's Andes** — a magnitude 6.9 earthquake
   struck central Peru in the early hours of Saturday (00:09 UTC);
   tremors were felt in Lima, with no damage or casualties reported
   (USGS; Korea JoongAng Daily).
2. **COP31 runs into overtime** — the Antalya climate talks missed
   their Friday deadline; a third draft was due on Saturday as France
   and Panama threatened to block any deal that drops fossil fuels.
3. **Fined $811m — the scams didn't stop** — a BBC investigation
   published on 21 November found the immigration bail business fined
   $811m for conning detained migrants kept operating under a new name.
4. **Joburg turns off the taps** — Level 2 water restrictions began
   in Johannesburg on Saturday, aiming to cut use by 200 million
   litres a day (Johannesburg Water).
5. **Home births at risk** — Australian midwives warned that private
   home-birth services could collapse when an insurance exemption
   expires on 31 December (The Guardian, first published 21 November).

## Files

- `entry.png` — the finished front page (1024×1024, RGB, under 1 MiB).
- `render.py` — draws `entry.png` with Pillow (shapes and DejaVu
  fonts only; no photos or logos). Run it with `python3 render.py`.
- `main.py` — the entrypoint. It copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`) and
  verifies the copy's SHA-256 against the original. Standard library
  only; no network access at run time.

## Verification

```sh
python3 render.py
python3 main.py          # writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR)
```

The image is 1024×1024, RGB, and under the 1 MiB limit.
