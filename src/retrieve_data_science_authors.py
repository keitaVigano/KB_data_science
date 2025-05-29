import pandas as pd

authors_raw = [
    ("Andreotti", "Alberta Argia", "SPS/09"),
    ("Bernasconi", "Davide Paolo", "MED/01"),
    ("Bianco", "Simone", "INF/01"),
    ("Bissiri", "Pier Giovanni", "SECS-S/01"),
    ("Cesarini", "Mirko", "ING-INF/05"),
    ("Chicco", "Davide", "INF/01"),
    ("Ciavotta", "Michele", "INF/01"),
    ("Della Vedova", "Gianluca", "INF/01"),
    ("Di Domenica", "Nico", "SECS-P/08"),
    ("Fattore", "Marco", "SECS-S/03"),
    ("Ferretti", "Claudio", "INF/01"),
    ("Fersini", "Elisabetta", "INF/01"),
    ("Forte", "Gianfranco", "SECS-P/11"),
    ("Gianini", "Gabriele", "INF/01"),
    ("Guerzoni", "Marco", "SECS-P/06"),
    ("Maurino", "Andrea", "INF/01"),
    ("Mercorio", "Fabio", "INF/01"),
    ("Messina", "Enza", "MAT/09"),
    ("Monti", "Gianna", "SECS-S/01"),
    ("Moretto", "Enrico", "SECS-S/06"),
    ("Napoletano", "Paolo", "INF/01"),
    ("Paganoni", "Marco", "FIS/01"),
    ("Palmonari", "Matteo", "INF/01"),
    ("Pasi", "Gabriella", "INF/01"),
    ("Pelagatti", "Matteo", "SECS-S/03"),
    ("Pennoni", "Fulvia", "SECS-S/01"),
    ("Pescini", "Dario", "INF/01"),
    ("Presotto", "Luca", "FIS/07"),
    ("Rebora", "Paola", "MED/01"),
    ("Stella", "Fabio Antonio", "MAT/09"),
    ("Viviani", "Marco", "INF/01")
]

df_authors = pd.DataFrame(authors_raw, columns=["Last name", "Name", "SSD"])

df_authors.to_csv("data/authors/authors_data_science.csv", index=False)