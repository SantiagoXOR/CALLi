import sys
from typing import Any

from app.config.settings import get_settings


def validate_settings() -> dict[str, Any]:
    settings = get_settings()
    validation_results = {}

    # Validar Database
    try:
        assert settings.DATABASE_URL.startswith("postgresql://")
        validation_results["database"] = "OK"
    except Exception as e:
        validation_results["database"] = f"ERROR: {e!s}"

    # Validar Supabase
    try:
        assert settings.SUPABASE_URL.startswith("https://")
        assert len(settings.SUPABASE_KEY) > 50
        validation_results["supabase"] = "OK"
    except Exception as e:
        validation_results["supabase"] = f"ERROR: {e!s}"

    # Validar Twilio
    try:
        assert settings.TWILIO_ACCOUNT_SID.startswith("AC")
        assert len(settings.TWILIO_AUTH_TOKEN) > 0
        validation_results["twilio"] = "OK"
    except Exception as e:
        validation_results["twilio"] = f"ERROR: {e!s}"

    return validation_results


if __name__ == "__main__":
    results = validate_settings()
    all_ok = all(result == "OK" for result in results.values())

    for service, status in results.items():
        print(f"{service}: {status}")

    sys.exit(0 if all_ok else 1)
