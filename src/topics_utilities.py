import requests
import time


def get_subfield_by_author(orcid):
    search_url = f"https://api.openalex.org/authors?filter=orcid:{orcid}"
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"Timeout per ORCID {orcid}")
        return {}
    except requests.exceptions.RequestException as e:
        print(f"Errore per ORCID {orcid}: {e}")
        return {}

    fields = []

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])

        for author in results:

            topics = author.get("topics", [])
            i = 0
            for t in topics:
                if i > 4:
                    break
                field = t.get("subfield").get("display_name")
                if field and field not in fields:
                    fields.append(field)
                i += 1

            break

        if not results:
            print(f"Nessun autore affiliato trovato per ORCID: {orcid}")

    else:
        print(f"Errore nella richiesta: {response.status_code}")

    return fields


def get_subfield(doi):
    doi_formatted = f"https://doi.org/{doi}"
    url = f"https://api.openalex.org/works/doi:{doi_formatted}"
    fields = []

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Errore nella richiesta OpenAlex: {e}")
        return None

    data = res.json()
    concepts = data.get("topics", [])
    if concepts:
        field = concepts[0].get("subfield").get("display_name")
    else:
        field = None

    return field


def find_wikidata_entity(label, lang="en", delay=1.0):
    endpoint = "https://query.wikidata.org/sparql"
    headers = {"Accept": "application/sparql-results+json"}

    query = f"""
    SELECT ?item ?itemLabel WHERE {{
      ?item rdfs:label "{label}"@{lang}.
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{lang}". }}
    }}
    LIMIT 1
    """

    # Attendi prima della chiamata
    time.sleep(delay)

    response = requests.get(endpoint, params={"query": query}, headers=headers)

    if response.status_code == 200:
        results = response.json()["results"]["bindings"]
        if results:
            return results[0]["item"]["value"]

    return None