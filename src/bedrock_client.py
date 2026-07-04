import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

def invoke_claude(system_prompt: str, user_prompt: str, max_tokens: int = 1000) -> str:
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    response = client.invoke_model(
        modelId=os.getenv("BEDROCK_MODEL_ID"),
        body=json.dumps(body),
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]

if __name__ == "__main__":
    answer = invoke_claude("You are a helpful assistant.", "Say hello in one sentence.")
    print(answer)