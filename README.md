# KB_data_science

This project builds a semantic knowledge base representing the research output, people, topics, and institutional affiliations of the Data Science course at the University of Milano-Bicocca. It integrates publication metadata, researcher identifiers (ORCID, OpenAlex), course information, and topic annotations enriched with external ontologies (e.g., Wikidata), and represents them in RDF/OWL format. The knowledge base supports SPARQL querying, semantic inference, and can be loaded in triple stores like RDF4J.

## Project Structure

```
KB_data_science/
├── data/           # CSV files for authors, papers, topics, courses, etc.
│   └── DSkg.ttl    # RDF/OWL knowledge base in Turtle format
├── notebooks/      # Jupyter notebooks for data exploration and graph creation
├── src/           # Python scripts to build and export the RDF graph
├── environment.yaml # Conda environment configuration
└── LICENSE        # License information
```

## Getting Started

### Prerequisites

- Python 3.x
- Conda or Miniconda
- RDF4J (optional, for loading and querying the graph)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/keitaVigano/KB_data_science.git
cd KB_data_science
```

2. Create and activate the Conda environment:
```bash
conda env create -f environment.yaml
conda activate kb_data_science
```

### Using the Knowledge Base in RDF4J

1. Start RDF4J and open the Workbench interface (usually at http://localhost:8080/rdf4j-workbench)

2. Create a new repository (e.g., ds-graph)

3. Upload the RDF graph:
   - Go to "Repositories" → your repository (ds-graph) → "Upload"
   - Select the file `data/DSkg.ttl`
   - Set the format to Turtle
   - Click "Upload"

The graph is now available for SPARQL queries via the Workbench or programmatically.

## Usage

1. Prepare or edit source data in the `data/` directory
2. Use the Python scripts in `src/` to generate and export the RDF graph
3. Explore or analyze the graph using Jupyter notebooks

## Components

### Data Directory
Contains:
- Authors (with ORCID and affiliations)
- Scientific papers (with DOIs and topics)
- Course and department information
- Final RDF export `DSkg.ttl`

### Notebooks Directory
Includes Jupyter notebooks for:
- Data exploration
- Graph creation
- SPARQL query testing

### Source Directory
Contains Python scripts to:
- Build the RDF graph using rdflib
- Define ontological classes and properties
- Enrich with semantic links (e.g., owl:sameAs)
- Export the graph

## Semantic Enrichment

The graph includes:
- Ontological hierarchy and domain/range restrictions
- Inverse properties such as `ds:authored` and `ds:hasAuthor`
- Linking topics to Wikidata entities via `owl:sameAs`
- Inference rule: if an Author has authored a Paper, and the Paper has a Topic, then the Author has interest in that Topic (`ds:hasInterest`)

## License

This project is distributed under the terms of the LICENSE file.

## Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request.