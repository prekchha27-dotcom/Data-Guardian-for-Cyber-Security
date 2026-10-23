"""
Central data module — app catalogue, permissions knowledge base, risk rules.
All data is demonstration material unless explicitly labelled otherwise.
"""

# ── App Catalogue ────────────────────────────────────────────────────────────

APPS = {
    "Facebook": {
        "icon": "📘",
        "developer": "Meta Platforms, Inc.",
        "website": "https://www.facebook.com",
        "privacy_policy": "https://www.facebook.com/privacy/policy/",
        "policy_updated": "September 2023",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo",
        "status_label": "Demo Data",
        "category": "Social Media",
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
            "Location (if permitted)",
            "Contacts (if permitted)",
            "Browsing & activity data (on and off Facebook via Meta Pixel)",
            "Device & connection information",
            "Messages (not E2EE by default)",
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
        "icon": "📸",
        "developer": "Meta Platforms, Inc.",
        "website": "https://www.instagram.com",
        "privacy_policy": "https://privacycenter.instagram.com/policy/",
        "policy_updated": "September 2023",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo",
        "status_label": "Demo Data",
        "category": "Social Media",
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
        "icon": "💬",
        "developer": "Meta Platforms, Inc.",
        "website": "https://www.whatsapp.com",
        "privacy_policy": "https://www.whatsapp.com/legal/privacy-policy/",
        "policy_updated": "September 2023",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo",
        "status_label": "Demo Data",
        "category": "Messaging",
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
            "Device & connection data", "Usage data",
            "Profile photo & status (if public)",
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
        "icon": "👻",
        "developer": "Snap Inc.",
        "website": "https://www.snapchat.com",
        "privacy_policy": "https://snap.com/en-US/privacy/privacy-policy",
        "policy_updated": "February 2024",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo",
        "status_label": "Demo Data",
        "category": "Social Media",
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
        "icon": "✈️",
        "developer": "Telegram FZ-LLC",
        "website": "https://telegram.org",
        "privacy_policy": "https://telegram.org/privacy",
        "policy_updated": "August 2023",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo",
        "status_label": "Demo Data",
        "category": "Messaging",
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
        "icon": "🛒",
        "developer": "Amazon.com, Inc.",
        "website": "https://www.amazon.com",
        "privacy_policy": "https://www.amazon.com/gp/help/customer/display.html?nodeId=GX7NJQ4ZB8MHFRNJ",
        "policy_updated": "August 2023",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo",
        "status_label": "Demo Data",
        "category": "E-Commerce",
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
        "icon": "🛍️",
        "developer": "Flipkart Internet Pvt. Ltd.",
        "website": "https://www.flipkart.com",
        "privacy_policy": "https://www.flipkart.com/pages/privacypolicy",
        "policy_updated": "2023 (approximate)",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo",
        "status_label": "Demo Data",
        "category": "E-Commerce",
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
        "icon": "👗",
        "developer": "Myntra Designs Pvt. Ltd. (Flipkart Group)",
        "website": "https://www.myntra.com",
        "privacy_policy": "https://www.myntra.com/privacypolicy",
        "policy_updated": "2023 (approximate)",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo",
        "status_label": "Demo Data",
        "category": "E-Commerce",
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
        "icon": "🛵",
        "developer": "Roppen Transportation Services Pvt. Ltd.",
        "website": "https://rapido.bike",
        "privacy_policy": "https://rapido.bike/privacy-policy",
        "policy_updated": "2023 (approximate)",
        "source_date": "Demonstration data — policy link verified June 2025",
        "status": "demo",
        "status_label": "Demo Data",
        "category": "Ride-Hailing",
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

# ── Permissions Knowledge Base ────────────────────────────────────────────────

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
            "brokers or used for highly targeted advertising. It can also be exploited in the "
            "event of an account compromise."
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
            "Video calling or live streaming",
            "Scanning QR codes or barcodes",
            "Capturing photos to post or share",
            "Augmented reality features (filters, try-on)",
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
            "Voice or video calls",
            "Voice-to-text / dictation",
            "Voice search",
            "Audio messages",
            "Voice assistants (Alexa, Siri, Google Assistant integrations)",
        ],
        "data_exposed": (
            "Any audio captured while the app has microphone access. "
            "This could include conversations, background sounds, and environmental audio."
        ),
        "when_unnecessary": (
            "A shopping or news app with no calling, voice search, or audio recording feature."
        ),
        "risks": (
            "Continuous microphone access is one of the most sensitive permissions. "
            "While accidental or malicious activation is technically possible, "
            "this is rare and typically requires a device or app compromise. "
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
            "Selecting profile pictures or post images",
            "Sharing photos in messages",
            "Downloading media received in the app",
            "Saving screenshots or generated content",
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
            "Caching media for offline use",
            "Downloading files or documents",
            "Saving or opening attachments",
        ],
        "data_exposed": (
            "On older Android versions, this permission gives broad access to all files. "
            "On Android 10 and later, scoped storage limits access to the app's own files. "
            "Granting broad storage access to untrustworthy apps is higher risk."
        ),
        "when_unnecessary": (
            "Apps that don't handle files, documents, or offline media downloads."
        ),
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
            "Adding ride or order reminders",
            "Scheduling events from the app",
            "Productivity or meeting integrations",
        ],
        "data_exposed": (
            "Event titles, dates, times, locations, attendees, and notes in your calendar. "
            "This can reveal appointments at medical facilities, legal offices, or personal events."
        ),
        "when_unnecessary": (
            "Social media, shopping, or entertainment apps that don't involve scheduling."
        ),
        "risks": (
            "Calendar data can reveal sensitive personal information. "
            "Attendee information exposes other people's data."
        ),
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
        "when_unnecessary": (
            "Apps you use infrequently where notifications would be unwanted."
        ),
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
        "when_unnecessary": (
            "Any app that is not a dedicated SMS or messaging application and does not need OTP autofill."
        ),
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
        "when_unnecessary": (
            "Apps where phone number autofill is not needed and call detection is irrelevant."
        ),
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
        "when_unnecessary": (
            "Apps with no wearable, proximity, or smart-home integration."
        ),
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

