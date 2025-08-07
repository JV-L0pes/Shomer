# backend/main.py - Versão Ultra Otimizada para Alta Performance

from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv(".env")  # carrega do arquivo .env
import cv2
import csv
import io
import asyncio
import numpy as np
from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import FastAPI, Response, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, EmailStr, validator
from passlib.context import CryptContext
from jose import JWTError, jwt
import time
from collections import defaultdict

from detection import OptimizedDetector
from config import Config, brasilia_now
from db import users_collection, logs_collection

# carrega variáveis de .env.app

# constantes para JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))

# token de convite único (ou você pode ler vários e separar)
INVITATION_TOKEN = os.getenv("INVITATION_TOKEN")

# OAuth2 scheme para autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Configuração de logging otimizada
import logging

logging.basicConfig(level=logging.WARNING)  # Menos logs = mais performance
logger = logging.getLogger(__name__)

# Inicialização da aplicação
app = FastAPI(
    title="Shomer API - Ultra High Performance",
    description="Sistema de detecção ultra-otimizado para máxima velocidade",
    version="3.0.0",
)

# Configuração de autenticação
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rate limiting simples
request_counts = defaultdict(list)
RATE_LIMIT_WINDOW = 60  # 60 segundos
RATE_LIMIT_MAX_REQUESTS = 100  # 100 requests por minuto
LOGIN_RATE_LIMIT_MAX = 5  # 5 tentativas de login por minuto

# CORS otimizado - Apenas origens específicas
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Middleware personalizado para rate limiting e headers de segurança
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    # Rate limiting
    client_ip = request.client.host
    current_time = time.time()

    # Limpar requests antigos
    request_counts[client_ip] = [
        req_time
        for req_time in request_counts[client_ip]
        if current_time - req_time < RATE_LIMIT_WINDOW
    ]

    # Verificar limite
    if len(request_counts[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Adicionar request atual
    request_counts[client_ip].append(current_time)

    response = await call_next(request)

    # Headers de segurança
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    )

    # Adicionar headers CORS se não estiverem presentes
    if "Access-Control-Allow-Origin" not in response.headers:
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    if "Access-Control-Allow-Methods" not in response.headers:
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS"
        )
    if "Access-Control-Allow-Headers" not in response.headers:
        response.headers["Access-Control-Allow-Headers"] = "*"
    if "Access-Control-Allow-Credentials" not in response.headers:
        response.headers["Access-Control-Allow-Credentials"] = "true"

    return response


# Detector global
detector = None

# Configurações de câmera usando o arquivo de configuração
camera_config = Config.get_camera_config()

# Cache de frames ultra-otimizado
frame_cache = {
    "last_frame": None,
    "last_encoding": None,
    "last_time": 0,
    "cache_hits": 0,
    "cache_misses": 0,
}


