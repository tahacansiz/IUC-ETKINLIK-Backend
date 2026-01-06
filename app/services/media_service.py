import os
from fastapi import UploadFile, HTTPException
from uuid import uuid4

UPLOAD_DIR = "media/uploads/events"

class MediaService:

    @staticmethod
    async def save_event_poster(
        file: UploadFile,
        event_id: str
    ) -> str:

        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(400, "Only JPG and PNG allowed")

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        ext = file.filename.split(".")[-1]
        filename = f"{event_id}_{uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        return f"/{UPLOAD_DIR}/{filename}"