# ── Risk level helpers ────────────────────────────────────────────────────────

RISK_LABELS = {
    "low":     ("🟢", "Lower Concern",           "badge-low"),
    "review":  ("🟡", "Review Recommended",       "badge-review"),
    "high":    ("🔴", "Higher Concern",            "badge-high"),
    "unknown": ("⚪", "Unknown / Insufficient Evidence", "badge-unknown"),
}

STATUS_LABELS = {
    "demo":     ("status-demo",    "⚠️ Demo Data"),
    "verified": ("status-verified","✅ Source Verified"),
    "review":   ("status-review",  "🔍 Needs Review"),
    "updated":  ("status-updated", "📋 Policy Update Detected"),
}

# ── Third-party concepts glossary ────────────────────────────────────────────

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

# ── Policy change demo data ───────────────────────────────────────────────────

POLICY_CHANGES = [
    {
        "app": "Facebook",
        "date": "September 2023",
        "status": "change_detected",
        "summary": (
            "Meta updated its Privacy Policy to reflect new AI training data practices "
            "and updated information about data use across Meta technologies. "
            "The policy clarified how information from third-party sources is combined "
            "with on-platform activity."
        ),
        "old_excerpt": "We use information we have to show you ads that we think will be relevant to you.",
        "new_excerpt": (
            "We use information we have, including your activity on and off Meta technologies, "
            "to show you ads, offers, and other sponsored content we think will be relevant to you. "
            "We also use this information to train AI models."
        ),
        "note": "⚠️ This is demonstration data based on publicly reported policy updates. It is not a live monitored comparison.",
        "policy_link": "https://www.facebook.com/privacy/policy/",
    },
    {
        "app": "Snapchat",
        "date": "February 2024",
        "status": "change_detected",
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
        "note": "⚠️ This is demonstration data based on publicly reported policy updates. It is not a live monitored comparison.",
        "policy_link": "https://snap.com/en-US/privacy/privacy-policy",
    },
    {
        "app": "WhatsApp",
        "date": "No recent change detected in demo data",
        "status": "no_change",
        "summary": "No significant policy change was detected in the demonstration comparison.",
        "old_excerpt": None,
        "new_excerpt": None,
        "note": "⚠️ This is demonstration data. Live policy monitoring is not active.",
        "policy_link": "https://www.whatsapp.com/legal/privacy-policy/",
    },
]
