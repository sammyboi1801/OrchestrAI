from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_community.tools.pubmed.tool import PubmedQueryRun


ARXIV_SEARCH = ArxivAPIWrapper(
    top_k_results = 5,
    ARXIV_MAX_QUERY_LENGTH = 300,
    load_max_docs = 5,
    load_all_available_meta = False,
    doc_content_chars_max = 40000
)


PUBMED_SEARCH = PubmedQueryRun()