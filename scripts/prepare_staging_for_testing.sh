#!/bin/bash
# Script para preparar el entorno de staging para pruebas de usuario

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo "=== Preparación del Entorno de Staging para Pruebas de Usuario ==="

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}[ERROR] No se encontró el archivo docker-compose.yml${NC}"
    echo "Por favor, ejecuta este script desde el directorio raíz del proyecto."
    exit 1
fi

# Crear archivo docker-compose.staging.yml si no existe
if [ ! -f "docker-compose.staging.yml" ]; then
    echo "Creando archivo docker-compose.staging.yml..."
    cat > docker-compose.staging.yml << EOL
version: '3.8'

services:
  backend:
    environment:
      - APP_ENV=staging
      - APP_DEBUG=true
      - DEBUG=true
    volumes:
      - ./backend-call-automation:/app
      - /app/venv

  frontend:
    environment:
      - NODE_ENV=development
    volumes:
      - ./frontend-call-automation:/app
      - /app/node_modules
      - /app/.next

  # Servicio para cargar datos de ejemplo
  data-loader:
    build:
      context: ./scripts/data-loader
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=\${DATABASE_URL}
      - SUPABASE_URL=\${SUPABASE_URL}
      - SUPABASE_KEY=\${SUPABASE_KEY}
    depends_on:
      - backend
EOL
    echo -e "${GREEN}[OK] Archivo docker-compose.staging.yml creado.${NC}"
else
    echo -e "${GREEN}[OK] Archivo docker-compose.staging.yml ya existe.${NC}"
fi

# Crear directorio para data-loader si no existe
if [ ! -d "scripts/data-loader" ]; then
    echo "Creando directorio para data-loader..."
    mkdir -p scripts/data-loader
    
    # Crear Dockerfile para data-loader
    cat > scripts/data-loader/Dockerfile << EOL
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "load_test_data.py"]
EOL
    
    # Crear requirements.txt para data-loader
    cat > scripts/data-loader/requirements.txt << EOL
supabase==1.0.3
pandas==2.0.3
faker==18.13.0
python-dotenv==1.0.0
EOL
    
    # Crear script para cargar datos de ejemplo
    cat > scripts/data-loader/load_test_data.py << EOL
#!/usr/bin/env python3
"""
Script para cargar datos de ejemplo en el entorno de staging.
"""
import os
import time
import json
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client
from faker import Faker

# Cargar variables de entorno
load_dotenv()

# Configurar Supabase
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Configurar Faker
fake = Faker('es_ES')

def create_test_users():
    """Crear usuarios de prueba."""
    print("Creando usuarios de prueba...")
    
    users = [
        {"email": "admin@example.com", "password": "password123", "role": "admin"},
        {"email": "user@example.com", "password": "password123", "role": "user"},
        {"email": "marketing@example.com", "password": "password123", "role": "user"},
        {"email": "sales@example.com", "password": "password123", "role": "user"},
        {"email": "support@example.com", "password": "password123", "role": "user"},
    ]
    
    for user in users:
        try:
            # Registrar usuario en Supabase Auth
            auth_response = supabase.auth.sign_up({
                "email": user["email"],
                "password": user["password"]
            })
            
            user_id = auth_response.user.id
            
            # Insertar información adicional en la tabla de usuarios
            supabase.table("users").insert({
                "id": user_id,
                "email": user["email"],
                "role": user["role"],
                "full_name": fake.name(),
                "avatar_url": f"https://i.pravatar.cc/150?u={user_id}",
                "created_at": datetime.now().isoformat()
            }).execute()
            
            print(f"  Usuario creado: {user['email']} (Rol: {user['role']})")
        except Exception as e:
            print(f"  Error al crear usuario {user['email']}: {str(e)}")
    
    print("Usuarios de prueba creados.")

