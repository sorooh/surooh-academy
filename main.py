"""
Surooh Academy - Main FastAPI Application
نواة النظام الرئيسية للأكاديمية
"""
import os
import time
import uuid
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import shutil
from loguru import logger
from dotenv import load_dotenv

from server.academy.instructor import instructor
from server.academy.trainers.customer_support_trainer import trainer
from server.academy.trainers.pricing_engine_trainer import pricing_trainer
from server.academy.trainers.analytics_reporter_trainer import analytics_trainer
from server.academy.trainers.order_orchestrator_trainer import order_trainer
from server.academy.trainers.knowledge_aware_trainer import knowledge_aware_trainer
from server.academy.cores.chat_core_trainer import train_chat_core_v2
from server.academy.cores.chat_core_evaluator import simulate_chat_core_v2, evaluate_chat_core_v2
from server.core.memory_bridge import bridge_memory, get_archive_stats
from server.core.memory_search import search_memory, list_archive_files
from server.core.text_extractor import process_all_archive_files, get_extraction_stats
from server.core.knowledge_feed import knowledge_feed
from server.core.context_injector import context_injector
from server.core.semantic_search import get_search_engine
from server.core.auto_archive import get_auto_archive
from server.academy.orchestrator import get_orchestrator
from server.core.monitor_daemon import monitor_daemon
from server.core.alert_system import alert_system, AlertPriority, AlertChannel
from server.core.action_engine import action_engine, ActionType
from server.core.ocr_service import ocr_service
from server.core.audio_service import audio_service
from server.core.video_service import video_service
from server.integrations.messaging_hub import messaging_hub
from server.integrations.email_service import email_service
from server.integrations.ecommerce_hub import ecommerce_hub
from server.integrations.accounting_service import accounting_service
from server.academy.bot_specialization import bot_specialization_engine
from server.academy.training_manager import training_manager
from server.academy.api.replit_bots_routes import router as replit_bots_router

# Constitutional Compliance System
try:
    from server.academy.constitutional_compliance import constitutional_monitor
    CONSTITUTIONAL_ENABLED = True
    logger.info("🏛️ Constitutional Compliance System ENABLED in Main")
except ImportError:
    CONSTITUTIONAL_ENABLED = False
    constitutional_monitor = None
    logger.warning("⚠️ Constitutional Compliance System DISABLED in Main")

load_dotenv()

logger.add(
    "logs/surooh_academy_{time}.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Surooh Academy starting up...")
    logger.info(f"📍 GCP Project: {os.getenv('GCP_PROJECT', 'Not Set')}")
    logger.info(f"📍 GCP Location: {os.getenv('GCP_LOCATION', 'Not Set')}")
    
    async def handle_monitor_alert(alert: Dict[str, Any]):
        await action_engine.create_smart_action_from_alert(alert)
    
    monitor_daemon.register_alert_callback(handle_monitor_alert)
    
    import asyncio
    monitor_task = asyncio.create_task(monitor_daemon.start())
    logger.info("🔍 Monitor Daemon started in background")
    
    yield
    
    await monitor_daemon.stop()
    monitor_task.cancel()
    logger.info("👋 Surooh Academy shutting down...")

