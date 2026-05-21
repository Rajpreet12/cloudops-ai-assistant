import boto3
import json
import time
import random
from dotenv import load_dotenv
import os

load_dotenv()

REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("MODEL_ID", "anthropic.claude-sonnet-4-5")
KB_ID = os.getenv("KB_ID")

bedrock = boto3.client("bedrock-runtime", region_name=REGION)
bedrock_agent = boto3.client("bedrock-agent-runtime", region_name=REGION)
cw = boto3.client("cloudwatch", region_name=REGION)

def invoke_claude(prompt, system="You are a CloudOps AI assistant.", max_tokens=1000):
    for attempt in range(5):
        try:
            response = bedrock.invoke_model(
                modelId=MODEL_ID,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
                    "system": system,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            return json.loads(response["body"].read())["content"][0]["text"]
        except bedrock.exceptions.ThrottlingException:
            wait = (2 ** attempt) + random.uniform(0, 1)
            print(f"  Throttled — retrying in {wait:.1f}s (attempt {attempt+1})")
            time.sleep(wait)
    raise Exception("Bedrock quota exceeded after 5 retries")
