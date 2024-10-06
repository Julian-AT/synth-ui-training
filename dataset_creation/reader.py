import re
import unicodedata
from typing import Callable

from datatrove.pipeline.readers.base import BaseDiskReader
from datatrove.io import DataFolderLike

# Block the following formats.
IMAGE = ["png", "jpg", "jpeg", "gif"]
VIDEO = ["mp4", "jfif"]
DOC = ["key", "PDF", "pdf", "docx", "xlsx", "pptx", "csv", "tsv", "txt"]
AUDIO = ["flac", "ogg", "mid", "webm", "wav", "mp3"]
ARCHIVE = ["jar", "aar", "gz", "zip", "bz2"]
MODEL = ["onnx", "pickle", "model", "neuron"]
OTHERS = [
    "npy",
    "index",
    "inv",
    "index",
    "DS_Store",
    "rdb",
    "pack",
    "idx",
    "glb",
    "gltf",
    "len",
    "otf",
    "unitypackage",
    "ttf",
    "xz",
    "pcm",
    "opus",
    "package-lock.json",
    "lock",
    "yaml",
    "yml",
    "xml",
    "html",
    "editorconfig",
    "gitignore",
    "gitattributes",
    "gitmodules",
    "gitkeep",
    "git",
    "prettierignore",
    "prettier",
    "vue",
    "nvmrc",
    "npmrc",
    "npmignore",
    "json",
    "snap",
    "config.js",
    "md",
    "mdx"
]

ANTI_FOMATS = tuple(IMAGE + VIDEO + DOC + AUDIO + ARCHIVE + OTHERS)

def clean_markdown(text):
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\n+", "", text)
    text = text.replace("#", "")
    return text


class SynthUIDatasetReader(BaseDiskReader):
    name = "SynthUI Reader"

    def __init__(
        self,
        data_folder: DataFolderLike,
        limit: int = -1,
        progress: bool = True,
        adapter: Callable = None,
        text_key: str = "content",
        id_key: str = "file_path",
        default_metadata: dict = None,
        recursive: bool = True,
        glob_pattern: str | None = None,
    ):
        super().__init__(
            data_folder,
            limit,
            progress,
            adapter,
            text_key,
            id_key,
            default_metadata,
            recursive,
            glob_pattern,
        )
        self.empty_warning = False

    def read_file(self, filepath: str):
        try:
            if filepath.endswith(ANTI_FOMATS) or any(
                k in filepath for k in [".git", "__pycache__", "xcodeproj"]
            ):
                content = ""
            else:
                with self.data_folder.open(filepath, "r", encoding="utf-8",) as file:
                    content = file.read()
                    # encode all unicode characters to ascii
                    content = unicodedata.normalize("NFKD", content).encode(
                        "ascii", "ignore"
                    ).decode("ascii")
        except Exception:
            content = ""

        if not content:
            content = ""
            
            
        data = { "content": content, "file_path": filepath }
        with self.track_time():
            document = self.get_document_from_dict(data, filepath, 0)
            if not document:
                return
            
            document.metadata["file_path"] = document.metadata["file_path"].split(
                self.data_folder.path
            )[-1][1:]
            fp_parts = document.metadata["file_path"].split("/")
            document.metadata["repo_id"] = f"{fp_parts[0]}/{fp_parts[1]}"
        yield document