# Modelos Pydantic para autenticação e logs
class RegisterModel(BaseModel):
    username: str = Field(
        ..., min_length=3, description="Nome completo com sobrenome (ex: João Silva)"
    )
    email: EmailStr = Field(..., description="Email válido")
    password: str = Field(
        ..., min_length=6, description="Senha com mínimo 6 caracteres"
    )
    invitationToken: str = Field(..., description="Token de convite válido")
    
    @validator('username')
    def validate_full_name(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Nome deve ter pelo menos 3 caracteres')
        
        # Verificar se tem pelo menos um espaço (nome + sobrenome)
        if ' ' not in v.strip():
            raise ValueError('Nome deve incluir sobrenome (ex: João Silva)')
        
        # Verificar se não tem espaços múltiplos ou no início/fim
        parts = v.strip().split()
        if len(parts) < 2:
            raise ValueError('Nome deve incluir sobrenome (ex: João Silva)')
        
        # Verificar se cada parte tem pelo menos 2 caracteres
        for part in parts:
            if len(part) < 2:
                raise ValueError('Cada parte do nome deve ter pelo menos 2 caracteres')
        
        return v.strip()


class LoginModel(BaseModel):
    username: str = Field(..., description="Nome de usuário ou email")
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class LogModel(BaseModel):
    timestamp: datetime
    count: int
    details: dict  # opcional: pode guardar info extra da detecção


class LogOutModel(BaseModel):
    timestamp: datetime
    count: int
    details: dict
    created_at: datetime


# Funções de autenticação
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Cria um token JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = brasilia_now() + expires_delta
    else:
        expire = brasilia_now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """Verifica um token JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency para obter usuário atual a partir do token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(401, "Token inválido")
    except JWTError as e:
        raise HTTPException(401, "Token inválido")

    user = await users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(401, "Usuário não existe")
    return username


@app.on_event("startup")
async def startup_event():
    """Inicialização ultra-otimizada."""
    global detector
    try:
        detector = OptimizedDetector(src=camera_config["current_source"])

        # Aguardar inicialização completa
        await asyncio.sleep(1.5)  # Reduzido para inicialização mais rápida
    except Exception as e:
        pass


def encode_frame_ultra_fast(frame):
    """Codificação ultra-rápida com cache inteligente e qualidade otimizada."""
    global frame_cache

    if frame is None:
        return None

    try:
        current_time = datetime.now().timestamp()

        # Cache inteligente - se frame muito similar ao anterior, reusar encoding
        if (
            frame_cache["last_frame"] is not None
            and current_time - frame_cache["last_time"] < 0.02
        ):  # 20ms cache

            # Verificação rápida de similaridade (sample menor para velocidade)
            if np.array_equal(frame[::16, ::16], frame_cache["last_frame"][::16, ::16]):
                frame_cache["cache_hits"] += 1
                return frame_cache["last_encoding"]

        frame_cache["cache_misses"] += 1

        # Parâmetros de encoding ultra-otimizados para velocidade máxima
        encode_params = [
            cv2.IMWRITE_JPEG_QUALITY,
            50,  # Qualidade reduzida para velocidade máxima
            cv2.IMWRITE_JPEG_OPTIMIZE,
            0,  # Sem otimização = mais rápido
            cv2.IMWRITE_JPEG_PROGRESSIVE,
            0,  # Sem progressive = mais rápido
        ]

        ret, buffer = cv2.imencode(".jpg", frame, encode_params)

        if ret and buffer is not None:
            encoded = buffer.tobytes()

            # Atualizar cache com sample menor
            frame_cache.update(
                {
                    "last_frame": frame[
                        ::16, ::16
                    ].copy(),  # Sample menor para comparação
                    "last_encoding": encoded,
                    "last_time": current_time,
                }
            )

            return encoded

    except Exception as e:
        pass

    return None


async def generate_ultra_fast_stream():
    """Gerador de stream ultra-otimizado com FPS máximo."""
    global detector, camera_config

    if not detector:
        # Stream de erro se detector não disponível
        error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(
            error_frame,
            "DETECTOR NAO INICIADO",
            (150, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

        chunk = encode_frame_ultra_fast(error_frame)
        if chunk:
            while True:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n"
                    b"Content-Length: "
                    + str(len(chunk)).encode()
                    + b"\r\n\r\n"
                    + chunk
                    + b"\r\n"
                )
                await asyncio.sleep(0.016)  # ~60 FPS para erro
        return

    frame_count = 0

    while True:
        try:
            # Verificar se stream está habilitado
            if not camera_config["stream_enabled"]:
                # Frame de "aguardando liberação"
                waiting_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(
                    waiting_frame,
                    "AGUARDANDO LIBERACAO",
                    (120, 200),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2,
                )
                cv2.putText(
                    waiting_frame,
                    "Clique em 'Iniciar Stream'",
                    (140, 240),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    1,
                )

                chunk = encode_frame_ultra_fast(waiting_frame)
                if chunk:
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n"
                        b"Content-Length: "
                        + str(len(chunk)).encode()
                        + b"\r\n\r\n"
                        + chunk
                        + b"\r\n"
                    )
                await asyncio.sleep(0.1)  # 10 FPS para frame de espera
                continue

            # Obter frame mais recente
            frame = detector.get_frame()

            if frame is not None:
                # Anotar frame (usa cache de detecções)
                annotated_frame = detector.detect_and_annotate(frame)

                # Encoding ultra-rápido
                chunk = encode_frame_ultra_fast(annotated_frame)

                if chunk:
                    frame_count += 1

                    # Yield do frame SEM LIMITE DE FPS
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n"
                        b"Content-Length: "
                        + str(len(chunk)).encode()
                        + b"\r\n\r\n"
                        + chunk
                        + b"\r\n"
                    )

            # Yield mínimo para não travar (sem limite de FPS)
            await asyncio.sleep(0.001)

        except Exception as e:
            await asyncio.sleep(0.01)


@app.get("/")
async def root():
    """API info ultra-otimizada."""
    global detector, camera_config

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
        cache_ratio = (
            frame_cache["cache_hits"] / max(frame_cache["cache_misses"], 1) * 100
        )
        base_info["performance"] = {
            "fps": stats.get("capture_fps", 0),
            "models_ready": stats.get("models_ready", False),
            "cache_efficiency": f"{cache_ratio:.1f}%",
        }

    return base_info


@app.get("/video_feed")
async def video_feed():
    """Stream MJPEG ultra-otimizado com headers otimizados."""
    return StreamingResponse(
        generate_ultra_fast_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "X-Accel-Buffering": "no",  # Nginx optimization
            "Connection": "close",
            "Transfer-Encoding": "chunked",
            "X-Content-Type-Options": "nosniff",
        },
    )


@app.get("/demo-stream.jpg")
async def demo_stream():
    """Imagem única ultra-otimizada."""
    global detector, camera_config

    if not detector:
        return Response(content=b"", status_code=503, headers={"Retry-After": "3"})

    try:
        # Verificar se stream está habilitado
        if not camera_config["stream_enabled"]:
            # Frame de "aguardando liberação"
            waiting_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(
                waiting_frame,
                "AGUARDANDO LIBERACAO",
                (120, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2,
            )
            cv2.putText(
                waiting_frame,
                "Clique em 'Iniciar Stream'",
                (140, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1,
            )

            chunk = encode_frame_ultra_fast(waiting_frame)
            if chunk:
                return Response(
                    content=chunk,
                    media_type="image/jpeg",
                    headers={
                        "Cache-Control": "no-cache, max-age=0",
                        "Pragma": "no-cache",
                        "X-Content-Type-Options": "nosniff",
                    },
                )

        frame = detector.get_frame()
        if frame is not None:
            frame = detector.detect_and_annotate(frame)
            chunk = encode_frame_ultra_fast(frame)

            if chunk:
                return Response(
                    content=chunk,
                    media_type="image/jpeg",
                    headers={
                        "Cache-Control": "no-cache, max-age=0",
                        "Pragma": "no-cache",
                        "X-Content-Type-Options": "nosniff",
                    },
                )

        return Response(status_code=204)  # No content

    except Exception as e:
        return Response(status_code=500)


@app.get("/stats")
async def get_stats():
    """Stats ultra-rápidas com cache info e tracking."""
    global detector, camera_config

    if not detector:
        return {"current": 0, "total_passed": 0, "status": "starting"}

    cache_ratio = frame_cache["cache_hits"] / max(frame_cache["cache_misses"], 1) * 100

    stats_data = {
        "current": detector.prev_count,
        "total_passed": detector.total_passed,
        "status": "active",
        "fps": detector.current_fps,
        "cache_efficiency": f"{cache_ratio:.1f}%",
        "camera": {
            "current_source": (
                "webcam" if camera_config["current_source"] == 0 else "ip_camera"
            ),
            "stream_enabled": camera_config["stream_enabled"],
        },
        "tracking": {
            "total_entries": detector.person_tracking["total_entries"],
            "total_exits": detector.person_tracking["total_exits"],
            "current_persons": detector.person_tracking["current_session_persons"],
            "session_duration": (
                brasilia_now() - detector.person_tracking["session_start"]
            ).total_seconds(),
        },
    }

    return stats_data

    return stats_data


@app.get("/performance")
async def get_performance():
    """Métricas de performance detalhadas com cache."""
    global detector, camera_config

    try:
        if not detector:
            return {
                "capture_fps": 0,
                "detection_fps": 0,
                "buffer_size": 0,
                "models_status": {
                    "yolo": False,
                    "face": False,
                },
                "memory_usage": {
                    "total_detections": 0,
                    "current_people": 0,
                },
                "detection_rate": {
                    "detections_per_second": 0,
                    "total_detections": 0,
                    "detection_efficiency": 0,
                },
                "camera": {
                    "current_source": "webcam",
                    "stream_enabled": False,
                },
            }

        stats = detector.get_performance_stats()
        cache_ratio = (
            frame_cache["cache_hits"] / max(frame_cache["cache_misses"], 1) * 100
        )

        return {
            "capture_fps": stats.get("capture_fps", 0),
            "detection_fps": stats.get("detection_fps", 0),
            "buffer_size": stats.get("frame_queue_size", 0),
            "models_status": {
                "yolo": stats.get("yolo_available", False),
                "face": stats.get("face_available", False),
            },
            "memory_usage": {
                "total_detections": stats.get("total_detections", 0),
                "current_people": stats.get("current_people", 0),
            },
            "detection_rate": stats.get(
                "detection_rate",
                {
                    "detections_per_second": 0,
                    "total_detections": 0,
                    "detection_efficiency": 0,
                },
            ),
            "camera": {
                "current_source": (
                    "webcam" if camera_config["current_source"] == 0 else "ip_camera"
                ),
                "stream_enabled": camera_config["stream_enabled"],
            },
        }
    except Exception as e:
        # Retornar resposta de erro estruturada em vez de 500
        return {
            "capture_fps": 0,
            "detection_fps": 0,
            "buffer_size": 0,
            "models_status": {
                "yolo": False,
                "face": False,
            },
            "memory_usage": {
                "total_detections": 0,
                "current_people": 0,
            },
            "detection_rate": {
                "detections_per_second": 0,
                "total_detections": 0,
                "detection_efficiency": 0,
            },
            "camera": {
                "current_source": "webcam",
                "stream_enabled": False,
            },
            "error": str(e),
        }


# Novos endpoints para controle de câmera
@app.post("/camera/switch")
async def switch_camera(source: str, current_user: str = Depends(get_current_user)):
    """Troca entre webcam e IP camera."""
    global detector, camera_config

    if source not in camera_config["available_sources"]:
        raise HTTPException(
            status_code=400,
            detail=f"Fonte inválida. Use: {list(camera_config['available_sources'].keys())}",
        )

    try:
        new_source = camera_config["available_sources"][source]

        # Parar detector atual
        if detector:
            detector.stop()

        # Inicializar novo detector
        detector = OptimizedDetector(src=new_source)
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


@app.post("/stream/control")
async def control_stream(action: str, current_user: str = Depends(get_current_user)):
    """Controla o stream (start/stop)."""
    global camera_config

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


@app.get("/camera/status")
async def get_camera_status():
    """Retorna status atual da câmera."""
    global detector, camera_config

    return {
        "current_source": (
            "webcam" if camera_config["current_source"] == 0 else "ip_camera"
        ),
        "stream_enabled": camera_config["stream_enabled"],
        "available_sources": list(camera_config["available_sources"].keys()),
        "detector_ready": detector is not None,
        "ip_url": camera_config["ip_url"],
    }


@app.get("/config")
async def get_config():
    """Retorna configurações do sistema."""
    return {
        "camera": Config.get_camera_config(),
        "detection": Config.get_detection_config(),
        "server": Config.get_server_config(),
    }


@app.get("/export_log.csv")
async def export_log(current_user: str = Depends(get_current_user)):
    """Export simplificado com total de pessoas capturadas."""
    global detector

    # CSV simplificado
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    # Header simplificado
    writer.writerow(
        [
            "timestamp",
            "total_pessoas_capturadas",
            "pessoas_atuais",
            "fps_sistema",
            "usuario_exportacao",
        ]
    )

    if detector:
        # Dados atuais do sistema
        current_time = datetime.now()
        total_captured = detector.person_tracking["total_entries"]
        current_persons = detector.person_tracking["current_session_persons"]
        current_fps = detector.current_fps

        writer.writerow(
            [
                current_time.isoformat(),
                total_captured,
                current_persons,
                round(current_fps, 1),
                current_user,
            ]
        )

    csv_data = buffer.getvalue()
    buffer.close()

    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"shomer_total_pessoas_{timestamp}.csv"

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.get("/health")
async def health():
    """Health check ultra-rápido."""
    global detector, camera_config

    detector_info = {}
    if detector:
        detector_info = {
            "running": detector.running,
            "prev_count": detector.prev_count,
            "total_passed": detector.total_passed,
            "current_fps": detector.current_fps,
            "person_tracking": detector.person_tracking,
        }

    return {
        "status": "healthy",
        "detector": "ready" if detector else "loading",
        "detector_info": detector_info,
        "camera": {
            "current_source": (
                "webcam" if camera_config["current_source"] == 0 else "ip_camera"
            ),
            "stream_enabled": camera_config["stream_enabled"],
        },
        "timestamp": brasilia_now().isoformat(),
    }


# Endpoints de autenticação e logs
@app.post("/register")
async def register(data: RegisterModel):
    """Registra um novo usuário."""
    # valida token de convite
    if data.invitationToken != INVITATION_TOKEN:
        raise HTTPException(403, "Token de convite inválido")

    # verifica se usuário já existe
    existing = await users_collection.find_one({"username": data.username})
    if existing:
        raise HTTPException(400, "Usuário já existe")
    hashed = hash_password(data.password)
    await users_collection.insert_one(
        {
            "username": data.username,
            "email": data.email,
            "password": hashed,
            "created_at": brasilia_now(),
        }
    )
    return {"msg": "Registrado com sucesso"}


@app.post("/login", response_model=Token)
async def login(data: LoginModel, request: Request):
    """Autentica um usuário com username ou email."""
    # Rate limiting específico para login
    client_ip = request.client.host
    current_time = time.time()

    # Limpar tentativas antigas
    login_attempts = [
        attempt_time
        for attempt_time in request_counts.get(f"login_{client_ip}", [])
        if current_time - attempt_time < RATE_LIMIT_WINDOW
    ]

    # Verificar limite de tentativas de login
    if len(login_attempts) >= LOGIN_RATE_LIMIT_MAX:
        raise HTTPException(
            status_code=429, detail="Too many login attempts. Try again later."
        )

    # Verifica se é email ou username
    is_email = "@" in data.username

    if is_email:
        # Busca por email
        user = await users_collection.find_one({"email": data.username})
    else:
        # Busca por username
        user = await users_collection.find_one({"username": data.username})

    if not user or not verify_password(data.password, user["password"]):
        # Adicionar tentativa falhada
        if f"login_{client_ip}" not in request_counts:
            request_counts[f"login_{client_ip}"] = []
        request_counts[f"login_{client_ip}"].append(current_time)
        raise HTTPException(401, "Credenciais inválidas")

    # Gera token JWT usando o username real
    to_encode = {"sub": user["username"]}
    expire = brasilia_now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # devolve também o email e id
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user.get("email", ""),
            "createdAt": user["created_at"].isoformat(),
        },
    }


@app.post("/logs")
async def create_log(
    data: LogModel,
    current_user: str = Depends(get_current_user),
):
    """Cria um novo log de detecção."""
    payload = data.dict()
    payload["created_at"] = brasilia_now()
    payload["user"] = current_user
    await logs_collection.insert_one(payload)
    return {"msg": "Log registrado"}


@app.get("/me")
async def get_current_user_info(current_user: str = Depends(get_current_user)):
    """Retorna informações do usuário atual."""
    user = await users_collection.find_one({"username": current_user})
    return {"username": current_user, "created_at": user["created_at"]}


@app.get("/logs", response_model=List[LogOutModel])
async def list_logs(limit: int = 100):
    """
    Retorna os últimos `limit` logs, em ordem decrescente de timestamp.
    """
    cursor = logs_collection.find().sort("timestamp", -1).limit(limit)
    results = []
    async for doc in cursor:
        results.append(LogOutModel(**doc))
    return results


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown ultra-otimizado."""
    global detector
    if detector:
        detector.stop()


if __name__ == "__main__":
    import uvicorn
    import time

    # Configuração ultra-otimizada do servidor
    server_config = Config.get_server_config()

    uvicorn.run(
        "main:app",
        host=server_config["host"],
        port=server_config["port"],
        reload=False,  # Reload desabilitado para performance
        access_log=False,  # Logs de acesso desabilitados para velocidade
        log_level="warning",  # Menos logs = mais performance
        loop="asyncio",  # Loop assíncrono otimizado
        workers=1,  # Single worker para evitar conflitos de câmera
        limit_concurrency=200,  # Aumentado para mais conexões
        limit_max_requests=20000,  # Aumentado para evitar memory leaks
        timeout_keep_alive=3,  # Keep-alive otimizado
        timeout_graceful_shutdown=5,  # Shutdown mais rápido
    )
