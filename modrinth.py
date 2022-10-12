import requests
import json
import os
import time

session = requests.Session()
session.headers.update({'User-Agent': 'mc-mods.nix'})

result = {}


def save_and_exit():
    with open('modrinth.json', 'w') as f:
        json.dump(result, f, indent=1)
    os.sys.exit(0)


def httpget(url: str):
    r = session.get(url)
    print(r.headers['X-Ratelimit-Remaining'], file=os.sys.stderr)
    if int(r.headers['X-Ratelimit-Remaining']) <= 100:
        time.sleep(r.header['X-Ratelimit-Reset'])
    return r.json()


def get_mod(slug: str, info=None):
    if info is None:
        info = httpget(f'https://api.modrinth.com/v2/project/{slug}')
        license_ = info['license']['id']
    else:
        license_ = info['license']
    versions = httpget(
            f'https://api.modrinth.com/v2/project/{slug}/version')[::-1]
    for version in versions:
        if not version['files']:
            continue
        file = version['files'][0]
        for gv in version['game_versions']:
            if gv not in result:
                result[gv] = {}
            for loader in version['loaders']:
                if loader not in result[gv]:
                    result[gv][loader] = {}
                result[gv][loader][slug] = {
                    'url': file['url'],
                    'sha512': file['hashes']['sha512'],
                    'license': license_
                }


get_mod('wagyourminimap')

for offset in range(0, 1000, 100):
    mods = httpget(
        f'https://api.modrinth.com/v2/search?limit=100&index=follows&offset={offset}&facets=[["project_type:mod","project_type:resourcepack"]]')
    if len(mods['hits']) == 0:
        save_and_exit()
    for mod in mods['hits']:
        get_mod(mod['slug'], mod)
save_and_exit()