def create_test_contacts(num_contacts=50):
    """Crear contactos de prueba."""
    print(f"Creando {num_contacts} contactos de prueba...")
    
    contacts = []
    for _ in range(num_contacts):
        contact = {
            "name": fake.name(),
            "phone": fake.phone_number(),
            "email": fake.email(),
            "company": fake.company(),
            "position": fake.job(),
            "tags": random.sample(["cliente", "prospecto", "activo", "inactivo", "VIP"], random.randint(1, 3)),
            "notes": fake.paragraph(),
            "created_at": datetime.now().isoformat()
        }
        contacts.append(contact)
    
    # Insertar contactos en lotes de 10
    for i in range(0, len(contacts), 10):
        batch = contacts[i:i+10]
        try:
            supabase.table("contacts").insert(batch).execute()
            print(f"  Lote {i//10 + 1} de contactos creado.")
        except Exception as e:
            print(f"  Error al crear lote {i//10 + 1} de contactos: {str(e)}")
    
    print("Contactos de prueba creados.")

def create_test_campaigns(num_campaigns=5):
    """Crear campañas de prueba."""
    print(f"Creando {num_campaigns} campañas de prueba...")
    
    # Obtener contactos para asignar a las campañas
    contacts_response = supabase.table("contacts").select("id").execute()
    contact_ids = [contact["id"] for contact in contacts_response.data]
    
    campaign_types = ["ventas", "soporte", "encuesta", "seguimiento", "informativa"]
    campaign_statuses = ["draft", "scheduled", "active", "paused", "completed"]
    
    for i in range(num_campaigns):
        # Crear campaña
        campaign_type = campaign_types[i % len(campaign_types)]
        campaign_status = campaign_statuses[i % len(campaign_statuses)]
        
        start_date = datetime.now() + timedelta(days=random.randint(1, 30))
        end_date = start_date + timedelta(days=random.randint(7, 60))
        
        campaign = {
            "name": f"Campaña de {campaign_type.capitalize()} {i+1}",
            "description": fake.paragraph(),
            "type": campaign_type,
            "status": campaign_status,
            "schedule_start": start_date.isoformat(),
            "schedule_end": end_date.isoformat(),
            "calling_hours_start": "09:00",
            "calling_hours_end": "18:00",
            "script_template": f"Hola {{name}}, te llamamos de {{company}} para {fake.sentence()}",
            "created_at": datetime.now().isoformat()
        }
        
        try:
            # Insertar campaña
            campaign_response = supabase.table("campaigns").insert(campaign).execute()
            campaign_id = campaign_response.data[0]["id"]
            
            # Asignar contactos aleatorios a la campaña
            selected_contacts = random.sample(contact_ids, random.randint(5, 20))
            campaign_contacts = []
            
            for contact_id in selected_contacts:
                campaign_contact = {
                    "campaign_id": campaign_id,
                    "contact_id": contact_id,
                    "status": random.choice(["pending", "called", "no-answer", "scheduled"]),
                    "created_at": datetime.now().isoformat()
                }
                campaign_contacts.append(campaign_contact)
            
            # Insertar relaciones campaña-contacto
            supabase.table("campaign_contacts").insert(campaign_contacts).execute()
            
            print(f"  Campaña creada: {campaign['name']} con {len(selected_contacts)} contactos")
        except Exception as e:
            print(f"  Error al crear campaña {i+1}: {str(e)}")
    
    print("Campañas de prueba creadas.")

