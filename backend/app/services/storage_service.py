import os
import shutil
from pathlib import Path
from ..config import settings
from ..utils.sanitize import sanitize_filename
from ..utils.logger import get_logger

logger = get_logger("storage_service")

class StorageService:
    def get_project_dir(self, project_id: str) -> str:
        p_dir = os.path.join(settings.STORAGE_DIR, "projects", sanitize_filename(project_id))
        os.makedirs(p_dir, exist_ok=True)
        os.makedirs(os.path.join(p_dir, "characters"), exist_ok=True)
        os.makedirs(os.path.join(p_dir, "panels"), exist_ok=True)
        os.makedirs(os.path.join(p_dir, "exports"), exist_ok=True)
        return p_dir

    def get_panel_image_path(self, project_id: str, panel_number: int) -> str:
        p_dir = self.get_project_dir(project_id)
        return os.path.join(p_dir, "panels", f"panel_{panel_number}.png")

    def get_export_path(self, project_id: str, filename: str) -> str:
        p_dir = self.get_project_dir(project_id)
        return os.path.join(p_dir, "exports", sanitize_filename(filename))

    def delete_project_storage(self, project_id: str):
        p_dir = os.path.join(settings.STORAGE_DIR, "projects", sanitize_filename(project_id))
        if os.path.exists(p_dir):
            shutil.rmtree(p_dir, ignore_errors=True)
            logger.info(f"Deleted project storage for {project_id}")

storage_service = StorageService()
