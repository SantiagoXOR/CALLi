from setuptools import find_packages, setup

setup(
    name="call-automation",
    version="0.1",
    packages=find_packages(),
    package_data={"": ["*.py"]},
    include_package_data=True,
    install_requires=[
        "fastapi>=0.89.1",  # Use >= for flexibility or pin specific versions
        "uvicorn[standard]>=0.20.0",  # Include standard extras for performance
        "python-dotenv>=1.0.0",
        "pydantic>=2.0",  # Assuming migration to Pydantic v2 based on warnings
        "pydantic-settings>=2.0",  # For settings management in Pydantic v2
        "python-decouple>=3.8",
        "supabase>=1.0.3",
        "twilio>=8.10.0",
        "passlib[bcrypt]>=1.7.4",  # Include bcrypt extra
        "httpx>=0.23.3",
        "elevenlabs>=0.2.27",  # Pin or use a recent version
        "langchain>=0.0.300",  # Example, adjust based on actual usage
        "openai>=0.28.0",  # Example, adjust based on actual usage
        "redis>=4.0.0",  # Example, adjust based on actual usage
        "prometheus-client>=0.14.0",  # For metrics
        "tenacity>=8.0.0",  # For retry logic
        "hvac>=1.0.0",  # For Vault integration
        "anyio>=4.0.0",  # Required by pytest-asyncio
        # Add testing dependencies if needed, or manage via requirements-dev.txt
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
        "pytest-cov>=4.0.0",
        "pytest-mock>=3.0.0",
        "librosa>=0.9.0",  # For audio quality analysis in CallService (if used outside tests)
        "numpy>=1.21.0",  # Dependency for librosa
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.0.0",
            "pre-commit>=2.15.0",
            "ruff>=0.1.0",  # Example linter/formatter
        ]
    },
    python_requires=">=3.10",  # Update based on project requirements
)
