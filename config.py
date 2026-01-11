# Configuration file for AI Travel Planner

# API Configuration
ANTHROPIC_API_KEY = "your-api-key-here"

# Application Settings
APP_TITLE = "🎒 Student Travel Planner"
APP_DESCRIPTION = "Budget-friendly AI-powered travel planning for students"

# Budget Categories
BUDGET_RANGES = {
    "Ultra Budget": (0, 500),
    "Budget": (500, 1500),
    "Moderate": (1500, 3000),
    "Comfortable": (3000, 5000),
    "Luxury": (5000, 10000)
}

# Travel Preferences
TRAVEL_STYLES = [
    "Adventure & Outdoor",
    "Cultural & Historical",
    "Beach & Relaxation",
    "City Exploration",
    "Food & Culinary",
    "Party & Nightlife",
    "Nature & Wildlife",
    "Photography",
    "Budget Backpacking"
]

# Default Map Settings
DEFAULT_MAP_ZOOM = 6
MAP_TILE = "OpenStreetMap"

# PDF Export Settings
PDF_TITLE = "Student Travel Itinerary"
PDF_AUTHOR = "AI Travel Planner"