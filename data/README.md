# Datasets

The data behind the auction's built-in player pool. The app itself doesn't load these files: the pool is
baked into `index.html`. They're kept here so the pool can be checked, reused or rebuilt.

| Folder / file | What it is | Source |
| --- | --- | --- |
| `player-pool.csv` | The 742-player pool as the app ships it (players of 2013–2026): role, batting, bowling, rating, base price, category, overseas, tags, where each player comes from, IPL 2026 team and price, and IPL career numbers. It uses the column names that **Setup → Players → Import players** understands, so you can edit it and import it back. | Built by `tools/export_pool.py` |
| `ipl-auction-2026/IPL_Auction_2026_Sold_Player.csv` | The 77 players sold at the IPL 2026 auction: nationality, base price, winning bid, team, capped / uncapped. | [IPL Auction Dataset 2026](https://www.kaggle.com/datasets/sunnyyadav754/ipl-auction-dataset-2026) by Sunny Yadav, Kaggle |
| `ipl-auctions-2013-2022/eda-ipl-player-auction-dataset.ipynb` | An EDA notebook of the Kaggle *IPL Player Auction Dataset (from start to now)*. It keeps the full list of player names, but not every row. | Kaggle notebook (uploaded) |
| `ipl-auctions-2013-2022/player_names.csv` | The 543 player names from that notebook. | Extracted from the notebook |
| `ipl-dataset/` | Every IPL match from 2008 to 2026 (2026 partly): `ball_by_ball_data.csv.gz` (gzipped, 44 MB unpacked), `ipl_matches_data.csv`, `players-data-updated.csv` (batting and bowling style, full names), `teams_data.csv`, `team_aliases.csv`. | [IPL-DATASET](https://github.com/ritesh-ojha/IPL-DATASET) by Ritesh Ojha, MIT License (see the main README) |

Check each Kaggle dataset's page for its licence before reusing those files elsewhere.

## Rebuilding the pool

The scripts in `tools/` replace the `const IPL = {...}` block in `index.html`. Each one is safe to re-run.

```sh
# the earlier IPL-DATASET pool (photos, stats) lives in git history
git show 2329b58:index.html > /tmp/ipl-dataset-pool.html

python3 tools/build_pool.py data/ipl-auction-2026/IPL_Auction_2026_Sold_Player.csv /tmp/ipl-dataset-pool.html index.html
python3 tools/add_past_players.py data/ipl-auctions-2013-2022/eda-ipl-player-auction-dataset.ipynb /tmp/ipl-dataset-pool.html index.html
python3 tools/add_ipl_players.py data/ipl-dataset /tmp/ipl-dataset-pool.html index.html
python3 tools/export_pool.py index.html data/player-pool.csv
```

1. `build_pool.py`: the 77 IPL 2026 buys, rated by price.
2. `add_past_players.py`: the 2013–2022 auction players, skipping anyone already in the pool.
3. `add_ipl_players.py`: career stats from the match data, plus every other player who has played an IPL season since 2013 (players whose last season was before 2013 are left out). It uses `ipl_stats.py`, which reads the gzipped ball-by-ball file directly.
4. `export_pool.py`: refreshes `player-pool.csv`.
