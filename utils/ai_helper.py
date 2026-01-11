import anthropic
import config
import json

def generate_itinerary(destination, days, budget, travel_style, interests, start_date):
    """Generate a personalized travel itinerary using Claude AI"""
    
    if config.ANTHROPIC_API_KEY == "your-api-key-here":
        return generate_template_itinerary(destination, days, budget, travel_style, interests)
    
    try:
        client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        
        prompt = f"""Create a detailed {days}-day travel itinerary for a student visiting {destination}.

Budget: ${budget} USD (total for the entire trip)
Travel Style: {travel_style}
Interests: {interests}
Start Date: {start_date}

Please provide a comprehensive itinerary in JSON format with the following structure:
{{
    "destination": "{destination}",
    "overview": "Brief overview of the trip",
    "total_estimated_cost": estimated_cost,
    "daily_budget": daily_budget,
    "days": [...],
    "budget_breakdown": {{...}},
    "money_saving_tips": [...],
    "essential_info": {{...}}
}}

Focus on budget-friendly options suitable for students."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        try:
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            itinerary = json.loads(response_text.strip())
            return itinerary
        except json.JSONDecodeError:
            return {"destination": destination, "overview": response_text, "days": []}
            
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        return generate_template_itinerary(destination, days, budget, travel_style, interests)


def generate_template_itinerary(destination, days, budget, travel_style, interests):
    """Generate a template itinerary when API is not available"""
    daily_budget = budget / days
    
    itinerary = {
        "destination": destination,
        "overview": f"A {days}-day budget-friendly adventure to {destination}",
        "total_estimated_cost": budget,
        "daily_budget": round(daily_budget, 2),
        "days": []
    }
    
    for day in range(1, days + 1):
        day_plan = {
            "day": day,
            "title": f"Day {day}: Exploring {destination}",
            "activities": [
                {"time": "9:00 AM", "activity": "Breakfast at local cafe", "cost": 5, "tips": "Look for student discounts!"},
                {"time": "10:30 AM", "activity": f"Visit popular attraction", "cost": 15, "tips": "Book online for discounts"},
                {"time": "1:00 PM", "activity": "Lunch at local restaurant", "cost": 10, "tips": "Try street food"},
                {"time": "3:00 PM", "activity": "Explore local markets", "cost": 0, "tips": "Walking tours are free!"},
                {"time": "8:00 PM", "activity": "Dinner", "cost": 15, "tips": "Look for happy hour deals"}
            ],
            "meals": {"breakfast": "Local cafe ($5-8)", "lunch": "Street food ($8-12)", "dinner": "Local restaurant ($12-20)"},
            "accommodation": f"Budget hostel (${round(daily_budget * 0.3)}/night)",
            "daily_cost": round(daily_budget, 2)
        }
        itinerary["days"].append(day_plan)
    
    itinerary["budget_breakdown"] = {
        "accommodation": round(budget * 0.30),
        "food": round(budget * 0.30),
        "activities": round(budget * 0.25),
        "transportation": round(budget * 0.15)
    }
    
    itinerary["money_saving_tips"] = [
        "Book accommodation in advance",
        "Eat where locals eat",
        "Use public transportation",
        "Look for free walking tours"
    ]
    
    itinerary["essential_info"] = {
        "best_time_to_visit": "Spring or Fall",
        "currency": "Check exchange rates",
        "language": "Learn basic phrases",
        "safety_tips": ["Keep copies of documents", "Stay aware of surroundings"]
    }
    
    return itinerary