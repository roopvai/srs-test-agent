import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import boto3

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
index = pc.Index(INDEX_NAME)

bedrock = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

def embed_text(text: str) -> list:
    body = json.dumps({"inputText": text})
    resp = bedrock.invoke_model(modelId=os.getenv("EMBED_MODEL_ID"), body=body)
    return json.loads(resp["body"].read())["embedding"]

def upsert_chunk(chunk_id: str, text: str, metadata: dict = None):
    vector = embed_text(text)
    meta = metadata or {}
    meta["text"] = text
    index.upsert(vectors=[{"id": chunk_id, "values": vector, "metadata": meta}])

def retrieve_context(query: str, top_k: int = 5) -> list:
    vector = embed_text(query)
    results = index.query(vector=vector, top_k=top_k, include_metadata=True)
    return [m["metadata"] for m in results["matches"]]

if __name__ == "__main__":
    upsert_chunk("test-1", "The system shall allow users to reset their password via email.")
    print("Upserted a test chunk.")
    results = retrieve_context("password reset")
    print("Retrieved:", results)