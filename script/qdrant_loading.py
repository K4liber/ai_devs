import json
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


COLLECTION_NAME = 'ai_devs_intfloat_1024'


if __name__ == '__main__':
    client = QdrantClient(host="localhost", port=6333)
    client.set_model('intfloat/multilingual-e5-large')
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            'fast-multilingual-e5-large': VectorParams(
                size=1024,
                distance=Distance.COSINE
            )
        },
    )
    docs = []
    metadata = []
    ids = []

    with (Path('data') / 'archiwum.json', 'r') as archive_file:
        data = json.load(archive_file)

        for index, single_element in enumerate(data[:500], start=1):
            title = single_element['title']

            if 'pseudonimizacja od anonimizacji' in title:
                print(f'Found article under index {index}. Title = {title}')

            content = title + ' ' + single_element['info']
            docs.append(content)
            metadata.append({
                'source': single_element['url']
            })
            ids.append(index)

    client.add(
        collection_name=COLLECTION_NAME,
        documents=docs,
        metadata=metadata,
        ids=ids
    )
