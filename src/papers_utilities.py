import pandas as pd
import requests
import time


def get_most_specific_subfield(doi):
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
        field = concepts[0].get("display_name")
    else:
        field = None

    return field


def get_works(orcid_id, given_name=None, family_name=None):

    base_url = "https://api.crossref.org/works"

    def fetch_data(params):
        for i in range(3):
            try:
                res = requests.get(base_url, params=params, timeout=30)
                res.raise_for_status()
                return res.json().get("message", {}).get("items", [])
            except requests.exceptions.ReadTimeout:
                print(f"Timeout, ritento ({i+1}/3)...")
                time.sleep(5)
            except requests.RequestException as e:
                print(f"Errore generico: {e}")
                break
        return []


    # --- Prima prova con ORCID ---
    print(f"Ricerca con ORCID: {orcid_id}")
    items = fetch_data({"filter": f"orcid:{orcid_id}"})

    # --- Se non funziona, prova con nome e cognome ---
    if not items and given_name and family_name:
        print(f"Nessun risultato via ORCID. Fallback con nome: {given_name} {family_name}")
        items = fetch_data({"query.author": f"{given_name} {family_name}"})

    records = []
    for item in items:
        doi = item.get("DOI")
        type_ = item.get("type")
        title = item.get("title", [""])[0]
        year = item.get("created", {}).get("date-parts", [[None]])[0][0]

        if not year or year <= 2018:
            continue

        authors = item.get("author", [])
        author_names = [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in authors]
        author_orcids = [a.get("ORCID", "").replace("https://orcid.org/", "") if "ORCID" in a else None for a in authors]

        field = get_most_specific_subfield(doi)

        records.append({
            "doi": doi,
            "year": year,
            "authors": author_names,
            "author_orcids": author_orcids,
            "type": type_,
            "title": title,
            "topics": field
        })

    return pd.DataFrame(records)