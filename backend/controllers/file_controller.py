import os
import uuid
import json
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, UploadFile, status
from backend.models.file_model import FileMetadata, CreateFileRequest, RenameFileRequest
from backend.utils.file_utils import (
    get_language_from_filename,
    is_allowed_file,
    MAX_FILE_SIZE_BYTES
)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
METADATA_FILE = os.path.join(UPLOAD_DIR, "_metadata.json")

class FileController:
    @staticmethod
    def _ensure_upload_dir():
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            
        if not os.path.exists(METADATA_FILE):
            # Seed default demo files for MVP user experience
            demo_files = [
                {
                    "id": "file_demo_py",
                    "filename": "demo_algorithm.py",
                    "original_name": "demo_algorithm.py",
                    "extension": ".py",
                    "language": "python",
                    "size_bytes": 482,
                    "uploaded_at": datetime.now().isoformat(),
                    "content": """# AI Code Refactoring Assistant - Demo Script
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

if __name__ == "__main__":
    sample_data = [3, 6, 8, 10, 1, 2, 1]
    sorted_data = quick_sort(sample_data)
    print("Sorted Output:", sorted_data)
"""
                },
                {
                    "id": "file_demo_js",
                    "filename": "app_logic.js",
                    "original_name": "app_logic.js",
                    "extension": ".js",
                    "language": "javascript",
                    "size_bytes": 360,
                    "uploaded_at": datetime.now().isoformat(),
                    "content": """// Developer Assistant JS Demo
function calculateStats(items) {
    if (!Array.isArray(items)) {
        throw new Error("Invalid input: expected array");
    }
    const total = items.reduce((acc, curr) => acc + curr, 0);
    const average = total / items.length;
    return { total, average, count: items.length };
}

console.log(calculateStats([10, 20, 30, 40, 50]));
"""
                },
                {
                    "id": "file_demo_json",
                    "filename": "config.json",
                    "original_name": "config.json",
                    "extension": ".json",
                    "language": "json",
                    "size_bytes": 220,
                    "uploaded_at": datetime.now().isoformat(),
                    "content": """{
  "appName": "AI Code Refactoring Assistant",
  "version": "1.0.0-MVP",
  "theme": "dark",
  "autoSave": true,
  "maxUploadSizeMB": 5,
  "supportedLanguages": ["python", "javascript", "typescript", "java", "cpp", "c", "html", "css", "json"]
}"""
                }
            ]
            with open(METADATA_FILE, "w", encoding="utf-8") as f:
                json.dump(demo_files, f, indent=2)
                
            # Write initial demo disk files
            for df in demo_files:
                filePath = os.path.join(UPLOAD_DIR, df["filename"])
                with open(filePath, "w", encoding="utf-8") as f:
                    f.write(df["content"])

    @staticmethod
    def _read_metadata() -> List[dict]:
        FileController._ensure_upload_dir()
        try:
            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def _write_metadata(data: List[dict]):
        FileController._ensure_upload_dir()
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def list_files() -> List[FileMetadata]:
        raw_meta = FileController._read_metadata()
        results = []
        for item in raw_meta:
            results.append(FileMetadata(
                id=item["id"],
                filename=item["filename"],
                original_name=item.get("original_name", item["filename"]),
                extension=item.get("extension", os.path.splitext(item["filename"])[1]),
                language=item.get("language", get_language_from_filename(item["filename"])),
                size_bytes=item.get("size_bytes", 0),
                uploaded_at=item.get("uploaded_at", datetime.now().isoformat()),
                content=item.get("content")
            ))
        return results

    @staticmethod
    def get_file(file_id: str) -> FileMetadata:
        files = FileController._read_metadata()
        for item in files:
            if item["id"] == file_id:
                # Read on-disk content if present
                disk_path = os.path.join(UPLOAD_DIR, item["filename"])
                if os.path.exists(disk_path):
                    with open(disk_path, "r", encoding="utf-8", errors="ignore") as f:
                        item["content"] = f.read()
                return FileMetadata(**item)
        raise HTTPException(status_code=404, detail="File not found")

    @staticmethod
    async def upload_file(file: UploadFile) -> FileMetadata:
        FileController._ensure_upload_dir()

        if not is_allowed_file(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file format. Allowed formats: .py, .java, .js, .ts, .cpp, .c, .html, .css, .json"
            )

        content_bytes = await file.read()
        if len(content_bytes) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds maximum allowed limit of 5 MB."
            )

        try:
            content_str = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            content_str = content_bytes.decode("latin-1")

        file_id = f"file_{uuid.uuid4().hex[:8]}"
        ext = os.path.splitext(file.filename)[1].lower()
        language = get_language_from_filename(file.filename)
        
        # Save file to disk
        disk_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(disk_path, "w", encoding="utf-8") as f:
            f.write(content_str)

        new_entry = {
            "id": file_id,
            "filename": file.filename,
            "original_name": file.filename,
            "extension": ext,
            "language": language,
            "size_bytes": len(content_bytes),
            "uploaded_at": datetime.now().isoformat(),
            "content": content_str
        }

        metadata = FileController._read_metadata()
        # Check if file with same filename exists, update or append
        updated = False
        for idx, m in enumerate(metadata):
            if m["filename"].lower() == file.filename.lower():
                metadata[idx] = new_entry
                updated = True
                break
        if not updated:
            metadata.insert(0, new_entry)

        FileController._write_metadata(metadata)
        return FileMetadata(**new_entry)

    @staticmethod
    def create_file(req: CreateFileRequest) -> FileMetadata:
        FileController._ensure_upload_dir()
        
        filename = req.filename.strip()
        if not is_allowed_file(filename):
            ext = os.path.splitext(filename)[1]
            if not ext:
                # Append extension based on language
                ext_map_rev = {"python": ".py", "javascript": ".js", "typescript": ".ts", "java": ".java", "cpp": ".cpp", "c": ".c", "html": ".html", "css": ".css", "json": ".json"}
                filename += ext_map_rev.get(req.language.lower(), ".txt")

        file_id = f"file_{uuid.uuid4().hex[:8]}"
        ext = os.path.splitext(filename)[1].lower()
        lang = req.language or get_language_from_filename(filename)

        disk_path = os.path.join(UPLOAD_DIR, filename)
        with open(disk_path, "w", encoding="utf-8") as f:
            f.write(req.content)

        new_entry = {
            "id": file_id,
            "filename": filename,
            "original_name": filename,
            "extension": ext,
            "language": lang,
            "size_bytes": len(req.content.encode("utf-8")),
            "uploaded_at": datetime.now().isoformat(),
            "content": req.content
        }

        metadata = FileController._read_metadata()
        metadata.insert(0, new_entry)
        FileController._write_metadata(metadata)

        return FileMetadata(**new_entry)

    @staticmethod
    def rename_file(file_id: str, req: RenameFileRequest) -> FileMetadata:
        metadata = FileController._read_metadata()
        target = None
        for item in metadata:
            if item["id"] == file_id:
                target = item
                break

        if not target:
            raise HTTPException(status_code=404, detail="File not found")

        old_filename = target["filename"]
        new_filename = req.new_filename.strip()

        if not is_allowed_file(new_filename):
            raise HTTPException(status_code=400, detail="Invalid target file extension.")

        old_path = os.path.join(UPLOAD_DIR, old_filename)
        new_path = os.path.join(UPLOAD_DIR, new_filename)

        if os.path.exists(old_path):
            os.rename(old_path, new_path)

        target["filename"] = new_filename
        target["extension"] = os.path.splitext(new_filename)[1].lower()
        target["language"] = get_language_from_filename(new_filename)

        FileController._write_metadata(metadata)
        return FileMetadata(**target)

    @staticmethod
    def delete_file(file_id: str) -> dict:
        metadata = FileController._read_metadata()
        target = None
        new_metadata = []

        for item in metadata:
            if item["id"] == file_id:
                target = item
            else:
                new_metadata.append(item)

        if not target:
            raise HTTPException(status_code=404, detail="File not found")

        disk_path = os.path.join(UPLOAD_DIR, target["filename"])
        if os.path.exists(disk_path):
            try:
                os.remove(disk_path)
            except Exception:
                pass

        FileController._write_metadata(new_metadata)
        return {"success": True, "message": f"File '{target['filename']}' deleted successfully."}
