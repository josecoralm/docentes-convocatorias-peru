import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any
from datetime import datetime
from scrapers.base_scraper import BaseScraper

class ConvocatoriasTrabajoScraper(BaseScraper):
    def __init__(self):
        super().__init__("ConvocatoriasDeTrabajoPeru")
        self.base_url = "https://www.convocatoriasdetrabajo.com"
        self.search_url = f"{self.base_url}/buscar-empleo.php?palabra=docente+universitario"

    def run(self) -> List[Dict[str, Any]]:
        results = []
        try:
            resp = requests.get(self.search_url, headers=self.headers, timeout=12)
            if resp.status_code != 200:
                print(f"[{self.name}] Error status code {resp.status_code}")
                return results

            soup = BeautifulSoup(resp.text, "html.parser")
            # Buscar elementos de avisos / convocatorias
            articles = soup.find_all("article") or soup.find_all("div", class_=re.compile("convocatoria|item|post", re.I))

            for idx, art in enumerate(articles[:15]):
                title_elem = art.find(["h2", "h3", "h4", "a"])
                if not title_elem:
                    continue
                titulo = title_elem.get_text(strip=True)
                if not ("docente" in titulo.lower() or "profesor" in titulo.lower() or "universidad" in titulo.lower()):
                    continue

                link_elem = art.find("a", href=True)
                link = link_elem["href"] if link_elem else self.search_url
                if link.startswith("/"):
                    link = f"{self.base_url}{link}"

                snippet = art.get_text(" ", strip=True)

                # Detección de institución
                institucion = "Universidad Pública (Vía Convocatorias Perú)"
                for uni in ["San Marcos", "UNMSM", "UNI", "Villarreal", "UNFV", "Agraria", "UNALM", "Callao", "UNAC", "Faustino Sánchez Carrión", "San Agustín"]:
                    if uni.lower() in snippet.lower():
                        institucion = f"Universidad Nacional ({uni})"
                        break

                nivel = "Posgrado" if "posgrado" in snippet.lower() or "maestría" in snippet.lower() else "Pregrado"
                tipo_institucion = "Pública"

                conv_id = f"ctp-{abs(hash(titulo + link)) % 100000}"

                results.append({
                    "id": conv_id,
                    "titulo": titulo,
                    "institucion": institucion,
                    "tipo_institucion": tipo_institucion,
                    "nivel": nivel,
                    "modalidad": "Presencial" if "presencial" in snippet.lower() else "Presencial / Semipresencial",
                    "ubicacion": "Lima / Regiones",
                    "facultad_o_carrera": "Facultades Diversas",
                    "tipo_contrato": "Concurso Público de Méritos",
                    "remuneracion": "Según escala del Estado Peruano / Ley Universitaria",
                    "requisitos": [
                        "Grado de Maestro o Doctor registrado en SUNEDU",
                        "Cumplir requisitos de Ley N° 30220",
                        "Presentación de expediente foliado"
                    ],
                    "fecha_publicacion": datetime.now().strftime("%Y-%m-%d"),
                    "fecha_limite": "Revisar bases en enlace oficial",
                    "enlace_postulacion": link,
                    "fuente": "Convocatorias de Trabajo Perú / SERVIR",
                    "estado": "Abierta",
                    "descripcion": snippet[:280] + "...",
                    "contacto": "Mesa de partes virtual de la institución convocante",
                    "tags": ["Concurso Público", "Pública", "SUNEDU", "Docente"]
                })
        except Exception as e:
            print(f"[{self.name}] Exception during scraping: {e}")

        return results
