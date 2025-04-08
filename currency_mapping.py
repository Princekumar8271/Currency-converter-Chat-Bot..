# Dictionary mapping countries to their currency codes
COUNTRY_TO_CURRENCY = {
    # North America
    'united states': 'USD',
    'canada': 'CAD',
    'mexico': 'MXN',
    
    # Europe
    'european union': 'EUR',
    'united kingdom': 'GBP',
    'switzerland': 'CHF',
    
    # Asia
    'india': 'INR',
    'china': 'CNY',
    'japan': 'JPY',
    'south korea': 'KRW',
    'singapore': 'SGD',
    'malaysia': 'MYR',
    'indonesia': 'IDR',
    'thailand': 'THB',
    'philippines': 'PHP',
    'vietnam': 'VND',
    
    # Oceania
    'australia': 'AUD',
    'new zealand': 'NZD',
    
    # Common currency names
    'dollar': 'USD',
    'euro': 'EUR',
    'pound': 'GBP',
    'yen': 'JPY',
    'rupee': 'INR',
    'yuan': 'CNY'
}

def get_currency_code(country_name):
    """Convert country name to currency code."""
    country_name = country_name.lower().strip()
    return COUNTRY_TO_CURRENCY.get(country_name)

def get_supported_countries():
    """Return list of supported countries and currencies."""
    return [f"{country.title()}: {currency}" for country, currency in COUNTRY_TO_CURRENCY.items()]