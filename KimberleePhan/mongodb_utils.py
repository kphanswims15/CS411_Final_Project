# mongodb
from pymongo import MongoClient

# connects to mongo database
client = MongoClient("mongodb://localhost:27017/")

db = client["academicworld"]

# retrieves all keywords for a specific faculty member 
def get_keywords(uni_id, name):
    faculty = db["faculty"]
    filter = {"affiliation.id": uni_id, "name": name}
    fields = {"keywords.name": 1, "_id": 0}
    cursor = faculty.find(filter, fields)
    keywords_list = []
    for document in cursor:
        keywords = document.get("keywords", [])
        for keyword in keywords:
            keyword_name = keyword.get("name")
            if name: 
                keywords_list.append(keyword_name)
        keywords_text = ','.join(keywords_list)
        if not keywords_list:
            return "No Keywords"
        else:
            return keywords_text