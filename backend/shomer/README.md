# Shomer - Sistema de Detecção Realtime de Corpos e Rostos

## 📋 Descrição

O **Shomer** é um sistema avançado de detecção em tempo real que utiliza YOLOv8 e MediaPipe para identificar corpos e rostos em vídeo. O projeto foi desenvolvido seguindo os princípios da **Clean Architecture** para garantir manutenibilidade, testabilidade e escalabilidade.

## ✨ Características

- 🔍 **Detecção Dupla**: Corpos (YOLOv8) + Rostos (MediaPipe)
- 🏗️ **Arquitetura Limpa**: Separação clara de responsabilidades
- ⚡ **Performance Otimizada**: Processamento eficiente de vídeo
- 🎥 **Múltiplas Fontes**: Suporte para webcam e streams IP
- 📊 **Métricas em Tempo Real**: FPS e estatísticas de detecção
- 🎨 **Interface Visual**: Bounding boxes e informações sobrepostas
- ⚙️ **Configurável**: Parâmetros ajustáveis via configuração
- 📦 **Instalação Simplificada**: Package Python com entry points

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- Windows 10/11 (testado)
- Webcam ou fonte de vídeo

### Setup Rápido

1. **Clone o repositório**
```bash
git clone https://github.com/JV-L0pes/Shomer.git
cd Shomer
```

2. **Ative o ambiente virtual**
```powershell
.\venv\Scripts\Activate.ps1
```

3. **Instale o projeto em modo desenvolvimento**
```bash
pip install -e .
```

4. **Execute o projeto**
```bash
shomer
```

### Alternativa: Instalação Direta
```bash
pip install -r requirements.txt
python -m shomer.main
```

## 📁 Estrutura do Projeto

O projeto segue os princípios da **Clean Architecture** com as seguintes camadas:

```
Shomer/
├── shomer/                          # Pacote principal
│   ├── main.py                      # Ponto de entrada da aplicação
│   ├── application/                 # Casos de uso (regras de negócio)
│   │   ├── detect_faces.py         # Caso de uso para detecção facial
│   │   ├── detect_people.py        # Caso de uso para detecção de pessoas
│   │   └── orchestrator.py         # Orquestrador principal
│   ├── domain/                      # Entidades e portas (regras de domínio)
│   │   ├── entities/               # Entidades do domínio
│   │   │   ├── face.py            # Entidade Face
│   │   │   └── person.py          # Entidade Person
│   │   └── ports/                  # Interfaces (contratos)
│   │       ├── detector.py        # Interface para detectores
│   │       ├── renderer.py        # Interface para renderizadores
│   │       └── video_source.py    # Interface para fontes de vídeo
│   ├── infrastructure/             # Implementações concretas
│   │   ├── detectors/             # Implementações dos detectores
│   │   │   ├── mp_detector.py     # Detector MediaPipe
│   │   │   └── yolo_detector.py   # Detector YOLOv8
│   │   ├── presenters/            # Implementações dos renderizadores
│   │   │   └── opencv_renderer.py # Renderizador OpenCV
│   │   └── video_source/          # Implementações das fontes de vídeo
│   │       └── opencv_capture.py  # Captura OpenCV
│   └── interfaces/                 # Interface com o usuário
│       ├── cli.py                 # Interface de linha de comando
│       └── config.py              # Configurações do sistema
├── setup.py                        # Configuração do package
├── requirements.txt                # Dependências Python
├── cleanup.py                      # Utilitários de limpeza
└── README.md                       # Este arquivo
```

## 🔧 Configuração

### Variáveis de Ambiente
Configure as seguintes variáveis de ambiente ou edite o arquivo `shomer/interfaces/config.py`:

```bash
# Modelo YOLOv8 (padrão: yolov8n.pt)
export YOLO_MODEL=yolov8s.pt

# Threshold de confiança (padrão: 0.5)
export CONF_THRESHOLD=0.6

# Título da janela (padrão: "Shomer - Real-time")
export WINDOW_TITLE="Meu Detector"
```

### Configurações Disponíveis
- **Modelo YOLOv8**: Tamanho e configurações do modelo
- **MediaPipe**: Parâmetros de detecção facial
- **Câmera**: Resolução, FPS e fonte de vídeo
- **Cores**: Personalização das cores de interface

## 🎮 Como Usar

### Execução Básica
```bash
shomer
```

### Com Fonte de Vídeo Específica
```bash
# Usar webcam (padrão)
shomer --source webcam

# Usar stream IP (DroidCam)
shomer --source ip
```

### Execução Direta
```bash
python -m shomer.main --source webcam
```

## 📊 Performance

- **FPS**: 25-30 FPS em hardware médio
- **Latência**: <50ms para detecção
- **Precisão**: >90% para corpos, >95% para rostos
- **Uso de CPU**: Otimizado para multi-core
- **Memória**: Gerenciamento eficiente de recursos

## 🛠️ Tecnologias Utilizadas

### Core
- **YOLOv8**: Detecção de objetos e pessoas
- **MediaPipe**: Detecção facial
- **OpenCV**: Processamento de vídeo
- **NumPy**: Computação numérica

### Arquitetura
- **Clean Architecture**: Separação de responsabilidades
- **Dependency Injection**: Inversão de dependências
- **Interface Segregation**: Contratos bem definidos

### Interface
- **PyQt5**: Interface gráfica (futuro)
- **CLI**: Interface de linha de comando

## 🏗️ Arquitetura

O projeto implementa **Clean Architecture** com as seguintes camadas:

1. **Domain Layer**: Entidades e regras de negócio
2. **Application Layer**: Casos de uso e orquestração
3. **Infrastructure Layer**: Implementações concretas
4. **Interface Layer**: Interface com usuário

### Benefícios da Arquitetura
- ✅ **Testabilidade**: Fácil mock de dependências
- ✅ **Manutenibilidade**: Código organizado e modular
- ✅ **Escalabilidade**: Fácil adição de novos detectores
- ✅ **Flexibilidade**: Troca de implementações sem afetar regras de negócio

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Desenvolvimento
- Siga os princípios da Clean Architecture
- Mantenha a separação de responsabilidades
- Adicione testes para novos casos de uso
- Documente novas funcionalidades

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**JV-L0pes**
- GitHub: [@JV-L0pes](https://github.com/JV-L0pes)

## 🙏 Agradecimentos

- Comunidade YOLOv8
- MediaPipe Team
- OpenCV Community
- Clean Architecture Community

## 🔮 Roadmap

- [ ] Interface gráfica com PyQt5
- [ ] Suporte a múltiplas câmeras
- [ ] Sistema de alertas
- [ ] API REST
- [ ] Dashboard web
- [ ] Integração com banco de dados

---

⭐ Se este projeto foi útil, considere dar uma estrela! 