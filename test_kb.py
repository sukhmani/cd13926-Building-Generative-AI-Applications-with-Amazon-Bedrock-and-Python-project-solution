from bedrock_utils import query_knowledge_base

kb_id = "ETH49KVDLZ"

# Try a few queries to test retrieval
queries = [
    "Tell me about bulldozer hydraulics",
    "What are the specs of the DT1000 dump truck?",
    "How does the MC750 mobile crane operate?",
    "Describe the forklift F1250 features",
    "Explain the excavator X950 capabilities"
]

for q in queries:
    print(f"\n Query: {q}")
    results = query_knowledge_base(q, kb_id)
    if not results:
        print("No results returned.")
    else:
        for i, r in enumerate(results, start=1):
            print(f"\nResult {i}:")
            print(r.get("content", "No content found"))

