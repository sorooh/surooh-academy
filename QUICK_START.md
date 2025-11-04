# 🚀 Surooh Academy - Quick Start Guide

Get Surooh Academy up and running in minutes!

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose (recommended)
- Google Cloud Project with Vertex AI API enabled
- OpenAI API key (for semantic search)

## ⚡ 5-Minute Setup

### Option 1: Docker (Recommended)

1. **Clone & Configure**
   ```bash
   git clone https://github.com/sorooh/surooh-academy.git
   cd surooh-academy
   cp .env.example .env
   ```

2. **Edit Environment**
   ```bash
   # Edit .env file with your credentials:
   GCP_PROJECT=your-gcp-project-id
   GCP_LOCATION=europe-west4
   OPENAI_API_KEY=your-openai-api-key
   ```

3. **Add Service Account**
   ```bash
   # Place your Google Cloud service account JSON file as:
   # service-account.json
   ```

4. **Launch**
   ```bash
   docker-compose up -d
   ```

5. **Verify**
   ```bash
   curl http://localhost:5000/health
   ```

### Option 2: Local Python

1. **Setup Environment**
   ```bash
   git clone https://github.com/sorooh/surooh-academy.git
   cd surooh-academy
   pip install -r requirements.txt
   cp .env.example .env
   ```

2. **Configure & Run**
   ```bash
   # Edit .env with your credentials
   uvicorn main:app --host 0.0.0.0 --port 5000 --reload
   ```

## 🎯 First API Call

Test the system with a sample project analysis:

```bash
curl -X POST http://localhost:5000/academy/intake \
  -H "Content-Type: application/json" \
  -d '{
    "description": "نريد بناء متجر إلكتروني في هولندا يحتاج دعم عملاء ذكي ومحرك تسعير ديناميكي",
    "project_name": "Dutch E-Commerce Store",
    "tenant": "ecommerce-nl"
  }'
```

Expected response:
```json
{
  "status": "success",
  "bots_plan": {
    "bots": [
      {
        "name": "customer_support_bot",
        "type": "customer_support",
        "purpose": "Handle customer inquiries and order tracking"
      }
    ]
  },
  "processing_time_ms": 3247
}
```

## 🌐 Access Points

- **API Documentation**: http://localhost:5000/docs
- **Health Check**: http://localhost:5000/health
- **System Info**: http://localhost:5000/api
- **Monitoring** (if enabled): http://localhost:3000 (Grafana)

## 🎓 Core Features Demo

### 1. Bot Training
```bash
curl -X POST http://localhost:5000/academy/train \
  -H "Content-Type: application/json" \
  -d '{
    "bot_config": {
      "name": "support_bot_v1",
      "type": "customer_support",
      "capabilities": ["order_tracking", "faq", "escalation"],
      "language": "arabic"
    }
  }'
```

### 2. Semantic Search
```bash
curl -X POST http://localhost:5000/core/semantic_search \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "query=customer support automation&method=hybrid&top_k=5"
```

### 3. Multi-Agent Orchestration
```bash
curl -X POST http://localhost:5000/academy/orchestrate \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "task=Process 100 orders to Germany&context={\"product\":\"BORVAT\",\"priority\":\"high\"}"
```

## 📊 Monitoring

Access system metrics and health:

```bash
# System health
curl http://localhost:5000/health

# Current metrics
curl http://localhost:5000/proactive/metrics

# View alerts
curl http://localhost:5000/proactive/alerts
```

## 🐛 Troubleshooting

### Common Issues

1. **Service Account Error**
   ```
   Error: Could not load credentials
   ```
   **Solution**: Ensure `service-account.json` is in the root directory with proper permissions.

2. **Port Already in Use**
   ```
   Error: bind: address already in use
   ```
   **Solution**: Change port in `docker-compose.yml` or stop conflicting services.

3. **Dependencies Missing**
   ```
   ImportError: No module named 'xyz'
   ```
   **Solution**: Run `pip install -r requirements.txt`

### Health Check Commands

```bash
# Check all services
docker-compose ps

# View logs
docker-compose logs academy

# Restart services
docker-compose restart
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GCP_PROJECT` | Google Cloud Project ID | Required |
| `GCP_LOCATION` | GCP Region | `europe-west4` |
| `OPENAI_API_KEY` | OpenAI API Key | Required |
| `API_PORT` | Server Port | `5000` |
| `LOG_LEVEL` | Logging Level | `INFO` |

### Feature Toggles

```env
# Enable/disable features
CONSTITUTIONAL_ENABLED=true
MONITORING_ENABLED=true
SEMANTIC_SEARCH_ENABLED=true
```

## 📚 Next Steps

1. **Explore API**: Visit http://localhost:5000/docs for interactive documentation
2. **Upload Knowledge**: Use `/academy/upload` to add your company data
3. **Train Bots**: Create specialized bots for your use case
4. **Monitor System**: Set up alerts and monitoring
5. **Scale**: Deploy to production with Docker Swarm or Kubernetes

## 🤝 Getting Help

- 📖 [Full Documentation](./README.md)
- 🤝 [Contributing Guide](./CONTRIBUTING.md)
- 🐛 [Report Issues](https://github.com/sorooh/surooh-academy/issues)
- 💬 [Discord Community](https://discord.gg/surooh)

---

**Ready to build intelligent bots? Let's go! 🚀**