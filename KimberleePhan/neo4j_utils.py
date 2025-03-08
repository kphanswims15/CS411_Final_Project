# neo4j
from neo4j import GraphDatabase

# connects to the database
def db_connect():
    URI = "bolt://localhost:7687/academicworld"
    AUTH = ("neo4j", "password")

    db = GraphDatabase.driver(URI, auth=AUTH)
    return db

# returns the publication id for the selected faculty
def get_publication_count(name):
    try: 
        db = db_connect()
    except:
        print("neo4j connection unsuccessful")
        return 3
    else:
        print("neo4j connection successful")

    print(name)
    neo4j_query = "MATCH (f:FACULTY {name: $name})-[pub:PUBLISH]->(p:PUBLICATION) RETURN count(p) as count"
    with db.session(database='academicworld') as session:
        print("Executing query: " + neo4j_query)
        data = session.run(neo4j_query, name=name)
        process_data = data.single()
    db.close()
    return process_data