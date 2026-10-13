"""Build the auction's built-in player pool from the IPL 2026 auction list (Kaggle) plus IPL-DATASET stats.

Usage: python3 tools/build_pool.py IPL_Auction_2026_Sold_Player.csv <html with the IPL-DATASET pool> index.html
The second file is any older index.html whose `const IPL = {...}` still holds the IPL-DATASET players (git history
before the switch); roles, stats, photos and tags are matched from it by exact name or a known spelling variant.
Add confident roles for new players to KNOWN; anyone else is marked "Check role".
"""
import csv, json, re, sys, math
SRC_CSV, OLD_HTML, OUT_HTML = sys.argv[1], sys.argv[2], sys.argv[3]
pat = re.compile(r'^const IPL = (\{.*?\});$', re.M)
I = json.loads(pat.search(open(OLD_HTML, encoding='utf-8').read()).group(1))
nk = lambda x: re.sub(r'[^a-z]', '', x.lower())
old = {nk(p['n']): p for p in I['players']}
ALIAS = {'Lungisani Ngidi': 'Lungi Ngidi', 'Pravin Dubey': 'Praveen Dubey'}   # same player, different spelling
KNOWN = {
 'Kartik Sharma': ('WK', '', ''), 'Prashant Veer': ('AR', '', 'left-arm orthodox'), 'Akeal Hosein': ('BOWL', 'L', 'left-arm orthodox'),
 'Matthew Short': ('AR', 'R', 'right-arm offbreak'), 'Zak Foulkes': ('AR', '', 'right-arm medium-fast'), 'Sarfaraz Khan': ('BAT', 'R', ''),
 'Aman Khan': ('AR', '', 'right-arm medium'), 'Auqib Dar': ('BOWL', '', 'right-arm medium'), 'Pathum Nissanka': ('BAT', 'R', ''),
 'Kyle Jamieson': ('BOWL', 'R', 'right-arm fast'), 'Ben Duckett': ('BAT', 'L', ''),
 'Jason Holder': ('AR', 'R', 'right-arm fast-medium'), 'Tom Banton': ('BAT', 'R', ''), 'Finn Allen': ('BAT', 'R', ''),
 'Tim Seifert': ('WK', 'R', ''), 'Josh Inglis': ('WK', 'R', ''), 'Ben Dwarshuis': ('BOWL', 'L', 'left-arm fast-medium'),
 'Cooper Connolly': ('AR', 'L', 'left-arm orthodox'), 'Adam Milne': ('BOWL', 'R', 'right-arm fast'), 'Jacob Duffy': ('BOWL', 'R', 'right-arm fast-medium'),
 'Jordan Cox': ('WK', 'R', ''), 'Jack Edwards': ('AR', '', 'right-arm medium'), 'Vignesh Puthur': ('BOWL', '', 'left-arm wrist-spin'),
 'Akshat Raghuwanshi': ('BAT', '', ''), 'Naman Tiwari': ('BOWL', '', 'left-arm fast-medium'), 'Prithviraj Yarra': ('BOWL', '', 'left-arm fast-medium'),
}
lakh = lambda v: round(int(re.sub(r'[^0-9]', '', v)) / 100000)
recs = []
for r in csv.DictReader(open(SRC_CSV, encoding='utf-8-sig')):
    name = re.sub(r'\s+', ' ', r['Name']).strip()
    p = old.get(nk(ALIAS.get(name, name)))
    recs.append(dict(name=name, team=r['TeamName'].strip(), win=lakh(r['Winning Bid in Rs']), base=lakh(r['BasePrices in Rs']),
                     os=r['Nationality'].strip() == 'Overseas', cap=r['Capped/UnCapped'].strip(), old=p))
wmin, wmax = min(x['win'] for x in recs), max(x['win'] for x in recs)
rate = lambda w: round(62 + 34 * math.log(w / wmin) / math.log(wmax / wmin)) if wmax > wmin else 75
recs.sort(key=lambda x: -x['win'])
out, unsure, matched = [], [], 0
for i, x in enumerate(recs):
    p = x['old']
    e = {'n': x['name'], 'sn': x['name'], 'cid': p['cid'] if p else 0, 'rt': rate(x['win']), 'bp': max(25, round(x['base'] / 25) * 25), 'os': 1 if x['os'] else 0,
         'cat': 'Marquee' if i < 10 else ('Capped' if x['cap'] == 'Capped' else 'Uncapped'),
         'img': p['img'] if p else '', 'dob': p.get('dob', '') if p else '', 's26': {'t': x['team'], 'p': x['win']}}
    if p:
        matched += 1
        e.update({'r': p['r'], 'bat': p['bat'], 'bowl': p['bowl'], 'bk': p['bk'], 'tg': p['tg'][:], 'st': p['st']})
    else:
        k = KNOWN.get(x['name'])
        if k:
            spin = any(w in k[2] for w in ('orthodox', 'spin', 'break'))
            e.update({'r': k[0], 'bat': k[1], 'bowl': k[2], 'bk': 'spin' if spin else ('pace' if k[2] else ''), 'tg': []})
        else:
            e.update({'r': 'AR', 'bat': '', 'bowl': '', 'bk': '', 'tg': ['❓ Check role']}); unsure.append(x['name'])
        e['st'] = None
    out.append(e)
I['players'] = out
html = open(OUT_HTML, encoding='utf-8').read()
m = pat.search(html)
html = html[:m.start()] + 'const IPL = ' + json.dumps(I, ensure_ascii=False, separators=(',', ':')) + ';' + html[m.end():]
open(OUT_HTML, 'w', encoding='utf-8').write(html)
print('players', len(out), '| matched to IPL stats', matched, '| role from known list', len(out) - matched - len(unsure), '| check role', len(unsure))
print('check role:', ', '.join(unsure))
