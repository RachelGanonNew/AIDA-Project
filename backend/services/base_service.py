"""
Base service class implementing SOLID principles and dependency injection
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class BaseService(ABC):
    """
    Base service class implementing SOLID principles:
    - Single Responsibility: Each service has one reason to change
    - Open/Closed: Open for extension, closed for modification
    - Liskov Substitution: Derived classes can be substituted for base class
    - Interface Segregation: Clients depend only on methods they use
    - Dependency Inversion: High-level modules don't depend on low-level modules
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._validate_config()
    
    @abstractmethod
    def _validate_config(self) -> None:
        """Validate service configuration"""
        pass
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize service resources"""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup service resources"""
        pass
    
    @asynccontextmanager
    async def service_context(self):
        """Context manager for service lifecycle"""
        try:
            await self.initialize()
            yield self
        finally:
            await self.cleanup()
    
    def log_operation(self, operation: str, **kwargs) -> None:
        """Log service operations for monitoring"""
        logger.info(f"{self.__class__.__name__}: {operation}", extra=kwargs)
    
    def log_error(self, error: Exception, operation: str, **kwargs) -> None:
        """Log service errors"""
        logger.error(
            f"{self.__class__.__name__}: Error in {operation}: {str(error)}", 
            extra=kwargs
        )

class ServiceRegistry:
    """
    Service registry for dependency injection
    """
    def __init__(self):
        self._services: Dict[str, Any] = {}
    
    def register(self, name: str, service: Any) -> None:
        """Register a service"""
        self._services[name] = service
    
    def get(self, name: str) -> Any:
        """Get a registered service"""
        if name not in self._services:
            raise KeyError(f"Service '{name}' not found in registry")
        return self._services[name]
    
    def get_all(self) -> Dict[str, Any]:
        """Get all registered services"""
        return self._services.copy()

# Global service registry
service_registry = ServiceRegistry() 