"""
Base Models to enforce the following return schema from the scrapers:
{
        "general": {
            "team_map": [],
            "element_map": [],
            "gw_deadlines": [],
        },
        "player": {"player": []},
        "gameweek": {"gameweek": []}},
        "fixture": {"fixture": []},
    }
"""

from typing import Dict, List

from pydantic import BaseModel


class ScraperSubType(BaseModel):
    scraper_sub_type: str
    scraper_return_data: List[dict] = []


class ScraperType(BaseModel):
    scraper_type: str
    scraper_sub_types: Dict[str, ScraperSubType] = {}
