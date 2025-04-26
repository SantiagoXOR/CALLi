# Call Automation System

Sistema de automatización de llamadas que integra FastAPI, Supabase y Twilio para gestionar campañas de llamadas de manera eficiente y escalable.

## Requisitos del Sistema

- Node.js (v16+ o v18+)
- Python 3.9+
- Docker (opcional)
- Java Runtime Environment (JRE) para PlantUML
- Graphviz (para renderizar diagramas)

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd backend-call-automation
```

2. Instalar dependencias de documentación:
```bash
pip install sphinx sphinx-rtd-theme sphinxcontrib-plantuml

# Instalar PlantUML y Graphviz
# En Ubuntu/Debian:
sudo apt-get install plantuml graphviz

# En macOS:
brew install plantuml graphviz

# En Windows:
choco install plantuml graphviz
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
```

## Documentación

Para generar la documentación:
```bash
cd docs
sphinx-build -b html . _build/html
```

La documentación incluye:
- Diagramas de arquitectura
- Flujos de llamadas
- Esquema de base de datos
- Documentación de API

## CI/CD

El pipeline de CI incluye:
- Generación automática de documentación
- Despliegue en GitHub Pages
- Validación de diagramas PlantUML
