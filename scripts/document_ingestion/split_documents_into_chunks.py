from pathlib import Path
from typing import Annotated
import pandas as pd

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
    path_chuncks = pd.DataFrame(columns=["document_name", "chunk"])
    for document_path in documents_path:
        path_chuncks = path_chuncks.append(
            {
                "path": document_path.name,
                "chunk": split_documents_into_chunks(document_path),
            }
        )
        chunks.append(split_documents_into_chunks(document_path))


if __name__ == "__main__":
    typer.run(main)
