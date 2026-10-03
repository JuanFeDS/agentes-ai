"""ingest.py"""
import os
from datetime import datetime

from pathlib import Path
import json

import feedparser

def ingest_arxiv(
    max_results: int,
    query: 'str' = 'maths',
    out_dir: Path = Path('data/raw')
):
    """Ingestar documentos de arxiv.
    
    Args:
        max_results (int): Número máximo de documentos a ingestar.
        query (str, optional): Consulta a realizar. Defaults to 'maths'.
        out_dir (Path, optional): Directorio de salida. Defaults to Path('data/raw').

    Returns:
        feedparser.FeedParserDict: FeedParserDict con la respuesta de la consulta.
    """

    date_str = datetime.now().strftime('%Y%m%d')

    query = query.replace(' ', '_')
    url = f"""
        http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}
    """

    feed = feedparser.parse(url)

    docs = []

    for entry in feed.entries:
        doc = {
            'id': entry.id,
            'title': entry.title.replace('\n', ' '),
            'published': entry.published,
            'url_abstract': entry.link,
            'url_pdf': entry.link.replace('/abs/', '/pdf/'),
            'summary': entry.summary.replace('\n', ' '),
            'download_at': datetime.now().isoformat(),
        }

        docs.append(doc)

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f'arxiv_{query}_{date_str}.json')

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    return feed
