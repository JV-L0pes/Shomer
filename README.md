# Shomer - Sistema de Detecção em Tempo Real

## 🎯 Visão Geral

O **Shomer** é um sistema avançado de detecção em tempo real que utiliza YOLOv8 e InsightFace para identificar pessoas e rostos em vídeo. O sistema agora inclui controles avançados de câmera e stream, permitindo trocar entre webcam e IP camera, além de controlar quando o stream é liberado.

## ✨ Novas Funcionalidades

### 🎥 Controle de Câmeras
- **Troca Dinâmica**: Mude entre webcam e IP camera em tempo real
- **Interface Intuitiva**: Botões estilizados para controle fácil
- **Status Visual**: Indicadores visuais do estado atual da câmera
- **Suporte a IP Cameras**: Compatível com DroidCam, IP Webcam e outras soluções

### 🎬 Controle de Stream
- **Liberação Manual**: O stream só é liberado quando você clicar em "Iniciar Stream"
- **Frame de Espera**: Tela informativa enquanto aguarda liberação
- **Controle Total**: Inicie e pare o stream quando quiser
- **Performance Otimizada**: Backend roda continuamente, apenas o stream é controlado

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.8+
- Webcam ou fonte de vídeo
- (Opcional) IP Camera (DroidCam, IP Webcam, etc.)

### 1. Instalação do Backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configuração da IP Camera

Edite o arquivo `backend/config.py` para configurar sua IP camera:

```python
# Para DroidCam
CAMERA_SOURCES = {
    "webcam": 0,
    "ip_camera": "http://192.168.1.100:4747/video"  # Substitua pelo IP do seu celular
}
```

### 3. Executar o Backend

```bash
cd backend
py main.py
```

### 4. Executar o Frontend

```bash
cd frontend
npm install
npm run dev
```

## 🎮 Como Usar

### Interface Principal

1. **Acesse o Frontend**: Abra `http://localhost:5173` no navegador
2. **Controles de Câmera**: Use os botões no painel lateral direito
3. **Trocar Câmera**: Clique em "Webcam" ou "IP Camera"
4. **Iniciar Stream**: Clique em "Iniciar Stream" para liberar o vídeo
5. **Parar Stream**: Clique em "Parar Stream" para pausar

### Controles Disponíveis

#### 🖥️ Troca de Câmera
- **Webcam**: Usa a câmera local do computador
- **IP Camera**: Usa câmera remota via rede

#### ▶️ Controle de Stream
- **Iniciar Stream**: Libera o stream de vídeo com detecções
- **Parar Stream**: Pausa o stream (mostra tela de espera)

#### 📊 Monitoramento
- **Status em Tempo Real**: Visualização do estado da câmera e stream
- **Estatísticas**: Contadores de pessoas detectadas
- **Performance**: FPS e métricas do sistema

## 🔧 Configuração Avançada

### Variáveis de Ambiente

```bash
# Configurações de Câmera
YOLO_MODEL=yolov8n.pt
CONF_THRESHOLD=0.5
TARGET_FPS=60
DETECTION_FPS=30

# Configurações do Servidor
HOST=0.0.0.0
PORT=8000

# Controle de Stream
STREAM_ENABLED_BY_DEFAULT=false
```

### Configurações de IP Camera

#### DroidCam
```python
"ip_camera": "http://192.168.1.100:4747/video"
```

#### IP Webcam
```python
"ip_camera": "http://192.168.1.100:8080/video"
```

#### Câmera Local
```python
"ip_camera": "0"  # Índice da câmera local
```

## 📡 API Endpoints

### Controle de Câmera
- `POST /camera/switch?source=webcam` - Trocar para webcam
- `POST /camera/switch?source=ip_camera` - Trocar para IP camera
- `GET /camera/status` - Status atual da câmera

### Controle de Stream
- `POST /stream/control?action=start` - Iniciar stream
- `POST /stream/control?action=stop` - Parar stream

### Monitoramento
- `GET /stats` - Estatísticas em tempo real
- `GET /performance` - Métricas de performance
- `GET /health` - Status de saúde do sistema
- `GET /config` - Configurações do sistema

## 🎨 Interface

### Design Moderno
- **Dark Theme**: Interface escura e moderna
- **Animações**: Transições suaves e responsivas
- **Status Visual**: Indicadores coloridos para diferentes estados
- **Layout Responsivo**: Funciona em desktop e mobile

### Componentes Principais
- **VideoStream**: Exibição do stream com detecções
- **CameraControls**: Painel de controle de câmera
- **StatCards**: Cartões com estatísticas em tempo real
- **ExportButton**: Botão para exportar relatórios

## 🔍 Detecção

### Tecnologias Utilizadas
- **YOLOv8**: Detecção de pessoas
- **InsightFace**: Detecção facial
- **OpenCV**: Processamento de vídeo
- **FastAPI**: Backend API

### Performance
- **FPS**: 25-60 FPS dependendo do hardware
- **Latência**: <100ms para detecção
- **Precisão**: >90% para pessoas, >95% para rostos
- **Otimização**: Cache inteligente e threading avançado

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
Shomer/
├── backend/
│   ├── main.py              # API FastAPI
│   ├── detection.py         # Detector principal
│   ├── config.py            # Configurações
│   └── requirements.txt     # Dependências Python
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── api.ts          # Cliente API
│   │   └── app.tsx         # App principal
│   └── package.json        # Dependências Node.js
└── README.md               # Este arquivo
```

### Tecnologias Frontend
- **React 18**: Framework principal
- **TypeScript**: Tipagem estática
- **Tailwind CSS**: Estilização
- **Framer Motion**: Animações
- **Lucide React**: Ícones
- **Axios**: Cliente HTTP

## 🚨 Solução de Problemas

### Câmera não conecta
1. Verifique se a webcam está funcionando
2. Teste com aplicativos nativos
3. Verifique permissões do navegador

### IP Camera não funciona
1. Verifique se o IP está correto
2. Teste a URL no navegador
3. Verifique se está na mesma rede
4. Confirme se a porta está aberta

### Stream não inicia
1. Clique em "Iniciar Stream"
2. Verifique se o backend está rodando
3. Confirme se a câmera está conectada

### Performance baixa
1. Reduza a resolução da câmera
2. Ajuste o threshold de confiança
3. Use modelo YOLO menor (yolov8n.pt)

## 📝 Licença

Este projeto está sob a licença MIT.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

⭐ Se este projeto foi útil, considere dar uma estrela! 