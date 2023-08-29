# Purpose: Base Class for file services
# Path: backend/app/services/files/__init__.py

import os
from datetime import datetime
from uuid import uuid4


class FileService:
    chunk_size_bytes: int = 1024
    directory: str = "data"
    filename: str = "file"
    transcripted_files: str = "transcriptions"
    output_directory: str = "zips"

    audio_file_extensions: list[str] = [
        "aac",
        "mid",
        "mp3",
        "m4a",
        "ogg",
        "flac",
        "amr",
        "aiff",
        "mpeg",
    ]
    video_file_extensions: list[str] = [
        "3gp",
        "mp4",
        "m4v",
        "mkv",
        "webm",
        "mov",
        "avi",
        "wmv",
        "mpg",
        "flv",
    ]

    audio_file_types: list[str] = [
        "audio/aac",
        "audio/midi",
        "audio/mpeg",
        "audio/mp4",
        "audio/ogg",
        "audio/x-flac",
        "audio/x-wav",
        "audio/amr",
        "audio/x-aiff",
    ]
    video_file_types: list[str] = [
        "video/3gpp",
        "video/mp4",
        "video/x-m4v",
        "video/x-matroska",
        "video/webm",
        "video/quicktime",
        "video/x-msvideo",
        "video/x-ms-wmv",
        "video/mpeg",
        "video/x-flv",
    ]

    @classmethod
    def __init__(cls) -> None:
        if not os.path.exists(cls.directory):
            os.makedirs(cls.directory)

        if not os.path.exists(cls.output_directory):
            os.makedirs(cls.output_directory)

    @classmethod
    def is_audio_file_extension(cls, file_extension: str) -> bool:
        """
        Get file type
        :param file_path: str
        :return: bool
        """
        return file_extension in cls.audio_file_extensions

    @classmethod
    def is_video_file_extension(cls, file_extension: str) -> bool:
        """
        Get file type
        :param file_path: str
        :return: bool
        """
        return file_extension in cls.video_file_extensions

    @classmethod
    def is_valid_file_extension(cls, file_extension: str) -> bool:
        """
        Get file type
        :param file_path: str
        :return: bool
        """
        return cls.is_audio_file_extension(
            file_extension
        ) or cls.is_video_file_extension(file_extension)

    @classmethod
    def is_audio_file(cls, file_type: str) -> bool:
        """
        Get file type
        :param file_path: str
        :return: bool
        """
        return file_type in cls.audio_file_types

    @classmethod
    def is_video_file(cls, file_type: str) -> bool:
        """
        Get file type
        :param file_path: str
        :return: bool
        """
        return file_type in cls.video_file_types

    @classmethod
    def validate_file_type(cls, file_type: str) -> bool:
        """
        Validate file type
        :param file_type: str
        :return: bool
        """
        return cls.is_audio_file(file_type) or cls.is_video_file(file_type)

    @classmethod
    def get_unique_file_name(self) -> str:
        """
        Generate a unique file name
        :param file_name: str
        :return: str
        """
        return datetime.now().strftime("%Y%m-%d%H-%M%S-") + str(uuid4())

    @classmethod
    def get_file_extension(cls, file_name: str) -> str:
        """
        Get file extension
        :param file_name: str
        :return: str
        """
        indx: int = file_name.rfind(".")
        return file_name[indx:] if indx != -1 else ""

    @classmethod
    def get_file_path_from_id(cls, file_id: str) -> str:
        """
        Get file path
        :param file_name: str
        return: str
        """
        folder: str = cls.directory + "/" + file_id

        try:
            for file in os.listdir(folder):
                file_extension: str = cls.get_file_extension(file_name=file)
                if file_extension != "" and cls.is_valid_file_extension(
                    file_extension=file_extension[1:]
                ):
                    return folder + "/" + file

            return ""

        except FileNotFoundError:
            return ""

    @classmethod
    def generate_file_path(cls, file_name: str, file_extension: str) -> str:
        """
        Generate file path
        :param file_name: str
        :param file_extension: str
        :return: str
        """

        os.makedirs(cls.directory + "/" + file_name, exist_ok=True)
        return cls.directory + "/" + file_name + "/" + cls.filename + file_extension

    @classmethod
    def get_transcription_file_path(cls, file_id: str) -> str:
        """
        Get file path
        :param file_name: str
        :return: str
        """
        return cls.directory + "/" + file_id + "/" + cls.transcripted_files

    @classmethod
    def get_file_path(cls, file_id: str, file_extension: str) -> str:
        """
        Get file path
        :param file_name: str
        return: str
        """
        return cls.directory + "/" + file_id + "/" + cls.filename + file_extension

    @classmethod
    def validate_file_path(cls, file_path) -> bool:
        """
        Validate file path
        :param file_path: str
        :return: bool
        """
        return os.path.exists(file_path)
