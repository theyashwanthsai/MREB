from datetime import datetime
from typing import Optional
import random
from datetime import datetime


def multiply(a: int, b: int) -> int:
    """
    Multiply two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The product of a and b.
    """
    return a * b

def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculate the discounted price.

    Args:
        price: Original price.
        discount_percent: Discount percentage.

    Returns:
        Discounted price.
    """
    return price * (1 - discount_percent / 100)

def is_even(number: int) -> bool:
    """
    Check if a number is even.

    Args:
        number: Integer to check.

    Returns:
        True if even, False otherwise.
    """
    return number % 2 == 0
    
def get_user_profile(user_id: int, database: dict[int, dict]) -> dict:
    """
    Fetch a user's profile from a mock database.

    Args:
        user_id: ID of the user.
        database: Dictionary mapping user IDs to user profiles.

    Returns:
        The user's profile dictionary if found, else empty dict.
    """
    return database.get(user_id, {})

def calculate_tax(amount: float, tax_rate: float, include_tax: bool = False) -> float:
    """
    Calculate the tax for a given amount.

    Args:
        amount: Base amount.
        tax_rate: Tax percentage.
        include_tax: Whether to include the tax in the result.

    Returns:
        Final amount or tax amount.
    """
    tax = amount * (tax_rate / 100)
    return amount + tax if include_tax else tax

def analyze_text_stats(text: str) -> dict:
    """
    Analyze text and return word and character statistics.

    Args:
        text: Input text.

    Returns:
        Dictionary with 'word_count', 'char_count', and 'unique_words'.
    """
    words = text.split()
    return {
        "word_count": len(words),
        "char_count": len(text),
        "unique_words": len(set(words))
    }

def compute_statistics(data: list[float]) -> dict:
    """
    Compute mean, median, and variance of a list of numbers.

    Args:
        data: List of floating-point numbers.

    Returns:
        Dictionary with mean, median, and variance.
    """
    if not data:
        return {"mean": 0, "median": 0, "variance": 0}
    n = len(data)
    mean = sum(data) / n
    sorted_data = sorted(data)
    median = sorted_data[n // 2] if n % 2 else (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
    variance = sum((x - mean) ** 2 for x in data) / n
    return {"mean": mean, "median": median, "variance": variance}

MOCK_NEWS = {
    "technology": [
        "AI Revolution: New Models Surpass Human-Level Coding",
        "Quantum Computing Breakthrough Changes Encryption Forever",
        "Elon Musk Announces Neuralink for Memory Enhancement",
        "India Becomes Global Hub for Semiconductor Manufacturing",
        "New Robot Chef Can Cook 100 Dishes Automatically",
        "Meta Develops Brain-to-Text Interface",
        "New AI Ethics Guidelines Released Worldwide"
    ],
    "sports": [
        "India Wins Cricket World Cup 2025 Final",
        "Messi Announces Retirement After Legendary Career",
        "Olympic Games 2028 to Include eSports as Official Event",
        "Serena Williams Launches Tennis Academy for Girls",
        "F1: Ferrari Dominates the Season with Record Wins",
        "NBA Finals End in Nail-Biting Game 7",
        "New Soccer Stadium Opens in Tokyo"
    ],
    "politics": [
        "Global Climate Summit Reaches Landmark Agreement",
        "New Tax Policy Aims to Boost Startups",
        "Election 2025 Results Announced Amid Tight Contest",
        "UN Approves Resolution on Digital Privacy Rights",
        "Trade Talks Between India and EU Conclude Successfully",
        "Senate Passes New Education Bill",
        "National Security Policy Updated for Cyber Threats"
    ]
}

def get_news_headlines(topic: str, count: int = 5) -> list[str]:
    """Return rich mock news headlines for a topic."""
    topic = topic.lower()
    headlines = MOCK_NEWS.get(topic)
    if not headlines:
        return [f"No news available for topic: {topic}"]
    random.shuffle(headlines)
    return headlines[:count]

MOCK_WEATHER = {
    "Delhi": ["Sunny, 30°C", "Cloudy, 32°C", "Rainy, 28°C"],
    "London": ["Rainy, 12°C", "Cloudy, 14°C", "Sunny, 15°C"],
    "New York": ["Cloudy, 20°C", "Sunny, 22°C", "Rainy, 18°C"],
    "Tokyo": ["Humid, 27°C", "Rainy, 25°C", "Sunny, 29°C"]
}

def get_weather(city: str) -> str:
    """Return mock weather for a city."""
    city = city.title()
    return random.choice(MOCK_WEATHER.get(city, ["Weather data not available"]))

def get_weather_forecast(city: str, days: int = 3) -> dict:
    """Return mock weather forecast for given city."""
    forecasts = MOCK_WEATHER.get(city.title(), ["Clear"] * days)
    return {f"Day {i+1}": forecasts[i % len(forecasts)] for i in range(days)}

MOCK_STOCKS = {"AAPL": 176.5, "GOOG": 139.2, "TSLA": 254.1, "MSFT": 325.4}
MOCK_CRYPTO = {"BTC": 27123.8, "ETH": 1852.5, "DOGE": 0.067}
MOCK_CURRENCY = {("USD", "INR"): 83.1, ("EUR", "USD"): 1.08, ("GBP", "USD"): 1.25}

def get_stock_price(symbol: str) -> float:
    """Return mock stock price."""
    return MOCK_STOCKS.get(symbol.upper(), -1.0)

def get_crypto_price(coin: str) -> float:
    """Return mock crypto price."""
    return MOCK_CRYPTO.get(coin.upper(), -1.0)

def get_currency_conversion(from_currency: str, to_currency: str, amount: float) -> float:
    """Return mock currency conversion."""
    rate = MOCK_CURRENCY.get((from_currency.upper(), to_currency.upper()), 1.0)
    return round(amount * rate, 2)

MOCK_MOVIES = {
    "Inception": {"director": "Christopher Nolan", "year": 2010, "rating": 8.8},
    "Interstellar": {"director": "Christopher Nolan", "year": 2014, "rating": 8.6},
    "The Matrix": {"director": "The Wachowskis", "year": 1999, "rating": 8.7},
}

def get_movie_info(title: str) -> dict:
    """Return mock movie info."""
    return MOCK_MOVIES.get(title, {"director": "Unknown", "year": None, "rating": None})

def send_email(recipient: str, subject: str, body: str) -> bool:
    """Simulate sending email."""
    return bool(recipient and subject and body)

def get_public_holidays(country: str, year: int) -> list[str]:
    """Return mock public holidays for a country."""
    MOCK_HOLIDAYS = {
        "IN": ["Republic Day", "Independence Day", "Diwali", "Holi", "Gandhi Jayanti"],
        "US": ["New Year's Day", "Independence Day", "Thanksgiving", "Christmas"],
        "UK": ["New Year's Day", "Easter", "Christmas"]
    }
    return MOCK_HOLIDAYS.get(country.upper(), ["No data available"])

MOCK_FLIGHTS = {
    ("DEL", "NYC"): [
        {"airline": "Air India", "flight_no": "AI101", "duration": "15h"},
        {"airline": "Delta", "flight_no": "DL405", "duration": "16h"}
    ],
    ("LON", "TOK"): [
        {"airline": "British Airways", "flight_no": "BA307", "duration": "12h"},
        {"airline": "ANA", "flight_no": "NH202", "duration": "11h 45m"}
    ]
}

def get_flight_schedule(source: str, destination: str) -> list[dict]:
    """
    Return mock flight schedules between two airports.

    Args:
        source: Source airport code (e.g., 'DEL').
        destination: Destination airport code (e.g., 'NYC').

    Returns:
        A list of flight info dictionaries.
    """
    return MOCK_FLIGHTS.get((source.upper(), destination.upper()), [{"airline": "None", "flight_no": "N/A", "duration": "N/A"}])

MOCK_HOTELS = {
    "New York": [
        {"name": "The Plaza", "rating": 4.8, "price_per_night": 350},
        {"name": "Marriott Downtown", "rating": 4.5, "price_per_night": 280}
    ],
    "Tokyo": [
        {"name": "Park Hyatt Tokyo", "rating": 4.9, "price_per_night": 420},
        {"name": "Shinjuku Granbell", "rating": 4.2, "price_per_night": 150}
    ]
}

def get_hotel_info(city: str, count: int = 3) -> list[dict]:
    """
    Return mock hotel information for a city.

    Args:
        city: City name (e.g., 'New York').
        count: Number of hotels to return.

    Returns:
        A list of hotel info dictionaries.
    """
    hotels = MOCK_HOTELS.get(city.title(), [])
    return hotels[:count] if hotels else [{"name": "No hotels available", "rating": None, "price_per_night": None}]

def get_traffic_status(city: str) -> str:
    """
    Return mock traffic status for a city.

    Args:
        city: City name (e.g., 'Delhi').

    Returns:
        A string describing traffic.
    """
    mock_status = {
        "Delhi": "Heavy traffic on Ring Road, moderate elsewhere.",
        "New York": "Moderate traffic in Manhattan, smooth in Brooklyn.",
        "London": "Congestion on M25, minor delays in central London."
    }
    return mock_status.get(city.title(), "Traffic data not available")


