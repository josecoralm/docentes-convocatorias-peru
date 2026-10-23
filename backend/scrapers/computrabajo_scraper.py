import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any
from datetime import datetime
from scrapers.base_scraper import BaseScraper

class ComputrabajoScraper(BaseScraper):
    def __init__(self):
        super().__init__("ComputrabajoPeru")
        self.base_url = "https://pe.computrabajo.com"
        self.search_url = f"{self.base_url}/trabajo-de-docente-universitario"

    def run(self) -> List[Dict[str, Any]]:
        results = []
        try:
            resp = requests.get(self.search_url, headers=self.headers, timeout=12)
            if resp.status_code != 200:
                print(f"[{self.name}] Error status code {resp.status_code}")
                return results

            soup = BeautifulSoup(resp.text, "html.parser")
            box_offers = soup.find_all("article", class_=re.compile("box_offer", re.I))

            keywords_academicos = ["docente", "profesor", "cátedra", "universitario", "catedrático", "investigador", "maestría", "posgrado"]
            invalid_keywords = ["ventas", "comercial", "cajero", "seguridad", "limpieza", "recepcionista"]

            for offer in box_offers[:25]:
                h2 = offer.find("h2") or offer.find("h1")
                if not h2:
                    continue

                a_tag = h2.find("a", href=True)
                if not a_tag:
                    continue

                raw_title = a_tag.get_text(strip=True)
                # Limpiar badges como 'Postulado', 'Vista', etc.
                titulo = re.sub(r'(Postulado|Vista|Nuevo)$', '', raw_title, flags=re.IGNORECASE).strip()

                title_lower = titulo.lower()
                if not any(k in title_lower for k in keywords_academicos):
                    continue
                if any(inv in title_lower for inv in invalid_keywords):
                    continue

                raw_link = a_tag["href"]
                # Limpiar fragmentos #lc=... para que la URL sea directa y limpia
                clean_link = raw_link.split("#")[0]
                if clean_link.startswith("/"):
                    clean_link = f"{self.base_url}{clean_link}"

                # Extracción y limpieza del nombre de la institución / empresa
                p_company = offer.find("p", class_=re.compile("fc_base", re.I))
                if p_company:
                    comp_text = p_company.get_text(" ", strip=True)
                    # Quitar puntajes numéricos como '4,6'
                    comp_text = re.sub(r'^\d+[.,]\d+\s*', '', comp_text).strip()
                    company = comp_text if comp_text and len(comp_text) > 2 else "Universidad / Institución Educativa"
                else:
                    company = "Universidad / Institución Educativa"

                # Ubicación
                loc_span = offer.find("span", class_=re.compile("fc_aux", re.I))
                ubicacion = loc_span.get_text(strip=True) if loc_span else "Lima, Perú"

                # Descripción
                p_desc = offer.find("p", class_=re.compile("fs13|text_default", re.I)) or offer.find("p")
                desc = p_desc.get_text(" ", strip=True) if p_desc else f"Convocatoria docente activa en Computrabajo para {titulo} en {company}."

                nivel = "Posgrado" if ("posgrado" in title_lower or "maestría" in title_lower) else "Pregrado"
                modalidad = "100% Virtual / Remoto" if ("remoto" in desc.lower() or "virtual" in desc.lower()) else "Presencial"

                conv_id = f"ct-{abs(hash(clean_link)) % 100000}"

                results.append({
                    "id": conv_id,
                    "titulo": titulo,
                    "institucion": company,
                    "tipo_institucion": "Privada",
                    "nivel": nivel,
                    "modalidad": modalidad,
                    "ubicacion": ubicacion,
                    "facultad_o_carrera": "Facultad Universitaria / Departamento Académico",
                    "tipo_contrato": "Tiempo Parcial / Tiempo Completo",
                    "remuneracion": "Acorde al tarifario docente de la institución",
                    "requisitos": [
                        "Grado de Maestro registrado ante SUNEDU (Obligatorio)",
                        "Experiencia mínima en docencia universitaria o ejercicio profesional",
                        "Disponibilidad para el periodo académico"
                    ],
                    "fecha_publicacion": datetime.now().strftime("%Y-%m-%d"),
                    "fecha_limite": "Hasta cubrir vacantes (Aviso activo)",
                    "enlace_postulacion": clean_link,
                    "fuente": "Computrabajo Perú",
                    "estado": "Abierta",
                    "descripcion": desc,
                    "contacto": "Postulación directa a través de Computrabajo",
                    "tags": ["Computrabajo", "Convocatoria Activa", "SUNEDU", company]
                })
        except Exception as e:
            print(f"[{self.name}] Exception: {e}")

        return results
