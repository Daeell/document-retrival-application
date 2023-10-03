import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct, CollectionStatus, UpdateStatus
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from qdrant_client.http import models
from typing import List
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

class QdrantVectorStore:
    def __init__(self, host: str = "localhost",
                 port: int = 6333,
                 collection_name: str = "test_collection",
                 vector_size: int = 1536,
                 vector_distance=Distance.COSINE
                 ):
        self.client = QdrantClient(url=host,port=port)
        self.collection_name = collection_name

        try:
            collection_info = self.client.get_collection(collection_name=collection_name)
        except Exception as e:
            print("Collection does not exist, creating collection now")
            self.set_up_collection(collection_name,  vector_size, vector_distance)

    def set_up_collection(self, collection_name: str, vector_size: int, vector_distance: str):
        self.client.recreate_collection(collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=vector_distance))

        collection_info = self.client.get_collection(collection_name=collection_name)
    
    def upsert_data(self, data: List[dict]):
        points = []
        for item in data:
            nickname = item.get('nickname')
            question = item.get('question')
            answer = item.get('answer')
            text_vector = model.encode(question)
            text_id = str(uuid.uuid4())
            payload = {'nickname':nickname, 'question':question, 'answer':answer}
            point = PointStruct(
                id=text_id, vector=text_vector, payload=payload
            )
            points.append(point)
        
        operation_info = self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=points
        )

        if operation_info.status == UpdateStatus.COMPLETED:
            print("DATA INSERT SUCCESS")
        else:
            print("DATA INSERT FAIL")