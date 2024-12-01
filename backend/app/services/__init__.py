import importlib
import inspect
import pkgutil
from collections.abc import Callable
from typing import Union

from celery import Celery

from app.api.deps import get_db

from .exchange_rate_service import ExchangeRateService

# Base path for service discovery
SERVICES_PACKAGE = "app.services"

# Type alias for the services registry
ServiceType = Union[object, Callable[[], object]]

# Initialize the services registry
services_registry: dict[str, ServiceType] = {}

# Define lightweight and heavyweight services
LIGHTWEIGHT_SERVICES = {"EmailService", "ExchangeRateService"}  # Auto-initialized
HEAVYWEIGHT_SERVICES = {"PaymentService", "AnalyticsService"}  # Lazy-loaded

# Discovery and Registration
def discover_and_register_services():
    """
    Dynamically discovers all modules in the services directory and registers classes
    into the `services_registry` based on lightweight or heavyweight categorization.
    """
    for _, module_name, _ in pkgutil.iter_modules([SERVICES_PACKAGE.replace(".", "/")]):
        full_module_name = f"{SERVICES_PACKAGE}.{module_name}"
        module = importlib.import_module(full_module_name)

        # Inspect module to find classes
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Only register classes from the current module
            if obj.__module__ == full_module_name:
                # Normalize the service name (e.g., "email" for "EmailService")
                service_key = name.lower().replace("service", "")

                # Categorize into lightweight or heavyweight
                if name in LIGHTWEIGHT_SERVICES:
                    # Directly instantiate lightweight services
                    services_registry[service_key] = obj()
                elif name in HEAVYWEIGHT_SERVICES:
                    # Register heavyweight services as lazy-initialized lambdas
                    services_registry[service_key] = lambda cls=obj: cls()

            if name == "ExchangeRateService":
                db_session = get_db()  # Import from your dependency module
                celery_app = Celery("tasks", broker="redis://redis:6379/0")
                services_registry[name.lower().replace("service", "")] = ExchangeRateService(db_session=db_session, celery_app=celery_app)

# Run service discovery at import time
discover_and_register_services()

# Helper function for retrieving services
def get_service(service_name: str):
    """
    Retrieves a service from the registry.
    If the service is registered as a lambda (lazy-loaded), it will be instantiated and cached.
    """
    service = services_registry.get(service_name)
    if callable(service):  # If the service is lazily initialized
        service = service()  # Instantiate the service
        services_registry[service_name] = service  # Cache the instance
    return service
