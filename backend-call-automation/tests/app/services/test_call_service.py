import pytest
from datetime import datetime, timedelta
from enum import Enum
from unittest.mock import Mock, AsyncMock, MagicMock
from twilio.rest import Client as TwilioClient
from fastapi import HTTPException, status
from app.models.call import Call, CallCreate, CallStatus, CallUpdate
from app.models.campaign import Campaign, CampaignBase
from app.services.call_service import CallService
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MockTwilioCall:
    def __init__(self, sid: str, status: str):
        self.sid = sid
        self.status = status

@pytest.fixture
def test_campaign():
    now = datetime.now()
    return Campaign(
        id=1,
        name="Test Campaign",
        description="Test campaign description",
        status="active",
        schedule_start=now,
        schedule_end=now + timedelta(days=7),
        contact_list_ids=[1, 2],
        script_template="Hello, this is a test call {name}!",
        created_at=now,
        updated_at=now,
        total_calls=0,
        successful_calls=0,
        failed_calls=0,
        pending_calls=0
    )

@pytest.fixture
def mock_twilio_client():
    class MockTwilio:
        def __init__(self):
            self.calls = Mock()
            self.calls.create = AsyncMock()
            self.calls.get = AsyncMock()

    return MockTwilio()

@pytest.fixture
def mock_supabase_client():
    class MockSupabase:
        def __init__(self):
            self.responses = []
            self.current_response = 0
            self.last_query = None
            self.last_table = None
            self.last_operation = None
            self.last_data = None
            self.is_single = False

        def set_responses(self, *responses):
            self.responses = []
            for response in responses:
                if isinstance(response, dict):
                    self.responses.append({"data": response, "error": None})
                elif isinstance(response, list):
                    self.responses.append({"data": response, "error": None})
                else:
                    self.responses.append(response)
            self.current_response = 0
            logger.debug(f"Configuradas {len(self.responses)} respuestas: {self.responses}")

        def from_(self, table):
            logger.debug(f"Llamado from_ con tabla: {table}")
            self.last_table = table
            self.last_operation = None
            self.last_data = None
            self.is_single = False
            return self

        def select(self, *args):
            logger.debug(f"Llamado select con args: {args}")
            self.last_operation = "select"
            return self

        def insert(self, data):
            logger.debug(f"Llamado insert con data: {data}")
            self.last_operation = "insert"
            self.last_data = data
            return self

        def update(self, data):
            logger.debug(f"Llamado update con data: {data}")
            self.last_operation = "update"
            self.last_data = data
            return self

        def eq(self, column, value):
            logger.debug(f"Llamado eq con column: {column}, value: {value}")
            if not hasattr(self, 'conditions'):
                self.conditions = []
            self.conditions.append((column, value))
            return self

        def single(self):
            logger.debug("Llamado single")
            self.is_single = True
            return self

        async def execute(self):
            logger.debug(f"Ejecutando con operación: {self.last_operation}, tabla: {self.last_table}")
            logger.debug(f"Estado actual - is_single: {self.is_single}, current_response: {self.current_response}")
            
            if not self.responses:
                logger.debug("No hay respuestas configuradas")
                return {"data": None, "error": None}

            response = self.responses[self.current_response].copy()
            logger.debug(f"Respuesta inicial: {response}")
            
            # Si es una operación de insert o update, actualizar los datos con los valores proporcionados
            if self.last_operation in ["insert", "update"] and self.last_data:
                logger.debug(f"Actualizando datos para {self.last_operation}")
                base_data = {}
                
                # Si hay una respuesta previa, usarla como base
                if response["data"]:
                    if isinstance(response["data"], list):
                        base_data = response["data"][0].copy()
                    else:
                        base_data = response["data"].copy()
                
                # Actualizar con los nuevos datos
                if isinstance(self.last_data, dict):
                    for key, value in self.last_data.items():
                        if isinstance(value, Enum):
                            base_data[key] = value.value
                        elif isinstance(value, datetime):
                            base_data[key] = value.isoformat()
                        else:
                            base_data[key] = value
                
                response = {"data": [base_data], "error": None}
                logger.debug(f"Datos actualizados: {response}")
            
            # Si es single(), devolver solo el primer elemento
            if self.is_single and response["data"] and isinstance(response["data"], list):
                logger.debug("Convirtiendo respuesta a single")
                response["data"] = response["data"][0]
                logger.debug(f"Respuesta convertida a single: {response}")

            # Incrementar el índice de respuesta
            self.current_response = (self.current_response + 1) % len(self.responses)
            logger.debug(f"Índice de respuesta actualizado a: {self.current_response}")
            
            logger.debug(f"Respuesta final: {response}")
            return response

    return MockSupabase()

