import logging
from typing import Optional, List, Dict, Any

import tablestore
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import VectorStoreQuery
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.vector_stores.tablestore import TablestoreVectorStore
from pydantic import BaseModel

from tablestore_mcp_server.embedding.provider import create_embedding
from tablestore_mcp_server.settings import TablestoreSettings, EmbeddingProviderSettings

logger = logging.getLogger(__name__)

Metadata = Dict[str, Any]


class Entry(BaseModel):
    """
    A single entry in the table of Tablestore.
    """

    content: str
    metadata: Optional[Metadata] = None


class TablestoreConnector:
    def __init__(
        self,
        embedding: BaseEmbedding,
        instance_name: str,
        end_point: str,
        access_key_id: str,
        access_key_secret: str,
        table_name: str,
        index_name: str,
        vector_dimension: int,
        text_field: str,
        vector_field: str,
        metadata_mappings: Optional[List[tablestore.FieldSchema]] = None,
        **kwargs: Any,
    ):
        self._embedding = embedding
        tablestore_client = tablestore.OTSClient(
            end_point=end_point,
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            instance_name=instance_name,
            retry_policy=tablestore.WriteRetryPolicy(),
            **kwargs,
        )
        self._store = TablestoreVectorStore(
            tablestore_client=tablestore_client,
            table_name=table_name,
            index_name=index_name,
            vector_dimension=vector_dimension,
            text_field=text_field,
            vector_field=vector_field,
            # optional: custom metadata mapping is used to filter non-vector fields.
            metadata_mappings=metadata_mappings,
            **kwargs,
        )
        # validate parameters
        logger.info(f"""parameters:
            instance_name={instance_name}
            table_name={table_name}
            index_name={index_name}
            vector_dimension={vector_dimension}
            text_field={text_field}
            vector_field={vector_field}
            """)
        sample_embedding = self._embedding.get_text_embedding("check embedding dimension")
        if len(sample_embedding) != vector_dimension:
            raise ValueError(f"embedding dimension does not match, embedding provider is {len(sample_embedding)} but configuration is {vector_dimension}")
        self._store.create_table_if_not_exist()
        self._store.create_search_index_if_not_exist()
        (schemas, _) = tablestore_client.describe_search_index(table_name=table_name, index_name=index_name)
        for schema in schemas.fields:
            if schema.field_name == vector_field and schema.vector_options:
                if schema.vector_options.dimension != vector_dimension:
                    raise ValueError(
                        f"index vector options does not match dimension, dimension in schema is {schema.vector_options.dimension} but configuration is {vector_dimension}"
                    )
                else:
                    logger.debug(f"vector options matches dimension {schema.vector_options.dimension}")

    def store(self, entry: Entry):
        node = TextNode()
        node.text = entry.content
        if entry.metadata:
            node.metadata = entry.metadata
        node.embedding = self._embedding.get_text_embedding(node.text)
        logger.info(f"Storing {node}")
        self._store.add(nodes=[node])

    def search(self, query: str, size: int = 20) -> list[Entry]:
        logger.info(f"Search query: {query}, size: {size}")
        # Embed the query
        query_embedding = self._embedding.get_query_embedding(query)

        # Search in tablestore
        search_results = self._store.query(
            query=VectorStoreQuery(
                mode=VectorStoreQueryMode.HYBRID,
                query_embedding=query_embedding,
                query_str=query,
                similarity_top_k=size,
            ),
            knn_top_k=min(1000, size + 100),
        )
        return [
            Entry(
                content=node.text,
                metadata=node.metadata,
            )
            for node in search_results.nodes
        ]

    @classmethod
    def from_settings(cls, embedding_settings: EmbeddingProviderSettings, tablestore_settings: TablestoreSettings) -> "TablestoreConnector":
        embedding = create_embedding(embedding_settings)
        return cls(
            embedding=embedding,
            instance_name=tablestore_settings.instance_name,
            end_point=tablestore_settings.end_point,
            access_key_id=tablestore_settings.access_key_id,
            access_key_secret=tablestore_settings.access_key_secret,
            table_name=tablestore_settings.table_name,
            index_name=tablestore_settings.index_name,
            vector_dimension=tablestore_settings.vector_dimension,
            text_field=tablestore_settings.text_field,
            vector_field=tablestore_settings.vector_field,
        )