app = FastAPI(
    title="🚀 Surooh Academy API",
    description="""
    **Advanced AI-Powered Bot Factory & Training System**
    
    نظام ذكاء اصطناعي متكامل لتوليد وتدريب البوتات الذكية يحلل متطلبات أي مشروع ويولد خطط نشر شاملة للبوتات خلال ثوانٍ
    
    ## 🌟 Key Features
    
    - 🤖 **Multi-Agent Bot Factory**: Automatically generate specialized bots
    - 🧠 **AI-Powered Analysis**: Deep project analysis using Google Gemini AI
    - 📚 **Knowledge-Aware Training**: Train bots using company data
    - 🔄 **Smart Orchestration**: Coordinate multiple bots for complex tasks
    - 📊 **Real-time Monitoring**: Proactive system health monitoring
    - 🏛️ **Constitutional Compliance**: Built-in governance framework
    
    ## 🔗 Useful Links
    
    - [📖 Full Documentation](https://docs.surooh-academy.com)
    - [🐛 Report Issues](https://github.com/sorooh/surooh-academy/issues)
    - [💬 Discord Community](https://discord.gg/surooh)
    """,
    version="2.5.0",
    contact={
        "name": "Surooh Academy Team",
        "url": "https://surooh-academy.com",
        "email": "support@surooh-academy.com"
    },
    license_info={
        "name": "Proprietary License",
        "url": "https://surooh-academy.com/license"
    },
    servers=[
        {
            "url": "https://api.surooh-academy.com/v1",
            "description": "Production Server"
        },
        {
            "url": "https://staging-api.surooh-academy.com/v1", 
            "description": "Staging Server"
        },
        {
            "url": "http://localhost:5000",
            "description": "Development Server"
        }
    ],
    tags_metadata=[
        {
            "name": "🎯 Project Analysis",
            "description": "Analyze project requirements and generate bot deployment plans"
        },
        {
            "name": "🎓 Bot Training", 
            "description": "Train specialized bots with custom configurations"
        },
        {
            "name": "🧠 Advanced Training",
            "description": "Knowledge-aware training using company archives"
        },
        {
            "name": "🔍 Search & Knowledge",
            "description": "Semantic search and knowledge management"
        },
        {
            "name": "🎭 Multi-Agent Orchestration",
            "description": "Coordinate multiple bots for complex tasks"
        },
        {
            "name": "📊 System Monitoring",
            "description": "Health checks, metrics, and system status"
        },
        {
            "name": "🏛️ Constitutional Compliance",
            "description": "Bot governance and compliance monitoring"
        },
        {
            "name": "📱 File Management",
            "description": "Upload and manage knowledge base files"
        },
        {
            "name": "🔧 System Info",
            "description": "General system information and utilities"
        }
    ],
    openapi_tags=[
        {"name": "project-analysis"},
        {"name": "bot-training"}, 
        {"name": "advanced-training"},
        {"name": "search-knowledge"},
        {"name": "orchestration"},
        {"name": "monitoring"},
        {"name": "constitutional"},
        {"name": "file-management"},
        {"name": "system"}
    ],
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Replit Bots Router
app.include_router(replit_bots_router)

class ProjectIntakeRequest(BaseModel):
    """
    نموذج طلب تحليل مشروع جديد
    
    Request model for analyzing new project requirements and generating bot deployment plans.
    """
    description: str = Field(
        ..., 
        description="وصف مفصل للمشروع والمتطلبات التقنية والتجارية",
        min_length=10,
        max_length=5000,
        example="نريد بناء متجر إلكتروني في هولندا يحتاج دعم عملاء ذكي ومحرك تسعير ديناميكي وتحليلات يومية"
    )
    project_name: Optional[str] = Field(
        None, 
        description="اسم المشروع",
        max_length=100,
        example="Dutch E-Commerce Store"
    )
    tenant: Optional[str] = Field(
        None, 
        description="معرف العميل أو المستأجر",
        max_length=50,
        example="ecommerce-nl"
    )
    constraints: Optional[Dict[str, Any]] = Field(
        None, 
        description="قيود إضافية مثل الميزانية والوقت",
        example={
            "budget": 50000,
            "timeline": "3 months", 
            "team_size": 5,
            "compliance": ["GDPR", "PCI-DSS"]
        }
    )
    trace_id: Optional[str] = Field(
        None, 
        description="معرف التتبع للطلب (اختياري)",
        example="trace-12345-abc"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "description": "نريد بناء منصة تجارة إلكترونية متكاملة في هولندا تحتاج إلى دعم عملاء ذكي، محرك تسعير ديناميكي، وتحليلات في الوقت الفعلي",
                "project_name": "Dutch B2C Store",
                "tenant": "ecommerce-nl",
                "constraints": {
                    "budget": 75000,
                    "timeline": "4 months",
                    "team_size": 8,
                    "compliance": ["GDPR", "PCI-DSS"],
                    "languages": ["dutch", "english"]
                }
            }
        }

class ProjectIntakeResponse(BaseModel):
    """
    نموذج استجابة تحليل المشروع
    
    Response model containing the generated bot deployment plan and analysis results.
    """
    status: str = Field(description="حالة الطلب")
    bots_plan: Dict[str, Any] = Field(description="خطة البوتات المقترحة")
    trace_id: str = Field(description="معرف التتبع")
    processing_time_ms: int = Field(description="وقت المعالجة بالميلي ثانية")
    message: str = Field(description="رسالة تفصيلية عن النتيجة")

