from typing import List, Dict, Any
from scrapers.convocatorias_trabajo_scraper import ConvocatoriasTrabajoScraper
from scrapers.computrabajo_scraper import ComputrabajoScraper
from database import load_convocatorias, save_convocatorias

class CrawlerManager:
    def __init__(self):
        self.scrapers = [
            ConvocatoriasTrabajoScraper(),
            ComputrabajoScraper(),
        ]

    def run_all(self) -> Dict[str, Any]:
        existing_items = load_convocatorias()
        existing_ids = {c["id"] for c in existing_items}
        existing_titles = {c["titulo"].lower().strip() for c in existing_items}

        total_scraped = 0
        new_items = 0
        scraper_reports = {}

        for scraper in self.scrapers:
            try:
                results = scraper.run()
                scraper_reports[scraper.name] = len(results)
                total_scraped += len(results)

                for item in results:
                    # Deduplicación por id o título idéntico
                    if item["id"] not in existing_ids and item["titulo"].lower().strip() not in existing_titles:
                        existing_items.insert(0, item)
                        existing_ids.add(item["id"])
                        existing_titles.add(item["titulo"].lower().strip())
                        new_items += 1
            except Exception as e:
                scraper_reports[scraper.name] = f"Error: {e}"

        save_convocatorias(existing_items)

        return {
            "status": "success",
            "total_scraped": total_scraped,
            "new_items_added": new_items,
            "reports": scraper_reports,
            "total_in_database": len(existing_items)
        }
