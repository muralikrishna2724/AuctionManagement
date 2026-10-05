# AuctionManagement

A control room for running a college IPL-style player auction from one laptop. It is a single HTML file: no server, no install.

**Open `index.html` in Chrome, Edge or Firefox.** It starts with a practice auction: 8 made-up college teams bidding for real IPL players, about 40 players in. Clear it with the **SAMPLE DATA** button, or in **Setup → Backup & reset**.

## What it does

- **Real IPL players**: the player pool comes from the [IPL-DATASET](https://github.com/ritesh-ojha/IPL-DATASET), with career stats from IPL 2008–2026 on every player card and on the projector. Ratings, roles, base prices and special-ability tags are calculated from the numbers, with recent seasons counting most. Load any number of them in **Setup → Players**, or import your own list.
- **Control room**: the player on the block, current bid, one-click team bids, SOLD / UNSOLD / UNDO / PASS / RTM, team purses, the next-players queue and a live feed, all on one screen.
- **Manual bid close**: there is no countdown timer. The auctioneer closes each player by hand: click the **BIDDING** box (or press `G`) to call *going once*, then *going twice*, then close. Closing sells to the highest bidder, or marks the player unsold if nobody bid. Any new bid reopens the bidding. The projector shows each call.
- **Random order**: players pop up at random instead of one after another. In **Setup → Sets & order** you can switch to random within each set, or back to the fixed set-by-set order. The 🔀 button in the control room reshuffles the queue. While the order is random, the projector doesn't show who is coming up.
- **Surprises**: every few players, at random, a mystery player or a wild card pops into the auction on its own. Mystery players get clues written from their own IPL stats; the clues and the reveal can run by themselves. Set how often surprises happen, and how many of each, in **Setup → Surprises**.
- **Handler control over surprises**: the 🎲 box in the control room shows only the auctioneer who pops in next. Click it to pick a different mystery or wild card player, turn any available player into one, take a fresh random pick, or **pop one in now**. While a surprise player is on the block and nobody has bid yet, the same box swaps them for someone else, and the first player goes back to the surprise pool.
- **Budget safety**: blocks bids over a team's purse or past its squad, overseas or role limits, and warns about low purses and unmet role minimums.
- **Right to Match**, with an optional final raise. Teams named after an IPL franchise (for example CSK or Mumbai Indians) get the RTM for that franchise's last players.
- **Projector view**: press `V`, or open the page in a second window with `#projector` at the end of the address.
- **Corrections**: change a team or price, re-auction, send to the unsold pool, adjust purses, restore an earlier state. Nothing is deleted from the history.
- **Reports and judging**: team reports, auction statistics, a judging panel out of 100, and fun awards.
- **Exports**: CSV, Excel and PDF. Excel and PDF need internet the first time.

## Keyboard shortcuts

| Key | Action |
| --- | --- |
| `Space` | Next bid (the other team in a bidding war comes back in) |
| `1`–`9`, `0` | Bid for teams 1–10 |
| `Shift+1`–`5` | Bid for teams 11–15 |
| `G` | Going once → going twice → close the bidding |
| `S` / `U` | Sold / unsold |
| `R` | Undo |
| `N` / `P` | Next / previous player |
| `M` / `Shift+M` | Mystery player on the block: next clue / reveal now |
| `T` | Right to Match |
| `C` | Custom bid |
| `X` | Pass |
| `A` | Breaking news alert |
| `V` / `F` | Projector view / full screen |
| `Enter` / `Esc` | Confirm / cancel |

## Saving

Every action saves instantly in the browser the auction runs in, and the auction comes back after a refresh or a crash. That storage belongs to one browser on one laptop, so use **Export backup** (in Setup → Backup & reset, or Reports) before the event and at breaks. **Restore backup** loads it on any machine.

## Importing your own players

Use a CSV or Excel file with a header row. Recognised columns: Player ID, Name, Role, Batting, Bowling, Rating, Base Price, Category, Overseas, Tags, Mystery, Wild Card, Set, RTM Team, Clues, Photo URL. Separate several tags or clues with `|`. **Players → CSV template** downloads an example file.

## Data credits

Player data comes from the [IPL-DATASET](https://github.com/ritesh-ojha/IPL-DATASET) by Ritesh Ojha: the 2024 player details, match line-ups and ball-by-ball data. Stats are aggregated from it; ratings, roles, base prices and tags are calculated by this app. The dataset has no nationality column, so overseas players were marked by name. Player photos load from the image links listed in the dataset.

The dataset is published under the MIT License:

```
The MIT License (MIT)

Copyright (c) 2022 Ritesh Ojha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