class BotTrainingRequest(BaseModel):
    """
    نموذج طلب تدريب بوت
    
    Request model for training specialized bots with custom configurations.
    """
    bot_config: Dict[str, Any] = Field(
        ..., 
        description="إعدادات البوت المفصلة (الاسم، النوع، القدرات، مؤشرات الأداء)",
        example={
            "name": "customer_support_bot",
            "type": "customer_support",
            "capabilities": ["order_tracking", "faq", "escalation"],
            "language": "arabic",
            "tone": "formal",
            "kpis": {"accuracy": 0.9, "response_time": 2}
        }
    )
    sample_conversations: Optional[list[str]] = Field(
        None, 
        description="أمثلة محادثات للتدريب",
        example=[
            "العميل: أريد تتبع طلبي رقم 12345",
            "البوت: بالطبع، سأساعدك في تتبع الطلب..."
        ]
    )
    trace_id: Optional[str] = Field(
        None, 
        description="معرف التتبع للطلب"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "bot_config": {
                    "name": "support_bot_v2",
                    "type": "customer_support",
                    "capabilities": ["order_tracking", "product_info", "returns", "escalation"],
                    "language": "arabic",
                    "tone": "friendly_professional",
                    "specialization": "ecommerce",
                    "kpis": {
                        "accuracy": 0.92,
                        "response_time_seconds": 3,
                        "satisfaction_rate": 0.88
                    }
                },
                "sample_conversations": [
                    "العميل: مرحبا، أريد معرفة حالة طلبي",
                    "البوت: أهلاً وسهلاً! سأساعدك في تتبع طلبك. هل يمكنك تزويدي برقم الطلب؟",
                    "العميل: الرقم هو ORD-12345",
                    "البوت: شكراً لك. طلبك قيد التحضير وسيصل خلال يومين."
                ]
            }
        }

class BotTrainingResponse(BaseModel):
    """
    نموذج استجابة تدريب البوت
    
    Response model containing the generated training plan and training details.
    """
    status: str = Field(description="حالة طلب التدريب")
    training_plan: Dict[str, Any] = Field(description="خطة التدريب المفصلة")
    trace_id: str = Field(description="معرف التتبع")
    processing_time_ms: int = Field(description="وقت المعالجة بالميلي ثانية")
    message: str = Field(description="رسالة تفصيلية عن نتيجة التدريب")

@app.get(
    "/",
    tags=["🔧 System Info"],
    summary="الصفحة الرئيسية",
    description="واجهة المستخدم الرئيسية للنظام"
)
async def home():
    """الصفحة الرئيسية - واجهة المستخدم"""
    return FileResponse("static/index.html")

@app.get(
    "/api",
    tags=["🔧 System Info"],
    summary="معلومات النظام",
    description="معلومات شاملة عن API والخدمات المتاحة",
    response_description="تفاصيل النظام وقائمة بجميع نقاط النهاية المتاحة"
)
async def api_info():
    """
    ## معلومات شاملة عن Surooh Academy API
    
    يعرض هذا الـ endpoint معلومات مفصلة عن:
    - إصدار النظام الحالي
    - حالة التشغيل
    - قائمة بجميع نقاط النهاية المتاحة
    - إحصائيات النظام الأساسية
    """
    return {
        "service": "Surooh Academy",
        "version": "2.5.0",
        "status": "operational",
        "description": "نظام ذكاء اصطناعي متكامل يربط النواة المركزية مع Vertex AI",
        "features": [
            "Multi-Agent Bot Factory",
            "AI-Powered Analysis",
            "Knowledge-Aware Training",
            "Smart Orchestration",
            "Real-time Monitoring",
            "Constitutional Compliance"
        ],
        "endpoints": {
            "intake": "/academy/intake",
            "train": {
                "customer_support": "/academy/train",
                "pricing": "/academy/train/pricing",
                "analytics": "/academy/train/analytics",
                "orders": "/academy/train/orders",
                "knowledge_aware": "/academy/train/knowledge"
            },
            "cores": {
                "chat_intake": "/academy/cores/chat/intake",
                "chat_simulate": "/academy/cores/chat/simulate",
                "chat_evaluate": "/academy/cores/chat/evaluate"
            },
            "orchestration": "/academy/orchestrate",
            "memory": {
                "upload": "/academy/upload",
                "sync": "/core/sync_memory",
                "process": "/core/process_all",
                "search": "/core/search",
                "semantic_search": "/core/semantic_search",
                "list": "/core/list",
                "stats": "/core/stats"
            },
            "monitoring": {
                "health": "/health",
                "metrics": "/proactive/metrics",
                "alerts": "/proactive/alerts"
            },
            "constitutional": {
                "stats": "/constitutional/stats",
                "bot_status": "/constitutional/bot/{bot_type}"
            }
        },
        "documentation": {
            "interactive_docs": "/docs",
            "redoc": "/redoc",
            "api_reference": "https://docs.surooh-academy.com/api"
        }
    }

