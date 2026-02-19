from langchain_core.tools import tool
from vector_store import get_vector_store, CSV_PATH
from language_utils import detect_language
from query_normalizer import normalize_to_english


@tool
def search_faq(query: str) -> str:
    """
    Search IDALS FAQ knowledge base.
    Supports English, Hinglish, and Hindi queries.
    """
    lang = detect_language(query)

    search_query = query
    if lang in ["hi", "hi_en"]:
        search_query = normalize_to_english(query)

    store = get_vector_store(CSV_PATH)
    results = store.similarity_search(search_query, k=3)

    if not results:
        return "This information is not specified in the IDALS program details."

    return "\n\n".join(
        f"IDALS Official Info:\n{r.page_content}"
        for r in results
    )
