import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from os.path import join as pjoin

import data
from connection import Connection, transact_and_time


if __name__ == "__main__":

    # This file path
    path = os.path.dirname(os.path.realpath(__file__))
    # Dataset TODO scale 
    datafile = pjoin(path, 'data', 'Sloth.txt')

    from dotenv import load_dotenv
    load_dotenv()
    URI = os.getenv('NEO4J_URI')
    USERNAME = os.getenv('NEO4J_USERNAME')
    PASSWORD = os.getenv('NEO4J_PASSWORD')
    INSTANCE = os.getenv('AURA_INSTANCENAME')

    # Initialize connection to database
    connection = Connection(URI, USERNAME, PASSWORD, INSTANCE)

    # Durations dictionary
    durations = {}

    connection.clear_database()

    # Load data one at a time, execute transaction and then delete it
    papers = data.get_papers_data(datafile)
    authors = data.get_authors_data(datafile)
    citations = data.get_citations_data(datafile)
    authorships = data.get_authorships_data(datafile)

    connection.create_papers(papers)
    connection.create_authors(authors)
    connection.create_references(citations)
    connection.create_authorships(authorships)

    N_TRIALS = 10
    N_QUERIES = 3

    paper_ids = [paper['id'] for paper in papers][:N_TRIALS]
    author_ids = [author['id'] for author in authors][:N_TRIALS]

    trials = np.empty((N_TRIALS, N_QUERIES))

    for i, (paper_id, author_id) in enumerate(zip(paper_ids, author_ids)):
        durations = {}

        durations.update(transact_and_time(
            connection.delete_authorship, 
            (connection.authors_of(paper_id)[0], paper_id)
        ))
        durations.update(transact_and_time(connection.delete_paper, paper_id))
        durations.update(transact_and_time(connection.delete_author, author_id))

        trials[i] = list(durations.values())

    result = np.vstack((
        np.min(trials, axis=0),
        np.max(trials, axis=0),
        np.mean(trials, axis=0)
    ))

    df = pd.DataFrame(result, columns=durations.keys(), index=['min', 'max', 'mean'])
    df.to_csv(pjoin(path, 'results', 'neo4j_delete_scale2.csv'))

    print(df)

    # Close connection
    connection.close()

    # Print so that subprocess.check_output gets the result
    print(durations)