from pydantic import BaseModel
class Settings(BaseModel):
    PROJECT_NAME: str = "Garanti BBVA Finansal Pusula AI"
    VERSION: str = "1.1.0"
    API_STR: str = "/api/v1"

settings = Settings()