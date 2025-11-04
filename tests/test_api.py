"""
Tests for Surooh Academy API endpoints
"""
import pytest
from httpx import AsyncClient

class TestHealthEndpoints:
    """Test health check endpoints."""
    
    async def test_health_check(self, client: AsyncClient):
        """Test the health check endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data

    async def test_ready_check(self, client: AsyncClient):
        """Test the readiness check endpoint."""
        response = await client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert "services" in data

class TestProjectIntakeEndpoint:
    """Test project intake endpoint."""
    
    async def test_project_intake_success(self, client: AsyncClient, sample_project_data):
        """Test successful project intake."""
        response = await client.post("/academy/intake", json=sample_project_data)
        assert response.status_code == 200
        data = response.json()
        
        assert "intake_id" in data
        assert data["status"] == "received"
        assert data["project_name"] == sample_project_data["project_name"]
        assert "estimated_timeline" in data
        assert "recommended_approach" in data

    async def test_project_intake_missing_required_fields(self, client: AsyncClient):
        """Test project intake with missing required fields."""
        incomplete_data = {
            "project_name": "Test Project"
            # Missing other required fields
        }
        response = await client.post("/academy/intake", json=incomplete_data)
        assert response.status_code == 422

    async def test_project_intake_empty_request(self, client: AsyncClient):
        """Test project intake with empty request."""
        response = await client.post("/academy/intake", json={})
        assert response.status_code == 422

class TestBotTrainingEndpoints:
    """Test bot training endpoints."""
    
    async def test_train_content_creator_bot(self, client: AsyncClient, bot_training_data):
        """Test content creator bot training."""
        response = await client.post("/bots/train/content-creator", json=bot_training_data)
        assert response.status_code == 200
        data = response.json()
        
        assert "training_id" in data
        assert data["bot_type"] == "content-creator"
        assert data["status"] in ["initiated", "training"]

    async def test_train_customer_service_bot(self, client: AsyncClient, bot_training_data):
        """Test customer service bot training."""
        bot_training_data["bot_type"] = "customer_service"
        response = await client.post("/bots/train/customer-service", json=bot_training_data)
        assert response.status_code == 200
        data = response.json()
        
        assert "training_id" in data
        assert data["bot_type"] == "customer-service"

    async def test_train_educational_bot(self, client: AsyncClient, bot_training_data):
        """Test educational bot training."""
        response = await client.post("/bots/train/educational", json=bot_training_data)
        assert response.status_code == 200
        data = response.json()
        
        assert "training_id" in data
        assert data["bot_type"] == "educational"

class TestDocumentationEndpoints:
    """Test API documentation endpoints."""
    
    async def test_openapi_docs(self, client: AsyncClient):
        """Test OpenAPI documentation endpoint."""
        response = await client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    async def test_openapi_json(self, client: AsyncClient):
        """Test OpenAPI JSON schema."""
        response = await client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
        assert data["info"]["title"] == "Surooh Academy - AI Bot Factory"

class TestErrorHandling:
    """Test error handling scenarios."""
    
    async def test_404_endpoint(self, client: AsyncClient):
        """Test non-existent endpoint."""
        response = await client.get("/non-existent-endpoint")
        assert response.status_code == 404

    async def test_method_not_allowed(self, client: AsyncClient):
        """Test method not allowed."""
        response = await client.delete("/health")
        assert response.status_code == 405