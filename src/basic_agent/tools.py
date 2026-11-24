def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b

def get_weather(city: str) -> str:
    """Return a mock current weather string for a city."""
    data = {"paris": "sunny, 22°C", "london": "rainy, 14°C"}
    return data.get(city.lower(), "unknown city")
