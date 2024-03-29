def delete_paper(self, id):
    """
    Delete a paper and its associated references.
    """
    def delete_paper_tx(tx, id):
        query = (
            """
            MATCH (p:Paper)
            WHERE p.id = $id
            DETACH DELETE p
            """
        )
        tx.run(query, id=id)
    
    with self.driver.session(database=self.instance) as session:
        session.execute_write(delete_paper_tx, id)


def delete_author(self, id):
    """
    Delete an author and their associated authorships.
    """
    def delete_author_tx(tx, id):
        query = (
            """
            MATCH (a:Author)
            WHERE a.id = $id
            DETACH DELETE a
            """
        )
        tx.run(query, id=id)
    
    with self.driver.session(database=self.instance) as session:
        session.execute_write(delete_author_tx, id)


def delete_reference(self, reference):
    """
    Delete the edge corresponding to the relationship passed as argument.
    """
    def delete_reference_tx(tx, reference):
        query = (
            """
            MATCH (p1:Paper)-[r]->(p2:Paper)
            WHERE p1.id = $reference[0] AND p2.id = $reference[1]
            DELETE r
            """
        )
        tx.run(query, reference=reference)
    
    with self.driver.session(database=self.instance) as session:
        session.execute_write(delete_reference_tx, reference)


def delete_authorship(self, authorship):
    """
    Delete the edge corresponding to the relationship passed as argument.
    """
    def delete_authorship_tx(tx, authorship):
        query = (
            """
            MATCH (a:Author)-[r]-(p:Paper)
            WHERE a.id = $authorship[0] AND p.id = $authorship[1]
            DELETE r
            """
        )
        tx.run(query, authorship=authorship)
    
    with self.driver.session(database=self.instance) as session:
        session.execute_write(delete_authorship_tx, authorship)


def clear_database(self):
    """
    Clear the whole database.
    """
    def clear_database_tx(tx):
        tx.run(
            """
            CALL apoc.periodic.iterate("MATCH (n) RETURN n", "DETACH DELETE n", {batchSize:1000})
            """
        )
        
    with self.driver.session(database=self.instance) as session:
        session.execute_write(clear_database_tx)


def remove_constraints(self):
    """
    Remove all constraints and indexes.
    """
    def remove_constraints_tx(tx):
        tx.run(
            """
            CALL apoc.schema.assert({}, {})
            """
        ) 
    with self.driver.session(database=self.instance) as session:
        session.execute_write(remove_constraints_tx)
