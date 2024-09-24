from langchain_community.document_loaders import WikipediaLoader


async def wikipedia_query(parameters: dict) -> str:
    query = parameters.get("query")
    if not query:
        raise ValueError("Query parameter is required for Wikipedia search")

    load_max_docs = parameters.get("load_max_docs", 2)

    loader = WikipediaLoader(query=query, load_max_docs=load_max_docs)
    documents = loader.load()

    # Format the results as string
    result = "\n\n".join(
        [
            f"Title: {doc.metadata['title']}\n"
            f"Summary: {doc.metadata['summary']}\n"
            f"Content: {doc.page_content}..."
            for doc in documents
        ]
    )
    return result
