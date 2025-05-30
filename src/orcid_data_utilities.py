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
    ''' Attenzione al nome perché questo metodo viene usato per la ricerca dei matadata
    degli autori per nome di quelli della bicocca'''
    search_url = f"https://api.openalex.org/authors?search={author_name}"
    response = requests.get(search_url)
    ins_id = []
    ins_name = []
    fields = []
    result = {}

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])

        # Cerca tra tutti gli autori trovati
        for author in results:
            affiliations = author.get('affiliations', [])
            affiliated_to_bicocca = any(
                'bicocca' in (inst.get('institution', {}).get('display_name', '')).lower()
                or 'unimib' in (inst.get('institution', {}).get('display_name', '')).lower()
                for inst in affiliations
            )

            if affiliated_to_bicocca:
                author_id = author.get('id')
                display_name = author.get('display_name')
                orcid_raw = author.get('orcid')
                orcid = orcid_raw.split("/")[-1]

                for institution in affiliations:
                    ins = institution.get('institution', {})
                    ins_id.append(ins.get('id'))
                    ins_name.append(ins.get('display_name'))

                topics = author.get("topics", [])
                for t in topics:
                    field = t.get("display_name")
                    if field and field not in fields:
                        fields.append(field)

                hindex = author.get("summary_stats", {}).get("h_index", 0)

                result["id"] = author_id
                result["ins_id"] = ins_id
                result["ins_name"] = ins_name
                result["orcid"] = orcid
                result["topics"] = fields
                result["hindex"] = hindex

                break  # Prendi solo il primo autore affiliato a Bicocca

        if not result:
            print(f"Nessun autore affiliato a Bicocca trovato per: {author_name}")

    else:
        print(f"Errore nella richiesta: {response.status_code}")

    return result