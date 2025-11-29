# bedrock_utils.py
import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

REGION = "us-west-2"

bedrock = boto3.client("bedrock-runtime", region_name=REGION)
bedrock_kb = boto3.client("bedrock-agent-runtime", region_name=REGION)

def valid_prompt(prompt: str, model_id: str = "anthropic.claude-3-haiku-20240307") -> bool:
    """
    Validate prompt
    """

    if not prompt or not prompt.strip():
        return False


    p = prompt.lower()

    # Expanded keyword list
    keywords = [
        "machine", "machinery", "heavy machinery", "excavator", "bulldozer",
        "hydraulic", "engine", "crane", "loader", "gearbox", "transmission",
        "lift", "drill", "compressor", "industrial", "truck", "dump truck",
        "payload", "capacity", "specs", "specifications"
    ]


    try:
        validation_prompt = (
            f"Determine if the following user prompt is about heavy machinery. "
            f"Answer only 'YES' or 'NO'.\n\nPrompt: {prompt}"
        )

        resp = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "messages": [{"role": "user", "content": [{"type": "text", "text": validation_prompt}]}],
                "max_tokens": 10,
                "temperature": 0.0,
                "top_p": 1.0
            })
        )

        body = resp["body"].read()
        parsed = json.loads(body)
        answer = parsed.get("content", [{}])[0].get("text", "").strip().upper()

        if answer.startswith("YES"):
            return True

    except Exception as e:
        print("Semantic validation failed:", e)

    # Fallback to keyword filter
    return any(k in p for k in keywords)



def query_knowledge_base(query: str, kb_id: str, num_results: int = 3):
    """
    Calls Bedrock and retrieve info.
    """
    try:
        resp = bedrock_kb.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={"text": query},
            retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": num_results}}
        )
        return resp.get("retrievalResults", [])
    except (NoCredentialsError, PartialCredentialsError):
        print("AWS credentials not found or incomplete. Set AWS env/profile.")
        return []
    except ClientError as e:

        print("Client Error query KB:", e)
        return []
    except Exception as e:
        print("Unexpected error query run for KB:", e)
        return []

def generate_response(prompt: str, model_id: str, temperature: float = 0.7, top_p: float = 0.9):
    """
    Call for Bedrock .
    """
    try:
        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]

        resp = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",   # REQUIRED
                "messages": messages,
                "max_tokens": 400,
                "temperature": temperature,
                "top_p": top_p
            })
        )

        body = resp["body"].read()
        parsed = json.loads(body)
        return parsed.get("content", [{}])[0].get("text", "").strip()

    except (NoCredentialsError, PartialCredentialsError):
        return "Model call skipped: AWS credentials missing or incomplete."
    except ClientError as e:
        return f"Model call failed: {e}"
    except Exception as e:
        return f"Unexpected error generating response: {e}"


    except (NoCredentialsError, PartialCredentialsError):
        return "Model call skipped: AWS credentials missing or incomplete."
    except ClientError as e:
        return f"Model call failed: {e}"
    except Exception as e:
        return f"Unexpected error generating response: {e}"
