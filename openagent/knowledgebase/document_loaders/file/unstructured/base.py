"""Unstructured file reader.

A parser for unstructured text files using Unstructured.io.
Supports .txt, .docx, .pptx, .jpg, .png, .eml, .html, and .pdf documents.

"""
from pathlib import Path
from typing import Any, Dict, List, Optional

from openagent.knowledgebase.document_loaders.basereader import BaseReader
from openagent.schema import DocumentNode


class UnstructuredReader(BaseReader):
    """General unstructured text reader for a variety of files."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)

        # Prerequisite for Unstructured.io to work
        import nltk

        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")

    def load_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        split_documents: Optional[bool] = False,
    ) -> List[DocumentNode]:
        """Parse file."""
        from unstructured.partition.auto import partition

        elements = partition(str(file))
        text_chunks = [" ".join(str(el).split()) for el in elements]

        if split_documents:
            return [
                DocumentNode(text=chunk, extra_info=extra_info or {})
                for chunk in text_chunks
            ]
        else:
            return [
                DocumentNode(text="\n\n".join(text_chunks), extra_info=extra_info or {})
            ]
