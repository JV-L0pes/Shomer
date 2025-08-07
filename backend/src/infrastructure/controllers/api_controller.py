import asyncio
import time
import os
from datetime import timedelta
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse
from jose import jwt

from ...application.dto.models import RegisterModel, LoginModel, Token, LogModel, LogOutModel
from ...application.use_cases import RegisterUserUseCase, LoginUserUseCase, CreateLogUseCase, GetLogsUseCase
from ...infrastructure.repositories import MongoUserRepository, MongoLogRepository
from ...infrastructure.services import JWTAuthService, get_current_user, check_login_rate_limit
from ...shared.config import brasilia_now, Config
from ...shared.utils import (
    export_log_csv, get_logs_list, get_detector_stats, 
    get_performance_stats, get_health_info
)
from detection import VisualDetector

# Router para organizar as rotas
router = APIRouter()

# Token de convite único
INVITATION_TOKEN = os.getenv("INVITATION_TOKEN")

# Variáveis globais que serão injetadas
detector = None
camera_config = None

# Instâncias dos serviços e repositórios
auth_service = JWTAuthService()
user_repository = MongoUserRepository()
log_repository = MongoLogRepository()

# Casos de uso
register_use_case = RegisterUserUseCase(user_repository, auth_service)
login_use_case = LoginUserUseCase(user_repository, auth_service)
create_log_use_case = CreateLogUseCase(log_repository)
get_logs_use_case = GetLogsUseCase(log_repository)


def set_globals(detector_instance, camera_config_instance):
    """Define as variáveis globais para as rotas."""
    global detector, camera_config
    detector = detector_instance
    camera_config = camera_config_instance


@router.get("/")
async def root():
    """API info ultra-otimizada."""
    base_info = {
        "message": "Shomer API - Ultra High Performance Mode",
        "version": "3.0.0",
        "status": "active" if detector else "starting",
        "camera": {
            "current_source": (
                "webcam" if camera_config["current_source"] == 0 else "ip_camera"
            ),
            "stream_enabled": camera_config["stream_enabled"],
            "available_sources": list(camera_config["available_sources"].keys()),
        },
    }

    if detector:
        stats = detector.get_performance_stats()
        from ...infrastructure.services import get_cache_stats
        cache_stats = get_cache_stats()
        cache_ratio = cache_stats["cache_efficiency"]
        base_info["performance"] = {
            "fps": stats.get("capture_fps", 0),
            "models_ready": stats.get("models_ready", False),
            "cache_efficiency": cache_ratio,
        }

    return base_info


@router.get("/video_feed")
async def video_feed():
    """Stream MJPEG ultra-otimizado com headers otimizados."""
    from ...infrastructure.services import get_video_feed_response
    return get_video_feed_response(detector, camera_config)


@router.get("/demo-stream.jpg")
async def demo_stream():
    """Imagem única ultra-otimizada."""
    from ...infrastructure.services import get_demo_stream_response
    return get_demo_stream_response(detector, camera_config)


@router.get("/stats")
async def get_stats():
    """Stats ultra-rápidas com cache info e tracking."""
    return get_detector_stats(detector, camera_config)


@router.get("/performance")
async def get_performance():
    """Métricas de performance detalhadas com cache."""
    return get_performance_stats(detector, camera_config)


@router.post("/camera/switch")
async def switch_camera(source: str, current_user: str = Depends(get_current_user)):
    """Troca entre webcam e IP camera."""
    if source not in camera_config["available_sources"]:
        raise HTTPException(
            status_code=400,
            detail=f"Fonte inválida. Use: {list(camera_config['available_sources'].keys())}",
        )

    try:
        new_source = camera_config["available_sources"][source]

        # Parar detector atual
        global detector
        if detector:
            detector.stop()

        # Inicializar novo detector
        detector = VisualDetector(src=new_source)
        camera_config["current_source"] = new_source

        # Aguardar inicialização
        await asyncio.sleep(1.0)

        return {
            "success": True,
            "message": f"Câmera trocada para {source}",
            "current_source": source,
            "stream_enabled": camera_config["stream_enabled"],
            "user": current_user,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao trocar câmera: {str(e)}")


@router.post("/stream/control")
async def control_stream(action: str, current_user: str = Depends(get_current_user)):
    """Controla o stream (start/stop)."""
    if action not in ["start", "stop"]:
        raise HTTPException(status_code=400, detail="Ação inválida. Use: start ou stop")

    try:
        if action == "start":
            camera_config["stream_enabled"] = True
            message = "Stream iniciado"
        else:
            camera_config["stream_enabled"] = False
            message = "Stream parado"

        return {
            "success": True,
            "message": message,
            "stream_enabled": camera_config["stream_enabled"],
            "current_source": (
                "webcam" if camera_config["current_source"] == 0 else "ip_camera"
            ),
            "user": current_user,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao controlar stream: {str(e)}"
        )


@router.get("/camera/status")
async def get_camera_status():
    """Retorna status atual da câmera."""
    return {
        "current_source": (
            "webcam" if camera_config["current_source"] == 0 else "ip_camera"
        ),
        "stream_enabled": camera_config["stream_enabled"],
        "available_sources": list(camera_config["available_sources"].keys()),
        "detector_ready": detector is not None,
        "ip_url": camera_config["ip_url"],
    }


@router.get("/config")
async def get_config():
    """Retorna configurações do sistema."""
    return {
        "camera": Config.get_camera_config(),
        "detection": Config.get_detection_config(),
        "server": Config.get_server_config(),
    }


@router.get("/export_log.csv")
async def export_log(current_user: str = Depends(get_current_user)):
    """Export simplificado com total de pessoas capturadas."""
    csv_data, filename = export_log_csv(detector, current_user)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/health")
async def health():
    """Health check ultra-rápido."""
    return get_health_info(detector, camera_config)


# Endpoints de autenticação e logs
@router.post("/register")
async def register(data: RegisterModel):
    """Registra um novo usuário."""
    try:
        result = await register_use_case.execute(data, INVITATION_TOKEN)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login", response_model=Token)
async def login(data: LoginModel, request: Request):
    """Autentica um usuário com username ou email."""
    # Rate limiting específico para login
    client_ip = request.client.host
    current_time = time.time()

    # Verificar limite de tentativas de login
    check_login_rate_limit(client_ip, current_time)

    try:
        result = await login_use_case.execute(data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/logs")
async def create_log(
    data: LogModel,
    current_user: str = Depends(get_current_user),
):
    """Cria um novo log de detecção."""
    try:
        result = await create_log_use_case.execute(data, current_user)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me")
async def get_current_user_info(current_user: str = Depends(get_current_user)):
    """Retorna informações do usuário atual."""
    user = await user_repository.find_by_username(current_user)
    if user:
        return {"username": current_user, "created_at": user.created_at}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")


@router.get("/logs", response_model=List[LogOutModel])
async def list_logs(limit: int = 100):
    """
    Retorna os últimos `limit` logs, em ordem decrescente de timestamp.
    """
    try:
        results = await get_logs_use_case.execute(limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
