#!/usr/bin/env python3
"""Build player photos into index.html so they show with no internet and in any viewer.

For every player in the built-in IPL pool, download a small photo, trying in order:
  1. the dataset's image link (img1.hscicdn.com), as a 160 px thumbnail
  2. Wikipedia: the first search hit for "<name> cricketer" whose title has the surname
Each photo goes into index.html as a data: URI in the IPL_PHOTOS block, keyed by the
player's cricinfo id. Run again any time; players already embedded are kept unless --redo.

Usage: python3 tools/embed_photos.py [--redo] [--file index.html]
"""
import base64, json, os, re, ssl, sys, time, urllib.parse, urllib.request

FILE = sys.argv[sys.argv.index('--file') + 1] if '--file' in sys.argv else os.path.join(os.path.dirname(__file__), '..', 'index.html')
REDO = '--redo' in sys.argv
START, END = '/* IPL_PHOTOS:start */', '/* IPL_PHOTOS:end */'
MAX_BYTES = 60_000

ctx = ssl.create_default_context()
for ca in (os.environ.get('SSL_CERT_FILE'), '/root/.ccr/ca-bundle.crt'):
    if ca and os.path.exists(ca):
        ctx = ssl.create_default_context(cafile=ca)
        break
UA = {'User-Agent': 'college-ipl-auction/1.0 (photo embedder)', 'Accept': 'image/jpeg,image/png,image/webp,*/*;q=0.5'}


def get(url, accept=None):
    h = dict(UA)
    if accept:
        h['Accept'] = accept
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=20, context=ctx) as r:
        return r.headers.get('Content-Type', ''), r.read()


def as_data(url):
    try:
        ctype, body = get(url)
    except Exception as e:
        return None, f'{type(e).__name__}'
    ctype = ctype.split(';')[0].strip()
    if not ctype.startswith('image/') or not body or len(body) > MAX_BYTES:
        return None, f'{ctype or "?"} {len(body or b"")}B'
    return f'data:{ctype};base64,' + base64.b64encode(body).decode(), None


def wiki_thumb(name):
    q = urllib.parse.urlencode({'action': 'query', 'format': 'json', 'generator': 'search', 'gsrnamespace': 0, 'gsrlimit': 4,
                                'gsrsearch': name + ' cricketer', 'prop': 'pageimages', 'piprop': 'thumbnail', 'pithumbsize': 200})
    _, body = get('https://en.wikipedia.org/w/api.php?' + q, accept='application/json')
    pages = sorted(json.loads(body).get('query', {}).get('pages', {}).values(), key=lambda p: p.get('index', 0))
    last = re.sub(r'[^a-z0-9]', '', name.split()[-1].lower())
    for p in pages:
        if p.get('thumbnail', {}).get('source') and last in re.sub(r'[^a-z0-9]', '', p['title'].lower()):
            return p['thumbnail']['source']
    return None


def main():
    html = open(FILE, encoding='utf-8').read()
    m = re.search(r'^const IPL = (\{.*?\});$', html, re.M)
    if not m or START not in html:
        sys.exit('index.html is missing the IPL data or the IPL_PHOTOS block')
    ipl = json.loads(m.group(1))
    a, b = html.index(START), html.index(END)
    cur = re.search(r'const IPL_PHOTOS = (\{.*\});', html[a:b], re.S)
    photos = {} if REDO or not cur else json.loads(cur.group(1))
    base = ipl['img'].replace('t_ds_square_w_320,q_50', 't_ds_square_w_160,q_60')
    got, missed = 0, []
    for i, x in enumerate(ipl['players'], 1):
        key = str(x['cid'])
        if key in photos:
            continue
        data, why = (as_data(base + x['img']) if x.get('img') else (None, 'no link'))
        if not data:
            try:
                t = wiki_thumb(x['n'])
                data, why2 = as_data(t) if t else (None, 'not on Wikipedia')
                why = f'{why}; wiki: {why2}' if not data else why
            except Exception as e:
                why = f'{why}; wiki: {type(e).__name__}'
        if data:
            photos[key] = data
            got += 1
        else:
            missed.append(f"{x['n']} ({why})")
        print(f"[{i}/{len(ipl['players'])}] {x['n']}: {'ok' if data else 'missing'}", flush=True)
        time.sleep(0.1)
    block = START + '\nconst IPL_PHOTOS = ' + json.dumps(photos, separators=(',', ':')) + ';\n' + END
    html = html[:a] + block + html[b + len(END):]
    open(FILE, 'w', encoding='utf-8').write(html)
    print(f'\nEmbedded {got} new photos; {len(photos)} of {len(ipl["players"])} players have one. '
          f'index.html is now {len(html.encode()) / 1e6:.1f} MB.')
    if missed:
        print('No photo for:\n  ' + '\n  '.join(missed))


if __name__ == '__main__':
    main()
