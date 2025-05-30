import requests
import pandas as pd

def search_orcid_bicocca(given_name, family_name):
    base_url = "https://pub.orcid.org/v3.0/expanded-search/"
    query = f"given-names:{given_name} AND family-name:{family_name}"

    headers = {
        "Accept": "application/json"
    }

    params = {
        "q": query
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Errore nella richiesta: {response.status_code}")
        return None

    results = response.json().get("expanded-result", [])

    if not results:
        print("Nessun risultato trovato.")
        return None

    for res in results:
        affiliations = res.get("institution-name", [])
        if any("bicocca" in aff.lower() for aff in affiliations):
            full_name = res.get("given-names", "") + " " + res.get("family-name", "")
            orcid = res.get("orcid-id", "N/A")
            print(f"Trovato: {full_name} -> ORCID: {orcid}")
            return orcid

    print("Nessun ORCID trovato associato alla Bicocca.")
    return None

def get_author_info_bicocca(author_name):
    search_url = f"https://api.openalex.org/authors?search={author_name}"
    response = requests.get(search_url)
    ins_id = []
    ins_name = []
    fields = []
    result = {}

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])

        if results:
            author = results[0]
            author_id = author.get('id')
            display_name = author.get('display_name')
            orcid = author.get('orcid')

            instituions = author.get('affiliations', [])
            for institution in instituions:
                ins_id.append(institution.get('institution').get('id'))
                ins_name.append(institution.get('institution').get('display_name'))

            topics = author.get("topics", [])
            for t in topics:
                field = t.get("subfield").get("display_name")
                if field not in fields:
                    fields.append(field)

            hindex = author.get("summary_stats").get("h_index")
            if not hindex:
                hindex = 0

            result["id"] = author_id
            result["ins_id"] = ins_id
            result["ins_name"]= ins_name
            result["orcid"] = orcid
            result["topics"]= fields
            result["hindex"] = hindex

        else:
            print("Nessun risultato trovato.")

    else:
        print(f"Errore nella richiesta: {response.status_code}")

    return result