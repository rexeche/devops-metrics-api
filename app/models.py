from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DeploymentRecord(BaseModel):
    service_name: str
    environment: str  # dev, staging, prod
    version: str
    status: str  # success, failure, rollback
    deployed_at: datetime = datetime.now()
    deploy_duration_seconds: Optional[int] = None
    deployed_by: Optional[str] = None


class DeploymentMetrics(BaseModel):
    service_name: str
    total_deploys: int
    success_rate: float
    avg_deploy_duration_seconds: float
    deploys_last_7_days: int
    last_failure: Optional[datetime] = None
