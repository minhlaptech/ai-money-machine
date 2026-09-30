#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Central Master Repository of All 60 Enterprise Clients (Batches 1 to 6)
-----------------------------------------------------------------------
Provides a single source of truth for:
- scripts/generate_client_agreement.py
- scripts/generate_client_invoice.py
- scripts/batch_proposal_generator.py
- scripts/package_client_deliverables.py
- scripts/outreach_dispatcher.py
- scripts/export_crm_pipeline.py
"""

import sys
from pathlib import Path

def get_slug(name):
    return name.lower().replace(" ", "_").replace("&", "and").replace("/", "-").replace("\\", "-").replace(",", "").replace(".", "")

ALL_LEADS = [
    # =========================================================================
    # BATCH 1: Local High-Ticket Services (Healthcare & Trades)
    # =========================================================================
    {
        "id": 1, "batch": 1, "name": "Austin Dental Co", "niche": "Cosmetic Dentistry", "city": "Austin, TX",
        "to": "contact@austindentalco.example", "doc": "Dr. Miller", "type": "dental",
        "val": 750, "lost": 14, "value": 1200, "retainer": 650, "color": "#7c5cfc", "icon": "🦷"
    },
    {
        "id": 2, "batch": 1, "name": "Pure Radiance MedSpa", "niche": "Aesthetics & Spa", "city": "Miami, FL",
        "to": "info@pureradiancemedspa.example", "doc": "Sarah", "type": "medspa",
        "val": 650, "lost": 16, "value": 1200, "retainer": 650, "color": "#ec4899", "icon": "✨"
    },
    {
        "id": 3, "batch": 1, "name": "Premier 24/7 HVAC", "niche": "Heating & AC Repair", "city": "Dallas, TX",
        "to": "service@premierairdfw.example", "doc": "Mark", "type": "hvac",
        "val": 1200, "lost": 10, "value": 1200, "retainer": 650, "color": "#0ea5e9", "icon": "❄️"
    },
    {
        "id": 4, "batch": 1, "name": "Elite Smile Studio", "niche": "Orthodontics", "city": "San Jose, CA",
        "to": "hello@elitesmilestudio.example", "doc": "Dr. Nguyen", "type": "dental",
        "val": 1500, "lost": 8, "value": 1200, "retainer": 650, "color": "#3b82f6", "icon": "😁"
    },
    {
        "id": 5, "batch": 1, "name": "Apex Roofing & Solar", "niche": "Roofing & Solar", "city": "Phoenix, AZ",
        "to": "bids@apexroofsolar.example", "doc": "David", "type": "hvac",
        "val": 2500, "lost": 6, "value": 1200, "retainer": 650, "color": "#f59e0b", "icon": "☀️"
    },
    {
        "id": 6, "batch": 1, "name": "Lumina Wellness", "niche": "Regenerative Med", "city": "Seattle, WA",
        "to": "frontdesk@luminawellness.example", "doc": "Dr. Adams", "type": "medspa",
        "val": 850, "lost": 12, "value": 1200, "retainer": 650, "color": "#10b981", "icon": "🌿"
    },
    {
        "id": 7, "batch": 1, "name": "Vanguard Luxury RE", "niche": "Luxury Real Estate", "city": "Denver, CO",
        "to": "team@vanguardluxuryre.example", "doc": "Alex", "type": "realestate",
        "val": 4500, "lost": 4, "value": 1200, "retainer": 650, "color": "#6366f1", "icon": "🏰"
    },
    {
        "id": 8, "batch": 1, "name": "ProActive Spine & Chiro", "niche": "Chiropractic", "city": "Chicago, IL",
        "to": "appointments@proactivechiro.example", "doc": "Dr. Davis", "type": "dental",
        "val": 400, "lost": 18, "value": 1200, "retainer": 650, "color": "#14b8a6", "icon": "🩺"
    },
    {
        "id": 9, "batch": 1, "name": "Rapid Response Plumbing", "niche": "24/7 Emergency Plumber", "city": "Atlanta, GA",
        "to": "dispatch@rapidplumbatl.example", "doc": "Robert", "type": "hvac",
        "val": 800, "lost": 15, "value": 1200, "retainer": 650, "color": "#0284c7", "icon": "🔧"
    },
    {
        "id": 10, "batch": 1, "name": "Silicon Valley Skin Lab", "niche": "Dermatology & Laser", "city": "Palo Alto, CA",
        "to": "support@svskinlab.example", "doc": "Dr. Patel", "type": "medspa",
        "val": 950, "lost": 11, "value": 1200, "retainer": 650, "color": "#a855f7", "icon": "🔬"
    },

    # =========================================================================
    # BATCH 2: E-Commerce & High-Growth SaaS
    # =========================================================================
    {
        "id": 11, "batch": 2, "name": "Velora Activewear", "niche": "Athleisure Apparel", "city": "Los Angeles, CA",
        "to": "hello@veloraactive.example", "doc": "Team Velora", "type": "ecom",
        "val": 120, "lost": 65, "value": 1200, "retainer": 650, "color": "#f43f5e", "icon": "🏃"
    },
    {
        "id": 12, "batch": 2, "name": "NuvoGlow Skincare", "niche": "Clean D2C Beauty", "city": "New York, NY",
        "to": "partners@nuvoglowbeauty.example", "doc": "Founder", "type": "ecom",
        "val": 85, "lost": 90, "value": 1200, "retainer": 650, "color": "#ec4899", "icon": "🧴"
    },
    {
        "id": 13, "batch": 2, "name": "PulseMetrics AI", "niche": "B2B Analytics SaaS", "city": "San Francisco, CA",
        "to": "growth@pulsemetrics.example", "doc": "Founder", "type": "saas",
        "val": 1800, "lost": 7, "value": 1200, "retainer": 650, "color": "#8b5cf6", "icon": "📊"
    },
    {
        "id": 14, "batch": 2, "name": "HydroFlow Bottle", "niche": "Eco Hydration D2C", "city": "Boulder, CO",
        "to": "support@hydroflowbottle.example", "doc": "Team HydroFlow", "type": "ecom",
        "val": 60, "lost": 110, "value": 1200, "retainer": 650, "color": "#06b6d4", "icon": "💧"
    },
    {
        "id": 15, "batch": 2, "name": "CloudDesk Help", "niche": "Customer Support SaaS", "city": "Austin, TX",
        "to": "hello@clouddeskhelp.example", "doc": "Product Lead", "type": "saas",
        "val": 2200, "lost": 6, "value": 1200, "retainer": 650, "color": "#3b82f6", "icon": "☁️"
    },
    {
        "id": 16, "batch": 2, "name": "Artisan Roast Club", "niche": "Subscription Coffee", "city": "Portland, OR",
        "to": "orders@artisanroastclub.example", "doc": "Founder", "type": "ecom",
        "val": 45, "lost": 140, "value": 1200, "retainer": 650, "color": "#b45309", "icon": "☕"
    },
    {
        "id": 17, "batch": 2, "name": "StackSync Dev", "niche": "Developer Workflows", "city": "Seattle, WA",
        "to": "founders@stacksyncdev.example", "doc": "Engineering Lead", "type": "saas",
        "val": 3000, "lost": 5, "value": 1200, "retainer": 650, "color": "#6366f1", "icon": "⚡"
    },
    {
        "id": 18, "batch": 2, "name": "Pawsome Pet Boxes", "niche": "Pet Subscription D2C", "city": "Denver, CO",
        "to": "hello@pawsomepetbox.example", "doc": "Customer Team", "type": "ecom",
        "val": 70, "lost": 85, "value": 1200, "retainer": 650, "color": "#f97316", "icon": "🐾"
    },
    {
        "id": 19, "batch": 2, "name": "LeadFlow CRM", "niche": "SMB Sales CRM SaaS", "city": "Boston, MA",
        "to": "inquiries@leadflowcrm.example", "doc": "Growth Team", "type": "saas",
        "val": 1500, "lost": 8, "value": 1200, "retainer": 650, "color": "#10b981", "icon": "🎯"
    },
    {
        "id": 20, "batch": 2, "name": "ZenSleep Mattress", "niche": "D2C Sleep Wellness", "city": "Chicago, IL",
        "to": "concierge@zensleepbed.example", "doc": "Marketing Team", "type": "ecom",
        "val": 650, "lost": 22, "value": 1200, "retainer": 650, "color": "#475569", "icon": "🛏️"
    },

    # =========================================================================
    # BATCH 3: Enterprise Legal, Real Estate & Wealth Management
    # =========================================================================
    {
        "id": 21, "batch": 3, "name": "Sterling & Partners Legal", "niche": "Personal Injury Law", "city": "Chicago, IL",
        "to": "contact@sterlinglegalchi.example", "doc": "David Sterling", "type": "legal",
        "val": 3500, "lost": 5, "value": 1500, "retainer": 750, "color": "#1e293b", "icon": "⚖️"
    },
    {
        "id": 22, "batch": 3, "name": "Summit Crest Luxury Realty", "niche": "Luxury Real Estate", "city": "Aspen, CO",
        "to": "inquiries@summitcrestrealty.example", "doc": "Victoria Vance", "type": "realestate",
        "val": 6000, "lost": 3, "value": 1500, "retainer": 750, "color": "#854d0e", "icon": "🏔️"
    },
    {
        "id": 23, "batch": 3, "name": "Beacon Hill CPA & Tax", "niche": "Tax & Advisory Firm", "city": "Boston, MA",
        "to": "tax@beaconhillcpa.example", "doc": "Marcus Brody", "type": "cpa",
        "val": 2000, "lost": 7, "value": 1500, "retainer": 750, "color": "#334155", "icon": "📈"
    },
    {
        "id": 24, "batch": 3, "name": "Pacific Coast Family Law", "niche": "Divorce & Family Law", "city": "San Diego, CA",
        "to": "help@pacificfamilylawsd.example", "doc": "Elena Rostova", "type": "legal",
        "val": 2800, "lost": 6, "value": 1500, "retainer": 750, "color": "#0ea5e9", "icon": "🏛️"
    },
    {
        "id": 25, "batch": 3, "name": "Vanguard Wealth & Accounting", "niche": "Family Office & CPA", "city": "New York, NY",
        "to": "office@vanguardwealthnyc.example", "doc": "Jonathan Vance", "type": "cpa",
        "val": 4000, "lost": 4, "value": 1500, "retainer": 750, "color": "#0f766e", "icon": "💼"
    },
    {
        "id": 26, "batch": 3, "name": "Redwood Corporate Counsel", "niche": "Corporate & M&A", "city": "Austin, TX",
        "to": "hello@redwoodcounseltx.example", "doc": "Sarah Jenkins", "type": "legal",
        "val": 5000, "lost": 3, "value": 1500, "retainer": 750, "color": "#991b1b", "icon": "📜"
    },
    {
        "id": 27, "batch": 3, "name": "Pinnacle Commercial RE", "niche": "Commercial Brokerage", "city": "Dallas, TX",
        "to": "deals@pinnaclecredfw.example", "doc": "Robert Miller", "type": "realestate",
        "val": 8000, "lost": 2, "value": 1500, "retainer": 750, "color": "#1e3a8a", "icon": "🏢"
    },
    {
        "id": 28, "batch": 3, "name": "Harborview Estate Planning", "niche": "Trusts & Estates", "city": "Seattle, WA",
        "to": "info@harborviewestateswa.example", "doc": "Cynthia Thorne", "type": "legal",
        "val": 2400, "lost": 7, "value": 1500, "retainer": 750, "color": "#0369a1", "icon": "⚓"
    },
    {
        "id": 29, "batch": 3, "name": "Apex Audit & Valuation", "niche": "Audit & Valuation", "city": "Atlanta, GA",
        "to": "valuation@apexauditadvisory.example", "doc": "Richard Hall", "type": "cpa",
        "val": 3200, "lost": 5, "value": 1500, "retainer": 750, "color": "#4338ca", "icon": "🔍"
    },
    {
        "id": 30, "batch": 3, "name": "Metro Injury Defense Group", "niche": "Insurance Litigation", "city": "Miami, FL",
        "to": "litigation@metroinjurydefense.example", "doc": "Carlos Mendez", "type": "legal",
        "val": 4500, "lost": 4, "value": 1500, "retainer": 750, "color": "#b91c1c", "icon": "🛡️"
    },

    # =========================================================================
    # BATCH 4: High-End Home Services & Luxury Contracting
    # =========================================================================
    {
        "id": 31, "batch": 4, "name": "BlueWave Custom Pools", "niche": "Luxury Pools & Spas", "city": "Phoenix, AZ",
        "to": "design@bluewavecustompools.example", "doc": "Jason Bennett", "type": "contractor",
        "val": 5000, "lost": 4, "value": 5000, "retainer": 750, "color": "#0284c7", "icon": "🏊"
    },
    {
        "id": 32, "batch": 4, "name": "SolarMatrix EPC", "niche": "Commercial & Residential Solar", "city": "Las Vegas, NV",
        "to": "quotes@solarmatrixepc.example", "doc": "Elena Hayes", "type": "contractor",
        "val": 6000, "lost": 3, "value": 6000, "retainer": 850, "color": "#f59e0b", "icon": "☀️"
    },
    {
        "id": 33, "batch": 4, "name": "Elite Artisan Kitchens", "niche": "Luxury Kitchen Remodeling", "city": "Charlotte, NC",
        "to": "concierge@eliteartisankitchens.example", "doc": "Marcus Sterling", "type": "contractor",
        "val": 4500, "lost": 4, "value": 4500, "retainer": 750, "color": "#b45309", "icon": "🍳"
    },
    {
        "id": 34, "batch": 4, "name": "Ironclad Foundation Repair", "niche": "Structural Foundation Engineering", "city": "Nashville, TN",
        "to": "inspections@ironcladfoundation.example", "doc": "Travis Cole", "type": "contractor",
        "val": 3800, "lost": 5, "value": 3800, "retainer": 700, "color": "#475569", "icon": "🏗️"
    },
    {
        "id": 35, "batch": 4, "name": "Sierra Vista Landscape Architecture", "niche": "High-End Hardscaping", "city": "Salt Lake City, UT",
        "to": "inquiries@sierravistalandscape.example", "doc": "Chloe Davies", "type": "contractor",
        "val": 3500, "lost": 5, "value": 3500, "retainer": 700, "color": "#15803d", "icon": "🌲"
    },
    {
        "id": 36, "batch": 4, "name": "Paramount Commercial Roofing", "niche": "Industrial Roofing Systems", "city": "Houston, TX",
        "to": "estimates@paramountcommroofing.example", "doc": "Robert Lang", "type": "contractor",
        "val": 7500, "lost": 3, "value": 7500, "retainer": 950, "color": "#1e293b", "icon": "🏢"
    },
    {
        "id": 37, "batch": 4, "name": "Precision Climate HVAC", "niche": "Commercial Smart HVAC", "city": "Tampa, FL",
        "to": "service@precisionclimatefl.example", "doc": "Derek Vance", "type": "hvac",
        "val": 1200, "lost": 12, "value": 1200, "retainer": 650, "color": "#0ea5e9", "icon": "❄️"
    },
    {
        "id": 38, "batch": 4, "name": "Tri-State Architectural Glass", "niche": "Custom Glazing & Railings", "city": "Philadelphia, PA",
        "to": "bids@tristateglasspa.example", "doc": "Anthony Russo", "type": "contractor",
        "val": 4200, "lost": 4, "value": 4200, "retainer": 750, "color": "#06b6d4", "icon": "🪟"
    },
    {
        "id": 39, "batch": 4, "name": "Benchmark Custom Builders", "niche": "Modern Luxury Custom Homes", "city": "Raleigh, NC",
        "to": "plans@benchmarkcustomnc.example", "doc": "Jonathan Drake", "type": "contractor",
        "val": 8000, "lost": 3, "value": 8000, "retainer": 1000, "color": "#854d0e", "icon": "🏡"
    },
    {
        "id": 40, "batch": 4, "name": "Apex Disaster Restoration", "niche": "24/7 Fire & Water Mitigation", "city": "Minneapolis, MN",
        "to": "emergency@apexrestorationmn.example", "doc": "Sarah Lindqvist", "type": "hvac",
        "val": 5500, "lost": 4, "value": 5500, "retainer": 800, "color": "#dc2626", "icon": "🚨"
    },

    # =========================================================================
    # BATCH 5: High-Growth B2B Agencies & Tech Staffing
    # =========================================================================
    {
        "id": 41, "batch": 5, "name": "Kinetic Growth Media", "niche": "Paid Acquisition & Performance Ads", "city": "Austin, TX",
        "to": "growth@kineticgrowthmedia.example", "doc": "Alex Rivera", "type": "agency",
        "val": 2800, "lost": 6, "value": 2800, "retainer": 750, "color": "#8b5cf6", "icon": "📈"
    },
    {
        "id": 42, "batch": 5, "name": "HyperScale Search", "niche": "Executive Tech Search & Staffing", "city": "San Francisco, CA",
        "to": "talent@hyperscalesearch.example", "doc": "Samantha Reed", "type": "agency",
        "val": 4500, "lost": 4, "value": 4500, "retainer": 900, "color": "#6366f1", "icon": "🎯"
    },
    {
        "id": 43, "batch": 5, "name": "CinemaCraft Studios", "niche": "B2B SaaS 3D & Product Video", "city": "Los Angeles, CA",
        "to": "producers@cinemacraftstudios.example", "doc": "Julian Mercer", "type": "agency",
        "val": 3200, "lost": 5, "value": 3200, "retainer": 750, "color": "#ec4899", "icon": "🎥"
    },
    {
        "id": 44, "batch": 5, "name": "SearchVelocity AI", "niche": "Enterprise AI Search & SEO", "city": "New York, NY",
        "to": "strategy@searchvelocityai.example", "doc": "Nathan Ross", "type": "agency",
        "val": 3000, "lost": 6, "value": 3000, "retainer": 800, "color": "#10b981", "icon": "🔍"
    },
    {
        "id": 45, "batch": 5, "name": "Fractional CFO Partners", "niche": "Strategic Finance & M&A Advisory", "city": "Chicago, IL",
        "to": "advisory@fractionalcfochi.example", "doc": "William Thornton", "type": "cpa",
        "val": 4000, "lost": 4, "value": 4000, "retainer": 900, "color": "#334155", "icon": "💼"
    },
    {
        "id": 46, "batch": 5, "name": "BrandForge Creative", "niche": "Luxury Brand Identity & Design", "city": "Seattle, WA",
        "to": "hello@brandforgecreative.example", "doc": "Maya Lin", "type": "agency",
        "val": 2600, "lost": 7, "value": 2600, "retainer": 700, "color": "#d946ef", "icon": "🎨"
    },
    {
        "id": 47, "batch": 5, "name": "LeadIgnite B2B", "niche": "Outbound Sales & Lead Gen Engine", "city": "Boston, MA",
        "to": "pipeline@leadigniteb2b.example", "doc": "Connor Hayes", "type": "agency",
        "val": 2400, "lost": 8, "value": 2400, "retainer": 700, "color": "#f97316", "icon": "🔥"
    },
    {
        "id": 48, "batch": 5, "name": "DevSprint Staffing", "niche": "Nearshore Cloud & AI Engineers", "city": "Miami, FL",
        "to": "engineers@devsprintstaffing.example", "doc": "Ricardo Silva", "type": "agency",
        "val": 3500, "lost": 5, "value": 3500, "retainer": 800, "color": "#3b82f6", "icon": "💻"
    },
    {
        "id": 49, "batch": 5, "name": "Quantum Content Lab", "niche": "Technical Writing & Thought Leadership", "city": "Denver, CO",
        "to": "editors@quantumcontentlab.example", "doc": "Hannah Brooks", "type": "agency",
        "val": 2200, "lost": 8, "value": 2200, "retainer": 650, "color": "#a855f7", "icon": "✍️"
    },
    {
        "id": 50, "batch": 5, "name": "RetentionLoop CRM", "niche": "Customer Success & Churn Mitigation", "city": "Atlanta, GA",
        "to": "success@retentionloopcrm.example", "doc": "Marcus Bell", "type": "saas",
        "val": 2500, "lost": 7, "value": 2500, "retainer": 700, "color": "#14b8a6", "icon": "🔄"
    },

    # =========================================================================
    # BATCH 6: Specialized Luxury Healthcare & Surgery
    # =========================================================================
    {
        "id": 51, "batch": 6, "name": "Beverly Hills Plastic Surgery", "niche": "Aesthetic & Reconstructive Surgery", "city": "Beverly Hills, CA",
        "to": "vip@bhplasticsurgeryca.example", "doc": "Dr. Katherine Cole", "type": "medical",
        "val": 6500, "lost": 3, "value": 6500, "retainer": 950, "color": "#f43f5e", "icon": "✨"
    },
    {
        "id": 52, "batch": 6, "name": "Apex Orthopedic Spine Institute", "niche": "Minimally Invasive Spine Surgery", "city": "Dallas, TX",
        "to": "intake@apexspineinstitute.example", "doc": "Dr. Gregory Vance", "type": "medical",
        "val": 5500, "lost": 4, "value": 5500, "retainer": 900, "color": "#0284c7", "icon": "🩺"
    },
    {
        "id": 53, "batch": 6, "name": "NovoGen Fertility Specialists", "niche": "IVF & Reproductive Genetics", "city": "San Diego, CA",
        "to": "care@novogenfertility.example", "doc": "Dr. Maria Santos", "type": "medical",
        "val": 7000, "lost": 3, "value": 7000, "retainer": 1000, "color": "#ec4899", "icon": "🧬"
    },
    {
        "id": 54, "batch": 6, "name": "Serenity Longevity & Cryo", "niche": "Executive Biohacking & Anti-Aging", "city": "Miami, FL",
        "to": "concierge@serenitylongevity.example", "doc": "Dr. Lucas Meyer", "type": "medical",
        "val": 2500, "lost": 8, "value": 2500, "retainer": 750, "color": "#06b6d4", "icon": "🧊"
    },
    {
        "id": 55, "batch": 6, "name": "Optima Concierge Medicine", "niche": "Private Executive Primary Care", "city": "Scottsdale, AZ",
        "to": "membership@optimaconciergemed.example", "doc": "Dr. Arthur Pendelton", "type": "medical",
        "val": 3800, "lost": 5, "value": 3800, "retainer": 850, "color": "#059669", "icon": "⚕️"
    },
    {
        "id": 56, "batch": 6, "name": "Restore Regenerative Ortho", "niche": "Cellular Therapy & PRP Injections", "city": "Chicago, IL",
        "to": "appointments@restoreregenortho.example", "doc": "Dr. Steven Choi", "type": "medical",
        "val": 3200, "lost": 6, "value": 3200, "retainer": 800, "color": "#84cc16", "icon": "🩹"
    },
    {
        "id": 57, "batch": 6, "name": "ClearVision Lasik Center", "niche": "Contoura Vision & Refractive Surgery", "city": "Atlanta, GA",
        "to": "consult@clearvisionlasikatl.example", "doc": "Dr. Angela White", "type": "medical",
        "val": 3500, "lost": 6, "value": 3500, "retainer": 800, "color": "#2563eb", "icon": "👁️"
    },
    {
        "id": 58, "batch": 6, "name": "PureBreathe Sinus Institute", "niche": "Advanced Balloon Sinuplasty & ENT", "city": "Houston, TX",
        "to": "relief@purebreathesinus.example", "doc": "Dr. Farhan Qasim", "type": "medical",
        "val": 2800, "lost": 7, "value": 2800, "retainer": 750, "color": "#0891b2", "icon": "💨"
    },
    {
        "id": 59, "batch": 6, "name": "Radiance Hair Restoration", "niche": "Robotic ARTAS FUE Transplants", "city": "New York, NY",
        "to": "evaluations@radiancehairrestoration.example", "doc": "Dr. James Sterling", "type": "medical",
        "val": 5000, "lost": 4, "value": 5000, "retainer": 900, "color": "#d97706", "icon": "💈"
    },
    {
        "id": 60, "batch": 6, "name": "Thrive Neuro & Brain Health", "niche": "Deep TMS & Cognitive Optimization", "city": "San Jose, CA",
        "to": "eval@thriveneurohealth.example", "doc": "Dr. Rachel Green", "type": "medical",
        "val": 3000, "lost": 6, "value": 3000, "retainer": 800, "color": "#7c3aed", "icon": "🧠"
    },

    # =========================================================================
    # BATCH 7: Verified Inbound Scrapes (Dallas Law & Miami Dental)
    # =========================================================================
    # --- Dallas Legal Practices (15 Real Firms) ---
    {
        "id": 61, "batch": 7, "name": "Morgan Weisbrod", "niche": "Disability & Injury Law", "city": "Dallas, TX",
        "to": "contact@morganweisbrod.com", "doc": "Morgan Weisbrod", "type": "legal",
        "val": 3500, "lost": 5, "value": 3500, "retainer": 850, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 62, "batch": 7, "name": "Guajardo & Marks, LLP", "niche": "Personal Injury Law", "city": "Dallas, TX",
        "to": "contact@guajardomarks.com", "doc": "Michael Guajardo", "type": "legal",
        "val": 4000, "lost": 4, "value": 4000, "retainer": 900, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 63, "batch": 7, "name": "Law Office of William Teitelbaum", "niche": "Civil & Criminal Law", "city": "Dallas, TX",
        "to": "contact@lawofficeofwilliamteitelbaum.example", "doc": "William Teitelbaum", "type": "legal",
        "val": 3000, "lost": 5, "value": 3000, "retainer": 800, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 64, "batch": 7, "name": "Orsinger, Nelson, Downing and Anderson, LLP", "niche": "Family & Appellate Law", "city": "Dallas, TX",
        "to": "contact@ondafamilylaw.com", "doc": "Richard Orsinger", "type": "legal",
        "val": 4500, "lost": 4, "value": 4500, "retainer": 950, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 65, "batch": 7, "name": "Clements & Clements, Attorneys at Law", "niche": "Trial & Injury Attorneys", "city": "Dallas, TX",
        "to": "contact@clementslaw.com", "doc": "Robert Clements", "type": "legal",
        "val": 3800, "lost": 5, "value": 3800, "retainer": 900, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 66, "batch": 7, "name": "Saputo Law Firm", "niche": "Criminal Defense & Trial", "city": "Dallas, TX",
        "to": "contact@saputo.law", "doc": "Paul Saputo", "type": "legal",
        "val": 3500, "lost": 5, "value": 3500, "retainer": 850, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 67, "batch": 7, "name": "Law Office of Julie Johnson, PLLC", "niche": "Personal Injury & Employment", "city": "Dallas, TX",
        "to": "contact@juliejohnsonlaw.com", "doc": "Julie Johnson", "type": "legal",
        "val": 4200, "lost": 4, "value": 4200, "retainer": 900, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 68, "batch": 7, "name": "Zegen Law Firm PLLC", "niche": "Dallas Divorce & Family Law", "city": "Dallas, TX",
        "to": "contact@thedallasdivorceattorney.com", "doc": "Scott Zegen", "type": "legal",
        "val": 3200, "lost": 6, "value": 3200, "retainer": 850, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 69, "batch": 7, "name": "Kastl Law P.C.", "niche": "Personal Injury Litigation", "city": "Dallas, TX",
        "to": "contact@kastllaw.com", "doc": "Kristina Kastl", "type": "legal",
        "val": 4000, "lost": 4, "value": 4000, "retainer": 900, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 70, "batch": 7, "name": "Hastings Law Firm", "niche": "Medical Malpractice Attorneys", "city": "Dallas, TX",
        "to": "contact@hastingsfirm.com", "doc": "Tommy Hastings", "type": "legal",
        "val": 5000, "lost": 3, "value": 5000, "retainer": 1000, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 71, "batch": 7, "name": "The Benton Law Firm", "niche": "Serious Injury & Auto Litigation", "city": "Dallas, TX",
        "to": "contact@thebentonlawfirm.com", "doc": "Jeff Benton", "type": "legal",
        "val": 4200, "lost": 4, "value": 4200, "retainer": 950, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 72, "batch": 7, "name": "Slater Matsil", "niche": "Intellectual Property & Patents", "city": "Dallas, TX",
        "to": "contact@slatermatsil.example", "doc": "Ira Matsil", "type": "legal",
        "val": 5500, "lost": 3, "value": 5500, "retainer": 1000, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 73, "batch": 7, "name": "Brooker Law, PLLC", "niche": "Catastrophic Injury & Commercial Law", "city": "Dallas, TX",
        "to": "contact@brookerlaw.com", "doc": "Chip Brooker", "type": "legal",
        "val": 4800, "lost": 4, "value": 4800, "retainer": 950, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 74, "batch": 7, "name": "Scroggins Law Group PLLC", "niche": "Board Certified Family Law", "city": "Dallas, TX",
        "to": "contact@scrogginslawgroup.example", "doc": "Mark Scroggins", "type": "legal",
        "val": 3600, "lost": 5, "value": 3600, "retainer": 850, "color": "#38bdf8", "icon": "⚖️"
    },
    {
        "id": 75, "batch": 7, "name": "Lyons & Simmons, LLP", "niche": "High-Stakes Trial Lawyers", "city": "Dallas, TX",
        "to": "contact@lyons-simmons.com", "doc": "Michael Lyons", "type": "legal",
        "val": 5200, "lost": 3, "value": 5200, "retainer": 1000, "color": "#38bdf8", "icon": "⚖️"
    },

    # --- Miami Dental Clinics (9 Real Clinics) ---
    {
        "id": 76, "batch": 7, "name": "Miami Village Dental", "niche": "Comprehensive Family Dentistry", "city": "Miami, FL",
        "to": "contact@miamivillagedental.example", "doc": "Dr. Elena Gomez", "type": "dental",
        "val": 1200, "lost": 10, "value": 1200, "retainer": 650, "color": "#00e676", "icon": "🦷"
    },
    {
        "id": 77, "batch": 7, "name": "Miami Premier Dental Care", "niche": "Cosmetic & Restorative Dentistry", "city": "Miami, FL",
        "to": "contact@miamipremierdental.example", "doc": "Dr. Carlos Ramos", "type": "dental",
        "val": 1400, "lost": 9, "value": 1400, "retainer": 700, "color": "#00e676", "icon": "🦷"
    },
    {
        "id": 78, "batch": 7, "name": "Vizcaya Dental Arts", "niche": "Cosmetic Veneers & Smile Makeovers", "city": "Miami, FL",
        "to": "contact@vizcayadentalarts.com", "doc": "Dr. Mario Alvarez", "type": "dental",
        "val": 1800, "lost": 8, "value": 1800, "retainer": 750, "color": "#00e676", "icon": "🦷"
    },
    {
        "id": 79, "batch": 7, "name": "Miami One Dental Studio", "niche": "Invisalign & Dental Implants", "city": "Miami, FL",
        "to": "contact@miamionedental.example", "doc": "Dr. Jessica Ortiz", "type": "dental",
        "val": 1600, "lost": 9, "value": 1600, "retainer": 700, "color": "#00e676", "icon": "🦷"
    },
    {
        "id": 80, "batch": 7, "name": "CAD/CAM Dental CENTER Miami", "niche": "Digital 3D Same-Day Crowns", "city": "Miami, FL",
        "to": "contact@cadcamcenter.com", "doc": "Dr. Alex Levin", "type": "dental",
        "val": 2000, "lost": 7, "value": 2000, "retainer": 800, "color": "#00e676", "icon": "🦷"
    },
    {
        "id": 81, "batch": 7, "name": "Epic Smiles Miami", "niche": "Orthodontics & Clear Aligners", "city": "Miami, FL",
        "to": "contact@epicsmilesmiami.example", "doc": "Dr. Sofia Morales", "type": "dental",
        "val": 1500, "lost": 8, "value": 1500, "retainer": 700, "color": "#00e676", "icon": "🦷"
    },
    {
        "id": 82, "batch": 7, "name": "Biscayne Modern Dental", "niche": "Laser Periodontics & Sleep Apnea", "city": "Miami, FL",
        "to": "contact@biscaynemoderndental.example", "doc": "Dr. David Chen", "type": "dental",
        "val": 1300, "lost": 10, "value": 1300, "retainer": 650, "color": "#00e676", "icon": "🦷"
    },
    {
        "id": 83, "batch": 7, "name": "Healthy Children Pediatric Dentistry", "niche": "Pediatric Dental Specialists", "city": "Miami, FL",
        "to": "contact@healthychildrenpediatrics.example", "doc": "Dr. Amanda Perez", "type": "dental",
        "val": 1100, "lost": 12, "value": 1100, "retainer": 650, "color": "#00e676", "icon": "🦷"
    },
    {
        "id": 84, "batch": 7, "name": "Ultra Smile Aesthetic Dental", "niche": "Teeth Whitening & Sedation", "city": "Miami, FL",
        "to": "contact@ultrasmile.example", "doc": "Dr. Gabriel Santos", "type": "dental",
        "val": 1700, "lost": 8, "value": 1700, "retainer": 750, "color": "#00e676", "icon": "🦷"
    }
]

# Enrich each lead with slug
for _lead in ALL_LEADS:
    _lead["slug"] = get_slug(_lead["name"])

def get_lead_by_id(lead_id: int):
    return next((l for l in ALL_LEADS if l["id"] == lead_id), None)

def get_lead_by_slug(slug: str):
    return next((l for l in ALL_LEADS if l["slug"] == slug), None)

if __name__ == "__main__":
    print(f"Total Leads Loaded: {len(ALL_LEADS)}")
    for b in range(1, 8):
        b_leads = [l for l in ALL_LEADS if l["batch"] == b]
        print(f"  Batch {b}: {len(b_leads)} accounts | IDs {b_leads[0]['id']} - {b_leads[-1]['id']}")