def create_test_calls(num_calls_per_campaign=10):
    """Crear llamadas de prueba."""
    print("Creando llamadas de prueba...")
    
    # Obtener campañas
    campaigns_response = supabase.table("campaigns").select("id,name").execute()
    
    if not campaigns_response.data:
        print("  No hay campañas para crear llamadas.")
        return
    
    call_statuses = ["scheduled", "in-progress", "completed", "failed", "no-answer"]
    
    for campaign in campaigns_response.data:
        campaign_id = campaign["id"]
        
        # Obtener contactos de la campaña
        contacts_response = supabase.table("campaign_contacts").select("contact_id").eq("campaign_id", campaign_id).execute()
        
        if not contacts_response.data:
            print(f"  No hay contactos para la campaña {campaign['name']}.")
            continue
        
        contact_ids = [contact["contact_id"] for contact in contacts_response.data]
        
        # Crear llamadas para contactos aleatorios
        selected_contacts = random.sample(contact_ids, min(num_calls_per_campaign, len(contact_ids)))
        
        for contact_id in selected_contacts:
            call_status = random.choice(call_statuses)
            start_time = datetime.now() - timedelta(days=random.randint(0, 14), hours=random.randint(0, 23))
            
            call = {
                "campaign_id": campaign_id,
                "contact_id": contact_id,
                "status": call_status,
                "duration": random.randint(30, 600) if call_status == "completed" else None,
                "start_time": start_time.isoformat(),
                "end_time": (start_time + timedelta(seconds=random.randint(30, 600))).isoformat() if call_status == "completed" else None,
                "recording_url": f"https://example.com/recordings/{fake.uuid4()}.mp3" if call_status == "completed" else None,
                "notes": fake.paragraph() if random.random() > 0.5 else None,
                "created_at": datetime.now().isoformat()
            }
            
            try:
                supabase.table("calls").insert(call).execute()
            except Exception as e:
                print(f"  Error al crear llamada: {str(e)}")
        
        print(f"  {len(selected_contacts)} llamadas creadas para la campaña {campaign['name']}")
    
    print("Llamadas de prueba creadas.")

def main():
    """Función principal."""
    print("Iniciando carga de datos de prueba...")
    
    # Esperar a que el backend esté disponible
    print("Esperando a que el backend esté disponible...")
    time.sleep(10)
    
    # Crear datos de prueba
    create_test_users()
    create_test_contacts(50)
    create_test_campaigns(5)
    create_test_calls(10)
    
    print("Carga de datos de prueba completada.")

if __name__ == "__main__":
    main()
EOL
    
    echo -e "${GREEN}[OK] Directorio y archivos para data-loader creados.${NC}"
else
    echo -e "${GREEN}[OK] Directorio para data-loader ya existe.${NC}"
fi

# Crear archivo .env.staging si no existe
if [ ! -f ".env.staging" ]; then
    echo "Creando archivo .env.staging..."
    cp .env.example .env.staging
    echo -e "${GREEN}[OK] Archivo .env.staging creado. Por favor, edita este archivo con las credenciales adecuadas.${NC}"
else
    echo -e "${GREEN}[OK] Archivo .env.staging ya existe.${NC}"
fi

# Verificar si hay un entorno de staging en ejecución
if docker-compose -f docker-compose.yml -f docker-compose.staging.yml ps | grep -q "Up"; then
    echo -e "${YELLOW}[ADVERTENCIA] Ya hay un entorno de staging en ejecución.${NC}"
    echo "Si deseas reiniciar el entorno, ejecuta:"
    echo "docker-compose -f docker-compose.yml -f docker-compose.staging.yml down"
    echo "docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d"
else
    echo "El entorno de staging no está en ejecución."
fi

echo ""
echo "=== Instrucciones para Iniciar el Entorno de Staging ==="
echo "1. Edita el archivo .env.staging con las credenciales adecuadas."
echo "2. Ejecuta el siguiente comando para iniciar el entorno de staging:"
echo -e "${YELLOW}docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d${NC}"
echo ""
echo "3. Para cargar datos de ejemplo, ejecuta:"
echo -e "${YELLOW}docker-compose -f docker-compose.yml -f docker-compose.staging.yml run --rm data-loader${NC}"
echo ""
echo "4. Para acceder al entorno de staging:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend: http://localhost:8000"
echo ""
echo "5. Credenciales de prueba:"
echo "   - Admin: admin@example.com / password123"
echo "   - Usuario: user@example.com / password123"
echo ""
echo "=== Preparación Completada ==="
