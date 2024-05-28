from pathlib import Path
from typing import Annotated

import typer

from src.document_ingestion.split_documents import split_documents_into_chunks


def main(
    documents_folder_path: Annotated[Path, typer.Option(...)],
    output_parquet_path: Annotated[Path, typer.Option(...)],
):
    print(
        f"Splitting documents from {documents_folder_path} into chunks and saving them to {output_parquet_path}"
    )
    documents_path = documents_folder_path.glob("*.pdf")
    chunks = []
    for document_path in documents_path:
        chunks.append(split_documents_into_chunks(document_path))


if __name__ == "__main__":
    typer.run(main)
