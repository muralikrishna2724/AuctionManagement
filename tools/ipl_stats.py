"""Career IPL stats for every player in the IPL-DATASET match files (ball_by_ball_data.csv, ipl_matches_data.csv,
players-data-updated.csv, teams_data.csv), in the format the auction's built-in pool uses for `st`.

    stats, players, last_season = load(folder)
    stats['V Kohli'] -> {'m': ..., 'runs': ..., 'wk': ..., 'from': 2008, 'to': 2026, 'team': ..., 'rm': ...}

m counts the matches a player shows up in the ball-by-ball data (batting, bowling or fielding). The r* fields are
the last two seasons only (rr runs, rb balls faced, rw wickets, rlb legal balls bowled, rrc runs conceded, rm matches).
"""
import csv, collections

OUT_KINDS = {'bowled', 'caught', 'lbw', 'caught and bowled', 'stumped', 'hit wicket'}
CURRENT = {1: 'Royal Challengers Bengaluru'}   # franchises renamed since; teams_data has the old name


def load(folder):
    teams = {int(r['team_id']): r['team_name'] for r in csv.DictReader(open(folder + '/teams_data.csv', encoding='utf-8'))}
    teams.update(CURRENT)
    matches = {r['match_id']: r for r in csv.DictReader(open(folder + '/ipl_matches_data.csv', encoding='utf-8'))}
    year = {k: int(r['season'][:4]) for k, r in matches.items()}
    last = max(year.values())
    recent = {last - 1, last}
    players = list(csv.DictReader(open(folder + '/players-data-updated.csv', encoding='utf-8')))
    pid = {}
    for p in players:
        pid.setdefault(p['player_id'], p['player_name'])
    potm = collections.Counter()
    for r in matches.values():
        x = r['player_of_match'].split('.')[0]
        if x in pid: potm[pid[x]] += 1

    P = collections.defaultdict(lambda: {'ms': set(), 'inn': set(), 'runs': 0, 'bf': 0, 'outs': 0, 'inr': collections.Counter(),
                                          'f4': 0, 's6': 0, 'balls': 0, 'rc': 0, 'wk': 0, 'fig': collections.defaultdict(lambda: [0, 0]),
                                          'ct': 0, 'stp': 0, 'seen': {}, 'teams': set(), 'rr': 0, 'rb': 0, 'rw': 0, 'rlb': 0, 'rrc': 0, 'rms': set()})
    for b in csv.DictReader(open(folder + '/ball_by_ball_data.csv', encoding='utf-8')):
        mid = b['match_id']
        if mid not in year: continue
        y, rec, sup = year[mid], year[mid] in recent, b['is_super_over'] == 'True'
        tb, tw = int(b['team_batting']), int(b['team_bowling'])
        key = (mid, b['innings'])
        fielders = [f.strip(" '\"") for f in b['fielders_involved'].strip('[]').split(',') if f.strip(" '\"") not in ('', 'None')]
        for name, team in ((b['batter'], tb), (b['non_striker'], tb), (b['bowler'], tw), *((f, tw) for f in fielders)):
            s = P[name]
            s['ms'].add(mid); s['teams'].add(team)
            if rec: s['rms'].add(mid)
            if mid not in s['seen'] or s['seen'][mid][0] < y: s['seen'][mid] = (y, b['match_date'] if 'match_date' in b else matches[mid]['match_date'], team)
        if sup: continue
        wide, nob = b['is_wide_ball'] == 'True', b['is_no_ball'] == 'True'
        bat, bowl = P[b['batter']], P[b['bowler']]
        bat['inn'].add(key); P[b['non_striker']]['inn'].add(key)
        br = int(b['batter_runs'])
        bat['runs'] += br; bat['inr'][key] += br
        if not wide: bat['bf'] += 1
        if br == 4: bat['f4'] += 1
        if br == 6: bat['s6'] += 1
        rc = int(b['total_runs']) - int(b['leg_bye_runs']) - int(b['bye_runs']) - int(b['penalty_runs'])
        legal = not wide and not nob
        bowl['rc'] += rc; bowl['fig'][key][1] += rc
        if legal: bowl['balls'] += 1
        if rec:
            bat['rr'] += br; bat['rb'] += 0 if wide else 1
            bowl['rrc'] += rc; bowl['rlb'] += 1 if legal else 0
        kind, out = b['wicket_kind'], b['player_out']
        if out and kind not in ('retired hurt', ''):
            P[out]['outs'] += 1
        if kind in OUT_KINDS:
            bowl['wk'] += 1; bowl['fig'][key][0] += 1
            if rec: bowl['rw'] += 1
        if kind == 'caught':
            for f in fielders: P[f]['ct'] += 1
        if kind == 'caught and bowled': bowl['ct'] += 1
        if kind == 'stumped':
            for f in fielders: P[f]['stp'] += 1

    out = {}
    for name, s in P.items():
        if not s['ms']: continue
        ys = [year[m] for m in s['ms']]
        inns = s['inr']
        last_match = max(s['seen'].values())
        best = max(s['fig'].values(), key=lambda f: (f[0], -f[1]), default=[0, 0])
        out[name] = {
            'm': len(s['ms']), 'inn': len(s['inn']), 'runs': s['runs'], 'bf': s['bf'], 'no': max(0, len(s['inn']) - s['outs']),
            'hs': max(inns.values(), default=0), 'f50': sum(1 for v in inns.values() if 50 <= v < 100), 'f100': sum(1 for v in inns.values() if v >= 100),
            'f4': s['f4'], 's6': s['s6'], 'balls': s['balls'], 'rc': s['rc'], 'wk': s['wk'],
            'bbi': f'{best[0]}/{best[1]}' if s['balls'] else '', 'ct': s['ct'], 'stp': s['stp'], 'potm': potm[name],
            'from': min(ys), 'to': max(ys), 'team': teams.get(last_match[2], ''), 'teams': len(s['teams']),
            'rr': s['rr'], 'rb': s['rb'], 'rw': s['rw'], 'rlb': s['rlb'], 'rrc': s['rrc'], 'rm': len(s['rms']),
        }
    return out, players, last
