from typing import List
from fastapi import APIRouter, UploadFile, File
from backend.models.file_model import (
    FileMetadata,
    CreateFileRequest,
    RenameFileRequest
)
from backend.controllers.file_controller import FileController

router = APIRouter(prefix="/api/files", tags=["File Management"])

@router.get("", response_model=List[FileMetadata])
def list_files():
    return FileController.list_files()

@router.get("/{file_id}", response_model=FileMetadata)
def get_file(file_id: str):
    return FileController.get_file(file_id)

@router.post("/upload", response_model=FileMetadata)
async def upload_file(file: UploadFile = File(...)):
    return await FileController.upload_file(file)

@router.post("/create", response_model=FileMetadata)
def create_file(req: CreateFileRequest):
    return FileController.create_file(req)

@router.put("/{file_id}/rename", response_model=FileMetadata)
def rename_file(file_id: str, req: RenameFileRequest):
    return FileController.rename_file(file_id, req)

@router.delete("/{file_id}")
def delete_file(file_id: str):
    return FileController.delete_file(file_id)
