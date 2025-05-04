from app.config.settings import get_settings

"""
Módulo de pruebas para la configuración de la aplicación.

Este módulo contiene pruebas unitarias que verifican que la configuración
de la aplicación se cargue correctamente desde las variables de entorno.
Las pruebas aseguran que los valores de configuración críticos estén disponibles
y tengan los valores esperados durante la ejecución de pruebas.
"""


def test_settings_loaded():
    """
    Verifica que la configuración básica de la aplicación se cargue correctamente.

    Esta prueba asegura que los parámetros fundamentales de la aplicación como
    el nombre, el entorno y el modo de depuración tengan los valores esperados
    durante la ejecución de pruebas.
    """
    settings = get_settings()
    assert settings.APP_NAME == "test_app_name"
    assert settings.ENVIRONMENT == "testing"
    assert settings.DEBUG is True


def test_database_config():
    """
    Verifica que la configuración de la base de datos se cargue correctamente.

    Esta prueba asegura que la URL de conexión a la base de datos tenga el valor
    esperado durante la ejecución de pruebas, lo que es esencial para garantizar
    que la aplicación pueda conectarse a la base de datos de prueba.
    """
    settings = get_settings()
    assert settings.DATABASE_URL == "test_database_url"


def test_supabase_config():
    """
    Verifica que la configuración de Supabase se cargue correctamente.

    Esta prueba asegura que los parámetros de conexión a Supabase (URL, clave de API
    y clave de servicio) tengan los valores esperados durante la ejecución de pruebas.
    Estos parámetros son esenciales para la autenticación y el acceso a los servicios
    de Supabase durante las pruebas.
    """
    settings = get_settings()
    assert settings.SUPABASE_URL == "test_supabase_url"
    assert settings.SUPABASE_KEY == "test_supabase_key"
    assert settings.SUPABASE_SERVICE_KEY == "test_supabase_service_key"


def test_twilio_config():
    """
    Verifica que la configuración de Twilio se cargue correctamente.

    Esta prueba asegura que los parámetros de conexión a Twilio (SID de cuenta,
    token de autenticación y número de teléfono) tengan los valores esperados
    durante la ejecución de pruebas. Estos parámetros son esenciales para la
    autenticación y el uso de los servicios de telefonía de Twilio durante las pruebas.
    """
    settings = get_settings()
    assert settings.TWILIO_ACCOUNT_SID == "test_twilio_account_sid"
    assert settings.TWILIO_AUTH_TOKEN == "test_twilio_auth_token"
    assert settings.TWILIO_PHONE_NUMBER == "test_twilio_phone_number"
