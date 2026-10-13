"""Write the auction's built-in player pool (the `const IPL = {...}` block in index.html) to a CSV.

Usage: python3 tools/export_pool.py index.html data/player-pool.csv
The CSV uses the columns the app's Import players understands (Name, Role, Batting, Bowling, Rating, Base Price,
Category, Overseas, Tags), plus where each player comes from and their IPL numbers.
"""
import csv, json, re, sys
SRC, OUT = sys.argv[1], sys.argv[2]
I = json.loads(re.search(r'^const IPL = (\{.*?\});$', open(SRC, encoding='utf-8').read(), re.M).group(1))
ROLE = {'BAT': 'Batter', 'BOWL': 'Bowler', 'AR': 'All-rounder', 'WK': 'Wicketkeeper'}
cols = ['Name', 'Role', 'Batting', 'Bowling', 'Rating', 'Base Price (Cr)', 'Category', 'Overseas', 'Tags', 'Source',
        'IPL 2026 Team', 'IPL 2026 Price (Cr)', 'IPL Matches', 'IPL Runs', 'Strike Rate', 'IPL Wickets', 'Economy',
        'First Season', 'Last Season', 'Last IPL Team', 'Photo URL']
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(cols)
    for p in I['players']:
        s = p.get('st') or {}
        src = 'IPL 2026 auction' if p.get('s26') else 'IPL auctions 2013-22' if p.get('pa') else 'IPL player 2013-26'
        w.writerow([p['n'], ROLE.get(p['r'], p['r']), {'L': 'Left Hand', 'R': 'Right Hand'}.get(p['bat'], ''), p['bowl'], p['rt'],
                    p['bp'] / 100, p['cat'], 'Yes' if p['os'] else 'No', '|'.join(t for t in p['tg'] if not t.startswith('❓')), src,
                    (p.get('s26') or {}).get('t', ''), (p['s26']['p'] / 100) if p.get('s26') else '',
                    s.get('m', ''), s.get('runs', ''), round(100 * s['runs'] / s['bf'], 1) if s.get('bf') else '',
                    s.get('wk', ''), round(6 * s['rc'] / s['balls'], 2) if s.get('balls') else '',
                    s.get('from', ''), s.get('to', ''), s.get('team', ''), (I['img'] + p['img']) if p.get('img') else ''])
print('players', len(I['players']), '->', OUT)
