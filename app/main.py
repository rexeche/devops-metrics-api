from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="DevOps Metrics API",
    description="Track DORA deployment metrics",
    version="1.0.0"
)

# In-memory store (you could swap this for DynamoDB later)
deployments: list = []


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.post("/deployments")
def record_deployment(record: dict):
    record["recorded_at"] = datetime.now().isoformat()
    deployments.append(record)
    return {"message": "Deployment recorded", "total_records": len(deployments)}


@app.get("/deployments")
def list_deployments(service_name: str = None, environment: str = None):
    results = deployments
    if service_name:
        results = [d for d in results if d.get("service_name") == service_name]
    if environment:
        results = [d for d in results if d.get("environment") == environment]
    return {"deployments": results, "count": len(results)}


@app.get("/metrics/{service_name}")
def get_metrics(service_name: str):
    service_deploys = [d for d in deployments if d.get("service_name") == service_name]
    if not service_deploys:
        return {"error": f"No deployments found for {service_name}"}

    successful = [d for d in service_deploys if d.get("status") == "success"]
    success_rate = len(successful) / len(service_deploys) * 100 if service_deploys else 0

    return {
        "service_name": service_name,
        "total_deploys": len(service_deploys),
        "success_rate": round(success_rate, 1),
        "environments": list(set(d.get("environment", "unknown") for d in service_deploys))
    }