# -*- coding: utf-8 -*-

"""
Script for get contributions from Wikidata
return user, comment, size and timestamp
This module can be used as a generator
"""

import requests
import pandas as pd


def get_contributions(qid):
    def get_revisions(rvcontinue):
        s = requests.Session()
        url = "https://www.wikidata.org/w/api.php"

        params = {
            "action": "query",
            "prop": "revisions",
            "titles": qid,
            "rvslots": "*",
            "rvlimit": "max",
            "rvprop": "user|comment|size|timestamp",
            # "generator": "revisions",
            # "grvcontinue": rvcontinue,
            "format": "json"
        }

        r = s.get(url=url, params=params)
        payload = r.json()
        data = payload['query']['pages']

        for page_id, page_info in data.items():
            if 'revisions' in page_info:
                for revision in page_info['revisions']:
                    revisions.append(revision)

        return payload

    revisions = []

    rvcontinue = ''
    while True:
        payload_temp = get_revisions(rvcontinue)
        if 'continue' in payload_temp:
            rvcontinue = payload_temp['continue']['rvcontinue']
        else:
            break

    df = pd.DataFrame(revisions)
    df['qid'] = qid

    return df


if __name__ == '__main__':
    df_final = pd.DataFrame()

    with open('input.txt') as qids:
        qids = qids.readlines()

    i = 1
    n = len(qids)
    for qid in qids:
        qid = qid.strip()

        df_temp = get_contributions(qid)
        df_final = pd.concat([df_final, df_temp])

        print(f'{i}/{n}')
        i += 1

    df_final.to_excel('get_contributions.xlsx', index=False)
