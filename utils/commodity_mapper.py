"""
Commodity mapper utility for detecting and mapping commodities to their symbols.
"""

COMMODITY_MAP = {
    "gold": {
        "symbols": ["GLD", "IAU", "GC=F"],
        "aliases": ["gold", "au", "precious metal", "yellow metal", "bullion"],
        "display_name": "Gold",
        "unit": "USD/oz",
        "news_query": "gold commodity prices"
    },
    "silver": {
        "symbols": ["SLV", "SI=F"],
        "aliases": ["silver", "ag", "white metal"],
        "display_name": "Silver",
        "unit": "USD/oz",
        "news_query": "silver commodity prices"
    },
    "crude oil": {
        "symbols": ["USO", "CL=F", "BZ=F"],
        "aliases": ["crude oil", "oil", "wti", "petroleum", "crude", "brent"],
        "display_name": "Crude Oil",
        "unit": "USD/barrel",
        "news_query": "crude oil prices market"
    },
    "natural gas": {
        "symbols": ["NG=F"],
        "aliases": ["natural gas", "gas", "ng", "methane"],
        "display_name": "Natural Gas",
        "unit": "USD/MMBtu",
        "news_query": "natural gas prices"
    },
    "copper": {
        "symbols": ["HG=F"],
        "aliases": ["copper", "cu", "red metal"],
        "display_name": "Copper",
        "unit": "USD/lb",
        "news_query": "copper commodity prices"
    },
    "wheat": {
        "symbols": ["ZW=F"],
        "aliases": ["wheat", "grain"],
        "display_name": "Wheat",
        "unit": "USD/bu",
        "news_query": "wheat prices commodity"
    },
    "corn": {
        "symbols": ["ZC=F"],
        "aliases": ["corn", "maize"],
        "display_name": "Corn",
        "unit": "USD/bu",
        "news_query": "corn prices commodity"
    },
    "soybeans": {
        "symbols": ["ZS=F"],
        "aliases": ["soybeans", "soy", "soybean"],
        "display_name": "Soybeans",
        "unit": "USD/bu",
        "news_query": "soybeans prices commodity"
    }
}


def detect_commodity(query):
    """
    Detect commodity from user query.
    
    Args:
        query (str): User query text
        
    Returns:
        dict: Commodity info or None if not detected
    """
    query_lower = query.lower()
    
    for commodity_key, commodity_data in COMMODITY_MAP.items():
        for alias in commodity_data.get("aliases", []):
            if alias.lower() in query_lower:
                return {
                    "key": commodity_key,
                    "symbols": commodity_data["symbols"],
                    "display_name": commodity_data["display_name"],
                    "unit": commodity_data["unit"],
                    "news_query": commodity_data["news_query"]
                }
    
    return None


def get_all_commodities():
    """Get list of all supported commodities."""
    return [data["display_name"] for data in COMMODITY_MAP.values()]


def get_symbols(commodity_key):
    """Get symbols for a commodity."""
    if commodity_key in COMMODITY_MAP:
        return COMMODITY_MAP[commodity_key]["symbols"]
    return []


def get_display_name(commodity_key):
    """Get display name for commodity."""
    if commodity_key in COMMODITY_MAP:
        return COMMODITY_MAP[commodity_key]["display_name"]
    return commodity_key.title()


def get_unit(commodity_key):
    """Get unit of measurement for commodity."""
    if commodity_key in COMMODITY_MAP:
        return COMMODITY_MAP[commodity_key]["unit"]
    return "USD"