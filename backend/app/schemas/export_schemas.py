from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ExportRequest(BaseModel):
    export_type: str = "pdf"  # pdf or png

class ExportResponse(BaseModel):
    id: str
    project_id: str
    export_type: str
    file_path: str
    download_url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
