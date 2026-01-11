from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import config
from datetime import datetime

def generate_itinerary_pdf(itinerary_data, filename="travel_itinerary.pdf"):
    """
    Generate a PDF document of the travel itinerary
    """
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E86AB'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#A23B72'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#F18F01'),
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    # Title
    elements.append(Paragraph(f"Travel Itinerary: {itinerary_data['destination']}", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Overview
    elements.append(Paragraph("Trip Overview", heading_style))
    elements.append(Paragraph(itinerary_data.get('overview', 'Your personalized travel adventure!'), styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Budget Summary
    elements.append(Paragraph("Budget Summary", heading_style))
    budget_data = [
        ['Total Budget:', f"${itinerary_data.get('total_estimated_cost', 0)}"],
        ['Daily Budget:', f"${itinerary_data.get('daily_budget', 0)}"],
        ['Number of Days:', f"{len(itinerary_data.get('days', []))} days"]
    ]
    
    budget_table = Table(budget_data, colWidths=[3*inch, 2*inch])
    budget_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0F0F0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    elements.append(budget_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Daily Itinerary
    elements.append(Paragraph("Daily Itinerary", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    for day in itinerary_data.get('days', []):
        elements.append(Paragraph(f"Day {day['day']}: {day['title']}", subheading_style))
        
        # Activities
        for activity in day.get('activities', []):
            activity_text = f"<b>{activity['time']}</b> - {activity['activity']}"
            if activity.get('cost'):
                activity_text += f" (${activity['cost']})"
            elements.append(Paragraph(activity_text, styles['BodyText']))
            
            if activity.get('tips'):
                tip_style = ParagraphStyle('Tip', parent=styles['BodyText'], 
                                          leftIndent=20, textColor=colors.HexColor('#666666'),
                                          fontSize=9)
                elements.append(Paragraph(f"💡 {activity['tips']}", tip_style))
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Meals
        if day.get('meals'):
            meals_text = f"<b>Meals:</b> Breakfast: {day['meals'].get('breakfast', 'N/A')}, " \
                        f"Lunch: {day['meals'].get('lunch', 'N/A')}, " \
                        f"Dinner: {day['meals'].get('dinner', 'N/A')}"
            elements.append(Paragraph(meals_text, styles['BodyText']))
        
        # Accommodation
        if day.get('accommodation'):
            elements.append(Paragraph(f"<b>Accommodation:</b> {day['accommodation']}", styles['BodyText']))
        
        # Daily cost
        if day.get('daily_cost'):
            elements.append(Paragraph(f"<b>Estimated Daily Cost:</b> ${day['daily_cost']}", styles['BodyText']))
        
        elements.append(Spacer(1, 0.2*inch))
    
    # Budget Breakdown
    if 'budget_breakdown' in itinerary_data:
        elements.append(PageBreak())
        elements.append(Paragraph("Budget Breakdown", heading_style))
        
        breakdown = itinerary_data['budget_breakdown']
        breakdown_data = [[k.replace('_', ' ').title(), f"${v}"] for k, v in breakdown.items()]
        
        breakdown_table = Table(breakdown_data, colWidths=[3*inch, 2*inch])
        breakdown_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E8F4F8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        elements.append(breakdown_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Money Saving Tips
    if 'money_saving_tips' in itinerary_data:
        elements.append(Paragraph("Money Saving Tips 💰", heading_style))
        for tip in itinerary_data['money_saving_tips']:
            elements.append(Paragraph(f"• {tip}", styles['BodyText']))
        elements.append(Spacer(1, 0.2*inch))
    
    # Transportation
    if 'transportation' in itinerary_data:
        elements.append(Paragraph("Transportation", heading_style))
        trans = itinerary_data['transportation']
        elements.append(Paragraph(f"<b>Getting There:</b> {trans.get('getting_there', 'N/A')}", styles['BodyText']))
        elements.append(Paragraph(f"<b>Local Transport:</b> {trans.get('local_transport', 'N/A')}", styles['BodyText']))
        elements.append(Paragraph(f"<b>Estimated Cost:</b> ${trans.get('estimated_cost', 0)}", styles['BodyText']))
        elements.append(Spacer(1, 0.2*inch))
    
    # Essential Info
    if 'essential_info' in itinerary_data:
        elements.append(Paragraph("Essential Information", heading_style))
        info = itinerary_data['essential_info']
        
        for key, value in info.items():
            if isinstance(value, list):
                elements.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b>", styles['BodyText']))
                for item in value:
                    elements.append(Paragraph(f"• {item}", styles['BodyText']))
            else:
                elements.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", styles['BodyText']))
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_text = f"Generated by {config.APP_TITLE} on {datetime.now().strftime('%B %d, %Y')}"
    footer_style = ParagraphStyle('Footer', parent=styles['BodyText'], 
                                 alignment=TA_CENTER, fontSize=8, 
                                 textColor=colors.grey)
    elements.append(Paragraph(footer_text, footer_style))
    
    # Build PDF
    doc.build(elements)
    return filename