class TestCallService:

    @pytest.mark.asyncio
    async def test_handle_webhooks(self, mock_twilio_client, mock_supabase_client, test_campaign):
        """
        Prueba el manejo de webhooks de Twilio.

        Verifica:
            - Actualización correcta del estado
            - Manejo de errores
            - Validaciones de campaña
            - Manejo adecuado de errores
        """
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Test webhook with completed status
        mock_twilio_client.calls.get.return_value = AsyncMock(
            status="completed",
            duration=120,
            recording_url="http://example.com/recording"
        )
        await call_service.handle_call_webhook("TEST_SID_12345")
        call = await call_service.get_call("TEST_SID_12345")
        assert call.status == CallStatus.COMPLETED
        assert call.duration == 120
        assert call.recording_url == "http://example.com/recording"

        # Test webhook with failed status
        mock_twilio_client.calls.get.return_value = AsyncMock(
            status="failed"
        )
        await call_service.handle_call_webhook("TEST_SID_12345")
        call = await call_service.get_call("TEST_SID_12345")
        assert call.status == CallStatus.FAILED

        # Test webhook with invalid status
        mock_twilio_client.calls.get.return_value = AsyncMock(
            status="invalid_status"
        )
        with pytest.raises(ValueError):
            await call_service.handle_call_webhook("TEST_SID_12345")

        # Test webhook with timeout
        mock_twilio_client.calls.get.side_effect = TimeoutError
        with pytest.raises(TimeoutError):
            await call_service.handle_call_webhook("TEST_SID_12345")

        # Test webhook with connection error
        mock_twilio_client.calls.get.side_effect = ConnectionError
        with pytest.raises(ConnectionError):
            await call_service.handle_call_webhook("TEST_SID_12345")

        # Test webhook with campaign inactive
        test_campaign.status = "inactive"
        with pytest.raises(ValueError):
            await call_service.handle_call_webhook("TEST_SID_12345")

    @pytest.mark.asyncio
    async def test_create_call(self, mock_twilio_client, mock_supabase_client, test_campaign):
        """
        Prueba la creación de llamadas.

        Verifica:
            - Creación exitosa
            - Validación de datos
            - Manejo de errores de Twilio
            - Actualización de estado
        """
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Crear datos de prueba
        call_data = CallCreate(
            campaign_id=test_campaign.id,
            phone_number="+1234567890",
            from_number="+0987654321",
            webhook_url="http://example.com/webhook",
            status_callback_url="http://example.com/callback"
        )

        # Crear llamada
        call = await call_service.create_call(call_data)

        # Verificar resultado
        assert call.twilio_sid == "TEST_SID_12345"
        assert call.status == CallStatus.INITIATED
        assert call.campaign_id == test_campaign.id

        # Verificar que se llamó a Twilio correctamente
        mock_twilio_client.calls.create.assert_called_once_with(
            to=call_data.phone_number,
            from_=call_data.from_number,
            url=call_data.webhook_url,
            status_callback=call_data.status_callback_url,
            status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
            timeout=30
        )

    @pytest.mark.asyncio
    async def test_get_call(self, mock_twilio_client, mock_supabase_client, test_campaign):
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Crear llamada
        call_data = CallCreate(
            campaign_id=test_campaign.id,
            phone_number="+1234567890",
            from_number="+0987654321",
            webhook_url="http://example.com/webhook",
            status_callback_url="http://example.com/callback"
        )
        call = await call_service.create_call(call_data)

        # Test getting an existing call
        retrieved_call = await call_service.get_call(call.id)
        assert retrieved_call is not None
        assert retrieved_call.id == call.id
        assert retrieved_call.campaign_id == test_campaign.id
        assert retrieved_call.phone_number == "+1234567890"

        # Test getting a non-existent call
        with pytest.raises(ValueError):
            await call_service.get_call(999)

        # Test that all required fields are present
        assert hasattr(retrieved_call, 'id')
        assert hasattr(retrieved_call, 'campaign_id')
        assert hasattr(retrieved_call, 'phone_number')
        assert hasattr(retrieved_call, 'status')
        assert hasattr(retrieved_call, 'created_at')
        assert hasattr(retrieved_call, 'updated_at')

    @pytest.mark.asyncio
    async def test_list_calls(self, mock_twilio_client, mock_supabase_client, test_campaign):
        """
        Escenarios a probar:
        1. Listado sin filtros
        2. Filtrado por campaign_id
        3. Filtrado por status
        4. Paginación
        5. Filtros combinados
        """
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Create test calls
        call_data1 = CallCreate(
            campaign_id=test_campaign.id,
            phone_number="+1234567890",
            from_number="+0987654321",
            webhook_url="http://example.com/webhook",
            status_callback_url="http://example.com/callback"
        )
        call1 = await call_service.create_call(call_data1)

        test_campaign2 = test_campaign.copy()
        test_campaign2.id = 2

        call_data2 = CallCreate(
            campaign_id=test_campaign2.id,
            phone_number="+0987654321",
            from_number="+1234567890",
            webhook_url="http://example.com/webhook",
            status_callback_url="http://example.com/callback"
        )
        call2 = await call_service.create_call(call_data2)

        call_data3 = CallCreate(
            campaign_id=test_campaign.id,
            phone_number="+1122334455",
            from_number="+0987654321",
            webhook_url="http://example.com/webhook",
            status_callback_url="http://example.com/callback"
        )
        call3 = await call_service.create_call(call_data3)

        # Test listing all calls
        calls = await call_service.list_calls()
        assert len(calls) == 3

        # Test filtering by campaign_id
        campaign_calls = await call_service.list_calls(campaign_id=test_campaign.id)
        assert len(campaign_calls) == 2

        # Test filtering by status
        await call_service.update_call_status(call1.id, status=CallStatus.COMPLETED)
        status_filtered_calls = await call_service.list_calls(status=CallStatus.COMPLETED)
        assert len(status_filtered_calls) == 1

        # Test pagination
        paginated_calls = await call_service.list_calls(skip=1, limit=1)
        assert len(paginated_calls) == 1

        # Test combined filters
        combined_filtered_calls = await call_service.list_calls(campaign_id=test_campaign.id, status=CallStatus.PENDING)
        assert len(combined_filtered_calls) == 1

    @pytest.mark.asyncio
    async def test_update_call_status(self, mock_twilio_client, mock_supabase_client, test_campaign):
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Create test call
        call_data = CallCreate(
            campaign_id=test_campaign.id,
            phone_number="+1234567890",
            from_number="+0987654321",
            webhook_url="http://example.com/webhook",
            status_callback_url="http://example.com/callback"
        )
        call = await call_service.create_call(call_data)

        # Test updating status successfully
        updated_call = await call_service.update_call_status(call.id, status=CallStatus.COMPLETED)
        assert updated_call.status == CallStatus.COMPLETED

        # Test updating with duration and recording URL
        updated_call = await call_service.update_call_status(
            call.id,
            status=CallStatus.COMPLETED,
            duration=120,
            recording_url="http://example.com/recording"
        )
        assert updated_call.duration == 120
        assert updated_call.recording_url == "http://example.com/recording"

        # Test invalid status
        with pytest.raises(ValueError):
            await call_service.update_call_status(call.id, status="invalid_status")

        # Test timestamp update
        initial_updated_at = updated_call.updated_at
        updated_call = await call_service.update_call_status(call.id, status=CallStatus.COMPLETED)
        assert updated_call.updated_at > initial_updated_at

    @pytest.mark.asyncio
    async def test_get_call_metrics(self, mock_twilio_client, mock_supabase_client, test_campaign):
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Create test calls
        call_data1 = CallCreate(
            campaign_id=test_campaign.id,
            phone_number="+1234567890",
            from_number="+0987654321",
            webhook_url="http://example.com/webhook",
            status_callback_url="http://example.com/callback"
        )
        call1 = await call_service.create_call(call_data1)

        test_campaign2 = test_campaign.copy()
        test_campaign2.id = 2

        call_data2 = CallCreate(
            campaign_id=test_campaign2.id,
            phone_number="+0987654321",
            from_number="+1234567890",
            webhook_url="http://example.com/webhook",
            status_callback_url="http://example.com/callback"
        )
        call2 = await call_service.create_call(call_data2)

        call_data3 = CallCreate(
            campaign_id=test_campaign.id,
            phone_number="+1122334455",
            from_number="+0987654321",
            webhook_url="http://example.com/webhook",
            status_callback_url="http://example.com/callback"
        )
        call3 = await call_service.create_call(call_data3)

        await call_service.update_call_status(call1.id, status=CallStatus.COMPLETED, duration=120)
        await call_service.update_call_status(call2.id, status=CallStatus.COMPLETED, duration=180)
        await call_service.update_call_status(call3.id, status=CallStatus.FAILED)

        # Test metrics without filters
        metrics = await call_service.get_call_metrics()
        assert metrics['total_calls'] == 3
        assert metrics['average_duration'] == 150
        assert metrics['status_counts'][CallStatus.COMPLETED] == 2
        assert metrics['status_counts'][CallStatus.FAILED] == 1

        # Test metrics filtered by campaign
        metrics = await call_service.get_call_metrics(campaign_id=test_campaign.id)
        assert metrics['total_calls'] == 2
        assert metrics['average_duration'] == 120
        assert metrics['status_counts'][CallStatus.COMPLETED] == 1
        assert metrics['status_counts'][CallStatus.FAILED] == 1

    @pytest.mark.asyncio
    async def test_get_call_metrics(self, mock_supabase_client):
        # Configurar múltiples llamadas con diferentes estados y duraciones
        calls_data = [
            {
                "id": 1,
                "campaign_id": 1,
                "status": CallStatus.COMPLETED.value,
                "duration": 120,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": 2,
                "campaign_id": 1,
                "status": CallStatus.FAILED.value,
                "duration": None,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": 3,
                "campaign_id": 2,
                "status": CallStatus.COMPLETED.value,
                "duration": 180,
                "created_at": datetime.now().isoformat()
            }
        ]

        # Configurar respuestas del mock
        mock_supabase_client.set_responses(calls_data)

        call_service = CallService(supabase_client=mock_supabase_client)

        # Obtener métricas globales
        metrics = await call_service.get_call_metrics()
        assert metrics['total_calls'] == 3
        assert metrics['average_duration'] == 150
        assert metrics['status_counts'][CallStatus.COMPLETED] == 2
        assert metrics['status_counts'][CallStatus.FAILED] == 1

        # Obtener métricas filtradas por campaña
        metrics_campaign_1 = await call_service.get_call_metrics(campaign_id=1)
        assert metrics_campaign_1['total_calls'] == 2
        assert metrics_campaign_1['status_counts'][CallStatus.COMPLETED] == 1
        assert metrics_campaign_1['status_counts'][CallStatus.FAILED] == 1

        metrics_campaign_2 = await call_service.get_call_metrics(campaign_id=2)
        assert metrics_campaign_2['total_calls'] == 1
        assert metrics_campaign_2['status_counts'][CallStatus.COMPLETED] == 1
        assert metrics_campaign_2['status_counts'][CallStatus.FAILED] == 0

    @pytest.mark.asyncio
    async def test_retry_mechanism(self, mock_twilio_client, mock_supabase_client):
        # Configurar una llamada que fallará y será reintentada
        call_data = {
            "id": 1,
            "campaign_id": 1,
            "status": CallStatus.FAILED.value,
            "retry_attempts": 1,
            "max_retries": 3
        }

        # Configurar respuestas del mock
        mock_supabase_client.set_responses(call_data)

        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Reintento exitoso después de fallo
        retried_call = await call_service.retry_call(call_data['id'])
        assert retried_call.retry_attempts == 2
        assert retried_call.status == CallStatus.PENDING

        # Límite máximo de reintentos alcanzado
        call_data['retry_attempts'] = 3
        mock_supabase_client.set_responses(call_data)
        with pytest.raises(ValueError):
            await call_service.retry_call(call_data['id'])

        # Actualización correcta del contador de reintentos
        call_data['retry_attempts'] = 1
        mock_supabase_client.set_responses(call_data)
        retried_call = await call_service.retry_call(call_data['id'])
        assert retried_call.retry_attempts == 2

        # Estado final después de reintento exitoso/fallido
        call_data['status'] = CallStatus.COMPLETED.value
        mock_supabase_client.set_responses(call_data)
        retried_call = await call_service.retry_call(call_data['id'])
        assert retried_call.status == CallStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_campaign_stats_update(self, mock_supabase_client):
        # Configurar campaña inicial
        campaign_data = {
            "id": 1,
            "total_calls": 10,
            "successful_calls": 5
        }

        # Configurar respuestas del mock
        mock_supabase_client.set_responses(campaign_data)

        call_service = CallService(supabase_client=mock_supabase_client)

        # Actualización después de llamada exitosa
        await call_service.update_campaign_stats(1, CallStatus.COMPLETED)
        updated_campaign = await call_service.get_campaign(1)
        assert updated_campaign.total_calls == 11
        assert updated_campaign.successful_calls == 6

        # Actualización después de llamada fallida
        await call_service.update_campaign_stats(1, CallStatus.FAILED)
        updated_campaign = await call_service.get_campaign(1)
        assert updated_campaign.total_calls == 12
        assert updated_campaign.successful_calls == 6

        # Manejo de estados intermedios
        await call_service.update_campaign_stats(1, CallStatus.IN_PROGRESS)
        updated_campaign = await call_service.get_campaign(1)
        assert updated_campaign.total_calls == 13
        assert updated_campaign.successful_calls == 6

        # Concurrencia en actualizaciones
        # Simular múltiples actualizaciones concurrentes
        await asyncio.gather(
            call_service.update_campaign_stats(1, CallStatus.COMPLETED),
            call_service.update_campaign_stats(1, CallStatus.FAILED),
            call_service.update_campaign_stats(1, CallStatus.IN_PROGRESS)
        )
        updated_campaign = await call_service.get_campaign(1)
        assert updated_campaign.total_calls == 16
        assert updated_campaign.successful_calls == 7

    @pytest.mark.asyncio
    async def test_complete_call_flow(self, mock_twilio_client, mock_supabase_client):
        """
        Prueba el flujo completo de una llamada desde su creación hasta su finalización.
        
        Flujo a probar:
        1. Crear llamada
        2. Simular inicio de llamada
        3. Simular respuesta
        4. Simular finalización
        5. Verificar métricas de campaña
        """
        logger.info("Iniciando prueba de flujo completo de llamada")
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)
        
        # Configurar datos de prueba
        campaign_data = {
            "id": 1,
            "name": "Test Campaign",
            "status": "active",
            "total_calls": 0,
            "successful_calls": 0
        }
        logger.debug(f"Datos de campaña configurados: {campaign_data}")
        
        base_call_data = {
            "id": 1,
            "campaign_id": 1,
            "phone_number": "+1234567890",
            "from_number": "+15005550006",
            "webhook_url": "http://example.com/webhook",
            "status_callback_url": "http://example.com/callback",
            "status": CallStatus.PENDING.value,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "twilio_sid": None,
            "duration": None,
            "recording_url": None,
            "error_message": None,
            "retry_attempts": 0,
            "max_retries": 3,
            "timeout": 30
        }
        logger.debug(f"Datos base de llamada configurados: {base_call_data}")
        
        # Configurar secuencia de respuestas para Supabase
        mock_supabase_client.set_responses(
            campaign_data,  # Para la validación de campaña
            base_call_data,  # Para la inserción inicial
            {**base_call_data, "status": CallStatus.INITIATED.value, "twilio_sid": "TEST_SID_12345"},  # Para la actualización con Twilio SID
            {**base_call_data, "status": CallStatus.INITIATED.value, "twilio_sid": "TEST_SID_12345"},  # Para get_call
            {**base_call_data, "status": CallStatus.COMPLETED.value, "twilio_sid": "TEST_SID_12345", "duration": 120, "recording_url": "http://example.com/recording.mp3"}  # Para la actualización final
        )
        
        # Configurar mock de Twilio
        mock_twilio_client.calls.create.return_value = MockTwilioCall(
            sid="TEST_SID_12345",
            status="initiated"
        )
        logger.debug("Mock de Twilio configurado")
        
        # Crear datos de la llamada
        call_data = CallCreate(
            campaign_id=1,
            phone_number="+1234567890",
            from_number="+15005550006",
            webhook_url="http://example.com/webhook",
            status_callback_url="http://example.com/callback",
            timeout=30
        )
        logger.debug(f"Datos de llamada creados: {call_data}")
        
        # Probar creación de llamada
        logger.info("Probando creación de llamada")
        call = await call_service.create_call(call_data)
        logger.debug(f"Llamada creada: {call}")
        assert call.status == CallStatus.INITIATED
        assert call.twilio_sid == "TEST_SID_12345"
        
        # Probar actualización de estado
        logger.info("Probando actualización de estado de llamada")
        updated_call = await call_service.update_call_status(
            call_id=call.id,
            status=CallStatus.COMPLETED,
            duration=120,
            recording_url="http://example.com/recording.mp3"
        )
        logger.debug(f"Llamada actualizada: {updated_call}")
        
        assert updated_call.status == CallStatus.COMPLETED
        assert updated_call.duration == 120
        assert updated_call.recording_url == "http://example.com/recording.mp3"

    @pytest.mark.asyncio
    async def test_retry_mechanism(self, mock_twilio_client, mock_supabase_client, test_campaign):
        """
        Verifica el sistema de reintentos automáticos

        Prueba:
            - Reintento después de fallo
            - Límite máximo de reintentos
            - Incremento correcto del contador
            - Respeto del límite máximo
        """
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Create test call
        call_data = CallCreate(
            campaign_id=test_campaign.id,
            phone_number="+1234567890",
            from_number="+0987654321",
            webhook_url="http://example.com/webhook",
            status_callback_url="http://example.com/callback"
        )
        call = await call_service.create_call(call_data)

        # Simulate call failure
        await call_service.update_call_status(call.id, status=CallStatus.FAILED)
        failed_call = await call_service.get_call(call.id)
        assert failed_call.status == CallStatus.FAILED
        assert failed_call.retry_attempts == 0

        # First retry
        retried_call = await call_service.retry_call(call.id)
        assert retried_call.retry_attempts == 1
        assert retried_call.status == CallStatus.PENDING

        # Second retry
        await call_service.update_call_status(retried_call.id, status=CallStatus.FAILED)
        retried_call = await call_service.retry_call(call.id)
        assert retried_call.retry_attempts == 2

        # Third retry (should succeed)
        await call_service.update_call_status(retried_call.id, status=CallStatus.FAILED)
        retried_call = await call_service.retry_call(call.id)
        await call_service.update_call_status(retried_call.id, status=CallStatus.COMPLETED)
        updated_call = await call_service.get_call(call.id)
        assert updated_call.status == CallStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_error_scenarios(self, mock_twilio_client, mock_supabase_client, test_campaign):
        """
        Valida el manejo de errores del servicio

        Prueba:
            1. Reintento en llamada completada
            2. Actualización con campaña inactiva
            3. Estados inválidos de Twilio
        """
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Create test call
        call_data = CallCreate(
            campaign_id=test_campaign.id,
            phone_number="+1234567890",
            from_number="+0987654321",
            webhook_url="http://example.com/webhook",
            status_callback_url="http://example.com/callback"
        )
        call = await call_service.create_call(call_data)

        # 1. Reintento en llamada completada
        await call_service.update_call_status(call.id, status=CallStatus.COMPLETED)
        with pytest.raises(ValueError):
            await call_service.retry_call(call.id)

        # 2. Actualización con campaña inactiva
        test_campaign.status = "inactive"
        with pytest.raises(ValueError):
            await call_service.update_call_status(call.id, status=CallStatus.COMPLETED)

        # 3. Estados inválidos de Twilio
        with pytest.raises(ValueError):
            await call_service.update_call_status(call.id, status="invalid_status")

    @pytest.mark.asyncio
    async def test_handle_webhook_error(self, mock_twilio_client, mock_supabase_client):
        """Test handling Twilio webhook errors"""
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Mock Twilio error
        mock_twilio_client.calls.get = AsyncMock(side_effect=Exception("Twilio API error"))

        with pytest.raises(HTTPException) as exc_info:
            await call_service.handle_call_webhook("TEST_SID_12345")

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error al obtener estado de llamada en Twilio" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_handle_webhook_not_found(self, mock_twilio_client, mock_supabase_client):
        """Test handling webhook for non-existent call"""
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Mock no data returned from Supabase
        mock_supabase_client.chain.data = {"data": []}

        with pytest.raises(HTTPException) as exc_info:
            await call_service.handle_call_webhook("NONEXISTENT_SID")

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Llamada no encontrada" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_update_call_status(self, mock_twilio_client, mock_supabase_client, test_campaign):
        """Prueba la actualización de estados de llamada"""
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Caso 1: Actualización exitosa
        call_update = CallUpdate(
            status=CallStatus.COMPLETED,
            duration=120,
            recording_url="http://example.com/recording.mp3"
        )

        updated_call = await call_service.update_call_status("TEST_SID_12345", call_update)
        assert updated_call.status == CallStatus.COMPLETED
        assert updated_call.duration == 120

        # Caso 2: Estado inválido
        with pytest.raises(HTTPException) as exc_info:
            invalid_update = CallUpdate(status="INVALID_STATUS")
            await call_service.update_call_status("TEST_SID_12345", invalid_update)
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST

        # Caso 3: Llamada no encontrada
        with pytest.raises(HTTPException) as exc_info:
            await call_service.update_call_status("NONEXISTENT_SID", call_update)
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_get_call_metrics(self, mock_twilio_client, mock_supabase_client, test_campaign):
        """Prueba la obtención de métricas de llamadas"""
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Preparar datos de prueba con diferentes estados
        test_calls = [
            {"status": CallStatus.COMPLETED, "duration": 120},
            {"status": CallStatus.FAILED, "duration": 0},
            {"status": CallStatus.NO_ANSWER, "duration": 30},
            {"status": CallStatus.COMPLETED, "duration": 180}
        ]

        # Configurar mock_supabase_client para retornar los datos de prueba
        mock_supabase_client.table().select().execute.return_value = {
            "data": test_calls
        }

        # Obtener métricas
        metrics = await call_service.get_call_metrics()

        # Validar métricas
        assert metrics.total_calls == 4
        assert metrics.successful_calls == 2
        assert metrics.failed_calls == 1
        assert metrics.no_answer_calls == 1
        assert metrics.average_duration == 150  # (120 + 180) / 2

    @pytest.mark.asyncio
    async def test_campaign_validation(self, mock_twilio_client, mock_supabase_client, test_campaign):
        """Prueba la validación de campaña al crear llamadas"""
        call_service = CallService(twilio_client=mock_twilio_client, supabase_client=mock_supabase_client)

        # Caso 1: Campaña activa
        test_campaign.status = "active"
        mock_supabase_client.table().select().eq().single().execute.return_value = {
            "data": test_campaign.dict()
        }

        call_data = CallCreate(
            campaign_id=test_campaign.id,
            phone_number="+1234567890"
        )
        call = await call_service.create_call(call_data)
        assert call.campaign_id == test_campaign.id

        # Caso 2: Campaña inactiva
        test_campaign.status = "inactive"
        with pytest.raises(HTTPException) as exc_info:
            await call_service.create_call(call_data)
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST