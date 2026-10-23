from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests

class BaseScraper(ABC):
    def __init__(self, name: str):
        self.name = name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept-Language": "es-419,es;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

    @abstractmethod
    def run(self) -> List[Dict[str, Any]]:
        """Ejecuta el scraper y retorna una lista de diccionarios de convocatorias normalizadas."""
        pass
