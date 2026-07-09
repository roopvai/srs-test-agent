# AI Test Case & Quality Risk Generator

An AI agent that takes a software requirements document and automatically generates test cases, edge cases, and quality risk flags, grounded with RAG so output reflects real testing standards instead of generic LLM guesses.

## The problem

QA teams spend a lot of time manually translating requirements into test cases. This process is inconsistent, prone to missed edge cases, and doesn't catch requirement-quality problems like ambiguity until much later, when they're expensive to fix.

## Stack

Amazon Bedrock (Claude), Amazon Titan Embeddings, Pinecone, Pydantic, Python, Streamlit.

## Validation

Tested with a self-designed check: a 49-requirement sample document included deliberately vague requirements planted on purpose. The quality-risk pass correctly flagged them as untestable across 5 separate detections.

Sample output is in the samples folder.

## Getting started
git clone https://github.com/roopvai/srs-test-agent.git
cd srs-test-agent
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

## Known limitations

- Chunking is regex-based
- No formal evaluation harness yet
- Sequential processing, not parallelized
- No human-in-the-loop review gate in the UI yet

## License

MIT
