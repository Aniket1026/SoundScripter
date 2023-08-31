# Purpose: Download service to handle file download related tasks
# Path: backend/app/services/files/download.py

import io
import zipfile
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse

from app.services.files import FileService


class DownloadService(FileService):
    """
    Download service
    """

    def __init__(self, file_id: str) -> None | HTTPException:
        """
        Download service
        :param file_id:
        :return None | HTTPException
        """

        super().__init__()

        self.file_id = file_id
        self.file_path: Path = Path(self.get_transcription_file_path(self.file_id))

        if not self.validate_file_path(self.file_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: Bad Request",
            )

    async def generate_zip(self) -> BytesIO | Exception:
        """
        Generate zip file
        :return: BytesIO | Exception
        """

        try:
            zip_stream = io.BytesIO()

            with zipfile.ZipFile(zip_stream, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file in self.file_path.glob("**/*"):
                    if file.is_file():
                        relative_path = file.relative_to(self.file_path)
                        zipf.write(file, arcname=str(relative_path))

            return zip_stream

        except Exception as e:
            raise Exception(
                {
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "detail": "Zip file generation failed",
                }
            ) from e

    async def download(self) -> StreamingResponse | HTTPException:
        """
        Download file
        :param file: UploadFile
        :return: StreamingResponse | HTTPException
        """

        try:
            # Generate the ZIP archive asynchronously
            zip_stream: BytesIO = await self.generate_zip()

            # Serve the ZIP archive as a downloadable file
            return StreamingResponse(
                io.BytesIO(zip_stream.getvalue()),
                media_type="application/zip",
                headers={
                    "Content-Disposition": f"attachment; filename={self.file_id}.zip"
                },
            )

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            detail = "Error: Bad Request"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e
