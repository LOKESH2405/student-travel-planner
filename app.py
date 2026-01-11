import streamlit as st
import config
from utils.ai_helper import generate_itinerary
from utils.map_helper import create_travel_map
from utils.pdf_generator import generate_itinerary_pdf
from streamlit_folium import folium_static
import pandas as pd
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        padding: 20px;
        background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #2E86AB;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #A23B72;
        color: white;
    }
    .info-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    .cost-badge {
        background-color: #28a745;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None
if 'show_itinerary' not in st.session_state:
    st.session_state.show_itinerary = False

# Header
st.markdown('<h1 class="main-header">🎒 Student Travel Planner</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Budget Travel Planning for Students</p>', unsafe_allow_html=True)

# Sidebar for input
with st.sidebar:
    st.header("✈️ Plan Your Trip")
    
    # Destination input
    destination = st.text_input(
        "📍 Where do you want to go?",
        placeholder="e.g., Paris, Tokyo, New York",
        help="Enter any city or country"
    )
    
    # Trip duration
    days = st.slider(
        "📅 How many days?",
        min_value=1,
        max_value=30,
        value=5,
        help="Select the duration of your trip"
    )
    
    # Start date
    start_date = st.date_input(
        "🗓️ Start Date",
        value=datetime.now() + timedelta(days=30),
        min_value=datetime.now()
    )
    
    # Budget
    budget_range = st.select_slider(
        "💰 Budget Range",
        options=list(config.BUDGET_RANGES.keys()),
        value="Budget"
    )
    
    min_budget, max_budget = config.BUDGET_RANGES[budget_range]
    budget = st.number_input(
        f"Specific Budget (${min_budget}-${max_budget})",
        min_value=min_budget,
        max_value=max_budget,
        value=(min_budget + max_budget) // 2,
        step=100
    )
    
    # Travel style
    travel_style = st.selectbox(
        "🎨 Travel Style",
        config.TRAVEL_STYLES,
        help="What kind of experience are you looking for?"
    )
    
    # Additional interests
    interests = st.text_area(
        "💭 Additional Interests",
        placeholder="e.g., photography, hiking, local cuisine, nightlife",
        help="Any specific interests or activities you want to include?"
    )
    
    st.markdown("---")
    
    # Generate button
    generate_btn = st.button("🚀 Generate Itinerary", type="primary")

# Main content area
if generate_btn and destination:
    with st.spinner("✨ Creating your perfect itinerary... This may take a moment!"):
        try:
            # Generate itinerary using AI
            itinerary = generate_itinerary(
                destination=destination,
                days=days,
                budget=budget,
                travel_style=travel_style,
                interests=interests,
                start_date=start_date.strftime("%Y-%m-%d")
            )
            
            st.session_state.itinerary = itinerary
            st.session_state.show_itinerary = True
            st.success("✅ Itinerary generated successfully!")
            
        except Exception as e:
            st.error(f"❌ Error generating itinerary: {str(e)}")
            st.info("💡 Make sure you have configured your API key in config.py or try again.")

elif generate_btn and not destination:
    st.warning("⚠️ Please enter a destination!")

# Display itinerary
if st.session_state.show_itinerary and st.session_state.itinerary:
    itinerary = st.session_state.itinerary
    
    # Overview section
    st.markdown("## 🌍 Trip Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Destination", itinerary['destination'])
    with col2:
        st.metric("Duration", f"{len(itinerary.get('days', []))} Days")
    with col3:
        st.metric("Total Budget", f"${itinerary.get('total_estimated_cost', budget)}")
    with col4:
        st.metric("Daily Budget", f"${itinerary.get('daily_budget', 0)}")
    
    st.markdown(f"**Overview:** {itinerary.get('overview', 'Enjoy your trip!')}")
    
    st.markdown("---")
    
    # Map section
    st.markdown("## 🗺️ Interactive Map")
    travel_map = create_travel_map(destination, itinerary)
    folium_static(travel_map, width=1200, height=500)
    
    st.markdown("---")
    
    # Daily itinerary
    st.markdown("## 📅 Daily Itinerary")
    
    for day in itinerary.get('days', []):
        with st.expander(f"**Day {day['day']}: {day['title']}** - Estimated Cost: ${day.get('daily_cost', 0)}", expanded=True):
            
            # Activities
            st.markdown("### 🎯 Activities")
            for activity in day.get('activities', []):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{activity['time']}** - {activity['activity']}")
                    if activity.get('tips'):
                        st.info(f"💡 {activity['tips']}")
                with col2:
                    if activity.get('cost'):
                        st.markdown(f'<span class="cost-badge">${activity["cost"]}</span>', unsafe_allow_html=True)
                st.markdown("")
            
            # Meals
            if day.get('meals'):
                st.markdown("### 🍽️ Meals")
                meal_cols = st.columns(3)
                with meal_cols[0]:
                    st.markdown(f"**Breakfast:** {day['meals'].get('breakfast', 'N/A')}")
                with meal_cols[1]:
                    st.markdown(f"**Lunch:** {day['meals'].get('lunch', 'N/A')}")
                with meal_cols[2]:
                    st.markdown(f"**Dinner:** {day['meals'].get('dinner', 'N/A')}")
            
            # Accommodation
            if day.get('accommodation'):
                st.markdown("### 🏨 Accommodation")
                st.markdown(f"{day['accommodation']}")
    
    st.markdown("---")
    
    # Budget breakdown
    if 'budget_breakdown' in itinerary:
        st.markdown("## 💰 Budget Breakdown")
        
        breakdown = itinerary['budget_breakdown']
        df = pd.DataFrame({
            'Category': [k.replace('_', ' ').title() for k in breakdown.keys()],
            'Amount ($)': list(breakdown.values())
        })
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(df.set_index('Category'))
        with col2:
            st.dataframe(df, hide_index=True)
        
        st.markdown("---")
    
    # Accommodation options
    if 'accommodation_options' in itinerary:
        st.markdown("## 🏨 Accommodation Options")
        
        acc_cols = st.columns(len(itinerary['accommodation_options']))
        for idx, acc in enumerate(itinerary['accommodation_options']):
            with acc_cols[idx]:
                st.markdown(f"### {acc['name']}")
                st.markdown(f"**Type:** {acc['type']}")
                st.markdown(f"**Price/Night:** ${acc['price_per_night']}")
                st.info(f"💡 {acc['tips']}")
        
        st.markdown("---")
    
    # Transportation
    if 'transportation' in itinerary:
        st.markdown("## 🚌 Transportation")
        
        trans = itinerary['transportation']
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Getting There:** {trans.get('getting_there', 'N/A')}")
        with col2:
            st.markdown(f"**Local Transport:** {trans.get('local_transport', 'N/A')}")
        
        st.markdown(f"**Estimated Cost:** ${trans.get('estimated_cost', 0)}")
        st.markdown("---")
    
    # Money saving tips
    if 'money_saving_tips' in itinerary:
        st.markdown("## 💡 Money Saving Tips")
        
        tips_cols = st.columns(2)
        for idx, tip in enumerate(itinerary['money_saving_tips']):
            with tips_cols[idx % 2]:
                st.success(f"✅ {tip}")
        
        st.markdown("---")
    
    # Essential information
    if 'essential_info' in itinerary:
        st.markdown("## ℹ️ Essential Information")
        
        info = itinerary['essential_info']
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Best Time to Visit:** {info.get('best_time_to_visit', 'N/A')}")
            st.markdown(f"**Currency:** {info.get('currency', 'N/A')}")
        with col2:
            st.markdown(f"**Language:** {info.get('language', 'N/A')}")
        
        if 'safety_tips' in info:
            st.markdown("**Safety Tips:**")
            for tip in info['safety_tips']:
                st.warning(f"⚠️ {tip}")
    
    st.markdown("---")
    
    # Export options
    st.markdown("## 📥 Export Your Itinerary")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📄 Download as PDF"):
            try:
                pdf_filename = f"{destination.replace(' ', '_')}_itinerary.pdf"
                generate_itinerary_pdf(itinerary, pdf_filename)
                
                with open(pdf_filename, "rb") as file:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=file,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
                st.success("✅ PDF generated successfully!")
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")
    
    with col2:
        if st.button("📋 Copy to Clipboard"):
            st.info("💡 Use the PDF export or manually copy the content above")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Made with ❤️ for students who love to travel</p>
        <p style='font-size: 12px;'>Powered by AI • Budget-Friendly • Student-Focused</p>
    </div>
    """, unsafe_allow_html=True)

# Info sidebar at the bottom
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. Enter your destination
    2. Set your trip duration
    3. Choose your budget
    4. Select travel style
    5. Click 'Generate Itinerary'
    6. Download as PDF
    """)
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Book in advance for better prices
    - Look for student discounts
    - Use public transportation
    - Try local street food
    - Stay in hostels for cheaper accommodation
    """)
    
    st.markdown("---")
    st.markdown("**Need help?** Check our documentation or contact support.")