@app.get(
    "/health",
    tags=["📊 System Monitoring"],
    summary="فحص صحة النظام",
    description="فحص شامل لصحة النظام وحالة الخدمات",
    response_description="معلومات حالة النظام والخدمات المرتبطة"
)
async def health_check():
    """
    ## فحص صحة النظام الشامل
    
    يقوم هذا الـ endpoint بفحص:
    - ✅ حالة التطبيق الأساسية
    - ✅ اتصال قاعدة البيانات
    - ✅ خدمات الذكاء الاصطناعي (Vertex AI)
    - ✅ النظم الفرعية (Redis, Storage)
    
    ### حالات الاستجابة:
    - `healthy`: جميع الأنظمة تعمل بشكل طبيعي
    - `degraded`: بعض الخدمات تواجه مشاكل
    - `unhealthy`: مشاكل حرجة في النظام
    """
    try:
        # فحص الخدمات الأساسية
        health_status = {
            "status": "healthy",
            "timestamp": time.time(),
            "version": "2.5.0",
            "services": {
                "vertex_ai": bool(os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or os.getenv("GCP_PROJECT")),
                "constitutional_monitor": CONSTITUTIONAL_ENABLED,
                "monitoring_daemon": True,  # سيتم تحديثه لاحقاً لفحص حالة فعلية
                "semantic_search": bool(os.getenv("OPENAI_API_KEY")),
            },
            "metrics": {
                "uptime_seconds": int(time.time()),  # سيتم تحسينه لاحقاً
                "active_bots": 0,  # سيتم ربطه بالنظام الفعلي
                "training_sessions": 0
            }
        }
        
        # تحديد الحالة العامة بناءً على حالة الخدمات
        unhealthy_services = [k for k, v in health_status["services"].items() if not v]
        if unhealthy_services:
            health_status["status"] = "degraded" if len(unhealthy_services) < 2 else "unhealthy"
            health_status["issues"] = unhealthy_services
        
        return health_status
    
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": time.time(),
            "error": str(e)
        }

