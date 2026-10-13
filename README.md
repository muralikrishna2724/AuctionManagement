# AuctionManagement

A control room for running a college IPL-style player auction from one laptop. It is a single HTML file: no server, no install.

**Live site: https://auctionmanagement.vercel.app/** (Vercel, redeploys on every push). Or **open `index.html` in Chrome, Edge or Firefox.** New to running the auction? Read the 3-page [Auctioneer's guide (PDF)](docs/Auctioneer-Guide.pdf). It opens with the fixed auction ready to run: the 10 IPL franchises and the 159-player list (150 players + 5 mystery players + 4 wild cards), not started. That list stays, in this browser, until you change the players yourself in **Setup**; **Setup → Backup & reset → LOAD THE FIXED AUCTION LIST** brings it back, and **LOAD THE SAMPLE AUCTION** loads a practice auction with made-up results.

## Screenshots

A full demo run, step by step: your laptop (control room) and the big screen (projector). All 13 steps are also in one PDF: [Auction-Demo-Screenshots.pdf](docs/Auction-Demo-Screenshots.pdf).

| Control room | Projector |
| --- | --- |
| ![Start the auction](docs/screenshots/01-start.png) | ![Player revealed](docs/screenshots/05-projector-player-revealed.png) |
| ![Going once, going twice](docs/screenshots/07-control-going-twice.png) | ![Who bought the player, next one hidden](docs/screenshots/11-projector-sold-to-next-hidden.png) |

All steps:

1. [Start the auction](docs/screenshots/01-start.png)
2. [Projector before the start](docs/screenshots/02-projector-starts-soon.png)
3. [Next player on your screen only](docs/screenshots/03-control-show-player.png)
4. [Audience waits: player hidden](docs/screenshots/04-projector-first-player-hidden.png)
5. [Player revealed on the projector](docs/screenshots/05-projector-player-revealed.png)
6. [Taking bids](docs/screenshots/06-control-bidding.png)
7. [Going once, going twice](docs/screenshots/07-control-going-twice.png)
8. [The room sees the call](docs/screenshots/08-projector-going-twice.png)
9. [Close and confirm the sale](docs/screenshots/09-control-confirm-sale.png)
10. [SOLD! on the projector](docs/screenshots/10-projector-sold.png)
11. [Who bought the player, next one hidden](docs/screenshots/11-projector-sold-to-next-hidden.png)
12. [Mystery and wild card picker](docs/screenshots/12-control-surprise-picker.png)
13. [Setup: player order](docs/screenshots/13-setup-order.png)

## What it does

