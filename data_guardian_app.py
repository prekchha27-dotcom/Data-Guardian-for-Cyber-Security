"""
Data Guardian — Social Media Privacy & Legal Policy Research Dashboard
Single-file Streamlit application (backend + frontend combined).
All section modules inlined — no local imports required.
Run with:  streamlit run data_guardian_app.py
"""

# ── External imports ──────────────────────────────────────────────────────────
import re
import math
import heapq
import textwrap
import collections
import streamlit as st
import streamlit.components.v1 as components

# ══════════════════════════════════════════════════════════════════════════════
# SECTION: STYLES  (from sections/styles.py)
# ══════════════════════════════════════════════════════════════════════════════

def inject_styles():
    st.markdown(
        """
        <style>
        /* ── Base ── */
        html, body, [class*="css"] {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 17px;
            line-height: 1.7;
            letter-spacing: 0.012em;
        }
        .stApp {
            background-color: #0b1a28;
            color: #f0f4f8;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background-color: #0d2035 !important;
            border-right: 2px solid #1e3d60;
        }
        [data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            border: none !important;
            color: #c8dff0 !important;
            text-align: left !important;
            font-size: 0.97rem !important;
            font-weight: 500 !important;
            padding: 0.55rem 0.9rem !important;
            border-radius: 8px !important;
            width: 100% !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            transition: background 0.15s, color 0.15s;
        }
        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: #006647 !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 700 !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: #1a3f60 !important;
            color: #00e8bb !important;
        }
        [data-testid="stSidebar"] .stButton > button:focus-visible {
            outline: 3px solid #00e8bb !important;
            outline-offset: 2px !important;
        }
        [data-testid="stSidebar"] .stButton > button p {
            font-size: 0.97rem !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }

        /* ── Headings ── */
        h1, h2, h3, h4 { color: #f0f4f8; line-height: 1.35; }
        h1 { font-size: 2.1rem; font-weight: 800; }
        h2 { font-size: 1.6rem; font-weight: 700; }
        h3 { font-size: 1.25rem; font-weight: 700; }
        h4 { font-size: 1.05rem; font-weight: 600; }

        /* ── Metric cards ── */
        [data-testid="metric-container"] {
            background: #0d2035;
            border: 1px solid #1e3d60;
            border-radius: 10px;
            padding: 0.8rem 1.1rem;
        }
        [data-testid="metric-container"] label { color: #aac4d8 !important; font-size: 0.9rem; }
        [data-testid="metric-container"] [data-testid="stMetricValue"] {
            color: #00e8bb !important; font-size: 2rem; font-weight: 800;
        }

        /* ── Cards ── */
        .dg-card {
            background: #0d2035; border: 1px solid #1e3d60;
            border-radius: 12px; padding: 1.1rem 1.3rem; margin-bottom: 0.9rem;
        }
        .dg-card-title { font-size: 1.08rem; font-weight: 700; color: #00e8bb; margin-bottom: 0.45rem; }
        .dg-card-body  { font-size: 1rem; color: #cce0f0; line-height: 1.7; }

        /* ── Risk badges ── */
        .badge-low    { background:#00401f; color:#4dffaa; border:2px solid #00cc66; border-radius:6px; padding:3px 12px; font-size:0.85rem; font-weight:700; }
        .badge-review { background:#4a3000; color:#ffd166; border:2px solid #ffb300; border-radius:6px; padding:3px 12px; font-size:0.85rem; font-weight:700; }
        .badge-high   { background:#4a0a0a; color:#ff6b6b; border:2px solid #cc2222; border-radius:6px; padding:3px 12px; font-size:0.85rem; font-weight:700; }
        .badge-unknown{ background:#1a2d40; color:#aac4d8; border:2px solid #2a4d6a; border-radius:6px; padding:3px 12px; font-size:0.85rem; font-weight:700; }

        /* ── Status pills ── */
        .status-demo    { background:#093d5c; color:#66d9ff; border:2px solid #0099cc; border-radius:6px; padding:3px 10px; font-size:0.82rem; font-weight:600; }
        .status-verified{ background:#004020; color:#4dffaa; border:2px solid #00cc66; border-radius:6px; padding:3px 10px; font-size:0.82rem; font-weight:600; }
        .status-review  { background:#4a3000; color:#ffd166; border:2px solid #ffb300; border-radius:6px; padding:3px 10px; font-size:0.82rem; font-weight:600; }
        .status-updated { background:#3a1050; color:#cc99ff; border:2px solid #9955dd; border-radius:6px; padding:3px 10px; font-size:0.82rem; font-weight:600; }

        /* ── Info/warning/error/ok boxes ── */
        .dg-info   { background:#082840; border-left:5px solid #3399ff; border-radius:6px; padding:0.9rem 1.1rem; margin:0.65rem 0; color:#cce6ff; font-size:1rem; line-height:1.65; }
        .dg-warn   { background:#3a2500; border-left:5px solid #ffd166; border-radius:6px; padding:0.9rem 1.1rem; margin:0.65rem 0; color:#ffe599; font-size:1rem; line-height:1.65; }
        .dg-danger { background:#3a0808; border-left:5px solid #ff6b6b; border-radius:6px; padding:0.9rem 1.1rem; margin:0.65rem 0; color:#ffaaaa; font-size:1rem; line-height:1.65; }
        .dg-ok     { background:#003018; border-left:5px solid #4dffaa; border-radius:6px; padding:0.9rem 1.1rem; margin:0.65rem 0; color:#99ffcc; font-size:1rem; line-height:1.65; }

        .dg-info-light   { background:#e8f4ff; border-left:5px solid #0066cc; border-radius:6px; padding:0.9rem 1.1rem; margin:0.65rem 0; color:#003366; font-size:1rem; line-height:1.65; }
        .dg-warn-light   { background:#fff8e0; border-left:5px solid #cc8800; border-radius:6px; padding:0.9rem 1.1rem; margin:0.65rem 0; color:#5c3d00; font-size:1rem; line-height:1.65; }
        .dg-danger-light { background:#fff0f0; border-left:5px solid #cc0022; border-radius:6px; padding:0.9rem 1.1rem; margin:0.65rem 0; color:#660011; font-size:1rem; line-height:1.65; }
        .dg-ok-light     { background:#edfff5; border-left:5px solid #008833; border-radius:6px; padding:0.9rem 1.1rem; margin:0.65rem 0; color:#003312; font-size:1rem; line-height:1.65; }

        /* ── Policy summary box ── */
        .dg-summary-box {
            background:#ffffff; border:2px solid #aac4d8; border-radius:10px;
            padding:1.2rem 1.4rem; margin:0.7rem 0 1rem 0;
            color:#0d1f2d; font-size:1rem; line-height:1.8; white-space:pre-wrap;
        }

        /* ── Expander ── */
        [data-testid="stExpander"] { background:#0d2035; border:1px solid #1e3d60; border-radius:10px; }
        [data-testid="stExpander"] summary { color:#cce0f0; font-size:1rem; font-weight:500; }

        /* ── Buttons ── */
        .stButton > button { border-radius:8px; font-weight:700; font-size:1rem; padding:0.45rem 1.2rem; }
        .stButton > button[kind="primary"] { background-color:#007a55; color:#ffffff; border:none; }
        .stButton > button[kind="primary"]:hover { background-color:#00a370; }
        .stButton > button:focus-visible { outline:3px solid #00e8bb !important; outline-offset:2px !important; }

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab"] { color:#aac4d8; font-weight:600; font-size:1rem; }
        .stTabs [aria-selected="true"] { color:#00e8bb !important; border-bottom:3px solid #00e8bb !important; }

        /* ── Inputs ── */
        .stTextInput input, .stSelectbox select, .stTextArea textarea {
            background:#0d2035 !important; border:2px solid #2a4d70 !important;
            color:#f0f4f8 !important; border-radius:6px !important; font-size:1rem !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color:#00e8bb !important; box-shadow:0 0 0 3px rgba(0,232,187,0.3) !important;
        }
        [data-baseweb="select"] { background:#0d2035 !important; border-color:#2a4d70 !important; }
        [data-baseweb="select"] > div { background:#0d2035 !important; color:#f0f4f8 !important; }

        /* ── Progress bar ── */
        [data-testid="stProgress"] > div > div { background-color:#00e8bb !important; }

        /* ── Misc ── */
        hr { border-color:#1e3d60 !important; }
        .stCaption, small, caption { color:#aac4d8 !important; font-size:0.9rem !important; }
        ::-webkit-scrollbar { width:7px; }
        ::-webkit-scrollbar-track { background:#0b1a28; }
        ::-webkit-scrollbar-thumb { background:#2a4d70; border-radius:4px; }
        ::-webkit-scrollbar-thumb:hover { background:#00e8bb; }
        a { color:#66ccff !important; text-decoration:underline; }
        a:hover { color:#00e8bb !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# SECTION: DATA  (from sections/data.py)
# ══════════════════════════════════════════════════════════════════════════════

APPS = {
    "Facebook": {
        "icon": "📘", "developer": "Meta Platforms, Inc.",
        "website": "https://www.facebook.com",
        "privacy_policy": "https://www.facebook.com/privacy/policy/",
        "policy_updated": "September 2023",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo", "status_label": "Demo Data", "category": "Social Media",
        "summary": (
            "Facebook is a social networking service operated by Meta Platforms. "
            "It collects a broad range of personal data including profile information, "
            "location, contacts, browsing activity (via the Meta Pixel and partner sites), "
            "messages (not end-to-end encrypted by default on Facebook), and device data. "
            "It shares information with Meta-family companies, advertisers, and service providers. "
            "Third-party applications connected via Facebook Login may receive profile data and "
            "friend-list information depending on the scopes authorised."
        ),
        "data_categories": [
            "Profile information (name, photo, birthday, email)",
            "Location (if permitted)", "Contacts (if permitted)",
            "Browsing & activity data (on and off Facebook via Meta Pixel)",
            "Device & connection information", "Messages (not E2EE by default)",
            "Payment information (if used)",
        ],
        "permissions": ["Location", "Camera", "Microphone", "Contacts", "Photos & Media",
                        "Notifications", "Files & Storage"],
        "third_party_sharing": (
            "Meta shares data with advertisers (in aggregate or via targeting), "
            "service providers, Meta-family apps (Instagram, WhatsApp), "
            "and third-party applications authorised by the user via Facebook Login. "
            "Data may also be shared under legal requirements."
        ),
        "risks": [
            "Broad third-party app access via Facebook Login (OAuth scopes)",
            "Cross-site tracking via Meta Pixel on external websites",
            "Data profiling for targeted advertising",
            "Historical case: Cambridge Analytica accessed ~87 million user profiles via a connected quiz app (2014–2018)",
            "Session-token theft enabling account takeover",
        ],
        "actions": [
            "Review connected apps at facebook.com/settings/applications",
            "Check location permission in device Settings → Apps → Facebook",
            "Review Ad Preferences at facebook.com/adpreferences",
            "Enable two-factor authentication",
        ],
        "official_settings": "https://www.facebook.com/settings",
        "connected_apps_link": "https://www.facebook.com/settings?tab=applications",
    },
    "Instagram": {
        "icon": "📸", "developer": "Meta Platforms, Inc.",
        "website": "https://www.instagram.com",
        "privacy_policy": "https://privacycenter.instagram.com/policy/",
        "policy_updated": "September 2023",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo", "status_label": "Demo Data", "category": "Social Media",
        "summary": (
            "Instagram is a photo and video sharing service owned by Meta. "
            "It collects profile data, photos, videos, messages (not E2EE by default), "
            "location, device data, and browsing activity. "
            "As a Meta product it shares infrastructure and data practices with Facebook. "
            "Third-party logins and connected shopping integrations may expose additional data."
        ),
        "data_categories": [
            "Profile information", "Photos & videos", "Location", "Device data",
            "Messages (not E2EE by default)", "Browsing & interaction data",
        ],
        "permissions": ["Camera", "Microphone", "Location", "Photos & Media",
                        "Contacts", "Notifications"],
        "third_party_sharing": (
            "Shared with Meta-family companies, advertisers, and service providers. "
            "Instagram Shopping integrations may share purchase intent data with sellers."
        ),
        "risks": [
            "Cross-platform tracking with Facebook via shared Meta infrastructure",
            "Broad camera/microphone access for Stories and Reels",
            "Third-party shopping integrations receiving browsing and purchase data",
        ],
        "actions": [
            "Review account Privacy Settings in the Instagram app",
            "Check connected apps at instagram.com/accounts/manage_access",
            "Limit location to 'While Using' only",
            "Enable two-factor authentication",
        ],
        "official_settings": "https://www.instagram.com/accounts/privacy_and_security/",
        "connected_apps_link": "https://www.instagram.com/accounts/manage_access/",
    },
    "WhatsApp": {
        "icon": "💬", "developer": "Meta Platforms, Inc.",
        "website": "https://www.whatsapp.com",
        "privacy_policy": "https://www.whatsapp.com/legal/privacy-policy/",
        "policy_updated": "September 2023",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo", "status_label": "Demo Data", "category": "Messaging",
        "summary": (
            "WhatsApp is an end-to-end encrypted messaging service owned by Meta. "
            "Message content is E2EE by default. However, metadata — including who you "
            "communicate with, frequency, and device information — is collected and shared with Meta. "
            "Contact information is uploaded to provide the service. "
            "Backup messages stored on Google Drive or iCloud are not covered by WhatsApp E2EE unless "
            "end-to-end encrypted backup is enabled."
        ),
        "data_categories": [
            "Phone number", "Contacts (uploaded)", "Message metadata",
            "Device & connection data", "Usage data", "Profile photo & status (if public)",
        ],
        "permissions": ["Contacts", "Camera", "Microphone", "Photos & Media",
                        "Notifications", "Files & Storage"],
        "third_party_sharing": (
            "Metadata shared with Meta-family companies. "
            "Businesses using the WhatsApp Business API may use third-party service providers."
        ),
        "risks": [
            "Metadata collection even though message content is E2EE",
            "Contact upload exposes your address book to Meta servers",
            "Cloud backups (without E2EE backup enabled) are not protected by WhatsApp encryption",
        ],
        "actions": [
            "Enable End-to-End Encrypted Backup: Settings → Chats → Chat Backup",
            "Review privacy settings: Settings → Privacy",
            "Limit profile visibility to Contacts only",
            "Enable two-step verification: Settings → Account → Two-step verification",
        ],
        "official_settings": "https://www.whatsapp.com/legal/privacy-policy/",
        "connected_apps_link": None,
    },
    "Snapchat": {
        "icon": "👻", "developer": "Snap Inc.",
        "website": "https://www.snapchat.com",
        "privacy_policy": "https://snap.com/en-US/privacy/privacy-policy",
        "policy_updated": "February 2024",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo", "status_label": "Demo Data", "category": "Social Media",
        "summary": (
            "Snapchat is a multimedia messaging app. Despite its ephemeral message concept, "
            "Snap collects significant data including location (Snap Map), contacts, device information, "
            "and usage patterns. In 2014, approximately 4.6 million usernames and phone numbers were "
            "exposed via an unofficial API exploitation (Find Friends feature). "
            "Snap Map shares real-time location with friends unless Ghost Mode is enabled."
        ),
        "data_categories": [
            "Username & profile data", "Location (Snap Map)", "Contacts",
            "Snaps & Stories metadata", "Device data", "Usage patterns",
        ],
        "permissions": ["Camera", "Microphone", "Location", "Contacts",
                        "Photos & Media", "Notifications"],
        "third_party_sharing": (
            "Shared with service providers, advertisers, and analytics partners. "
            "Snap Audience Network enables ad targeting across partner apps."
        ),
        "risks": [
            "Real-time location sharing via Snap Map (unless Ghost Mode is enabled)",
            "2014 API incident: ~4.6M usernames and partial phone numbers exposed via Find Friends API abuse",
            "Contact upload to match users",
            "Snaps/Stories may be retained by Snap's servers longer than users expect",
        ],
        "actions": [
            "Enable Ghost Mode: Snap Map → Settings icon → Ghost Mode",
            "Review who can see your location: Settings → See My Location",
            "Limit 'Find Me by Phone Number' to Friends only",
            "Review connected apps in Snap Account settings",
        ],
        "official_settings": "https://accounts.snapchat.com/",
        "connected_apps_link": "https://accounts.snapchat.com/",
    },
    "Telegram": {
        "icon": "✈️", "developer": "Telegram FZ-LLC",
        "website": "https://telegram.org",
        "privacy_policy": "https://telegram.org/privacy",
        "policy_updated": "August 2023",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo", "status_label": "Demo Data", "category": "Messaging",
        "summary": (
            "Telegram is a cloud-based messaging app. Regular chats are encrypted in transit "
            "but stored on Telegram's servers in a decryptable form. "
            "Only 'Secret Chats' use client-to-client end-to-end encryption. "
            "Group chats and channels are not E2EE. Telegram bots and mini-apps may access "
            "user data depending on their implementation."
        ),
        "data_categories": [
            "Phone number", "Contacts", "Messages (stored on servers except Secret Chats)",
            "Media files", "IP address", "Device data",
        ],
        "permissions": ["Contacts", "Camera", "Microphone", "Photos & Media",
                        "Notifications", "Files & Storage"],
        "third_party_sharing": (
            "Telegram states it does not sell data to advertisers. "
            "Data may be shared under legal requirements. "
            "Third-party bots and mini-apps interact with Telegram's Bot API and may collect their own data."
        ),
        "risks": [
            "Regular chats are NOT end-to-end encrypted",
            "Bots and mini-apps may access message content depending on group settings",
            "Phone number visible to anyone who has your number (unless hidden in settings)",
            "Large public channels are unencrypted and may be monitored",
        ],
        "actions": [
            "Use Secret Chats for sensitive conversations",
            "Set phone number visibility: Settings → Privacy and Security → Phone Number",
            "Review active sessions: Settings → Privacy and Security → Active Sessions",
            "Enable Two-Step Verification: Settings → Privacy and Security",
        ],
        "official_settings": "https://telegram.org/privacy",
        "connected_apps_link": None,
    },
    "Amazon": {
        "icon": "🛒", "developer": "Amazon.com, Inc.",
        "website": "https://www.amazon.com",
        "privacy_policy": "https://www.amazon.com/gp/help/customer/display.html?nodeId=GX7NJQ4ZB8MHFRNJ",
        "policy_updated": "August 2023",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo", "status_label": "Demo Data", "category": "E-Commerce",
        "summary": (
            "Amazon collects extensive purchase, browsing, search, and device data to power "
            "its recommendations and advertising ecosystem. "
            "Amazon Advertising (formerly Amazon DSP) enables cross-site tracking. "
            "Alexa voice assistant (if used) records and processes voice data. "
            "Amazon shares data with third-party sellers on its marketplace."
        ),
        "data_categories": [
            "Purchase history", "Search & browsing history", "Payment information",
            "Shipping address", "Device & Alexa data", "Location",
        ],
        "permissions": ["Notifications", "Camera", "Microphone (Alexa)", "Location"],
        "third_party_sharing": (
            "Shared with third-party sellers, advertisers, AWS partners, and service providers. "
            "Amazon Advertising enables retargeting across the web."
        ),
        "risks": [
            "Extensive purchase and browsing profiling for advertising",
            "Voice recordings stored and analysed by Alexa",
            "Third-party marketplace sellers receiving order data",
            "Login with Amazon OAuth scopes may expose profile data to connected apps",
        ],
        "actions": [
            "Review Alexa voice history: Alexa app → More → Activity",
            "Manage advertising preferences: amazon.com/adprefs",
            "Review login with Amazon authorisations: amazon.com/ap/adam",
            "Enable two-step verification",
        ],
        "official_settings": "https://www.amazon.com/gp/css/homepage.html",
        "connected_apps_link": "https://www.amazon.com/ap/adam",
    },
    "Flipkart": {
        "icon": "🛍️", "developer": "Flipkart Internet Pvt. Ltd.",
        "website": "https://www.flipkart.com",
        "privacy_policy": "https://www.flipkart.com/pages/privacypolicy",
        "policy_updated": "2023 (approximate)",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo", "status_label": "Demo Data", "category": "E-Commerce",
        "summary": (
            "Flipkart is a major Indian e-commerce platform owned by Walmart. "
            "It collects purchase history, device data, payment information, and location. "
            "Flipkart uses analytics and advertising SDKs. "
            "Login via Google/Facebook OAuth may share profile scopes with Flipkart."
        ),
        "data_categories": [
            "Purchase history", "Payment information", "Shipping address",
            "Device & browser data", "Location", "Search history",
        ],
        "permissions": ["Location", "Camera", "Notifications", "Photos & Media", "Files & Storage"],
        "third_party_sharing": (
            "Shared with seller partners, payment processors, logistics providers, "
            "advertising networks, and analytics providers."
        ),
        "risks": [
            "Payment data shared with multiple processors",
            "Location used for delivery but may be retained beyond necessity",
            "Analytics SDKs may collect device fingerprinting data",
        ],
        "actions": [
            "Review location permission — allow only While Using",
            "Check saved payment methods and remove unused cards",
            "Review linked social logins in account settings",
        ],
        "official_settings": "https://www.flipkart.com/account",
        "connected_apps_link": None,
    },
    "Myntra": {
        "icon": "👗", "developer": "Myntra Designs Pvt. Ltd. (Flipkart Group)",
        "website": "https://www.myntra.com",
        "privacy_policy": "https://www.myntra.com/privacypolicy",
        "policy_updated": "2023 (approximate)",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo", "status_label": "Demo Data", "category": "E-Commerce",
        "summary": (
            "Myntra is a fashion e-commerce platform in India, part of the Flipkart Group. "
            "It collects browsing, purchase, and style preference data for personalised recommendations. "
            "It uses advertising and analytics SDKs and may share data within the Flipkart Group."
        ),
        "data_categories": [
            "Purchase & browse history", "Style preferences", "Payment information",
            "Shipping address", "Device data", "Location",
        ],
        "permissions": ["Location", "Camera", "Notifications", "Photos & Media"],
        "third_party_sharing": (
            "Shared with Flipkart Group, brand partners, payment processors, "
            "logistics providers, and advertising networks."
        ),
        "risks": [
            "Style and preference profiling for targeted advertising",
            "Data sharing within the Flipkart Group ecosystem",
            "Camera access used for virtual try-on features",
        ],
        "actions": [
            "Limit location to While Using only",
            "Review saved payment methods",
            "Check notification permissions",
        ],
        "official_settings": "https://www.myntra.com/profile",
        "connected_apps_link": None,
    },
    "Rapido": {
        "icon": "🛵", "developer": "Roppen Transportation Services Pvt. Ltd.",
        "website": "https://rapido.bike",
        "privacy_policy": "https://rapido.bike/privacy-policy",
        "policy_updated": "2023 (approximate)",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo", "status_label": "Demo Data", "category": "Ride-Hailing",
        "summary": (
            "Rapido is an Indian bike-taxi and auto-rickshaw aggregator. "
            "It requires precise location access to match riders with captains. "
            "It collects ride history, payment data, and device information. "
            "Real-time location is a core requirement for the service."
        ),
        "data_categories": [
            "Precise location (real-time)", "Ride history", "Phone number",
            "Payment information", "Device data",
        ],
        "permissions": ["Location", "Camera", "Contacts", "Notifications",
                        "Phone Access", "Files & Storage"],
        "third_party_sharing": (
            "Shared with payment processors, insurance partners, mapping providers, "
            "and analytics services."
        ),
        "risks": [
            "Continuous location tracking during rides",
            "Location history may reveal home/work addresses and daily routines",
            "Phone number shared with captains during rides",
        ],
        "actions": [
            "Set location to 'While Using' so background tracking is limited",
            "Review ride history and delete if possible",
            "Use UPI or masked payment methods to limit payment data exposure",
        ],
        "official_settings": "https://rapido.bike",
        "connected_apps_link": None,
    },
}

PERMISSIONS = {
    "Location": {
        "icon": "📍",
        "what_it_means": (
            "Allows the app to read your device's geographic coordinates, "
            "either precisely (GPS) or approximately (network-based). "
            "Some apps distinguish between 'While Using' and 'Always' (background) access."
        ),
        "why_requested": [
            "Navigation and maps (core feature)",
            "Ride-hailing — matching with nearby drivers",
            "Local search — showing nearby restaurants, shops",
            "Weather based on your current location",
            "Check-in and location tagging in social posts",
        ],
        "data_exposed": (
            "Your current position, movement patterns, frequently visited places "
            "(home, work, religious sites, medical facilities), travel history, and daily routine."
        ),
        "when_unnecessary": (
            "A messaging app that is not location-enabled, a shopping app that only ships "
            "to a manually typed address, or any app that requests 'Always On' access "
            "when it only needs location during active use."
        ),
        "risks": (
            "Persistent location access can reveal home/work addresses, religious attendance, "
            "medical appointments, and other sensitive patterns. This data may be sold to data "
            "brokers or used for highly targeted advertising."
        ),
        "recommended_action": "review",
        "action_text": (
            "Grant location only 'While Using' unless background access is essential to the app's function. "
            "Deny location entirely to apps where the feature is unrelated to location services."
        ),
        "risk_level": "review",
    },
    "Camera": {
        "icon": "📷",
        "what_it_means": "Allows the app to activate the device camera and capture photos or video.",
        "why_requested": [
            "Video calling or live streaming", "Scanning QR codes or barcodes",
            "Capturing photos to post or share", "Augmented reality features (filters, try-on)",
            "Document scanning",
        ],
        "data_exposed": (
            "Any image or video captured while the app is in use. "
            "Photos may contain embedded metadata (EXIF) including location, device model, and timestamp."
        ),
        "when_unnecessary": (
            "Any app that has no photo, video, or scanning feature. "
            "An e-commerce app that only shows product listings does not need camera access."
        ),
        "risks": (
            "Malicious or poorly secured apps could capture images without obvious user awareness. "
            "EXIF metadata in shared photos can reveal location even when location permission is denied."
        ),
        "recommended_action": "low",
        "action_text": (
            "Allow camera access to apps that genuinely use it. "
            "Consider stripping EXIF data from photos before sharing online."
        ),
        "risk_level": "low",
    },
    "Microphone": {
        "icon": "🎤",
        "what_it_means": "Allows the app to record audio through the device microphone.",
        "why_requested": [
            "Voice or video calls", "Voice-to-text / dictation", "Voice search",
            "Audio messages", "Voice assistants (Alexa, Siri, Google Assistant integrations)",
        ],
        "data_exposed": (
            "Any audio captured while the app has microphone access. "
            "This could include conversations, background sounds, and environmental audio."
        ),
        "when_unnecessary": "A shopping or news app with no calling, voice search, or audio recording feature.",
        "risks": (
            "Continuous microphone access is one of the most sensitive permissions. "
            "Voice assistant data is often processed on remote servers."
        ),
        "recommended_action": "review",
        "action_text": (
            "Allow microphone only to apps that require it for a clear, stated function. "
            "Revoke for apps where you no longer use audio features."
        ),
        "risk_level": "review",
    },
    "Contacts": {
        "icon": "👥",
        "what_it_means": "Allows the app to read your device address book, including names, phone numbers, and email addresses.",
        "why_requested": [
            "Finding friends who are already on the service",
            "Sending invitations to contacts",
            "Autofill for sending payments or messages",
        ],
        "data_exposed": (
            "The entire contents of your address book — including names, numbers, emails, "
            "and notes — are typically uploaded to the app's servers. "
            "This exposes data about people who have not consented to share their information with the app."
        ),
        "when_unnecessary": (
            "Any app that does not offer contact-matching, friend-finding, or invitation features. "
            "Contact access is often granted during onboarding and then forgotten."
        ),
        "risks": (
            "Your contacts have not agreed to have their data uploaded. "
            "Contact data is used to build social graphs and identify relationships. "
            "In the Snapchat Find Friends incident (2014), contact matching via an unofficial API "
            "was exploited to expose approximately 4.6 million usernames and partial phone numbers."
        ),
        "recommended_action": "review",
        "action_text": (
            "Consider denying contact access to apps where friend-finding is not important to you. "
            "If you grant access, be aware that your contacts' data is shared without their explicit consent."
        ),
        "risk_level": "review",
    },
    "Photos & Media": {
        "icon": "🖼️",
        "what_it_means": "Allows the app to read, and sometimes write, photos and media files on your device.",
        "why_requested": [
            "Selecting profile pictures or post images", "Sharing photos in messages",
            "Downloading media received in the app", "Saving screenshots or generated content",
        ],
        "data_exposed": (
            "Depending on the permission level, the app may access all photos on your device, "
            "including photos with embedded location data, screenshots, and downloaded documents."
        ),
        "when_unnecessary": (
            "Apps that do not involve sharing, editing, or displaying user photos. "
            "On modern Android and iOS, you can grant access to selected photos only."
        ),
        "risks": (
            "Broad photo library access allows an app to view all stored images. "
            "Photos taken with location enabled contain GPS coordinates in their metadata."
        ),
        "recommended_action": "review",
        "action_text": (
            "On iOS, choose 'Selected Photos' rather than 'All Photos' where possible. "
            "On Android, check whether the app uses the photo picker (which does not expose the whole library)."
        ),
        "risk_level": "review",
    },
    "Files & Storage": {
        "icon": "📁",
        "what_it_means": "Allows the app to read and write files on device storage.",
        "why_requested": [
            "Caching media for offline use", "Downloading files or documents",
            "Saving or opening attachments",
        ],
        "data_exposed": (
            "On older Android versions, this permission gives broad access to all files. "
            "On Android 10 and later, scoped storage limits access to the app's own files."
        ),
        "when_unnecessary": "Apps that don't handle files, documents, or offline media downloads.",
        "risks": (
            "Older devices and apps targeting older Android APIs may still use broad storage access. "
            "A malicious app with storage access could read documents and files."
        ),
        "recommended_action": "review",
        "action_text": (
            "Check whether your device is running Android 10 or newer, which limits storage scope. "
            "Revoke storage from apps that have no legitimate file-handling use case."
        ),
        "risk_level": "review",
    },
    "Calendar": {
        "icon": "📅",
        "what_it_means": "Allows the app to read and, sometimes, write events to your device calendar.",
        "why_requested": [
            "Adding ride or order reminders", "Scheduling events from the app",
            "Productivity or meeting integrations",
        ],
        "data_exposed": (
            "Event titles, dates, times, locations, attendees, and notes in your calendar. "
            "This can reveal appointments at medical facilities, legal offices, or personal events."
        ),
        "when_unnecessary": "Social media, shopping, or entertainment apps that don't involve scheduling.",
        "risks": "Calendar data can reveal sensitive personal information. Attendee information exposes other people's data.",
        "recommended_action": "review",
        "action_text": "Deny calendar access to apps where scheduling is not a core feature.",
        "risk_level": "review",
    },
    "Notifications": {
        "icon": "🔔",
        "what_it_means": "Allows the app to send push notifications to your device.",
        "why_requested": [
            "Alerting you to messages, updates, or order status",
            "Sending marketing or promotional messages",
            "Security alerts (e.g. login notifications)",
        ],
        "data_exposed": (
            "Notification content may include message previews, order details, or personal information "
            "visible on the lock screen."
        ),
        "when_unnecessary": "Apps you use infrequently where notifications would be unwanted.",
        "risks": (
            "Notification abuse for spam or phishing (fake security alerts). "
            "Notification content visible on the lock screen may expose private information."
        ),
        "recommended_action": "low",
        "action_text": (
            "Allow notifications from apps where they are genuinely useful. "
            "Disable lock-screen notification previews for sensitive apps."
        ),
        "risk_level": "low",
    },
    "SMS": {
        "icon": "💬",
        "what_it_means": "Allows the app to send, receive, and read SMS messages.",
        "why_requested": [
            "Auto-reading OTP codes for two-factor authentication (with user awareness)",
            "Messaging apps that operate over SMS",
        ],
        "data_exposed": (
            "All SMS messages on the device, including one-time passwords, "
            "bank transaction alerts, and personal conversations."
        ),
        "when_unnecessary": "Any app that is not a dedicated SMS or messaging application and does not need OTP autofill.",
        "risks": (
            "SMS access by a malicious app could intercept two-factor authentication codes, "
            "bank alerts, and private messages. This is a high-sensitivity permission."
        ),
        "recommended_action": "high",
        "action_text": (
            "Grant SMS access only to apps that explicitly require it for OTP autofill or messaging. "
            "Prefer authenticator apps over SMS for two-factor authentication where possible."
        ),
        "risk_level": "high",
    },
    "Phone Access": {
        "icon": "📞",
        "what_it_means": "Allows the app to read the device phone number, IMEI, and call state.",
        "why_requested": [
            "Autofilling the phone number during registration",
            "Detecting incoming calls to pause media",
        ],
        "data_exposed": (
            "Device identifiers (IMEI, IMSI), phone number, and call state. "
            "These can be used for device fingerprinting."
        ),
        "when_unnecessary": "Apps where phone number autofill is not needed and call detection is irrelevant.",
        "risks": (
            "IMEI and IMSI are persistent identifiers useful for cross-app tracking and fingerprinting. "
            "They cannot be reset like advertising IDs."
        ),
        "recommended_action": "review",
        "action_text": "Grant phone access only to apps where registration autofill is a clear benefit.",
        "risk_level": "review",
    },
    "Bluetooth & Nearby Devices": {
        "icon": "📶",
        "what_it_means": "Allows the app to scan for and connect to nearby Bluetooth devices.",
        "why_requested": [
            "Pairing with wearables, speakers, or IoT devices",
            "Proximity-based features (finding nearby friends)",
            "Contact tracing features",
        ],
        "data_exposed": (
            "Nearby Bluetooth device names and identifiers. "
            "This can be used for indoor location tracking even when GPS is denied."
        ),
        "when_unnecessary": "Apps with no wearable, proximity, or smart-home integration.",
        "risks": (
            "Bluetooth scanning can reveal your precise indoor location and nearby devices. "
            "Social media apps requesting Bluetooth access for 'proximity features' "
            "may use it for location inference."
        ),
        "recommended_action": "review",
        "action_text": "Deny Bluetooth access to apps that have no obvious hardware pairing or proximity feature.",
        "risk_level": "review",
    },
}

RISK_LABELS = {
    "low":     ("🟢", "Lower Concern",                "badge-low"),
    "review":  ("🟡", "Review Recommended",           "badge-review"),
    "high":    ("🔴", "Higher Concern",               "badge-high"),
    "unknown": ("⚪", "Unknown / Insufficient Evidence", "badge-unknown"),
}

STATUS_LABELS = {
    "demo":     ("status-demo",    "⚠️ Demo Data"),
    "verified": ("status-verified","✅ Source Verified"),
    "review":   ("status-review",  "🔍 Needs Review"),
    "updated":  ("status-updated", "📋 Policy Update Detected"),
}

GLOSSARY = {
    "OAuth": (
        "An open standard that lets you authorise a third-party app to access your account "
        "on another service (e.g. 'Login with Google') without sharing your password. "
        "The scope of access granted depends on what permissions are requested."
    ),
    "API Scope": (
        "A defined boundary of access within an API. For example, an OAuth scope might allow "
        "an app to read your profile but not post on your behalf. Overly broad scopes increase risk."
    ),
    "Access Token": (
        "A credential issued after authorisation that allows an app to make API requests "
        "on your behalf. If stolen, an attacker can access your account without your password "
        "until the token expires or is revoked."
    ),
    "Session Token / Cookie": (
        "A small identifier stored in your browser that keeps you logged in. "
        "If stolen via XSS or a network attack, it can be used to hijack your session."
    ),
    "SDK (Software Development Kit)": (
        "A package of code that developers embed in their app to add features like analytics, "
        "advertising, or crash reporting. The SDK may collect data as part of its function, "
        "depending on its implementation."
    ),
    "Tracking Pixel": (
        "A tiny invisible image embedded in a webpage or email. When it loads, it signals "
        "to the tracking server that the page or email was opened, often including IP address "
        "and browser details."
    ),
    "Meta Pixel (formerly Facebook Pixel)": (
        "A tracking script placed on external websites by Meta that reports browsing activity "
        "back to Meta for advertising purposes, even for users not actively using Facebook."
    ),
    "Data Profiling": (
        "The process of combining data from multiple sources to build a detailed picture of "
        "an individual's interests, behaviour, finances, health, or relationships."
    ),
    "Data Broker": (
        "A company that collects personal data from various sources and sells or shares it "
        "with third parties, often without the individual's direct knowledge."
    ),
    "End-to-End Encryption (E2EE)": (
        "A method of communication where only the communicating parties can read the messages. "
        "Even the service provider cannot read the content. Metadata (who communicated with whom "
        "and when) may still be collected."
    ),
    "Metadata": (
        "Data about data. For example, who you called, when, and for how long — "
        "without revealing the conversation content. Metadata can be as revealing as content."
    ),
    "Phishing": (
        "An attack where an adversary impersonates a trusted entity (a login page, email, "
        "or message) to trick users into revealing credentials or installing malware."
    ),
    "XSS (Cross-Site Scripting)": (
        "An attack where malicious scripts are injected into a trusted website, "
        "potentially stealing cookies, session tokens, or other sensitive data."
    ),
    "CSRF (Cross-Site Request Forgery)": (
        "An attack that tricks a user's browser into making unintended requests "
        "to a site where they are authenticated, potentially changing settings or transferring data."
    ),
}

POLICY_CHANGES = [
    {
        "app": "Facebook", "date": "September 2023", "status": "change_detected",
        "summary": (
            "Meta updated its Privacy Policy to reflect new AI training data practices "
            "and updated information about data use across Meta technologies."
        ),
        "old_excerpt": "We use information we have to show you ads that we think will be relevant to you.",
        "new_excerpt": (
            "We use information we have, including your activity on and off Meta technologies, "
            "to show you ads, offers, and other sponsored content we think will be relevant to you. "
            "We also use this information to train AI models."
        ),
        "note": "⚠️ This is demonstration data based on publicly reported policy updates.",
        "policy_link": "https://www.facebook.com/privacy/policy/",
    },
    {
        "app": "Snapchat", "date": "February 2024", "status": "change_detected",
        "summary": (
            "Snap updated its Privacy Policy to include new sections on My AI, "
            "the Snapchat AI chatbot, including what data My AI can access "
            "and how conversations may be used."
        ),
        "old_excerpt": "We do not have a dedicated AI assistant feature.",
        "new_excerpt": (
            "My AI may retain your conversations to improve the service. "
            "My AI can see your Snapchat display name and Bitmoji. "
            "If you choose to share your location with My AI, it can access that too."
        ),
        "note": "⚠️ This is demonstration data based on publicly reported policy updates.",
        "policy_link": "https://snap.com/en-US/privacy/privacy-policy",
    },
    {
        "app": "WhatsApp", "date": "No recent change detected in demo data",
        "status": "no_change",
        "summary": "No significant policy change was detected in the demonstration comparison.",
        "old_excerpt": None, "new_excerpt": None,
        "note": "⚠️ This is demonstration data. Live policy monitoring is not active.",
        "policy_link": "https://www.whatsapp.com/legal/privacy-policy/",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# SECTION: POLICY_DATA  (from sections/policy_data.py)
# ══════════════════════════════════════════════════════════════════════════════

REGIONS = {
    "India": "India",
    "United States": "United States",
    "Global": "Global / Not region-specific",
}

POLICY_CATEGORIES = [
    ("privacy_policy",        "Privacy Policy"),
    ("terms_of_service",      "Terms of Service"),
    ("community_guidelines",  "Community Guidelines & Acceptable Use"),
    ("third_party",           "Third-Party Material & Services"),
    ("limitation_liability",  "Limitation of Liability"),
    ("arbitration",           "Arbitration & Legal Dispute Waivers"),
]

PLATFORM_CATEGORIES = {
    "Messaging & Social Networking": ["WhatsApp", "Instagram", "Facebook", "Telegram", "Snapchat"],
    "E-Commerce": ["Flipkart", "Google", "Gmail"],
    "Search, Email & Online Services": ["Google", "Gmail"],
}

AVAILABILITY_STYLES = {
    "Verified":           ("status-verified", "✅ Verified"),
    "Partially verified": ("status-review",   "🔍 Partially Verified"),
    "Embedded":           ("status-demo",     "📎 Embedded in Larger Doc"),
    "Not found":          ("badge-unknown",   "⚪ Not Found"),
    "Region-specific":    ("status-updated",  "📋 Region-Specific"),
}

BASE_PROMPT = """You are a privacy-focused legal-document explainer. Read the complete official policy text I provide below. Explain it in simple English that a Grade 10 student can understand.\n\nPolicy text:\n[PASTE THE COMPLETE POLICY TEXT HERE]"""

PRIVACY_PROMPT_TEMPLATE = """You are a privacy-focused legal-document explainer for {platform}'s Privacy Policy.\n\nRead the complete Privacy Policy text I paste below and explain it in simple English.\n\nPolicy text:\n[PASTE THE COMPLETE PRIVACY POLICY TEXT HERE]"""

TOS_PROMPT_TEMPLATE = """You are a legal-document explainer for {platform}'s Terms of Service.\n\nRead the complete Terms of Service text I paste below and explain it in simple English.\n\nTerms of Service text:\n[PASTE THE COMPLETE TERMS OF SERVICE TEXT HERE]"""

COMMUNITY_PROMPT_TEMPLATE = """You are a legal-document explainer for {platform}'s Community Guidelines.\n\nRead the complete document text I paste below and explain it in simple English.\n\nPolicy text:\n[PASTE THE COMPLETE COMMUNITY GUIDELINES TEXT HERE]"""

THIRD_PARTY_PROMPT_TEMPLATE = """You are a legal-document explainer for {platform}'s third-party material provisions.\n\nRead the supplied text and explain it in simple English.\n\nPolicy text:\n[PASTE THE RELEVANT POLICY TEXT HERE]"""

LIABILITY_PROMPT_TEMPLATE = """You are a legal-document explainer for {platform}'s Limitation of Liability clause.\n\nRead the supplied text and explain it in simple English.\n\nPolicy text:\n[PASTE THE LIMITATION OF LIABILITY CLAUSE TEXT HERE]"""

ARBITRATION_PROMPT_TEMPLATE = """You are a legal-document explainer for {platform}'s Arbitration and Dispute Resolution provisions.\n\nRead the supplied text and explain it in simple English.\n\nPolicy text:\n[PASTE THE DISPUTE RESOLUTION / ARBITRATION CLAUSE TEXT HERE]"""


def build_prompt(platform: str, category_key: str) -> str:
    templates = {
        "privacy_policy":       PRIVACY_PROMPT_TEMPLATE,
        "terms_of_service":     TOS_PROMPT_TEMPLATE,
        "community_guidelines": COMMUNITY_PROMPT_TEMPLATE,
        "third_party":          THIRD_PARTY_PROMPT_TEMPLATE,
        "limitation_liability": LIABILITY_PROMPT_TEMPLATE,
        "arbitration":          ARBITRATION_PROMPT_TEMPLATE,
    }
    tmpl = templates.get(category_key, BASE_PROMPT)
    return tmpl.replace("{platform}", platform)


PLATFORMS = {
    "WhatsApp": {
        "icon": "💬", "category": "Messaging & Social Networking",
        "developer": "Meta Platforms, Inc.",
        "description": "End-to-end encrypted messaging and voice/video calling service.",
        "official_home": "https://www.whatsapp.com/legal/",
        "policies": {
            "privacy_policy": {
                "title": "WhatsApp Privacy Policy",
                "url": "https://www.whatsapp.com/legal/privacy-policy/",
                "region_urls": {
                    "India": "https://www.whatsapp.com/legal/privacy-policy/",
                    "United States": "https://www.whatsapp.com/legal/privacy-policy/",
                    "Global": "https://www.whatsapp.com/legal/privacy-policy/",
                },
                "availability_status": "Verified",
                "applicable_region": "Global (with regional notes inside)",
                "last_updated": "September 2023 (per Meta disclosure)",
                "last_verified": "June 2025",
                "notes": "Single global policy. Regional variations for Indian users noted inside the document.",
            },
            "terms_of_service": {
                "title": "WhatsApp Terms of Service",
                "url": "https://www.whatsapp.com/legal/terms-of-service/",
                "region_urls": {
                    "India": "https://www.whatsapp.com/legal/terms-of-service/",
                    "United States": "https://www.whatsapp.com/legal/terms-of-service/",
                    "Global": "https://www.whatsapp.com/legal/terms-of-service/",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "September 2023",
                "last_verified": "June 2025",
                "notes": "Global terms. US arbitration clause may not apply to Indian users.",
            },
            "community_guidelines": {
                "title": "WhatsApp Usage Policy (Acceptable Use)",
                "url": "https://www.whatsapp.com/legal/acceptable-use-policy/",
                "region_urls": {
                    "India": "https://www.whatsapp.com/legal/acceptable-use-policy/",
                    "United States": "https://www.whatsapp.com/legal/acceptable-use-policy/",
                    "Global": "https://www.whatsapp.com/legal/acceptable-use-policy/",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "Not specified",
                "last_verified": "June 2025",
                "notes": "WhatsApp uses an Acceptable Use Policy rather than Community Guidelines.",
            },
            "third_party": {
                "title": "Third-Party Services — WhatsApp Terms of Service",
                "url": "https://www.whatsapp.com/legal/terms-of-service/",
                "region_urls": {
                    "India": "https://www.whatsapp.com/legal/terms-of-service/",
                    "Global": "https://www.whatsapp.com/legal/terms-of-service/",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "September 2023",
                "last_verified": "June 2025",
                "notes": "Third-party provisions are embedded in the Terms of Service.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — WhatsApp Terms of Service",
                "url": "https://www.whatsapp.com/legal/terms-of-service/",
                "region_urls": {
                    "India": "https://www.whatsapp.com/legal/terms-of-service/",
                    "Global": "https://www.whatsapp.com/legal/terms-of-service/",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "September 2023",
                "last_verified": "June 2025",
                "notes": "Embedded in Terms of Service. Look for 'Disclaimers and Limitation of Liability'.",
            },
            "arbitration": {
                "title": "Dispute Resolution — WhatsApp Terms of Service",
                "url": "https://www.whatsapp.com/legal/terms-of-service/",
                "region_urls": {
                    "India": "https://www.whatsapp.com/legal/terms-of-service/",
                    "United States": "https://www.whatsapp.com/legal/terms-of-service/",
                    "Global": "https://www.whatsapp.com/legal/terms-of-service/",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global (with US-specific arbitration clause)",
                "last_updated": "September 2023",
                "last_verified": "June 2025",
                "notes": "⚠️ Arbitration and class-action waiver provisions in WhatsApp's ToS are specifically applicable to US users. Indian users are subject to Indian law dispute resolution.",
            },
        },
    },
    "Instagram": {
        "icon": "📸", "category": "Messaging & Social Networking",
        "developer": "Meta Platforms, Inc.",
        "description": "Photo and video sharing social network.",
        "official_home": "https://help.instagram.com/",
        "policies": {
            "privacy_policy": {
                "title": "Instagram Privacy Policy (Meta Privacy Policy)",
                "url": "https://privacycenter.instagram.com/policy/",
                "region_urls": {"India": "https://privacycenter.instagram.com/policy/", "United States": "https://privacycenter.instagram.com/policy/", "Global": "https://privacycenter.instagram.com/policy/"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "September 2023", "last_verified": "June 2025",
                "notes": "Instagram shares its Privacy Policy with Meta.",
            },
            "terms_of_service": {
                "title": "Instagram Terms of Use",
                "url": "https://help.instagram.com/581066165581870",
                "region_urls": {"India": "https://help.instagram.com/581066165581870", "United States": "https://help.instagram.com/581066165581870", "Global": "https://help.instagram.com/581066165581870"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "January 2023", "last_verified": "June 2025",
                "notes": "Instagram-specific Terms of Use.",
            },
            "community_guidelines": {
                "title": "Instagram Community Guidelines",
                "url": "https://help.instagram.com/477434105621119",
                "region_urls": {"India": "https://help.instagram.com/477434105621119", "Global": "https://help.instagram.com/477434105621119"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "Not specified", "last_verified": "June 2025", "notes": "",
            },
            "third_party": {
                "title": "Third-Party Content — Instagram Terms of Use",
                "url": "https://help.instagram.com/581066165581870",
                "region_urls": {"India": "https://help.instagram.com/581066165581870", "Global": "https://help.instagram.com/581066165581870"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "January 2023", "last_verified": "June 2025", "notes": "Embedded in Terms of Use.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Instagram Terms of Use",
                "url": "https://help.instagram.com/581066165581870",
                "region_urls": {"India": "https://help.instagram.com/581066165581870", "Global": "https://help.instagram.com/581066165581870"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "January 2023", "last_verified": "June 2025", "notes": "Embedded in Terms of Use.",
            },
            "arbitration": {
                "title": "Dispute Resolution — Instagram Terms of Use",
                "url": "https://help.instagram.com/581066165581870",
                "region_urls": {"India": "https://help.instagram.com/581066165581870", "United States": "https://help.instagram.com/581066165581870", "Global": "https://help.instagram.com/581066165581870"},
                "availability_status": "Embedded", "applicable_region": "Global (US-specific arbitration provisions)",
                "last_updated": "January 2023", "last_verified": "June 2025",
                "notes": "⚠️ Arbitration/class-action waiver provisions are US-specific. Indian users are subject to Indian law.",
            },
        },
    },
    "Facebook": {
        "icon": "📘", "category": "Messaging & Social Networking",
        "developer": "Meta Platforms, Inc.",
        "description": "Social networking platform.",
        "official_home": "https://www.facebook.com/terms/",
        "policies": {
            "privacy_policy": {
                "title": "Meta Privacy Policy",
                "url": "https://www.facebook.com/privacy/policy/",
                "region_urls": {"India": "https://www.facebook.com/privacy/policy/", "United States": "https://www.facebook.com/privacy/policy/", "Global": "https://www.facebook.com/privacy/policy/"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "September 2023", "last_verified": "June 2025",
                "notes": "Covers Facebook, Instagram, and other Meta products.",
            },
            "terms_of_service": {
                "title": "Facebook Terms of Service",
                "url": "https://www.facebook.com/terms/",
                "region_urls": {"India": "https://www.facebook.com/terms/", "United States": "https://www.facebook.com/terms/", "Global": "https://www.facebook.com/terms/"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "September 2023", "last_verified": "June 2025", "notes": "",
            },
            "community_guidelines": {
                "title": "Facebook Community Standards",
                "url": "https://transparency.fb.com/policies/community-standards/",
                "region_urls": {"India": "https://transparency.fb.com/policies/community-standards/", "Global": "https://transparency.fb.com/policies/community-standards/"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "Updated regularly", "last_verified": "June 2025", "notes": "",
            },
            "third_party": {
                "title": "Third-Party Content — Facebook Terms of Service",
                "url": "https://www.facebook.com/terms/",
                "region_urls": {"India": "https://www.facebook.com/terms/", "Global": "https://www.facebook.com/terms/"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "September 2023", "last_verified": "June 2025", "notes": "Embedded in Terms of Service.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Facebook Terms of Service",
                "url": "https://www.facebook.com/terms/",
                "region_urls": {"India": "https://www.facebook.com/terms/", "Global": "https://www.facebook.com/terms/"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "September 2023", "last_verified": "June 2025", "notes": "Embedded in Terms of Service.",
            },
            "arbitration": {
                "title": "Dispute Resolution — Facebook Terms of Service",
                "url": "https://www.facebook.com/terms/",
                "region_urls": {"India": "https://www.facebook.com/terms/", "United States": "https://www.facebook.com/terms/", "Global": "https://www.facebook.com/terms/"},
                "availability_status": "Embedded", "applicable_region": "Global (US-specific arbitration clause)",
                "last_updated": "September 2023", "last_verified": "June 2025",
                "notes": "⚠️ Arbitration/class-action waiver is US-specific. Indian users dispute under Indian law.",
            },
        },
    },
    "Telegram": {
        "icon": "✈️", "category": "Messaging & Social Networking",
        "developer": "Telegram FZ-LLC",
        "description": "Cloud-based messaging and broadcasting platform.",
        "official_home": "https://telegram.org/",
        "policies": {
            "privacy_policy": {
                "title": "Telegram Privacy Policy", "url": "https://telegram.org/privacy",
                "region_urls": {"India": "https://telegram.org/privacy", "United States": "https://telegram.org/privacy", "Global": "https://telegram.org/privacy"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "August 2023", "last_verified": "June 2025", "notes": "Single global privacy policy.",
            },
            "terms_of_service": {
                "title": "Telegram Terms of Service", "url": "https://telegram.org/tos",
                "region_urls": {"India": "https://telegram.org/tos", "United States": "https://telegram.org/tos", "Global": "https://telegram.org/tos"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "September 2022", "last_verified": "June 2025", "notes": "",
            },
            "community_guidelines": {
                "title": "Telegram Usage Guidelines (within ToS)", "url": "https://telegram.org/tos",
                "region_urls": {"India": "https://telegram.org/tos", "Global": "https://telegram.org/tos"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "September 2022", "last_verified": "June 2025",
                "notes": "Telegram does not publish a separate Community Guidelines document.",
            },
            "third_party": {
                "title": "Third-Party Content — Telegram Privacy Policy & ToS", "url": "https://telegram.org/privacy",
                "region_urls": {"India": "https://telegram.org/privacy", "Global": "https://telegram.org/privacy"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "August 2023", "last_verified": "June 2025", "notes": "",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Telegram Terms of Service", "url": "https://telegram.org/tos",
                "region_urls": {"India": "https://telegram.org/tos", "Global": "https://telegram.org/tos"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "September 2022", "last_verified": "June 2025", "notes": "Embedded in Terms of Service.",
            },
            "arbitration": {
                "title": "Dispute Resolution — Telegram Terms of Service", "url": "https://telegram.org/tos",
                "region_urls": {"India": "https://telegram.org/tos", "Global": "https://telegram.org/tos"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "September 2022", "last_verified": "June 2025",
                "notes": "Review current document for arbitration applicability to Indian users.",
            },
        },
    },
    "Snapchat": {
        "icon": "👻", "category": "Messaging & Social Networking",
        "developer": "Snap Inc.",
        "description": "Multimedia messaging and social media app.",
        "official_home": "https://values.snap.com/",
        "policies": {
            "privacy_policy": {
                "title": "Snap Privacy Policy", "url": "https://values.snap.com/privacy/privacy-policy",
                "region_urls": {"India": "https://values.snap.com/privacy/privacy-policy", "United States": "https://values.snap.com/privacy/privacy-policy", "Global": "https://values.snap.com/privacy/privacy-policy"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "February 2024", "last_verified": "June 2025", "notes": "",
            },
            "terms_of_service": {
                "title": "Snap Terms of Service", "url": "https://values.snap.com/privacy/terms-of-service",
                "region_urls": {"India": "https://values.snap.com/privacy/terms-of-service", "United States": "https://values.snap.com/privacy/terms-of-service", "Global": "https://values.snap.com/privacy/terms-of-service"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "February 2024", "last_verified": "June 2025", "notes": "Includes arbitration clause applicable to US users.",
            },
            "community_guidelines": {
                "title": "Snap Community Guidelines", "url": "https://values.snap.com/privacy/transparency/community-guidelines",
                "region_urls": {"India": "https://values.snap.com/privacy/transparency/community-guidelines", "Global": "https://values.snap.com/privacy/transparency/community-guidelines"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "Not specified", "last_verified": "June 2025", "notes": "",
            },
            "third_party": {
                "title": "Third-Party Content — Snap Terms of Service", "url": "https://values.snap.com/privacy/terms-of-service",
                "region_urls": {"India": "https://values.snap.com/privacy/terms-of-service", "Global": "https://values.snap.com/privacy/terms-of-service"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "February 2024", "last_verified": "June 2025", "notes": "Embedded in Terms of Service.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Snap Terms of Service", "url": "https://values.snap.com/privacy/terms-of-service",
                "region_urls": {"India": "https://values.snap.com/privacy/terms-of-service", "Global": "https://values.snap.com/privacy/terms-of-service"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "February 2024", "last_verified": "June 2025", "notes": "Embedded in Terms of Service.",
            },
            "arbitration": {
                "title": "Arbitration and Class Action Waiver — Snap Terms of Service", "url": "https://values.snap.com/privacy/terms-of-service",
                "region_urls": {"India": "https://values.snap.com/privacy/terms-of-service", "United States": "https://values.snap.com/privacy/terms-of-service", "Global": "https://values.snap.com/privacy/terms-of-service"},
                "availability_status": "Embedded", "applicable_region": "United States — specific arbitration and class action waiver",
                "last_updated": "February 2024", "last_verified": "June 2025",
                "notes": "⚠️ Snap's arbitration and class-action waiver provisions are explicitly for US users.",
            },
        },
    },
    "Flipkart": {
        "icon": "🛍️", "category": "E-Commerce",
        "developer": "Flipkart Internet Pvt. Ltd. (Walmart Group)",
        "description": "Major Indian e-commerce marketplace.",
        "official_home": "https://www.flipkart.com/",
        "policies": {
            "privacy_policy": {
                "title": "Flipkart Privacy Policy", "url": "https://www.flipkart.com/pages/privacypolicy",
                "region_urls": {"India": "https://www.flipkart.com/pages/privacypolicy", "Global": "https://www.flipkart.com/pages/privacypolicy"},
                "availability_status": "Verified", "applicable_region": "India (primary market)",
                "last_updated": "2023 (approximate)", "last_verified": "June 2025", "notes": "",
            },
            "terms_of_service": {
                "title": "Flipkart Terms of Use", "url": "https://www.flipkart.com/pages/terms",
                "region_urls": {"India": "https://www.flipkart.com/pages/terms"},
                "availability_status": "Verified", "applicable_region": "India",
                "last_updated": "2023 (approximate)", "last_verified": "June 2025", "notes": "",
            },
            "community_guidelines": {
                "title": "Flipkart Marketplace Seller / User Conduct Terms", "url": "https://www.flipkart.com/pages/terms",
                "region_urls": {"India": "https://www.flipkart.com/pages/terms"},
                "availability_status": "Embedded", "applicable_region": "India",
                "last_updated": "2023 (approximate)", "last_verified": "June 2025", "notes": "Embedded in Terms of Use.",
            },
            "third_party": {
                "title": "Third-Party Services — Flipkart Terms of Use", "url": "https://www.flipkart.com/pages/terms",
                "region_urls": {"India": "https://www.flipkart.com/pages/terms"},
                "availability_status": "Embedded", "applicable_region": "India",
                "last_updated": "2023 (approximate)", "last_verified": "June 2025", "notes": "Embedded in Terms of Use.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Flipkart Terms of Use", "url": "https://www.flipkart.com/pages/terms",
                "region_urls": {"India": "https://www.flipkart.com/pages/terms"},
                "availability_status": "Embedded", "applicable_region": "India",
                "last_updated": "2023 (approximate)", "last_verified": "June 2025", "notes": "Embedded in Terms of Use.",
            },
            "arbitration": {
                "title": "Dispute Resolution — Flipkart Terms of Use", "url": "https://www.flipkart.com/pages/terms",
                "region_urls": {"India": "https://www.flipkart.com/pages/terms"},
                "availability_status": "Embedded", "applicable_region": "India",
                "last_updated": "2023 (approximate)", "last_verified": "June 2025",
                "notes": "Flipkart's dispute resolution provisions are India-specific.",
            },
        },
    },
    "Google": {
        "icon": "🔵", "category": "Search, Email & Online Services",
        "developer": "Google LLC (Alphabet Inc.)",
        "description": "Search engine, advertising, and cloud services platform.",
        "official_home": "https://policies.google.com/",
        "policies": {
            "privacy_policy": {
                "title": "Google Privacy Policy", "url": "https://policies.google.com/privacy",
                "region_urls": {"India": "https://policies.google.com/privacy", "United States": "https://policies.google.com/privacy", "Global": "https://policies.google.com/privacy"},
                "availability_status": "Verified", "applicable_region": "Global (covers all Google services)",
                "last_updated": "Periodically updated", "last_verified": "June 2025", "notes": "Covers all Google services.",
            },
            "terms_of_service": {
                "title": "Google Terms of Service", "url": "https://policies.google.com/terms",
                "region_urls": {"India": "https://policies.google.com/terms", "United States": "https://policies.google.com/terms", "Global": "https://policies.google.com/terms"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "January 2022 (major revision)", "last_verified": "June 2025", "notes": "",
            },
            "community_guidelines": {
                "title": "Google Prohibited Content Policies", "url": "https://policies.google.com/",
                "region_urls": {"India": "https://policies.google.com/", "Global": "https://policies.google.com/"},
                "availability_status": "Partially verified", "applicable_region": "Global",
                "last_updated": "Varies by product", "last_verified": "June 2025",
                "notes": "Google does not publish a single 'Community Guidelines' document.",
            },
            "third_party": {
                "title": "Third-Party Services — Google Terms of Service", "url": "https://policies.google.com/terms",
                "region_urls": {"India": "https://policies.google.com/terms", "Global": "https://policies.google.com/terms"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "January 2022", "last_verified": "June 2025", "notes": "Embedded in Google Terms of Service.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Google Terms of Service", "url": "https://policies.google.com/terms",
                "region_urls": {"India": "https://policies.google.com/terms", "Global": "https://policies.google.com/terms"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "January 2022", "last_verified": "June 2025", "notes": "Embedded in Terms of Service.",
            },
            "arbitration": {
                "title": "Dispute Resolution — Google Terms of Service", "url": "https://policies.google.com/terms",
                "region_urls": {"India": "https://policies.google.com/terms", "United States": "https://policies.google.com/terms", "Global": "https://policies.google.com/terms"},
                "availability_status": "Embedded", "applicable_region": "Global (US-specific arbitration provisions)",
                "last_updated": "January 2022", "last_verified": "June 2025",
                "notes": "⚠️ Google's ToS contains US-specific arbitration provisions. Indian users contract with Google India Pvt. Ltd.",
            },
        },
    },
    "Gmail": {
        "icon": "📧", "category": "Search, Email & Online Services",
        "developer": "Google LLC (Alphabet Inc.)",
        "description": "Google's email and communication service.",
        "official_home": "https://www.google.com/gmail/about/",
        "policies": {
            "privacy_policy": {
                "title": "Google Privacy Policy (applies to Gmail)", "url": "https://policies.google.com/privacy",
                "region_urls": {"India": "https://policies.google.com/privacy", "United States": "https://policies.google.com/privacy", "Global": "https://policies.google.com/privacy"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "Periodically updated", "last_verified": "June 2025",
                "notes": "Gmail does not have a separate Privacy Policy.",
            },
            "terms_of_service": {
                "title": "Gmail Program Policies & Google Terms of Service", "url": "https://policies.google.com/terms",
                "region_urls": {"India": "https://policies.google.com/terms", "United States": "https://policies.google.com/terms", "Global": "https://policies.google.com/terms"},
                "availability_status": "Verified", "applicable_region": "Global",
                "last_updated": "January 2022", "last_verified": "June 2025", "notes": "",
            },
            "community_guidelines": {
                "title": "Gmail Program Policies", "url": "https://policies.google.com/",
                "region_urls": {"India": "https://policies.google.com/", "Global": "https://policies.google.com/"},
                "availability_status": "Partially verified", "applicable_region": "Global",
                "last_updated": "Varies", "last_verified": "June 2025", "notes": "",
            },
            "third_party": {
                "title": "Third-Party Apps — Google Terms of Service", "url": "https://policies.google.com/terms",
                "region_urls": {"India": "https://policies.google.com/terms", "Global": "https://policies.google.com/terms"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "January 2022", "last_verified": "June 2025", "notes": "Embedded.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Google Terms", "url": "https://policies.google.com/terms",
                "region_urls": {"India": "https://policies.google.com/terms", "Global": "https://policies.google.com/terms"},
                "availability_status": "Embedded", "applicable_region": "Global",
                "last_updated": "January 2022", "last_verified": "June 2025", "notes": "Embedded.",
            },
            "arbitration": {
                "title": "Dispute Resolution — Google Terms", "url": "https://policies.google.com/terms",
                "region_urls": {"India": "https://policies.google.com/terms", "United States": "https://policies.google.com/terms", "Global": "https://policies.google.com/terms"},
                "availability_status": "Embedded", "applicable_region": "Global (US-specific arbitration)",
                "last_updated": "January 2022", "last_verified": "June 2025",
                "notes": "⚠️ US-specific arbitration provisions apply to US users only.",
            },
        },
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# SECTION: SUMMARIZER  (from sections/summarizer.py)
# ══════════════════════════════════════════════════════════════════════════════

_MAX_CHARS   = 300_000
_MIN_CHARS   = 200
AI_CONFIGURED = False  # local summarizer only — no API key needed

_STOPWORDS = {
    "a","about","above","after","all","also","an","and","any","are","as","at",
    "be","been","being","but","by","can","do","each","for","from","get","had",
    "has","have","he","her","him","his","how","if","in","into","is","it","its",
    "just","may","me","more","most","my","no","not","of","on","one","or","our",
    "out","shall","she","so","some","than","that","the","their","them","then",
    "there","these","they","this","those","to","up","us","was","we","were",
    "what","when","which","who","will","with","would","you","your",
    "including","without","limitation","hereby","thereof","therein","herein",
    "pursuant","provided","accordance","whether","otherwise","however","therefore",
}

_HEADINGS = {
    "privacy_policy": [
        "Information Collected", "Why Information Is Collected", "How Information Is Used",
        "Information Sharing", "Advertising and Personalization", "User Privacy Controls",
        "Data Retention and Account Deletion", "Security and Privacy Risks",
        "What This Means for You", "Important Things to Watch Out For",
    ],
    "terms_of_service": [
        "Who Can Use the Service", "Rights You Grant the Platform", "Privacy",
        "Personalization and Recommendations", "Moderation, Enforcement and Appeals",
        "User Responsibilities and Prohibited Activities", "Account Suspension and Termination",
        "Payments and Subscriptions", "Third-Party Services", "Intellectual Property and Ownership",
        "Changes to the Terms", "Disputes and Governing Law", "Liability and Disclaimers",
        "What This Means for You",
    ],
    "community_guidelines": [
        "What Is Allowed", "What Is Prohibited", "Harassment, Abuse, Spam and Scams",
        "Content Restrictions", "Reporting Violations", "Moderation and Enforcement",
        "Content Removal and Account Suspension", "Appeals", "What This Means for You",
    ],
    "third_party": [
        "What Counts as a Third-Party Service", "Examples Relevant to the Platform",
        "Responsibility for Third-Party Content", "External Links and Applications",
        "Data Sharing and Privacy Risks", "Disclaimers and Liability",
        "Precautions Users Can Take", "What This Means for You",
    ],
    "limitation_liability": [
        "What the Platform Says It Is Responsible For", "Types of Losses or Damages Covered",
        "Liability Limits and Financial Caps", "Disclaimers and Service Availability",
        "Exceptions and Protected Legal Rights", "Practical Examples", "What This Means for You",
    ],
    "arbitration": [
        "Does the Agreement Contain an Arbitration Clause?", "Individual Arbitration",
        "Class Action Waiver", "Jury Trial Waiver", "Exceptions and Small-Claims Options",
        "Opt-Out Procedures, If Available", "Notice and Dispute-Resolution Steps",
        "Applicable Country or Region", "What This Means for You",
    ],
}

_HEADING_KEYWORDS = {
    "Information Collected":               ["collect","gather","receive","information","data","personal"],
    "Why Information Is Collected":        ["purpose","why","reason","order to","in order","so that"],
    "How Information Is Used":             ["use","process","provide","improve","develop","service"],
    "Information Sharing":                 ["share","third","partner","disclose","transfer","sell","provide to"],
    "Advertising and Personalization":     ["advertis","personaliz","recommend","target","interest","ad "],
    "User Privacy Controls":               ["control","opt","delete","access","request","manage","right"],
    "Data Retention and Account Deletion": ["retain","retention","delet","remov","period","store"],
    "Security and Privacy Risks":          ["secur","protect","breach","risk","encrypt","unauthoriz"],
    "What This Means for You":             ["you","your","user"],
    "Important Things to Watch Out For":   ["important","note","aware","caution","warn"],
    "Who Can Use the Service":             ["age","eligib","account","register","user","minor","13","18"],
    "Rights You Grant the Platform":       ["license","grant","content","rights","royalt","worldwide"],
    "Privacy":                             ["privacy","personal","data","information"],
    "Personalization and Recommendations": ["personaliz","recommend","suggest","feed","algorith"],
    "Moderation, Enforcement and Appeals": ["enforce","moderat","appeal","review","decision","action"],
    "User Responsibilities and Prohibited Activities": ["prohibit","must not","may not","responsib","forbidden","illegal"],
    "Account Suspension and Termination":  ["suspend","terminat","ban","remov","close","account"],
    "Payments and Subscriptions":          ["payment","subscript","fee","charge","purchas","billing"],
    "Third-Party Services":                ["third","partner","external","link","integrat"],
    "Intellectual Property and Ownership": ["intellectu","copyright","trademark","own","propert"],
    "Changes to the Terms":                ["change","updat","modif","amend","revise","new version"],
    "Disputes and Governing Law":          ["dispute","govern","law","jurisdict","court","legal"],
    "Liability and Disclaimers":           ["liabilit","disclaim","warrant","damage","loss","responsible"],
    "What Is Allowed":                     ["allow","permit","may","can","accept"],
    "What Is Prohibited":                  ["prohibit","not allow","forbid","violat","illegal","must not"],
    "Harassment, Abuse, Spam and Scams":   ["harass","abuse","spam","scam","bully","threat","intimidat"],
    "Content Restrictions":                ["content","restrict","adult","graphic","violent","nudity"],
    "Reporting Violations":                ["report","flag","complain","submit","notify"],
    "Moderation and Enforcement":          ["moderat","enforce","review","action","team"],
    "Content Removal and Account Suspension": ["remov","delet","suspend","terminat","taken down"],
    "Appeals":                             ["appeal","contest","review","object","disput decision"],
    "What Counts as a Third-Party Service":["third party","external","integrat","app","plugin","service"],
    "Examples Relevant to the Platform":   ["example","such as","includ","like"],
    "Responsibility for Third-Party Content": ["responsib","liab","not responsible","no control"],
    "External Links and Applications":     ["link","url","website","click","redirect"],
    "Data Sharing and Privacy Risks":      ["share","data","privacy","risk","access","third"],
    "Disclaimers and Liability":           ["disclaim","liab","warrant","not responsible"],
    "Precautions Users Can Take":          ["recommend","suggest","best practice","should","careful"],
    "What the Platform Says It Is Responsible For": ["responsib","liable","accountab","obligat"],
    "Types of Losses or Damages Covered":  ["damage","loss","harm","cost","injur","consequential"],
    "Liability Limits and Financial Caps": ["cap","limit","maximum","dollar","amount","exceed"],
    "Disclaimers and Service Availability":["disclaim","availab","uninterrupt","downtime","warrant"],
    "Exceptions and Protected Legal Rights":["except","notwithstanding","consumer","rights","law"],
    "Practical Examples":                  ["example","such as","instance","scenario"],
    "Does the Agreement Contain an Arbitration Clause?": ["arbitrat","binding","clause"],
    "Individual Arbitration":              ["individual","arbitrat","binding","private"],
    "Class Action Waiver":                 ["class action","waiver","group","collective"],
    "Jury Trial Waiver":                   ["jury","trial","waiver","court"],
    "Exceptions and Small-Claims Options": ["small claim","exception","court","opt"],
    "Opt-Out Procedures, If Available":    ["opt out","opt-out","optout","30 day","written notice"],
    "Notice and Dispute-Resolution Steps": ["notice","informal","negotiat","attempt","60 day","30 day"],
    "Applicable Country or Region":        ["india","united states","country","region","jurisdict","applicable"],
}


def _sentences(text: str) -> list:
    raw = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in raw if len(s.strip()) > 30]


def _score_sentences(sentences: list) -> dict:
    word_freq: collections.Counter = collections.Counter()
    for sent in sentences:
        for word in re.findall(r'\b[a-z]{3,}\b', sent.lower()):
            if word not in _STOPWORDS:
                word_freq[word] += 1
    n = max(len(sentences), 1)
    scores = {}
    for i, sent in enumerate(sentences):
        words = re.findall(r'\b[a-z]{3,}\b', sent.lower())
        score = sum(word_freq[w] / n for w in words if w not in _STOPWORDS)
        if re.match(r'^[A-Z0-9]', sent):
            score *= 1.1
        scores[i] = score
    return scores


def _top_sentences(sentences: list, scores: dict, n: int) -> list:
    top_indices = heapq.nlargest(n, scores, key=lambda i: scores[i])
    return [sentences[i] for i in sorted(top_indices)]


def _match_heading(sentences: list, heading: str) -> list:
    keywords = _HEADING_KEYWORDS.get(heading, [heading.lower().split()])
    matched = [s for s in sentences if any(kw.lower() in s.lower() for kw in keywords)]
    return matched[:3]


def _build_summary(platform: str, category_key: str, sentences: list, scores: dict) -> str:
    headings = _HEADINGS.get(category_key, ["Summary"])
    cat_labels = {
        "privacy_policy": "Privacy Policy", "terms_of_service": "Terms of Service",
        "community_guidelines": "Community Guidelines",
        "third_party": "Third-Party Material & Services",
        "limitation_liability": "Limitation of Liability",
        "arbitration": "Arbitration & Legal Dispute Waivers",
    }
    lines = [
        f"## Extractive Summary: {platform} — {cat_labels.get(category_key, category_key)}",
        "",
        "⚠️ **This is a basic extractive summary.** It copies real sentences from "
        "the document you pasted — it does not rewrite, interpret, or add legal meaning. "
        "It is not legal advice. Always read the original official document.",
        "",
    ]
    found_any = False
    top_global = set(_top_sentences(sentences, scores, min(30, len(sentences))))
    for heading in headings:
        matched = _match_heading(sentences, heading)
        if not matched:
            fallback = [s for s in top_global if s not in
                        [m for h in headings for m in _match_heading(sentences, h)]]
            matched = fallback[:1]
        if matched:
            lines.append(f"### {heading}")
            for sent in matched:
                lines.append(f"- {textwrap.fill(sent, width=100)}")
            lines.append("")
            found_any = True
    if not found_any:
        lines.append("The pasted text did not contain enough recognizable content to organize under headings.")
    lines += [
        "---",
        "_This summary was generated locally on your device. No data was sent to any server or AI service._",
    ]
    return "\n".join(lines)


def summarize(platform: str, category_key: str, policy_text: str) -> dict:
    text = policy_text.strip()
    if not text:
        return {"ok": False, "summary": "", "error": "No policy text was provided.", "source": "local"}
    if len(text) < _MIN_CHARS:
        return {"ok": False, "summary": "", "error": f"Text too short ({len(text)} chars). Paste the complete policy.", "source": "local"}
    if len(text) > _MAX_CHARS:
        return {"ok": False, "summary": "", "error": f"Text too long ({len(text):,} chars). Limit is {_MAX_CHARS:,}.", "source": "local"}
    try:
        sents = _sentences(text)
        if len(sents) < 3:
            return {"ok": False, "summary": "", "error": "Not enough sentences. Paste more complete paragraphs.", "source": "local"}
        scores  = _score_sentences(sents)
        summary = _build_summary(platform, category_key, sents, scores)
        return {"ok": True, "summary": summary, "error": "", "source": "local"}
    except Exception as exc:
        return {"ok": False, "summary": "", "error": f"Summarization error: {exc}", "source": "local"}


# ══════════════════════════════════════════════════════════════════════════════
# SECTION: UPLOAD POLICY  (from sections/upload_policy.py)
# ══════════════════════════════════════════════════════════════════════════════

def _copy_button(label: str, text: str, key: str):
    col_btn, col_status = st.columns([2, 3])
    with col_btn:
        clicked = st.button(label, key=key, use_container_width=True)
    with col_status:
        if st.session_state.get(f"copied_{key}"):
            st.markdown("<div class='dg-ok-light' style='padding:0.3rem 0.7rem;margin:0;'>✅ Copied!</div>", unsafe_allow_html=True)
    if clicked:
        escaped = text.replace("`", "\\`").replace("\\", "\\\\").replace("$", "\\$")
        components.html(f"<script>navigator.clipboard.writeText(`{escaped}`);</script>", height=0)
        st.session_state[f"copied_{key}"] = True
        st.rerun()


def show_upload_policy():
    st.markdown("## 📤 Upload Latest Privacy Policy")
    st.markdown(
        """
        <div class="dg-info-light">
            <strong>How to use this workspace:</strong><br/>
            1️⃣ Select a platform and policy category below.<br/>
            2️⃣ Open the official policy document via the link shown.<br/>
            3️⃣ Select all text in that document (Ctrl+A / Cmd+A) and copy it.<br/>
            4️⃣ Paste it into <strong>Paste Policy Text</strong> below.<br/>
            5️⃣ Click <strong>Summarize Policy</strong> to generate a plain-English summary.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='dg-info-light'>"
        "💡 <strong>How summarization works:</strong> Paste the full policy text below, "
        "then click <strong>Summarize Policy</strong>. The summary is generated locally "
        "on your device — no internet connection or API key is needed."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<hr/>", unsafe_allow_html=True)
    region_col, _ = st.columns([2, 3])
    with region_col:
        selected_region = st.selectbox(
            "🌍 Applicable Region",
            ["India", "United States", "Global"],
            index=0, key="upload_region",
            help="Select your region.",
        )
    st.markdown(
        f"""
        <div class="dg-info">
            <strong>Selected region: {selected_region}</strong> — 
            Where a platform publishes region-specific legal terms, the document applicable to 
            <strong>{selected_region}</strong> will be shown.
            {"⚠️ US-specific arbitration, class-action waiver, and jury-waiver clauses are <strong>not automatically applicable to Indian users</strong>." if selected_region == "India" else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Step 1 — Select a Platform")

    all_platform_names = list(PLATFORMS.keys())
    platform_cols = st.columns(5)
    for i, name in enumerate(all_platform_names[:5]):
        info = PLATFORMS[name]
        with platform_cols[i]:
            active = st.session_state.get("upload_platform") == name
            border = "border:2px solid #00d4aa;" if active else "border:1px solid #1e3a5f;"
            st.markdown(
                f"""<div style="background:#0d2236;{border}border-radius:10px;padding:0.7rem;text-align:center;cursor:pointer;margin-bottom:0.3rem;">
                    <div style="font-size:1.8rem;">{info['icon']}</div>
                    <div style="font-size:0.82rem;color:#00d4aa;font-weight:600;">{name}</div>
                    <div style="font-size:0.7rem;color:#557788;">{info['category']}</div></div>""",
                unsafe_allow_html=True,
            )
            if st.button(f"Select {name}", key=f"up_sel_{name}", use_container_width=True):
                st.session_state["upload_platform"] = name
                st.session_state["upload_policy_cat"] = None
                st.rerun()

    platform_cols2 = st.columns(4)
    for i, name in enumerate(all_platform_names[5:]):
        info = PLATFORMS[name]
        with platform_cols2[i % 4]:
            active = st.session_state.get("upload_platform") == name
            border = "border:2px solid #00d4aa;" if active else "border:1px solid #1e3a5f;"
            st.markdown(
                f"""<div style="background:#0d2236;{border}border-radius:10px;padding:0.7rem;text-align:center;margin-bottom:0.3rem;">
                    <div style="font-size:1.8rem;">{info['icon']}</div>
                    <div style="font-size:0.82rem;color:#00d4aa;font-weight:600;">{name}</div>
                    <div style="font-size:0.7rem;color:#557788;">{info['category']}</div></div>""",
                unsafe_allow_html=True,
            )
            if st.button(f"Select {name}", key=f"up_sel_{name}", use_container_width=True):
                st.session_state["upload_platform"] = name
                st.session_state["upload_policy_cat"] = None
                st.rerun()

    selected_platform = st.session_state.get("upload_platform")
    if not selected_platform:
        st.markdown("<div class='dg-card' style='text-align:center;color:#557788;'>👆 Select a platform above to begin.</div>", unsafe_allow_html=True)
        return

    plat = PLATFORMS[selected_platform]
    st.markdown(
        f"""<div style="background:#0a3a2a;border:1px solid #00d4aa;border-radius:10px;padding:0.7rem 1.2rem;margin:0.5rem 0;">
            <span style="font-size:1.5rem;">{plat['icon']}</span>
            <strong style="color:#00d4aa;font-size:1.1rem;margin-left:0.5rem;">{selected_platform}</strong>
            <span style="color:#8ab0cc;font-size:0.87rem;margin-left:0.8rem;">{plat['developer']}</span>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Step 2 — Select a Policy Category")

    cat_cols = st.columns(3)
    for i, (cat_key, cat_label) in enumerate(POLICY_CATEGORIES):
        policy = plat["policies"].get(cat_key, {})
        avail = policy.get("availability_status", "Not found")
        avail_cls, avail_text = AVAILABILITY_STYLES.get(avail, ("badge-unknown", "⚪ Unknown"))
        active_cat = st.session_state.get("upload_policy_cat") == cat_key
        border = "border:2px solid #00d4aa;" if active_cat else "border:1px solid #1e3a5f;"
        with cat_cols[i % 3]:
            st.markdown(
                f"""<div style="background:#0d2236;{border}border-radius:10px;padding:0.7rem;margin-bottom:0.4rem;">
                    <div style="font-size:0.92rem;color:#e8f0f7;font-weight:600;margin-bottom:0.3rem;">{cat_label}</div>
                    <span class="{avail_cls}">{avail_text}</span></div>""",
                unsafe_allow_html=True,
            )
            if st.button(f"Open: {cat_label[:25]}", key=f"up_cat_{cat_key}", use_container_width=True):
                st.session_state["upload_policy_cat"] = cat_key
                st.rerun()

    selected_cat = st.session_state.get("upload_policy_cat")
    if not selected_cat:
        st.markdown("<div class='dg-card' style='text-align:center;color:#557788;'>👆 Select a policy category above.</div>", unsafe_allow_html=True)
        return

    st.markdown("<hr/>", unsafe_allow_html=True)
    policy = plat["policies"].get(selected_cat, {})
    cat_label = dict(POLICY_CATEGORIES).get(selected_cat, selected_cat)
    avail = policy.get("availability_status", "Not found")
    avail_cls, avail_text = AVAILABILITY_STYLES.get(avail, ("badge-unknown", "⚪ Unknown"))
    region_urls = policy.get("region_urls", {})
    policy_url = region_urls.get(selected_region) or policy.get("url", "")

    st.markdown(f"### 📄 {selected_platform} — {cat_label}")
    st.markdown(
        f"""<div class="dg-card">
            <div class="dg-card-title">{policy.get('title', cat_label)}</div>
            <div class="dg-card-body">
                <strong>Official URL:</strong> <a href="{policy_url}" target="_blank" style="color:#00d4aa;">{policy_url}</a><br/>
                <strong>Applicable region:</strong> {policy.get('applicable_region','–')}<br/>
                <strong>Region selected:</strong> {selected_region}<br/>
                <strong>Availability:</strong> <span class="{avail_cls}">{avail_text}</span><br/>
                <strong>Last updated:</strong> {policy.get('last_updated','Not available')}<br/>
                <strong>Last verified by this dashboard:</strong> {policy.get('last_verified','Not verified')}<br/>
            </div></div>""",
        unsafe_allow_html=True,
    )

    if policy.get("notes"):
        st.markdown(f"<div class='dg-warn'>📎 <strong>Note:</strong> {policy['notes']}</div>", unsafe_allow_html=True)
    if avail == "Embedded":
        st.markdown("<div class='dg-info'>📎 This policy is <strong>embedded inside a larger document</strong>. Open the official link above, search for the relevant section heading, and copy only that section's text before pasting it below.</div>", unsafe_allow_html=True)

    st.markdown("#### Step 3 — Open the Official Document")
    if policy_url:
        st.markdown(f"🔗 **[Open Official Policy]({policy_url})** ← Click to open in a new tab")
    else:
        st.markdown(f"<div class='dg-danger'>⚠️ A verified direct URL is not available. Start from: <a href='{plat['official_home']}' target='_blank' style='color:#00d4aa;'>{plat['official_home']}</a></div>", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("#### Step 4 — Paste Policy Text")
    st.markdown("Open the official document above, select all text (Ctrl+A / Cmd+A), copy it, and paste it into the box below.")

    paste_key = f"pasted_{selected_platform}_{selected_cat}"
    if paste_key not in st.session_state:
        st.session_state[paste_key] = ""

    pasted_text = st.text_area(
        "Paste Policy Text",
        value=st.session_state[paste_key],
        height=300,
        key=f"ta_paste_{paste_key}",
        placeholder="Paste the complete official policy text here...",
        label_visibility="collapsed",
    )
    st.session_state[paste_key] = pasted_text

    if pasted_text:
        word_count = len(pasted_text.split())
        st.caption(f"📝 {len(pasted_text):,} characters / ~{word_count:,} words")
        if len(pasted_text) < 200:
            st.markdown("<div class='dg-warn-light'>⚠️ The pasted text is very short. Please paste the complete policy document.</div>", unsafe_allow_html=True)

    col_clr_paste, _ = st.columns([1, 5])
    with col_clr_paste:
        if st.button("🗑️ Clear Text", key=f"clr_{paste_key}"):
            st.session_state[paste_key] = ""
            st.session_state[f"summary_{selected_platform}_{selected_cat}"] = ""
            st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("#### Step 5 — Summarize Policy")

    summary_key = f"summary_{selected_platform}_{selected_cat}"
    if summary_key not in st.session_state:
        st.session_state[summary_key] = ""

    if st.button("🔍 Summarize Policy", key=f"sum_btn_{selected_platform}_{selected_cat}", type="primary"):
        if not st.session_state[paste_key].strip():
            st.markdown("<div class='dg-danger-light'>❌ No policy text pasted. Paste the full document in Step 4 first.</div>", unsafe_allow_html=True)
        else:
            with st.spinner("Summarizing — please wait…"):
                result = summarize(selected_platform, selected_cat, st.session_state[paste_key])
            if result["ok"]:
                st.session_state[summary_key] = result["summary"]
                st.rerun()
            else:
                st.markdown(f"<div class='dg-danger-light'>❌ {result['error']}</div>", unsafe_allow_html=True)

    generated_summary = st.session_state.get(summary_key, "")
    if generated_summary:
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("#### 📋 Policy Summary")
        st.markdown("<div class='dg-ok-light' style='margin-bottom:0.7rem;'>✅ Summary generated. Not legal advice — verify against the official document.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='dg-summary-box'>{generated_summary}</div>", unsafe_allow_html=True)
        col_cp, col_clr, _ = st.columns([1, 1, 4])
        with col_cp:
            _copy_button("📋 Copy Summary", generated_summary, key=f"cp_sum_{summary_key}")
        with col_clr:
            if st.button("🗑️ Clear Summary", key=f"clr_sum_{summary_key}"):
                st.session_state[summary_key] = ""
                st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)
    if st.button("↺  Reset All Fields for This Policy", key=f"reset_{selected_platform}_{selected_cat}"):
        st.session_state[paste_key] = ""
        st.session_state[summary_key] = ""
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION: APP LIBRARY  (from sections/app_library.py)
# ══════════════════════════════════════════════════════════════════════════════

def _risk_badge(level: str) -> str:
    icon, label, cls = RISK_LABELS.get(level, RISK_LABELS["unknown"])
    return f'<span class="{cls}">{icon} {label}</span>'


def _risk_label_text(level: str) -> str:
    icon, label, _ = RISK_LABELS.get(level, RISK_LABELS["unknown"])
    return f"{icon} {label}"


def show_app_library():
    st.markdown("## 📚 App Privacy Library")
    st.markdown(
        "<div class='dg-info'>Select an application to explore its privacy practices, "
        "permissions, third-party data sharing, and recommended actions. "
        "All data is demonstration material based on publicly available privacy policies.</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.get("selected_app") and st.session_state.selected_app in APPS:
        _show_app_profile(st.session_state.selected_app)
        if st.button("← Back to App Library"):
            st.session_state.selected_app = None
            st.rerun()
        return

    col_s, col_c = st.columns([3, 1])
    with col_s:
        search = st.text_input("🔎 Search apps…", placeholder="App name…", key="lib_search")
    with col_c:
        cat = st.selectbox("Category", ["All", "Social Media", "Messaging", "E-Commerce", "Ride-Hailing"], key="lib_cat")

    filtered = {
        name: info for name, info in APPS.items()
        if (search.lower() in name.lower() or not search)
        and (cat == "All" or info["category"] == cat)
    }

    if not filtered:
        st.markdown("<div class='dg-warn'>No apps match your search.</div>", unsafe_allow_html=True)
        return

    cols = st.columns(3)
    for i, (name, info) in enumerate(filtered.items()):
        status_class, status_text = STATUS_LABELS[info["status"]]
        with cols[i % 3]:
            st.markdown(
                f"""<div class="dg-card">
                    <div style="font-size:2.4rem;">{info['icon']}</div>
                    <div class="dg-card-title">{name}</div>
                    <div style="font-size:0.82rem;color:#7a9ab0;margin-bottom:0.4rem;">{info['category']}</div>
                    <div style="font-size:0.82rem;color:#a0b8c8;margin-bottom:0.6rem;">{info['developer']}</div>
                    <span class="{status_class}">{status_text}</span></div>""",
                unsafe_allow_html=True,
            )
            if st.button(f"Open {name} Profile", key=f"lib_open_{name}", use_container_width=True):
                st.session_state.selected_app = name
                st.rerun()


def _show_app_profile(name: str):
    info = APPS[name]
    status_class, status_text = STATUS_LABELS[info["status"]]
    st.markdown(
        f"""<div style="background:#0d2236;border:1px solid #1e3a5f;border-radius:14px;padding:1.5rem 2rem;margin-bottom:1rem;">
            <div style="font-size:3rem;margin-bottom:0.3rem;">{info['icon']}</div>
            <h2 style="margin:0;color:#00d4aa;">{name}</h2>
            <div style="color:#8ab0cc;font-size:0.92rem;margin:0.3rem 0;">{info['developer']}</div>
            <div style="margin-top:0.5rem;">
                <span class="{status_class}">{status_text}</span>
                &nbsp;<span style="font-size:0.82rem;color:#557788;">Source: {info['source_date']}</span>
            </div></div>""",
        unsafe_allow_html=True,
    )

    if st.button("← Back to App Library", key="back_lib"):
        st.session_state.selected_app = None
        st.rerun()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Overview", "🔑 Permissions", "🌐 Data Sharing", "⚠️ Security Risks", "📎 Sources"])

    with tab1:
        st.markdown("#### Plain-Language Summary")
        st.markdown(f"<div class='dg-card'><div class='dg-card-body'>{info['summary']}</div></div>", unsafe_allow_html=True)
        st.markdown("#### Key Data Categories Collected")
        for item in info["data_categories"]:
            st.markdown(f"- {item}")
        st.markdown("#### Recommended User Actions")
        for action in info["actions"]:
            st.markdown(f"✅ {action}")
        if info.get("official_settings"):
            st.markdown(f"🔗 [Open Official Settings Page]({info['official_settings']})")

    with tab2:
        st.markdown("<div class='dg-info'>Permissions listed here reflect what the app <em>may</em> request based on available documentation.</div>", unsafe_allow_html=True)
        for perm_name in info["permissions"]:
            perm = PERMISSIONS.get(perm_name, {})
            icon = perm.get("icon", "🔒")
            risk = perm.get("risk_level", "unknown")
            with st.expander(f"{icon} {perm_name} — {_risk_label_text(risk)}", expanded=False):
                if perm:
                    st.markdown(f"**What it means:** {perm['what_it_means']}")
                    st.markdown(f"**Data potentially accessible:** {perm['data_exposed']}")
                    st.markdown(f"**Recommended action:** {perm['action_text']}")
                    if st.button(f"Full details for {perm_name} →", key=f"perm_link_{name}_{perm_name}"):
                        st.session_state.nav = "Permission Explorer"
                        st.rerun()
                else:
                    st.markdown("Detailed information for this permission is not yet available.")

    with tab3:
        st.markdown("#### Third-Party Data Sharing")
        st.markdown(f"<div class='dg-card'><div class='dg-card-body'>{info['third_party_sharing']}</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='dg-warn'>The description above is derived from the app's privacy policy documentation.</div>", unsafe_allow_html=True)
        if info.get("connected_apps_link"):
            st.markdown(f"🔗 [Review Connected Applications]({info['connected_apps_link']})")
        if st.button("Explore Third-Party Data Access in depth →", key=f"tpa_{name}"):
            st.session_state.nav = "Third-Party Data Access"
            st.rerun()

    with tab4:
        st.markdown("#### Potential Privacy & Security Risks")
        st.markdown("<div class='dg-info'>These risks are identified based on the app's documented data practices and publicly reported security incidents.</div>", unsafe_allow_html=True)
        for risk in info["risks"]:
            st.markdown(f"<div class='dg-warn'>⚠️ {risk}</div>", unsafe_allow_html=True)

    with tab5:
        st.markdown("#### Source Information")
        st.markdown(
            f"""<div class='dg-card'>
                <div class='dg-card-title'>Privacy Policy</div>
                <div class='dg-card-body'>
                    <strong>Publisher:</strong> {info['developer']}<br/>
                    <strong>URL:</strong> <a href="{info['privacy_policy']}" target="_blank" style="color:#00d4aa;">{info['privacy_policy']}</a><br/>
                    <strong>Policy last updated:</strong> {info['policy_updated']}<br/>
                    <strong>Source date in this prototype:</strong> {info['source_date']}<br/>
                    <strong>Verification status:</strong> <span class="status-demo">⚠️ Demonstration Data</span>
                </div></div>
            <div class='dg-warn'>All data in this prototype is for educational demonstration.</div>""",
            unsafe_allow_html=True,
        )
        st.markdown(f"🔗 [View Official Privacy Policy]({info['privacy_policy']})")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION: PERMISSION EXPLORER  (from sections/permission_explorer.py)
# ══════════════════════════════════════════════════════════════════════════════

def show_permission_explorer():
    st.markdown("## 🔍 Permission Explorer")
    st.markdown(
        "<div class='dg-info'>Understand what each device permission means, why an app might request it, "
        "what data it exposes, and what action is recommended.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("#### Risk Level Legend")
    leg1, leg2, leg3, leg4 = st.columns(4)
    with leg1:
        st.markdown('<span class="badge-low">🟢 Lower Concern</span>', unsafe_allow_html=True)
        st.caption("Access appears relevant to the app's stated feature.")
    with leg2:
        st.markdown('<span class="badge-review">🟡 Review Recommended</span>', unsafe_allow_html=True)
        st.caption("Purpose, scope, or necessity warrants closer examination.")
    with leg3:
        st.markdown('<span class="badge-high">🔴 Higher Concern</span>', unsafe_allow_html=True)
        st.caption("Specific evidence of excessive access or documented security concern.")
    with leg4:
        st.markdown('<span class="badge-unknown">⚪ Unknown</span>', unsafe_allow_html=True)
        st.caption("Available evidence is insufficient to rate.")

    st.markdown("<div class='dg-warn'>These ratings reflect general patterns based on documented privacy practices.</div>", unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)

    risk_filter = st.selectbox("Filter by concern level", ["All", "🟢 Lower Concern", "🟡 Review Recommended", "🔴 Higher Concern"], key="perm_filter")
    risk_map = {"🟢 Lower Concern": "low", "🟡 Review Recommended": "review", "🔴 Higher Concern": "high"}
    selected_risk = risk_map.get(risk_filter)

    for perm_name, perm in PERMISSIONS.items():
        level = perm.get("risk_level", "unknown")
        if selected_risk and level != selected_risk:
            continue
        with st.expander(f"{perm['icon']}  {perm_name}   —   {_risk_label_text(level)}", expanded=False):
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.markdown("##### 📖 What it means")
                st.markdown(f"<div class='dg-card-body'>{perm['what_it_means']}</div>", unsafe_allow_html=True)
                st.markdown("##### ✅ Why an app might request it")
                for reason in perm["why_requested"]:
                    st.markdown(f"- {reason}")
                st.markdown("##### 🗂️ Data that may become accessible")
                st.markdown(f"<div class='dg-card-body'>{perm['data_exposed']}</div>", unsafe_allow_html=True)
            with col_b:
                st.markdown("##### ❌ When it may be unnecessary")
                st.markdown(f"<div class='dg-card-body'>{perm['when_unnecessary']}</div>", unsafe_allow_html=True)
                st.markdown("##### ⚠️ Potential privacy risks")
                st.markdown(f"<div class='dg-warn'>{perm['risks']}</div>", unsafe_allow_html=True)
                st.markdown("##### 💡 Recommended action")
                action_cls = {"low": "dg-ok", "review": "dg-warn", "high": "dg-danger"}.get(level, "dg-info")
                st.markdown(f"<div class='{action_cls}'>{perm['action_text']}</div>", unsafe_allow_html=True)
            st.markdown("<div class='dg-info' style='margin-top:0.5rem;'>📎 <strong>Evidence & limitations:</strong> This explanation is based on general platform documentation and documented privacy practices.</div>", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### 📱 How to Review Permissions on Your Device")
    with st.expander("Android — Reviewing App Permissions"):
        st.markdown("""
        1. Open **Settings** on your Android device.
        2. Tap **Apps** (or **Application Manager**).
        3. Select the app you want to review.
        4. Tap **Permissions**.
        5. Review each permission — tap to Allow, Deny, or set to **Allow only while using**.
        6. For a full overview, go to **Settings → Privacy → Permission Manager**.
        """)
        st.markdown("<div class='dg-info'>Data Guardian cannot open these settings screens directly.</div>", unsafe_allow_html=True)
    with st.expander("iOS — Reviewing App Permissions"):
        st.markdown("""
        1. Open **Settings** on your iPhone or iPad.
        2. Scroll down and tap the app name (e.g. Instagram).
        3. Review each permission listed — tap to change between Never, Ask, or Allow.
        4. For a category-level view, go to **Settings → Privacy & Security**.
        """)
        st.markdown("<div class='dg-info'>Data Guardian cannot open iOS permission screens.</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION: THIRD PARTY  (from sections/third_party.py)
# ══════════════════════════════════════════════════════════════════════════════

DATA_FLOWS = {
    "Location": {
        "description": "Your precise or approximate geographic coordinates",
        "app_use": "Enables map features, ride matching, local search, delivery routing",
        "possible_recipients": [
            ("Mapping providers", "To render maps and calculate routes"),
            ("Advertisers", "For location-based ad targeting if the app shares location data"),
            ("Analytics SDKs", "For usage analytics that may include location context"),
            ("Data brokers (possible)", "Some apps sell location data to third-party data brokers"),
        ],
        "risk": "review",
        "risk_note": "Location history can reveal home address, workplace, medical appointments, religious attendance, and daily routine. Once shared, it may be retained indefinitely.",
        "action": "Grant location only to apps where it is essential. Use 'While Using' not 'Always'.",
    },
    "Contacts": {
        "description": "Names, phone numbers, and email addresses in your address book",
        "app_use": "Friend-finding, invitation sending, contact matching",
        "possible_recipients": [
            ("App servers", "Contacts are typically uploaded to match users"),
            ("Analytics SDKs", "May receive metadata about social graph size"),
            ("Affiliated companies", "Within a corporate family (e.g. Meta products)"),
        ],
        "risk": "review",
        "risk_note": "Your contacts have not consented to share their data. Contact data is used to build social graphs and identify relationships.",
        "action": "Deny contact access to apps where friend-finding is not important to you.",
    },
    "Profile Information": {
        "description": "Your name, email, phone number, and profile photo",
        "app_use": "Account creation, personalisation, account recovery",
        "possible_recipients": [
            ("Third-party apps (via OAuth)", "Apps authorised with 'Login with Facebook/Google' receive basic profile scopes"),
            ("Advertisers", "For audience targeting and lookalike audiences"),
            ("Affiliated companies", "Within a corporate family"),
            ("Business partners", "Per the platform's privacy policy"),
        ],
        "risk": "review",
        "risk_note": "OAuth scopes may grant third-party apps access to your profile even if you haven't explicitly shared it. Review connected apps regularly.",
        "action": "Regularly audit and revoke connected app authorisations.",
    },
    "Browsing Activity": {
        "description": "Pages visited, links clicked, time spent on content",
        "app_use": "Personalisation, recommendations, content ranking",
        "possible_recipients": [
            ("Advertisers", "Core to the targeted advertising business model"),
            ("Analytics partners", "Usage and behaviour analytics"),
            ("Data brokers", "May be sold to third parties for profiling"),
            ("Meta Pixel partners (if applicable)", "External website owners using tracking scripts may share browsing data with Meta"),
        ],
        "risk": "high",
        "risk_note": "Cross-site tracking via embedded pixels, SDKs, and cookies can build detailed profiles of your interests, health concerns, financial status, and political views.",
        "action": "Use browser privacy settings, content blocking extensions, and opt out of personalised advertising in app settings where available.",
    },
    "Account Data": {
        "description": "Login credentials, session tokens, and account settings",
        "app_use": "Authentication and personalisation",
        "possible_recipients": [
            ("App servers", "Session tokens are stored server-side"),
            ("Potential attackers", "Session hijacking via phishing or XSS"),
            ("Third-party apps (via OAuth)", "Receive an access token granting defined scopes"),
        ],
        "risk": "high",
        "risk_note": "Access tokens and session cookies are the keys to your account. If stolen via phishing, XSS, or a malicious third-party app, an attacker can act as you without knowing your password.",
        "action": "Enable multi-factor authentication. Regularly review active sessions and connected apps.",
    },
}

RECIPIENT_TYPES = {
    "The Application Itself": (
        "The service you directly use. It collects data as described in its privacy policy. "
        "Its access is defined by the permissions you grant and the features you use."
    ),
    "Third-Party Applications": (
        "External apps or websites that you have authorised through a login connection "
        "(e.g. 'Login with Facebook') or an in-app integration. "
        "Their access depends on the OAuth scopes you approved."
    ),
    "Third-Party SDKs & Service Providers": (
        "Software components embedded by the developer for analytics, advertising, crash reporting, "
        "or other services. They may collect data as part of their function."
    ),
    "Business Partners & Data Recipients": (
        "Organisations that may receive information under the service's privacy practices, "
        "such as affiliated companies, advertisers, data enrichment partners, or legal authorities."
    ),
    "Potential Attackers": (
        "Individuals who exploit phishing, stolen session tokens, insecure OAuth implementations, "
        "XSS vulnerabilities, or other weaknesses to gain unauthorised access."
    ),
}


def _risk_html(level: str) -> str:
    icon, label, cls = RISK_LABELS.get(level, RISK_LABELS["unknown"])
    return f'<span class="{cls}">{icon} {label}</span>'


def show_third_party():
    st.markdown("## 🌐 Third-Party Data Access")
    st.markdown("### Who Else Can Access My Data?")
    st.markdown(
        "<div class='dg-info'>When you use an app, your data may flow beyond the app itself — to service providers, "
        "advertising networks, affiliated companies, and potentially to third-party apps you have authorised.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("#### Types of Data Recipients")
    for rtype, desc in RECIPIENT_TYPES.items():
        with st.expander(f"🔹 {rtype}"):
            st.markdown(f"<div class='dg-card-body'>{desc}</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='dg-warn'>These groups do <strong>not</strong> automatically receive the same information. "
        "Access depends on permissions, authorisation scopes, service design, settings, and circumstances.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown("#### 🔄 Interactive Data Flow Explorer")
    st.markdown("Select a data category to see how it may flow from your device to potential recipients.")

    selected_category = st.selectbox("Choose a data category", list(DATA_FLOWS.keys()), key="df_category")
    flow = DATA_FLOWS[selected_category]

    st.markdown(
        f"""<div style="display:flex;align-items:center;flex-wrap:wrap;gap:0.5rem;margin:1rem 0;padding:1rem;background:#0d2236;border-radius:10px;border:1px solid #1e3a5f;">
            <div style="background:#1a3a5c;border-radius:8px;padding:0.5rem 0.9rem;color:#e8f0f7;font-weight:600;">👤 You</div>
            <div style="color:#00d4aa;font-size:1.3rem;">→</div>
            <div style="background:#0a3a2a;border-radius:8px;padding:0.5rem 0.9rem;color:#00d4aa;font-weight:600;">📱 App</div>
            <div style="color:#00d4aa;font-size:1.3rem;">→</div>
            <div style="background:#1a3a5c;border-radius:8px;padding:0.5rem 0.9rem;color:#55ccff;font-weight:600;">📦 {selected_category}</div>
            <div style="color:#00d4aa;font-size:1.3rem;">→</div>
            <div style="background:#2a1a3a;border-radius:8px;padding:0.5rem 0.9rem;color:#cc99ff;font-weight:600;">🌐 Possible Recipients</div>
            <div style="color:#00d4aa;font-size:1.3rem;">→</div>
            {_risk_html(flow['risk'])}
        </div>""",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(f"**Data description:** {flow['description']}")
        st.markdown(f"**How the app uses it:** {flow['app_use']}")
        st.markdown("**Possible recipients:**")
        for recipient, reason in flow["possible_recipients"]:
            st.markdown(
                f"""<div style="background:#0d2236;border:1px solid #1e3a5f;border-radius:8px;padding:0.5rem 0.8rem;margin-bottom:0.4rem;">
                    <strong style="color:#00d4aa;">{recipient}</strong><br/>
                    <span style="font-size:0.88rem;color:#b0c8e0;">{reason}</span></div>""",
                unsafe_allow_html=True,
            )
    with c2:
        st.markdown("**Risk explanation:**")
        st.markdown(f"<div class='dg-warn'>{flow['risk_note']}</div>", unsafe_allow_html=True)
        st.markdown("**Recommended action:**")
        st.markdown(f"<div class='dg-ok'>{flow['action']}</div>", unsafe_allow_html=True)
        st.markdown("<div class='dg-info'>📎 <strong>Evidence note:</strong> The recipient relationships shown are general illustrative examples based on common privacy policy practices.</div>", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("#### 📖 Key Concepts Glossary")
    for term, definition in GLOSSARY.items():
        with st.expander(f"📌 {term}"):
            st.markdown(f"<div class='dg-card-body'>{definition}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION: REVIEW ACCESS  (from sections/review_access.py)
# ══════════════════════════════════════════════════════════════════════════════

DEVICE_ACTIONS = [
    {
        "id": "location_permission", "icon": "📍", "title": "Review Location Permissions",
        "description": "Check which apps have access to your location and whether background ('Always On') access is granted unnecessarily.",
        "android_steps": ["Open Settings", "Tap Privacy → Permission Manager", "Tap Location", "Review each app — change to 'Allow only while using the app' or 'Deny' where appropriate"],
        "ios_steps": ["Open Settings", "Tap Privacy & Security → Location Services", "Review each app — tap to change to Never, Ask Next Time, or While Using the App"],
    },
    {
        "id": "camera_permission", "icon": "📷", "title": "Review Camera Permissions",
        "description": "Check which apps can activate your camera and revoke where unnecessary.",
        "android_steps": ["Open Settings → Privacy → Permission Manager", "Tap Camera", "Review apps — deny camera access to apps that do not need it"],
        "ios_steps": ["Open Settings → Privacy & Security → Camera", "Toggle off camera access for apps that don't require it"],
    },
    {
        "id": "microphone_permission", "icon": "🎤", "title": "Review Microphone Permissions",
        "description": "Identify apps with microphone access and deny where unneeded.",
        "android_steps": ["Open Settings → Privacy → Permission Manager", "Tap Microphone", "Review and revoke for apps without a legitimate audio need"],
        "ios_steps": ["Open Settings → Privacy & Security → Microphone", "Toggle off for apps that don't use voice features"],
    },
    {
        "id": "contacts_permission", "icon": "👥", "title": "Review Contacts Permissions",
        "description": "Contact access uploads your address book to the app's servers. Review which apps have this permission.",
        "android_steps": ["Open Settings → Privacy → Permission Manager", "Tap Contacts", "Deny for apps where friend-finding is not important to you"],
        "ios_steps": ["Open Settings → Privacy & Security → Contacts", "Toggle off for apps that don't need your address book"],
    },
]

CONNECTED_APP_ACTIONS = [
    {
        "id": "facebook_connected", "icon": "📘", "title": "Review Facebook Connected Apps",
        "description": "Third-party apps that you logged into using Facebook may still have active access to your profile, friends list, and other data.",
        "link": "https://www.facebook.com/settings?tab=applications",
        "link_label": "Open Facebook App Settings",
        "manual_steps": ["Go to facebook.com → Settings → Apps and Websites", "Review Active apps", "Click 'Remove' on any app you no longer use or trust"],
    },
    {
        "id": "google_connected", "icon": "🔵", "title": "Review Google Connected Apps",
        "description": "Apps authorised with 'Sign in with Google' may have access to your Google account data.",
        "link": "https://myaccount.google.com/permissions",
        "link_label": "Open Google Account Permissions",
        "manual_steps": ["Go to myaccount.google.com → Security → Third-party apps with account access", "Review the list — click an app to see its permissions", "Click 'Remove Access' for apps you no longer use"],
    },
    {
        "id": "instagram_connected", "icon": "📸", "title": "Review Instagram Connected Apps",
        "description": "Check third-party apps connected to your Instagram account.",
        "link": "https://www.instagram.com/accounts/manage_access/",
        "link_label": "Open Instagram App Access Settings",
        "manual_steps": ["Open Instagram → Profile → Menu (☰) → Settings and Privacy", "Tap Account → Apps and Websites", "Review Active authorisations and remove unused ones"],
    },
]

TRACKING_ACTIONS = [
    {
        "id": "ad_preferences_facebook", "icon": "🎯", "title": "Review Facebook Ad Preferences",
        "description": "Facebook builds an interest profile based on your activity on and off the platform. You can review and clear parts of this profile.",
        "link": "https://www.facebook.com/adpreferences",
        "link_label": "Open Facebook Ad Preferences",
        "manual_steps": ["Go to facebook.com → Settings → Ads → Ad Preferences", "Review 'Your interests' and 'Advertisers you've interacted with'", "Check 'Off-Facebook activity' and clear if desired"],
    },
    {
        "id": "snap_location", "icon": "👻", "title": "Enable Snapchat Ghost Mode",
        "description": "Snap Map shares your real-time location with friends by default. Ghost Mode hides your location from the map.",
        "link": None, "link_label": None,
        "manual_steps": ["Open Snapchat → Tap the Map icon (bottom left)", "Tap the Settings icon (top right of the map)", "Toggle on Ghost Mode"],
    },
    {
        "id": "telegram_privacy", "icon": "✈️", "title": "Set Telegram Phone Number Privacy",
        "description": "By default, anyone who has your phone number may find your Telegram account. Restrict this in Privacy settings.",
        "link": None, "link_label": None,
        "manual_steps": ["Open Telegram → Settings → Privacy and Security", "Tap Phone Number → Who can see my phone number: set to Nobody", "Tap Who can find me by my number: set to My Contacts or Nobody"],
    },
]

_STATUS_OPTIONS = ["Not reviewed", "Instructions viewed", "User marked as completed"]


def _item_key(item_id: str) -> str:
    return f"review_{item_id}"


def _status_color(status: str) -> str:
    if status == "User marked as completed":
        return "dg-ok"
    if status == "Instructions viewed":
        return "dg-info"
    return "dg-card"


def _render_action(action: dict, show_steps: bool = True):
    item_id = action["id"]
    current_status = st.session_state.reviewed_items.get(item_id, "Not reviewed")
    status_cls = _status_color(current_status)
    st.markdown(
        f"""<div class="{status_cls}">
            <div class="dg-card-title">{action['icon']} {action['title']}</div>
            <div class="dg-card-body">{action['description']}</div></div>""",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.caption(f"Status: **{current_status}**")
    with c2:
        if action.get("link"):
            st.markdown(f"🔗 [{action['link_label']}]({action['link']})")
    with c3:
        if current_status != "User marked as completed":
            if st.button("✅ Mark as Reviewed", key=f"mark_{item_id}", use_container_width=True):
                st.session_state.reviewed_items[item_id] = "User marked as completed"
                st.rerun()
        else:
            if st.button("↩️ Undo", key=f"undo_{item_id}", use_container_width=True):
                st.session_state.reviewed_items[item_id] = "Not reviewed"
                st.rerun()

    if show_steps:
        with st.expander("📋 Show Me How — Android & iOS Steps"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Android**")
                for step in action.get("android_steps", action.get("manual_steps", [])):
                    st.markdown(f"  {step}")
            with col_b:
                if action.get("ios_steps"):
                    st.markdown("**iOS**")
                    for step in action["ios_steps"]:
                        st.markdown(f"  {step}")

    st.markdown(
        "<div class='dg-info' style='margin-bottom:0.4rem;'>"
        "⚠️ <strong>Important:</strong> 'Mark as Reviewed' updates this dashboard only. "
        "It does not change any device permission or revoke any app authorisation.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")


def show_review_access():
    st.markdown("## ✅ Review My Access — Action Centre")
    st.markdown(
        "<div class='dg-info'>This section guides you through reviewing your device permissions, "
        "connected app authorisations, and data-sharing settings.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='dg-warn'><strong>Limitation:</strong> Data Guardian is a web application. "
        "It cannot inspect, change, or verify your device permissions.</div>",
        unsafe_allow_html=True,
    )

    total_actions = len(DEVICE_ACTIONS) + len(CONNECTED_APP_ACTIONS) + len(TRACKING_ACTIONS)
    completed = sum(
        1 for a in (DEVICE_ACTIONS + CONNECTED_APP_ACTIONS + TRACKING_ACTIONS)
        if st.session_state.reviewed_items.get(a["id"]) == "User marked as completed"
    )
    st.markdown(f"#### Progress: {completed} / {total_actions} items reviewed")
    st.progress(completed / total_actions if total_actions else 0)

    if st.button("🗑️ Clear All Review Progress"):
        st.session_state.reviewed_items = {}
        st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### 📱 Category 1: Device Permissions")
    st.markdown("Review which apps have access to sensitive device features. Changes must be made in your device Settings.")
    for action in DEVICE_ACTIONS:
        _render_action(action, show_steps=True)

    st.markdown("### 🌐 Category 2: Connected Applications & Account Access")
    st.markdown("Review third-party apps that are authorised to access your social media or Google accounts.")
    for action in CONNECTED_APP_ACTIONS:
        _render_action(action, show_steps=True)

    st.markdown("### 🎯 Category 3: Data Sharing & Tracking Settings")
    st.markdown("Review platform-level privacy settings for advertising, location sharing, and tracking.")
    for action in TRACKING_ACTIONS:
        _render_action(action, show_steps=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("#### Status Key")
    st.markdown("""
    | Status | Meaning |
    |--------|---------|
    | Not reviewed | No action taken in this session |
    | Instructions viewed | You have expanded the step-by-step guide |
    | User marked as completed | You have self-reported completing this action |
    """)
    st.markdown("<div class='dg-info'>User-reported completion is not independently verified.</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION: LEARNING CENTRE  (from sections/learning_centre.py)
# ══════════════════════════════════════════════════════════════════════════════

TOPICS = [
    {
        "id": "excessive_permissions", "title": "Excessive Permissions & Least Privilege", "icon": "🔒",
        "explanation": "The 'least privilege' principle means an app should only request the access it genuinely needs to perform its function. When an app requests more permissions than necessary, it collects more data than intended.",
        "example": "A torch (flashlight) app that requests access to your contacts, microphone, and precise location has no obvious legitimate reason for those permissions.",
        "consequence": "Over-privileged apps collect more data, increasing exposure in the event of a breach, a company acquisition, a policy change, or a malicious update.",
        "prevention": "Review permissions before and after installing apps. Deny permissions that are not clearly needed.",
    },
    {
        "id": "oauth_api", "title": "OAuth & API Authorization", "icon": "🔑",
        "explanation": "OAuth is an open standard that lets you authorize a third-party app to access your account on another service — without sharing your password. When you click 'Login with Google' or 'Connect with Facebook', you are using OAuth.",
        "example": "You authorize a fitness app to access your Google account. If the app requests the 'email' and 'calendar.read' scopes, it can read your email address and calendar events. The 2014 Cambridge Analytica situation began with a quiz app that used Facebook Login to request access to users' friends lists.",
        "consequence": "Overly broad OAuth scopes mean third-party apps can access more of your account than necessary. Access tokens persist until revoked.",
        "prevention": "Review which scopes an app is requesting before authorizing. Regularly audit and revoke connected apps in your account settings.",
    },
    {
        "id": "third_party_app_risks", "title": "Third-Party Application Risks", "icon": "🌐",
        "explanation": "Third-party apps connect to social media platforms, cloud services, and email providers through APIs and OAuth. A connected app can access your data even if it is insecure, acquired by another company, or operated with different privacy practices.",
        "example": "A social media scheduling tool authorised to post on your behalf also receives read access to your messages if that scope was granted. If the scheduling tool is hacked or sold, your message data may be exposed.",
        "consequence": "Data exposure, account takeover, or privacy violations through a less-secure connected app.",
        "prevention": "Authorize only apps you currently use and trust. Regularly review and revoke unused connected apps.",
    },
    {
        "id": "token_theft", "title": "Access Token & Session Token Theft", "icon": "🪙",
        "explanation": "An access token or session cookie is a credential that proves your identity to a service. If this token is stolen, an attacker can use it to access your account — without knowing your password.",
        "example": "An attacker sends you a phishing link that looks like a Facebook login page. You enter your credentials. The attacker captures your session token and can now read your messages and change your settings.",
        "consequence": "Full account access for an attacker until the token expires or is revoked.",
        "prevention": "Enable multi-factor authentication. Regularly review active sessions in account security settings and log out unknown sessions.",
    },
    {
        "id": "phishing", "title": "Phishing & Fake Login Pages", "icon": "🎣",
        "explanation": "Phishing is a social engineering attack where an adversary impersonates a trusted entity to trick users into revealing login credentials, installing malware, or authorizing transactions.",
        "example": "You receive a message saying your Instagram account will be disabled unless you verify your email. The link leads to a convincing-looking but fake Instagram login page.",
        "consequence": "Account takeover, identity theft, financial loss, or deployment of further attacks.",
        "prevention": "Check the URL before entering credentials. Enable multi-factor authentication. Be suspicious of urgency-based messages.",
    },
    {
        "id": "xss", "title": "Cross-Site Scripting (XSS)", "icon": "💻",
        "explanation": "XSS is an attack where malicious scripts are injected into a trusted website. When a victim's browser loads the page, the script runs in the context of that site — potentially stealing session cookies or redirecting the user.",
        "example": "An attacker posts a comment on a forum that contains a hidden script. When other users view the comment, the script runs in their browser and sends their session cookie to the attacker's server.",
        "consequence": "Session hijacking, credential theft, or malicious actions performed as the user.",
        "prevention": "Use browsers with XSS protection. Keep browsers and extensions updated.",
    },
    {
        "id": "csrf", "title": "Cross-Site Request Forgery (CSRF)", "icon": "🔄",
        "explanation": "CSRF tricks your browser into making an unintended request to a site where you are already authenticated — without your knowledge.",
        "example": "You are logged into your bank. You visit a malicious website that contains a hidden form that submits a transfer request to your bank. Your browser sends the request with your bank's session cookie.",
        "consequence": "Unauthorized account actions — changing settings, posting content, or financial transactions.",
        "prevention": "Log out of sensitive accounts when not in use. Avoid visiting untrusted sites while logged into important accounts.",
    },
    {
        "id": "sdks", "title": "Malicious or Poorly Configured SDKs", "icon": "📦",
        "explanation": "Developers embed third-party SDKs to add features like analytics, advertising, or payments. These SDKs run inside the app with the same permissions as the app itself. A poorly configured or malicious SDK can collect more data than the developer intended.",
        "example": "An app embeds an advertising SDK that also collects device location, unique device identifiers, and app usage patterns — even if the developer only intended to show ads.",
        "consequence": "Users' data collected beyond what the app's stated purpose requires.",
        "prevention": "Prefer apps from developers who are transparent about which SDKs they use.",
    },
    {
        "id": "tracking_pixels", "title": "Cookies & Tracking Pixels", "icon": "🍪",
        "explanation": "Cookies are small files stored by your browser that can track your session and activity. A tracking pixel is a tiny invisible image that, when loaded, signals to a remote server that you visited a page or opened an email.",
        "example": "The Meta Pixel (formerly Facebook Pixel) is a JavaScript snippet placed on external websites. When you visit a site with the Meta Pixel, it reports your visit to Meta — even if you are not currently using Facebook.",
        "consequence": "Cross-site browsing profiles built without direct interaction with the tracking platform.",
        "prevention": "Use a browser with third-party cookie blocking (e.g. Firefox, Safari) or privacy extensions.",
    },
    {
        "id": "data_profiling", "title": "Data Profiling & Data Brokerage", "icon": "📊",
        "explanation": "Data profiling involves combining data from multiple sources to build a detailed picture of an individual. Data brokers are companies that collect and sell these profiles to advertisers, insurers, employers, and others.",
        "example": "Your location data from a ride-hailing app, your purchase history from a shopping app, and your social media interests may be separately sold to data brokers.",
        "consequence": "Loss of privacy, discriminatory profiling, targeted manipulation, or exposure of sensitive information.",
        "prevention": "Limit the data you share with apps by reviewing permissions and account settings.",
    },
    {
        "id": "e2ee", "title": "End-to-End Encryption & Metadata", "icon": "🔐",
        "explanation": "End-to-end encryption (E2EE) means only the sender and recipient can read a message — not even the service provider. However, E2EE protects message content, not metadata.",
        "example": "WhatsApp encrypts message content by default. However, Meta can still see: who you message, how often, when, from which device, and from which IP address.",
        "consequence": "Metadata reveals social networks, relationships, routines, and potentially sensitive associations.",
        "prevention": "Enable E2EE backup in WhatsApp. For highly sensitive communications, use Signal, which collects minimal metadata.",
    },
    {
        "id": "account_security", "title": "Basic Account Security & Multi-Factor Authentication", "icon": "🛡️",
        "explanation": "Strong account security reduces the risk of unauthorized access even when credentials are stolen. Multi-factor authentication (MFA) requires a second proof of identity in addition to your password.",
        "example": "An attacker obtains your password via a data breach. Without MFA, they can immediately log in. With MFA enabled, they also need your second factor — a code from your authenticator app.",
        "consequence": "Without MFA, a stolen or guessed password is sufficient for account takeover.",
        "prevention": "Enable MFA on all important accounts. Use an authenticator app rather than SMS where possible.",
    },
]

CASE_STUDIES = [
    {
        "id": "cambridge_analytica",
        "title": "Facebook & Cambridge Analytica (2014–2018)", "icon": "📘",
        "what_happened": "A personality quiz app called 'This Is Your Digital Life' was connected to Facebook via Facebook Login. Approximately 270,000 users consented to share their profile data with the app. Due to Facebook's API permissions at the time, the app could also access the profile data of those users' Facebook friends — without those friends' explicit consent. This reportedly resulted in the data of approximately 87 million users being harvested.",
        "weakness": "Facebook's API at the time allowed apps to access friends' data through a single consenting user. This is an example of overly broad OAuth/API scopes and insufficient enforcement of third-party data use restrictions.",
        "why_it_matters": "The incident highlighted that consenting to one app's data access can expose your friends' data without their knowledge.",
        "what_users_can_learn": "Review which apps are connected to your social media accounts. Be cautious about authorizing apps that request access to your friends list.",
        "what_dashboard_helps": "Data Guardian can help you understand OAuth permissions, review connected apps, and follow the steps to revoke unused third-party authorisations.",
        "what_dashboard_cannot_do": "Data Guardian cannot detect whether an app has already harvested data or reverse data that has already been collected.",
        "source": "Multiple news reports; Meta's own disclosures (2018). The approximately 87 million figure is from Meta's public statements in 2018.",
        "source_link": "https://about.fb.com/news/2018/04/restricting-data-access/",
    },
    {
        "id": "snapchat_findfriends",
        "title": "Snapchat Find Friends Incident (2014)", "icon": "👻",
        "what_happened": "In December 2013, security researchers at Gibson Security published a warning that Snapchat's Find Friends API could be exploited to match phone numbers to usernames at scale. In early January 2014, attackers exploited the API and published a database containing approximately 4.6 million Snapchat usernames paired with partial phone numbers.",
        "weakness": "Snapchat's Find Friends API did not implement adequate rate limiting or abuse detection. This allowed automated requests to enumerate a large portion of the user base.",
        "why_it_matters": "This incident illustrates how an API designed for a legitimate user feature (finding friends) can be abused at scale when appropriate controls are absent.",
        "what_users_can_learn": "Contact access on apps contributes to databases that can be targeted. Limiting contact access and restricting who can find you by phone number reduces exposure.",
        "what_dashboard_helps": "Data Guardian explains contact permission risks and guides users to review Snapchat's discoverability settings.",
        "what_dashboard_cannot_do": "Data Guardian cannot prevent API abuse at the platform level.",
        "source": "Gibson Security disclosure (December 2013); widespread media reporting (January 2014).",
        "source_link": "https://gibsonsec.org/snapchat/",
    },
    {
        "id": "cross_site_tracking",
        "title": "Cross-Site Tracking via Embedded Social Plugins", "icon": "🌐",
        "what_happened": "Social media platforms provide website owners with embedded 'Like' buttons, share widgets, and comment boxes. When a user visits a website with these plugins, the social platform may receive a signal that includes the page URL, the user's IP address, and — if the user is logged in — their account identity.",
        "weakness": "The HTTP protocol sends browser cookies and headers with every request to a domain. Third-party scripts embedded across many websites can build a browsing profile that spans many unrelated sites.",
        "why_it_matters": "Users may not realize that visiting a health information website, reading a news article, or browsing an online shop shares that activity with social media companies.",
        "what_users_can_learn": "Use browsers with built-in tracking protection (Firefox, Safari, Brave). Install content-blocking extensions.",
        "what_dashboard_helps": "Data Guardian explains how tracking pixels and cookies work and points users towards Facebook's Off-Facebook Activity settings.",
        "what_dashboard_cannot_do": "Data Guardian cannot block trackers on your device.",
        "source": "General cybersecurity and privacy research. No specific single incident — this is an ongoing, documented practice.",
        "source_link": "https://www.eff.org/issues/trackers",
    },
]


def show_learning_centre():
    st.markdown("## 🎓 Cybersecurity Learning Centre")
    st.markdown(
        "<div class='dg-info'>This section explains privacy and cybersecurity concepts in plain language, "
        "with real examples, consequences, and prevention steps.</div>",
        unsafe_allow_html=True,
    )

    tab_topics, tab_cases = st.tabs(["📖 Educational Topics", "🔍 Case Studies"])

    with tab_topics:
        st.markdown("### Privacy & Cybersecurity Concepts")
        st.markdown("Select any topic to expand it.")
        topic_filter = st.selectbox("Jump to topic", ["All topics"] + [t["title"] for t in TOPICS], key="topic_filter")

        for topic in TOPICS:
            if topic_filter != "All topics" and topic["title"] != topic_filter:
                continue
            with st.expander(f"{topic['icon']}  {topic['title']}", expanded=(topic_filter == topic["title"])):
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.markdown("#### What is it?")
                    st.markdown(f"<div class='dg-card-body'>{topic['explanation']}</div>", unsafe_allow_html=True)
                    st.markdown("#### Real example")
                    st.markdown(f"<div class='dg-info'>{topic['example']}</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown("#### Potential consequence")
                    st.markdown(f"<div class='dg-warn'>{topic['consequence']}</div>", unsafe_allow_html=True)
                    st.markdown("#### What you can do")
                    st.markdown(f"<div class='dg-ok'>{topic['prevention']}</div>", unsafe_allow_html=True)

    with tab_cases:
        st.markdown("### Case Studies")
        st.markdown(
            "<div class='dg-warn'>These are documented historical events described here for educational purposes. "
            "They are not current threats and Data Guardian cannot prevent similar incidents.</div>",
            unsafe_allow_html=True,
        )
        for cs in CASE_STUDIES:
            with st.expander(f"{cs['icon']}  {cs['title']}", expanded=False):
                st.markdown(
                    f"""<div class='dg-card'>
                        <div class='dg-card-title'>What Happened</div>
                        <div class='dg-card-body'>{cs['what_happened']}</div></div>""",
                    unsafe_allow_html=True,
                )
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Security weakness involved**")
                    st.markdown(f"<div class='dg-danger'>{cs['weakness']}</div>", unsafe_allow_html=True)
                    st.markdown("**Why it matters**")
                    st.markdown(f"<div class='dg-warn'>{cs['why_it_matters']}</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown("**What users can learn**")
                    st.markdown(f"<div class='dg-ok'>{cs['what_users_can_learn']}</div>", unsafe_allow_html=True)
                    st.markdown("**What Data Guardian can help with**")
                    st.markdown(f"<div class='dg-info'>{cs['what_dashboard_helps']}</div>", unsafe_allow_html=True)
                    st.markdown("**What the dashboard cannot do**")
                    st.markdown(f"<div class='dg-card-body' style='color:#ff9090;'>⚠️ {cs['what_dashboard_cannot_do']}</div>", unsafe_allow_html=True)
                st.markdown(f"📎 **Source:** {cs['source']}  \n🔗 [View source]({cs['source_link']})")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Data Guardian — Privacy & Legal Policy Research",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

# Session state initialisation
if "reviewed_items" not in st.session_state:
    st.session_state.reviewed_items = {}
if "selected_app" not in st.session_state:
    st.session_state.selected_app = None
if "nav" not in st.session_state:
    st.session_state.nav = "Upload Latest Privacy Policy"

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
            <span style='font-size:2.4rem;'>🛡️</span><br/>
            <span style='font-size:1.25rem; font-weight:800; color:#00e8bb;'>Data Guardian</span><br/>
            <span style='font-size:0.8rem; color:#aac4d8;'>Privacy &amp; Legal Policy Research</span>
        </div>
        <hr style='border-color:#1e3d60; margin:0.75rem 0;'/>
        """,
        unsafe_allow_html=True,
    )

    nav_items = [
        ("📤", "Upload Latest Privacy Policy"),
        ("📱", "App Privacy Library"),
        ("🔍", "Permission Explorer"),
        ("🌐", "Third-Party Data Access"),
        ("✅", "Review My Access"),
        ("🎓", "Cybersecurity Learning Centre"),
    ]

    for icon, label in nav_items:
        active = st.session_state.nav == label
        if st.button(
            f"{icon}  {label}",
            key=f"nav_{label}",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state.nav = label
            st.rerun()

    st.markdown(
        """
        <hr style='border-color:#1e3d60; margin:0.75rem 0;'/>
        <div style='font-size:0.8rem; color:#aac4d8; text-align:center; padding-bottom:1rem;'>
            &#9888; Educational prototype.<br/>
            Demo data only &mdash; no real device access.<br/>
            Not legal advice.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Main content router ───────────────────────────────────────────────────────
nav = st.session_state.nav

if nav == "Upload Latest Privacy Policy":
    show_upload_policy()
elif nav == "App Privacy Library":
    show_app_library()
elif nav == "Permission Explorer":
    show_permission_explorer()
elif nav == "Third-Party Data Access":
    show_third_party()
elif nav == "Review My Access":
    show_review_access()
elif nav == "Cybersecurity Learning Centre":
    show_learning_centre()