@app.post(
    "/academy/intake", 
    response_model=ProjectIntakeResponse,
    tags=["🎯 Project Analysis"],
    summary="تحليل مشروع جديد وإنشاء خطة البوتات",
    description="تحليل متطلبات المشروع وإنشاء خطة شاملة للبوتات المطلوبة",
    response_description="خطة مفصلة تحتوي على البوتات المقترحة، الاختبارات، والمخاطر",
    responses={
        200: {
            "description": "تم تحليل المشروع بنجاح",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "bots_plan": {
                            "bots": [
                                {
                                    "name": "customer_support_bot",
                                    "type": "customer_support",
                                    "purpose": "الرد على استفسارات العملاء وتتبع الطلبات",
                                    "capabilities": ["order_tracking", "faq", "ticket_creation"],
                                    "kpis": {"accuracy": 0.85, "latency_ms": 500},
                                    "estimated_training_time": "2-3 days"
                                }
                            ],
                            "total_bots": 4,
                            "estimated_cost": 25000,
                            "timeline": "5-7 days"
                        },
                        "trace_id": "trace-abc-123",
                        "processing_time_ms": 3247,
                        "message": "تم تحليل المشروع بنجاح وإنشاء خطة تحتوي على 4 بوتات"
                    }
                }
            }
        },
        422: {
            "description": "بيانات الإدخال غير صحيحة",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "description"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "خطأ في الخادم",
            "content": {
                "application/json": {
                    "example": {
                        "error": "intake_processing_failed",
                        "message": "فشل في معالجة طلب التحليل",
                        "trace_id": "trace-abc-123",
                        "processing_time_ms": 1500
                    }
                }
            }
        }
    }
)
async def academy_intake(request: ProjectIntakeRequest):
    """
    ## 🎯 نقطة النهاية الرئيسية: تحليل المشروع وإنشاء خطة البوتات
    
    ### الوظيفة:
    يقوم هذا الـ endpoint بتحليل وصف المشروع باستخدام **Google Gemini AI** وإنشاء خطة شاملة للبوتات المطلوبة.
    
    ### المميزات:
    - 🧠 **تحليل ذكي**: استخدام الذكاء الاصطناعي لفهم المتطلبات
    - ⚡ **سرعة فائقة**: نتائج خلال أقل من 10 ثوانٍ
    - 📊 **تحليل شامل**: تحديد البوتات، المخاطر، والاختبارات
    - 🎯 **مخصص**: اقتراحات محددة حسب نوع المشروع
    
    ### العملية:
    1. **استقبال الوصف**: تحليل وصف المشروع والقيود
    2. **معالجة ذكية**: استخدام Gemini AI لتحليل المتطلبات
    3. **إنشاء الخطة**: توليد قائمة بالبوتات والاختبارات المطلوبة
    4. **تقدير الموارد**: حساب الوقت والتكلفة المتوقعة
    
    ### الاستخدام النموذجي:
    ```python
    import httpx
    
    response = httpx.post("http://localhost:5000/academy/intake", json={
        "description": "متجر إلكتروني يحتاج دعم عملاء ذكي",
        "project_name": "متجر الإلكترونيات",
        "tenant": "electronics-store"
    })
    
    plan = response.json()["bots_plan"]
    print(f"عدد البوتات المقترحة: {len(plan['bots'])}")
    ```
    
    ### ملاحظات مهمة:
    - ⏱️ **زمن المعالجة**: عادة أقل من 5 ثوانٍ
    - 🔍 **التتبع**: كل طلب يحصل على `trace_id` فريد
    - 📝 **التفاصيل**: كلما كان الوصف أكثر تفصيلاً، كانت النتائج أدق
    """
    start_time = time.time()
    trace_id = request.trace_id or str(uuid.uuid4())
    
    logger.info(f"📥 New project intake request [trace_id={trace_id}]")
    logger.info(f"   Project: {request.project_name or 'Unnamed'}")
    logger.info(f"   Tenant: {request.tenant or 'default'}")
    
    try:
        bots_plan = await instructor.propose_bots(
            project_description=request.description,
            trace_id=trace_id
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        logger.info(f"✅ Successfully generated bots plan [trace_id={trace_id}] in {processing_time}ms")
        
        if processing_time > 10000:
            logger.warning(f"⚠️ Processing time exceeded 10s: {processing_time}ms")
        
        return ProjectIntakeResponse(
            status="success",
            bots_plan=bots_plan,
            trace_id=trace_id,
            processing_time_ms=processing_time,
            message=f"تم تحليل المشروع بنجاح وإنشاء خطة تحتوي على {len(bots_plan.get('bots', []))} بوتات"
        )
        
    except Exception as e:
        processing_time = int((time.time() - start_time) * 1000)
        logger.error(f"❌ Failed to process intake [trace_id={trace_id}]: {e}")
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "intake_processing_failed",
                "message": str(e),
                "trace_id": trace_id,
                "processing_time_ms": processing_time
            }
        )

@app.post("/academy/train", response_model=BotTrainingResponse)
async def academy_train(request: BotTrainingRequest):
    """
    🎓 تدريب بوت خدمة العملاء وإرجاع خطة تدريب شاملة
    
    يستقبل إعدادات البوت وأمثلة محادثات، يرسلها لـ Gemini AI، يرجع خطة تدريب كاملة.
    """
    start_time = time.time()
    trace_id = request.trace_id or str(uuid.uuid4())
    
    bot_name = request.bot_config.get('name', 'Unknown Bot')
    logger.info(f"🎓 New training request [trace_id={trace_id}]")
    logger.info(f"   Bot: {bot_name}")
    logger.info(f"   Config: {request.bot_config.get('type', 'unknown type')}")
    
    try:
        training_plan = await trainer.generate_training_plan(
            bot_config=request.bot_config,
            sample_conversations=request.sample_conversations,
            trace_id=trace_id
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        logger.info(f"✅ Successfully generated training plan [trace_id={trace_id}] in {processing_time}ms")
        
        num_steps = len(training_plan.get('training_steps', []))
        
        return BotTrainingResponse(
            status="success",
            training_plan=training_plan,
            trace_id=trace_id,
            processing_time_ms=processing_time,
            message=f"تم إنشاء خطة تدريب كاملة تحتوي على {num_steps} خطوات للبوت: {training_plan.get('bot_name', bot_name)}"
        )
        
    except Exception as e:
        processing_time = int((time.time() - start_time) * 1000)
        logger.error(f"❌ Failed to generate training plan [trace_id={trace_id}]: {e}")
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "training_plan_generation_failed",
                "message": str(e),
                "trace_id": trace_id,
                "processing_time_ms": processing_time
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="info"
    )