- **Real IPL players of 2013–2026 (741)**: the pool starts with the 77 players sold at the real IPL 2026 auction ([IPL Auction Dataset 2026](https://www.kaggle.com/datasets/sunnyyadav754/ipl-auction-dataset-2026)), with each player's base price, capped / uncapped, overseas status and the team and price they went for (shown as an “IPL 2026” badge). Ratings follow the 2026 price and the 10 biggest buys form the marquee set. After them, best rated first, come 488 players sold at the IPL auctions of 2013–2022 (marked “IPL auctions 2013–22”) and 176 more players who have played an IPL season since 2013, from AB de Villiers, Chris Gayle and Lasith Malinga to today's stars like Virat Kohli and Rohit Sharma. Only players from 2013 to 2026 are included: players whose last IPL season was before 2013 are left out. All 741 are loaded by default (725 in the main auction plus 8 mystery players and 8 wild cards); for a shorter auction, lower the number in Setup and the best rated stay in. Every player with IPL matches gets their role, batting and bowling style, career stats and special-ability tags from the 2008–2026 match data of the [IPL-DATASET](https://github.com/ritesh-ojha/IPL-DATASET). Base prices go in steps of ₹0.25 Cr (₹0.25, 0.50, 0.75, 1, 1.5, 2 Cr): the ₹0.2 and ₹0.3 Cr base prices of the source data are rounded to ₹0.25 Cr, and the unsold-round price cut rounds to ₹0.25 Cr steps too. Players marked **❓ Check role** have no matches in the data and only a guessed role; check it on the Players page. Load them in **Setup → Players** (set how many go into the main auction), or import your own list.
- **Start Auction button**: a new or reset auction waits on a start screen that shows the teams, players, purse, player order and a readiness checklist. Press **▶ START AUCTION** (or `Enter`, or the green button in the top bar) to put “THE AUCTION IS LIVE” on the projector and bring the first player onto the block. Until then, the projector shows “The auction starts soon”.
- **Projector shows the player, not the numbers**: the big screen shows the player's photo, role, batting and bowling, rating and tags; their IPL career stats stay on the auctioneer's control-room screen.
- **Next player kept hidden on the projector**: after each sale the projector shows who bought the player (photo, team and price) while the next player stays hidden behind a "Next player coming up" card. Press `Enter` (or **SHOW PLAYER ON PROJECTOR**) to reveal them, and `Enter` again to open the bidding. Turn it off in **Setup → Sets & order**.
- **Automatic bid step**: the opening bid is the player's base price. Each team button, `Space` or number key then adds **₹0.25 Cr while the bid is below ₹2 Cr** and **₹0.50 Cr once it reaches ₹2 Cr** (… ₹1.75 Cr → ₹2 Cr → ₹2.5 Cr → ₹3 Cr …). The bid panel shows both steps and highlights the one in use. There are no other raise or custom-amount buttons.
- **Control room**: the player on the block, current bid, one-click team bids, SOLD / UNSOLD / UNDO / PASS, team purses, the next-players queue and a live feed, all on one screen.
- **Manual bid close**: there is no countdown timer. The auctioneer closes each player by hand: click the **BIDDING** box (or press `G`) to call *going once*, then *going twice*, then close. Closing sells to the highest bidder, or marks the player unsold if nobody bid. Any new bid reopens the bidding. The projector shows each call.
- **Auction in 4 sets, exact 7-player squads**: **Setup → Players → 🗂 Auction in 4 sets** builds the auction as four role sets: batters, all-rounders, wicketkeepers and bowlers. By default every team buys exactly 7 players: 1 wicketkeeper, 2 batters, 2 all-rounders and 2 bowlers. Each set holds enough players for every team to fill that role (2 batters × 10 teams = 20, and so on) plus spare players, best rated first from the 741: by default the auction has 150 players, and the 80 spare places are shared between the sets in proportion to each role's need (23 batters, 23 all-rounders, 11 wicketkeepers, 23 bowlers). The 5 mystery players and 4 wild cards come on top, so the auction has 159 players. With **Exact squads** on (the default), building the sets sets the minimum and maximum squad to 7 and each role's minimum and maximum to the plan, so a team can't buy a third batter or a second wicketkeeper. The Indian players in each set alone cover every team's need for that role, and each set gets only its share of the 40 overseas players that 10 teams × 4 can buy, so the default 159 players are 120 Indian and 39 overseas, and a team at its overseas limit can always finish its squad. The mystery players and wild cards are spread over the sets, so every set has some, and they still pop in by surprise: they are spaced over the squad places still open, and the next one comes from the role with the fewest places left, so all of them come up while a team can still buy them (in 60 simulated random-order auctions, all 9 came up every time). Once no team can buy a player any more (every squad has its 2 batters, say), the rest of that set is passed over automatically instead of coming up one by one, and the feed and a message say how many were passed over. Every build picks the same ones, so a printed player list stays correct; to change them, select players on the Players page and mark them mystery, wild card or normal. All of them come up, even if the queue runs out first. A bid is blocked if it would leave the team no room for its role minimums, or take a player of a role that other teams still need when too few are left (counting only Indian players for a team at its overseas limit). The Setup table shows the Indian / overseas split and confirms every team can fill its squad. In 60 simulated auctions (with an unsold round), every team ended with exactly 7 players in the right roles and the overseas limit met, in about 1 h 30 min plus the unsold round. Turn **Exact squads** off for a plan where teams buy at least the plan and up to one more per role. The sets only decide who is in the auction: players come up **at random from the whole list**, or the auctioneer picks each one. Switch between the two with **🎲 Random / ✋ I pick** above the queue in the control room (or in Setup → Sets & order); in both modes `K` picks a player and `N` brings a random one.
- **Surprises spread through the whole auction**: the gap to the next mystery player or wild card follows how many players and surprises are left (give or take a quarter), so with the 4 sets they turn up in every set, about every 20 players, right to the bowlers. Turn it off in **Setup → Surprises** to use a fixed gap instead.
- **How long it will take**: the 4-set card in Setup estimates the auction's length (159 players at 60 s each is about 2 h 40 min at most, plus breaks and the unsold round) and how much fewer spare players would save. During the auction the top bar shows the time left and the expected finish (⏱ 2 h 38 min · ends ~17:30), from the actual pace of the last results.
- **Choose your own player list**: in **Setup → Players → ✅ CHOOSE PLAYERS**, set how many players to keep, fill the list with the best rated or at random (filter by role, by source — IPL 2026 auction, auctions 2013–22, other IPL players — or Indian / overseas to build it role by role, say 40 batters then 40 bowlers), and tick or untick anyone. **LOAD** puts exactly those players in the auction, with the mystery players and wild cards drawn from your list. The ticked list is remembered in the browser.
- **Change the player on the block**: the **🔄 CHANGE PLAYER** button on the auctioneer's player card swaps in a different player (search, pick, or 🎲 random) as long as nobody has bid yet. The player taken off goes back into the queue at a random place in the same set, so they don't come straight back. For a mystery player or wild card it opens the surprise picker to swap in another one.
- **Pick the next player yourself**: press `K` (or **🔍 Pick** above the queue) to search the waiting players by name, role or set, sort them by rating or base price, and put one on the block; **🎲 RANDOM PLAYER** brings a random one. It works in every order mode. Choose **The auctioneer picks each player** in **Setup → Sets & order** and the block waits for your pick (`K`) or a random one (`N`) after every result, while mystery players and wild cards still pop in by themselves.
- **Random order**: players pop up at random instead of one after another. In **Setup → Sets & order** you can switch to random within each set, or back to the fixed set-by-set order. The 🔀 button in the control room reshuffles the queue. While the order is random, the projector doesn't show who is coming up.
- **Surprises**: every few players, at random, a mystery player or a wild card pops into the auction on its own. Mystery players get clues written from their own IPL stats. Teams bid on the clues alone: the projector reveals the player **only when a team buys them** (an unsold mystery player stays hidden), while the control room always shows the auctioneer who it is. Set how often surprises happen, and how many of each, in **Setup → Surprises**.
- **Handler control over surprises**: the 🎲 box in the control room shows only the auctioneer who pops in next. Click it to pick a different mystery or wild card player, turn any available player into one, take a fresh random pick, or **pop one in now**. While a surprise player is on the block and nobody has bid yet, the same box swaps them for someone else, and the first player goes back to the surprise pool.
- **Budget safety**: blocks bids over a team's purse or past its squad, overseas or role limits, or that would leave other teams short of a role they still need, and warns about low purses and unmet role minimums.
- **The 10 IPL franchises as teams**: Chennai Super Kings, Delhi Capitals, Gujarat Titans, Kolkata Knight Riders, Lucknow Super Giants, Mumbai Indians, Punjab Kings, Rajasthan Royals, Royal Challengers Bengaluru and Sunrisers Hyderabad. Their names and codes (CSK, DC, GT, KKR, LSG, MI, PBKS, RR, RCB, SRH) are fixed; in **Setup → Event & teams** you fill in each team's owner / manager, and can change its colour or upload a logo you have permission to use. Auctions saved by older versions take the franchise names in order and keep their owners, purses and players.
- **Animations and sound effects**: each big moment has its own look and sound, made in the page with no sound files. **SOLD**: three gavel knocks, a crowd cheer and a brass fanfare, with spinning gold rays, shockwave rings and confetti in the buying team's colours (a mystery player gets a rising reveal first). **New player**: a swoosh and a stadium chime as a light sweeps across the projector, a gold ring pulses out of the photo and the name glows. **Mystery player**: a dark drone, a heartbeat and an unresolved question motif, over purple fog, scanlines, a glitching, heart-beating "?" and drifting question marks. **Wild card**: a drum-and-beep 3-2-1 with an orange flash on every count, then a riser, a big impact and a power chord as the card flips in with sparks and spinning rays. Unsold gets a sad trombone. The sound plays from the control-room laptop (turn it on or off with 🔊 in the top bar), and the motion is reduced when the computer asks for less motion.
- **No Right to Match**: RTM isn't used in this auction; every player goes to the highest bidder.
- **Event logo**: upload your college or event logo in **Setup → Event & teams** and it shows on the projector (top bar and the “starts soon” screen). Use a logo you have permission to use.
- **Projector view**: press `V`, or open the page in a second window with `#projector` at the end of the address.
- **Corrections**: change a team or price, re-auction, send to the unsold pool, adjust purses, restore an earlier state. Nothing is deleted from the history.
- **Reports and judging**: team reports, auction statistics, a judging panel out of 100, and fun awards.
- **Exports**: CSV, Excel and PDF. Excel and PDF need internet the first time.

## Keyboard shortcuts

| Key | Action |
| --- | --- |
| `Space` | Next bid (the other team in a bidding war comes back in) |
| `1`–`9`, `0` | Bid for teams 1–10 |
| `G` | Going once → going twice → close the bidding |
| `S` / `U` | Sold / unsold |
| `R` | Undo |
| `N` / `P` | Next / previous player (`N` brings a random one when you pick players yourself) |
| `K` | Pick the next player yourself |
| `M` | Mystery player on the block: show the next clue (revealed when sold) |
| `X` | Pass |
| `A` | Breaking news alert |
| `V` / `F` | Projector view / full screen |
| `Enter` | Start the auction, show the next player on the projector, open the bidding, or confirm |
| `Esc` | Cancel |

## Saving

Every action saves instantly in the browser the auction runs in, and the auction comes back after a refresh or a crash. Everything (the auction, the undo history, saved photos and photo lookups) is kept in the browser's IndexedDB database, which has room for hundreds of MB, not the 5 MB of localStorage; data from older versions is moved over automatically, and the app asks the browser to keep it permanently. **Setup → Backup & reset** shows how much space it uses. If a browser blocks IndexedDB (some private windows), the app falls back to localStorage and says so. That storage belongs to one browser on one laptop, so use **Export backup** (in Setup → Backup & reset, or Reports) before the event and at breaks. **Restore backup** loads it on any machine.

## Player photos

Photos need internet. The app tries the dataset's image link first, then a photo from Wikipedia found by the player's name; players with neither show their initials. Before the event, open **Players** (or **Setup → Players**) and press **📷 SAVE PHOTOS OFFLINE** once while online. Every photo it finds is saved inside the auction, so it shows without internet and is included in **Export backup**. Add any missing photos with **BULK PHOTOS** or **Edit player**.

## Importing your own players

Use a CSV or Excel file with a header row. Recognised columns: Player ID, Name, Role, Batting, Bowling, Rating, Base Price, Category, Overseas, Tags, Mystery, Wild Card, Set, Clues, Photo URL. Separate several tags or clues with `|`. **Players → CSV template** downloads an example file.

## Data credits

All the source datasets are in [`data/`](data/), with [`data/player-pool.csv`](data/player-pool.csv) (the whole 741-player pool as a spreadsheet you can edit and import back) and the steps to rebuild the pool.


The auction player list (names, nationality, base price, winning bid, team, capped / uncapped) comes from the [IPL Auction Dataset 2026](https://www.kaggle.com/datasets/sunnyyadav754/ipl-auction-dataset-2026) by Sunny Yadav on Kaggle; check its page for the licence before reusing it. Ratings are calculated from the winning bid. Roles, career stats, photo links and tags for players with IPL history come from the [IPL-DATASET](https://github.com/ritesh-ojha/IPL-DATASET) by Ritesh Ojha (2024 player details, match line-ups and ball-by-ball data). The players from the IPL auctions of 2013–2022 come from the player list in an EDA notebook of the IPL Player Auction Dataset (from start to now) on Kaggle; that notebook only keeps the names, so their roles, overseas status and ratings come from the IPL-DATASET where they appear and were otherwise added by hand (`tools/add_past_players.py`). Career stats, batting hand, bowling style and roles for players without them, and the 176 other IPL players of 2013–2026, come from the IPL-DATASET match files (ball-by-ball data for 2008–2026, `tools/ipl_stats.py` and `tools/add_ipl_players.py`); their ratings are worked out from career runs, wickets, strike rate, economy and matches played, and their overseas status was added by hand. Roles for some 2026 newcomers were also added by hand; players without a confirmed role are marked “❓ Check role”.

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
