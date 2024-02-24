from fastapi import APIRouter,UploadFile,HTTPException
import shutil
from typing import List,Optional
import os
from fastapi.responses import FileResponse


router = APIRouter(prefix='/attachments')

@router.post('/upload_pics',tags=['Attachments'])
async def add_attachment(request: List[UploadFile] = None):
    for data1 in request:
        filename = data1.filename
        print("file_name==>",filename)
        file_path = f"/Users/mango/Documents/updated_project_file/pgWorld/pg_pics/{filename}"
        try:
            with open(file_path, "wb") as f:
                shutil.copyfileobj(data1.file, f)
            print("saved successfully")
        except Exception as e:
            print("exception rasised==>",e)
            raise HTTPException(status_code=100, detail="wrong attachment received")
    return {"msg" : "pic attached Successfully"}



@router.post('/download', tags=['Attachments'])
async def download_ticket(filename: str):
    file_path = f"/Users/mango/Documents/updated_project_file/pgWorld/pg_pics/{filename}"
    if not os.path.exists(file_path):
        print("file not found")
    return FileResponse(file_path, filename=filename) 
