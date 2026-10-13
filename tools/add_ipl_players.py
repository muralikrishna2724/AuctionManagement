"""Fill in and extend the built-in pool from the IPL-DATASET match files (2008-2026 ball-by-ball data).

Usage: python3 tools/add_ipl_players.py data/ipl-dataset <html with the IPL-DATASET pool> index.html
(the folder holds ball_by_ball_data.csv[.gz], ipl_matches_data.csv, players-data-updated.csv and teams_data.csv)

1. Players in the pool without career stats (IPL 2026 newcomers and the 2013-2022 auction players typed in by hand)
   get their stats, batting hand and bowling style from the match data; their role is worked out from the stats.
2. Every other player who has played in the IPL and is not in the pool yet is added after them (ip: 1), with a
   rating worked out from career numbers. Players who were in the earlier IPL-DATASET pool (the second file, any
   older index.html from git history) come with that entry: photo link, later stats, rating and tags. The match data
   has no nationality, so overseas players are listed in OVERSEAS below.
Players who already have stats keep them (they came from a later copy of the same dataset). Safe to re-run.
"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ipl_stats

DATA, OLD_HTML, OUT_HTML = sys.argv[1], sys.argv[2], sys.argv[3]
pat = re.compile(r'^const IPL = (\{.*?\});$', re.M)
nk = lambda x: re.sub(r'[^a-z]', '', x.lower())
tk = lambda x: [t for t in re.sub(r'[^a-z ]', ' ', x.lower()).split() if t]

# pool name -> dataset name, where the automatic match is wrong or missing (None = not in the match data)
MATCH = {
 'Finn Allen': 'FH Allen', 'Praveen Kumar': 'P Kumar', 'Chris Green': 'CJ Green', 'Albie Morkel': 'JA Morkel', 'Brad Hogg': 'GB Hogg',
 'Gurkeerat Mann': 'Gurkeerat Singh', 'Hardus Viljoen': 'GC Viljoen', 'Rusty Theron': 'J Theron', 'Mujeeb Zadran': 'Mujeeb Ur Rahman',
 'Rassie van der Dussen': 'HE van der Dussen', 'Auqib Dar': 'Auqib Nabi', 'Iqbal Abdullah': 'Iqbal Abdulla', 'Prasanth Padmanabhan': 'P Prasanth',
 'Anirudha Srikkanth': 'S Anirudha', 'Sanjay Yadav': 'R Sanjay Yadav', 'Monu Singh': 'Monu Kumar', 'Wanindu Hasaranga': 'PWH de Silva',
 'Domnic Muthuswamy': 'DJ Muthuswami', 'Parveez Rasool': 'Parvez Rasool', 'Subhranshu Senapati': 'Subhransu Senapati',
 'Shubham Agrawal': 'SS Agarwal', 'Ankeet Bawane': 'AR Bawne', 'Navdeep Saini': 'Navdeep Saini',
 'Mangesh Yadav': None, 'Amit Kumar': None, 'Zahir Khan': None, 'Jatin Saxena': None, 'Manan Sharma': None, 'Ramesh Kumar': None,
 'Saurabh Dubey': None, 'Syed Mehdi Hasan': None, 'Ansh Patel': None, 'Sagar Trivedi': None, 'Pratham Singh': None, 'Pratyush Singh': None,
 'Kshitiz Sharma': None, 'Anunay Singh': None, 'Saurabh Kumar': None, 'HS Sharath': None, 'Jack Edwards': None, 'Akshat Raghuwanshi': None,
}
SKIP = {'Arshad Khan (2)', 'NA Saini'}   # second records of players already in the pool
OVERSEAS = set("""AB de Villiers|SP Narine|Sohail Tanvir|PD Salt|RD Rickelton|Umar Gul|ML Hayden|CK Langeveldt|Azhar Mahmood|LMP Simmons|
MF Maharoof|AD Mascarenhas|DE Bollinger|AC Gilchrist|A Symonds|CRD Fernando|HM Amla|ST Jayasuriya|RJ Harris|E Malinga|SK Warne|WPUJC Vaas|
WG Jacks|J Fraser-McGurk|T Stubbs|RE van der Merwe|KC Sangakkara|Naveen-ul-Haq|T Thushara|PD Collingwood|JR Hopes|SM Pollock|DPMD Jayawardene|
DL Vettori|IS Sodhi|MN van Wyk|AB McDonald|AM Ghazanfar|DJ Hussey|YA Abdulla|SW Tait|RR Rossouw|Shahid Afridi|SE Bond|MG Bracewell|
Kamran Akmal|TM Dilshan|W O'Rourke|GD McGrath|GC Smith|HH Gibbs|MJ Lumb|CL White|D Ferreira|J Overton|KMDN Kulasekara|OA Shah|AC Thomas|
Rahmanullah Gurbaz|Sikandar Raza|B Lee|JE Taylor|BJ Rohrer|JL Pattinson|SD Hope|N Burger|Salman Butt|J Little|SM Katich|M Ntini|SM Harwood|
JEC Franklin|G Coetzee|N Thushara|A Flintoff|LJ Wright|SB Styris|AC Voges|MN Samuels|Azmatullah Omarzai|Mohammad Asif|JG Bethell|UT Khawaja|
BKG Mendis|MV Boucher|HC Brook|SP Fleming|S Randiv|PHKD Mendis|C Bosch|JJ van der Wath|BJ Haddin|DJ Harris|Misbah-ul-Haq|Sediqullah Atal|
AU Rashid|LPC Silva|LA Carseldine|XC Bartlett|RJW Topley|DNT Zoysa|TR Birt|LE Plunkett|GHS Garton|T Shamsi|RR Sarwan|RE Levi|SH Johnson|
RJ Gleeson|RJ Quiney|DJ Jacobs|M Klinger|Mohammad Hafeez|KT Maphaka|V Viyaskanth|T Kohler-Cadmore|T Taibu|AB Barath|CJ Ferguson|DAJ Bracewell|
MP Breetzke|GF Linde|MD Shanaka|Gulbadin Naib|Shoaib Malik|GR Napier|DR Martyn|AA Noffke|PWA Mulder|DS Lehmann|L Ronchi|DJ Thornely|JM Kemp|
RJ Peterson|D Jansen|JE Root|B Geeves|S Chanderpaul|CK Kapugedera|Younis Khan|T Henderson|D du Preez|Mohammad Ashraful|KAJ Roach|TD Paine|
MJ Owen|D Madushanka|SSB Magala|Liton Das|KA Maharaj|LB Williams|Shoaib Akhtar|Mashrafe Mortaza|NJ Rimmington|RW Price|MG Neser|Karim Janat|
B Muzarabani|LG Pretorius|CJ Dala|SC Kuggeleijn|S Joseph|Abdur Razzak|A Nel|DA Payne""".replace('\n', '').split('|'))
NAME = {   # dataset name -> the name people know the player by (default: the dataset's own spelling)
 'RA Jadeja': 'Ravindra Jadeja', 'RG Sharma': 'Rohit Sharma', 'SP Narine': 'Sunil Narine', 'SK Raina': 'Suresh Raina', 'PD Salt': 'Phil Salt',
 'AB de Villiers': 'AB de Villiers', 'MS Dhoni': 'MS Dhoni', 'WPUJC Vaas': 'Chaminda Vaas', 'CRD Fernando': 'Dilhara Fernando',
 'DPMD Jayawardene': 'Mahela Jayawardene', 'KC Sangakkara': 'Kumar Sangakkara', 'ST Jayasuriya': 'Sanath Jayasuriya', 'SR Tendulkar': 'Sachin Tendulkar',
 'SK Warne': 'Shane Warne', 'ML Hayden': 'Matthew Hayden', 'AC Gilchrist': 'Adam Gilchrist', 'HM Amla': 'Hashim Amla', 'RJ Harris': 'Ryan Harris',
 'E Malinga': 'Eshan Malinga', 'WG Jacks': 'Will Jacks', 'RE van der Merwe': 'Roelof van der Merwe', 'Naveen-ul-Haq': 'Naveen-ul-Haq',
 'T Thushara': 'Thilan Thushara', 'PD Collingwood': 'Paul Collingwood', 'JR Hopes': 'James Hopes', 'SM Pollock': 'Shaun Pollock',
 'SC Ganguly': 'Sourav Ganguly', 'R Dravid': 'Rahul Dravid', 'DL Vettori': 'Daniel Vettori', 'SK Trivedi': 'Siddharth Trivedi', 'IS Sodhi': 'Ish Sodhi',
 'Nithish Kumar Reddy': 'Nitish Kumar Reddy', 'DJ Hussey': 'David Hussey', 'SW Tait': 'Shaun Tait', 'RR Rossouw': 'Rilee Rossouw',
 'Shahid Afridi': 'Shahid Afridi', 'Azhar Mahmood': 'Azhar Mahmood', 'Sikandar Raza': 'Sikandar Raza', 'S Sreesanth': 'S Sreesanth',
 'TM Dilshan': 'Tillakaratne Dilshan', 'MG Bracewell': 'Michael Bracewell', 'GD McGrath': 'Glenn McGrath', 'GC Smith': 'Graeme Smith',
 'HH Gibbs': 'Herschelle Gibbs', 'CL White': 'Cameron White', 'KMDN Kulasekara': 'Nuwan Kulasekara', 'MF Maharoof': 'Farveez Maharoof',
 'LMP Simmons': 'Lendl Simmons', 'DE Bollinger': 'Doug Bollinger', 'AD Mascarenhas': 'Dimitri Mascarenhas', 'CK Langeveldt': 'Charl Langeveldt',
 'MN van Wyk': 'Morne van Wyk', 'AB McDonald': 'Andrew McDonald', 'VY Mahesh': 'Yo Mahesh', 'Harmeet Singh': 'Harmeet Singh', 'SE Bond': 'Shane Bond',
 'PC Valthaty': 'Paul Valthaty', 'OA Shah': 'Owais Shah', 'AC Thomas': 'Alfonso Thomas', 'JE Taylor': 'Jerome Taylor', 'MV Boucher': 'Mark Boucher',
 'SP Fleming': 'Stephen Fleming', 'S Randiv': 'Suraj Randiv', 'AL Menaria': 'Ashok Menaria', 'RR Powar': 'Ramesh Powar',
 'JJ van der Wath': 'Johan van der Wath', 'Misbah-ul-Haq': 'Misbah-ul-Haq', 'K Kartikeya': 'Kumar Kartikeya', 'DB Ravi Teja': 'Ravi Teja',
 'BJ Haddin': 'Brad Haddin', 'LPC Silva': 'Chamara Silva', 'VVS Laxman': 'VVS Laxman', 'DNT Zoysa': 'Nuwan Zoysa', 'MD Shanaka': 'Dasun Shanaka',
 'Younis Khan': 'Younis Khan', 'D Madushanka': 'Dilshan Madushanka', 'BKG Mendis': 'Kusal Mendis', 'PHKD Mendis': 'Kamindu Mendis',
 'KB Arun Karthik': 'Arun Karthik', 'Y Gnaneswara Rao': 'Gnaneswara Rao', 'AUK Pathan': 'Asad Pathan', 'PVSN Raju': 'Satyanarayana Raju',
 'T Stubbs': 'Tristan Stubbs', 'B Lee': 'Brett Lee', 'A Symonds': 'Andrew Symonds', 'A Kumble': 'Anil Kumble', 'Umar Gul': 'Umar Gul',
 'S Aravind': 'Sreenath Aravind', 'A Singh': 'Amit Singh', 'A Flintoff': 'Andrew Flintoff', 'AB Agarkar': 'Ajit Agarkar', 'M Kaif': 'Mohammad Kaif',
 'W Jaffer': 'Wasim Jaffer', 'A Chopra': 'Aakash Chopra', 'T Shamsi': 'Tabraiz Shamsi', 'KA Maharaj': 'Keshav Maharaj', 'AU Rashid': 'Adil Rashid',
 'JE Root': 'Joe Root', 'HC Brook': 'Harry Brook', 'UT Khawaja': 'Usman Khawaja', 'SD Hope': 'Shai Hope', 'JL Pattinson': 'James Pattinson',
 'G Coetzee': 'Gerald Coetzee', 'N Thushara': 'Nuwan Thushara', 'MN Samuels': 'Marlon Samuels', 'SB Styris': 'Scott Styris', 'AC Voges': 'Adam Voges',
 'SM Katich': 'Simon Katich', 'M Ntini': 'Makhaya Ntini', 'LJ Wright': 'Luke Wright', 'J Overton': 'Jamie Overton', 'D Ferreira': 'Donovan Ferreira',
 'J Fraser-McGurk': 'Jake Fraser-McGurk', 'RD Rickelton': 'Ryan Rickelton', 'V Suryavanshi': 'Vaibhav Suryavanshi', 'A Mhatre': 'Ayush Mhatre',
 'A Raghuvanshi': 'Angkrish Raghuvanshi', 'A Kamboj': 'Anshul Kamboj', 'N Wadhera': 'Nehal Wadhera', 'DS Rathi': 'Digvesh Rathi',
 'V Nigam': 'Vipraj Nigam', 'JG Bethell': 'Jacob Bethell', 'SB Dubey': 'Shubham Dubey', 'XC Bartlett': 'Xavier Bartlett', 'RJW Topley': 'Reece Topley',
 'SH Johnson': 'Spencer Johnson', 'KT Maphaka': 'Kwena Maphaka', 'C Bosch': 'Corbin Bosch', 'N Burger': 'Nandre Burger', 'J Little': 'Josh Little',
 'W O\'Rourke': "Will O'Rourke", 'MJ Suthar': 'Manav Suthar', 'R Minz': 'Robin Minz', 'GF Linde': 'George Linde', 'MP Breetzke': 'Matthew Breetzke',
 'PWA Mulder': 'Wiaan Mulder', 'MJ Owen': 'Mitchell Owen', 'S Joseph': 'Shamar Joseph', 'LB Williams': 'Lizaad Williams', 'SZ Mulani': 'Shams Mulani',
 'B Muzarabani': 'Blessing Muzarabani', 'LG Pretorius': 'Lhuan-dre Pretorius', 'DA Payne': 'David Payne', 'Parvez Rasool': 'Parvez Rasool',
 'MJ Lumb': 'Michael Lumb', 'LE Plunkett': 'Liam Plunkett', 'TD Paine': 'Tim Paine', 'KAJ Roach': 'Kemar Roach', 'DR Martyn': 'Damien Martyn',
 'DS Lehmann': 'Darren Lehmann', 'RR Sarwan': 'Ramnaresh Sarwan', 'CJ Ferguson': 'Callum Ferguson', 'JEC Franklin': 'James Franklin',
 'AM Ghazanfar': 'Allah Ghazanfar', 'RE Levi': 'Richard Levi', 'MG Neser': 'Michael Neser', 'GHS Garton': 'George Garton', 'SB Bangar': 'Sanjay Bangar',
 'FY Fazal': 'Faiz Fazal', 'RS Gavaskar': 'Rohan Gavaskar', 'DAJ Bracewell': 'Doug Bracewell', 'AA Noffke': 'Ashley Noffke', 'YA Abdulla': 'Yusuf Abdulla',
 'CK Kapugedera': 'Chamara Kapugedera', 'D du Preez': 'Dillon du Preez', 'SSB Magala': 'Sisanda Magala', 'CJ Dala': 'Junior Dala',
 'SC Kuggeleijn': 'Scott Kuggeleijn', 'RW Price': 'Ray Price', 'TR Birt': 'Travis Birt', 'JM Kemp': 'Justin Kemp', 'RJ Peterson': 'Robin Peterson',
 'Liton Das': 'Litton Das', 'SK Rasheed': 'Shaik Rasheed', 'AA Kulkarni': 'Arshin Kulkarni', 'K Goel': 'Karan Goel', 'T Kohli': 'Taruwar Kohli',
}

st, rows, last = ipl_stats.load(DATA)
OLD = json.loads(pat.search(open(OLD_HTML, encoding='utf-8').read()).group(1))['players']
info = {}
for r in rows:
    info.setdefault(r['player_name'], r)
full = {n: (info[n]['player_full_name'].strip() if n in info else '') for n in st}


def auto(name):
    t = tk(name)
    if not t: return None
    hits = [s for s in st if nk(s) == nk(name) or (full[s] and nk(full[s]) == nk(name))]
    if not hits: hits = [s for s in st if full[s] and tk(full[s])[0] == t[0] and tk(full[s])[-1] == t[-1]]
    if not hits: hits = [s for s in st if full[s] and t[0] in tk(full[s]) and t[-1] in tk(full[s])]
    if not hits:
        hits = [s for s in st if tk(s)[-1] == t[-1] and tk(s)[0][0] == t[0][0] and len(tk(s)[0]) <= 3 and len(t[-1]) > 2]
    return hits[0] if len(hits) == 1 else None


def find(p):
    if p['n'] in MATCH: return MATCH[p['n']]
    if p.get('sn') in st: return p['sn']
    return auto(p['n'])


def style(r):
    b = (r or {}).get('bowl_style', '').split(',')[0].strip()
    if b in ('', 'NULL'): return '', ''
    s = b.lower().replace('right arm', 'right-arm').replace('left arm', 'left-arm').replace('fast medium', 'fast-medium').replace('medium fast', 'medium-fast')
    return s, ('spin' if any(w in s for w in ('break', 'orthodox', 'spin', 'googly')) else 'pace')


def role(s, r):
    keeper = 'Wicketkeeper' in (r or {}).get('field_pos', '') and 'Occasional' not in (r or {}).get('field_pos', '')
    if keeper or s['stp'] >= 2: return 'WK'
    bpm, rpi = s['balls'] / max(1, s['m']), s['runs'] / max(1, s['inn'])
    if bpm >= 9 and rpi >= 14 and s['runs'] >= 150: return 'AR'
    if bpm >= 9: return 'BOWL'
    return 'BAT'


def impact(s):
    m = max(1, s['m'])
    sr = 100 * s['runs'] / s['bf'] if s['bf'] else 0
    eco = 6 * s['rc'] / s['balls'] if s['balls'] else 99
    bat = s['runs'] / m * min(1.4, max(0.6, sr / 130))
    bowl = s['wk'] / m * 25 * min(1.3, max(0.7, 7.8 / eco)) if s['balls'] >= 60 else 0
    keep = 2 * (s['ct'] + 2 * s['stp']) / m
    best, other = max(bat, bowl), min(bat, bowl)
    exp = min(1.0, math.log(1 + s['m']) / math.log(120))
    return (best + 0.5 * other + keep) * (0.15 + 0.85 * exp) + 0.4 * s['potm']


def tags(s, r_):
    m, out = max(1, s['m']), []
    sr = 100 * s['runs'] / s['bf'] if s['bf'] else 0
    eco = 6 * s['rc'] / s['balls'] if s['balls'] else 99
    if s['runs'] >= 300 and sr >= 145: out.append('🔥 Power Hitter')
    if s['runs'] >= 1500 and sr < 130: out.append('🧱 Anchor')
    if s['wk'] >= 40 and eco < 7.3: out.append('⚡ Pace Ace' if style(info.get(r_))[1] == 'pace' else '🌀 Spin Wizard')
    if r_ and role(s, info.get(r_)) == 'WK' and s['stp'] >= 10: out.append('🧤 Safe Hands')
    if s['potm'] >= 8: out.append('🏅 Match Winner')
    return out[:3]


html = open(OUT_HTML, encoding='utf-8').read()
m_ = pat.search(html)
I = json.loads(m_.group(1))
pool = [p for p in I['players'] if not p.get('ip')]          # earlier runs' additions are rebuilt
used, filled = set(), []
for p in pool:
    k = find(p)
    if k and k in st:
        used.add(k)
        if p['st'] and k != p['sn'] and st[k]['m'] > p['st']['m']:   # the earlier copy only had part of the career
            p['st'] = st[k]
        if not p['st']:
            s, r = st[k], info.get(k)
            p['st'] = s
            p['sn'] = k
            if r:
                p['bat'] = 'L' if r['bat_style'].startswith('Left') else 'R'
                b, bk = style(r)
                if b: p['bowl'], p['bk'] = b, bk
            if '❓ Check role' in p['tg'] and s['m'] >= 3:
                p['r'] = role(s, r); p['tg'].remove('❓ Check role')
            filled.append(p['n'])

# a rating scale from career impact: the same spread the pool already uses (50-94)
imp = {k: impact(s) for k, s in st.items()}
ranked = sorted(imp.values())
rate = lambda v: round(50 + 44 * (sum(1 for x in ranked if x <= v) / len(ranked)) ** 1.6)
for p in pool:   # 2013-2022 auction players typed in by hand: take the rating from their numbers once they have enough
    if p.get('pa') and p['cid'] == 0 and p['st'] and p['st']['m'] >= 10:
        hand = p.setdefault('rh', p['rt'])   # the typed-in rating, kept so re-runs start from it
        p['rt'] = max(hand - 6, min(hand + 6, rate(imp[p['sn']]), 68 + p['st']['m']))

old_for = {}
for o in OLD:   # earlier IPL-DATASET entries, keyed by their name in the match data
    k = o['sn'] if o['sn'] in st else auto(o['n'])
    if k and k not in old_for: old_for[k] = o
bp = lambda r: 200 if r >= 86 else 150 if r >= 80 else 100 if r >= 74 else 75 if r >= 68 else 50 if r >= 62 else 30 if r >= 56 else 20
new = []
for k, s in st.items():
    if k in used or k in SKIP: continue
    o = old_for.get(k)
    if o and o['st']:
        e = {key: (v[:] if isinstance(v, list) else v) for key, v in o.items()}
        e.update({'cat': 'Capped' if e['cat'] == 'Marquee' else e['cat'], 's26': None, 'ip': 1})
        new.append(e); continue
    r = info.get(k)
    name = NAME.get(k) or (' '.join(full[k].split()) if len(full[k].split()) == 2 else k)
    b, bk = style(r)
    rt = min(rate(imp[k]), 68 + s['m'])   # a handful of matches can't make a star
    new.append({'n': name, 'sn': k, 'cid': 0, 'r': role(s, r), 'rt': rt, 'bp': bp(rt), 'bat': ('L' if r['bat_style'].startswith('Left') else 'R') if r else '',
                'bowl': b, 'bk': bk, 'os': 1 if k in OVERSEAS else 0, 'cat': 'Capped' if s['m'] >= 20 or k in OVERSEAS else 'Uncapped',
                'tg': tags(s, k), 'img': '', 'dob': '', 'st': s, 's26': None, 'ip': 1})
if '--list' in sys.argv:
    for e in sorted(new, key=lambda x: -x['rt']): print(f"{e['sn']}|{e['n']}|{e['r']}|{e['rt']}|os{e['os']}|{e['st']['m']}|{e['st']['from']}-{e['st']['to']}|{'OLD' if e['cid'] else ''}")
    sys.exit()
rest = sorted([p for p in pool if not p.get('s26')] + new, key=lambda x: (-x['rt'], x['n']))
I['players'] = [p for p in pool if p.get('s26')] + rest
html = html[:m_.start()] + 'const IPL = ' + json.dumps(I, ensure_ascii=False, separators=(',', ':')) + ';' + html[m_.end():]
open(OUT_HTML, 'w', encoding='utf-8').write(html)
print('stats filled in for', len(filled), '| added', len(new), '| pool now', len(I['players']))
print('still checking role:', ', '.join(p['n'] for p in I['players'] if '❓ Check role' in p['tg']))
