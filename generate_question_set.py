import pinecone
import os

class QuestionSet:
    def __init__(self):
        self.kb_index_name = "kb"

    def fetch_qs_from_kb(self):
        pinecone.init(
            api_key = os.environ.get('pinecone_kb'),
            environment="gcp-starter",
        )
        index = pinecone.Index(self.kb_index_name)
        index.query(
            vector=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
            filter={
                "genre": {"$eq": "documentary"},
                "year": 2019
            },
            top_k=1,
            include_metadata=True
        )