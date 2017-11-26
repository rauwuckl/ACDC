from collections import OrderedDict
from sortedcontainers import SortedDict
import src.Json_Parsing as jp
import re
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json

## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()
client = ElsClient(config['apikey'])


def get_search_terms(patient_id):
    patient_report = jp.build_file(patient_id)
    conds = []
    for condition in patient_report['conditions']:
        conds.append(re.sub("\s+", "+", re.sub('[(){}<>]', '',patient_report['conditions'][str(condition)]['cond_name'])))
    return conds


def get_relevant_papers(conditions):
    results = {}
    count = 0
    for cond in conditions:
        doc_srch = ElsSearch(cond, 'scopus')
        doc_srch.execute(client, get_all=False)
        for res in doc_srch.results:
            results[str(count)] = res
            count += 1
        print("doc_srch for ", cond, " has", len(doc_srch.results), "results.")
    return json.dumps(get_n_most_cited(5, results))

def get_n_most_cited(n, papers):
    papers_by_citations = {}
    top_n = {}
    for group in papers:
        papers_by_citations[group] =  int(papers[group]['citedby-count'])
    s = OrderedDict(sorted(papers_by_citations.items(), reverse=True, key=lambda t: t[1]))
    print(s)
    srt = list(s.keys())
    print(srt)
    for i in range(0,n):
        print(papers[(srt[i])])
        top_n[str(i)] = papers[(srt[i])]
    return top_n

