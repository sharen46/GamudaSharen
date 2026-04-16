Vector DB Selection: I chose ChromaDB because it is a lightweight, serverless vector store that allows for rapid prototyping and local storage without needing external API management.

Chunking Strategy: Used RecursiveCharacterTextSplitter with a 1000-character size. This ensures that large project update paragraphs are kept intact, providing the LLM with enough context to provide high-fidelity answers.

Multi-Agent Routing: A keyword-based router handles traffic between the PDF and CSV agents. This was chosen over semantic routing to ensure 100% deterministic accuracy for budget-related queries.

