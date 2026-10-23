"""
Platform policy data — 9 platforms × 6 policy categories.
All URLs verified as official starting points (June 2025).
Direct document URLs are marked with availability_status.
"""

# ── Region labels ────────────────────────────────────────────────────────────
REGIONS = {
    "India": "India",
    "United States": "United States",
    "Global": "Global / Not region-specific",
}

# ── Policy category keys & display labels ───────────────────────────────────
POLICY_CATEGORIES = [
    ("privacy_policy",        "Privacy Policy"),
    ("terms_of_service",      "Terms of Service"),
    ("community_guidelines",  "Community Guidelines & Acceptable Use"),
    ("third_party",           "Third-Party Material & Services"),
    ("limitation_liability",  "Limitation of Liability"),
    ("arbitration",           "Arbitration & Legal Dispute Waivers"),
]

# ── Summarization prompt templates ──────────────────────────────────────────

BASE_PROMPT = """You are a privacy-focused legal-document explainer. Read the complete official policy text I provide below. Explain it in simple English that a Grade 10 student can understand. Explain difficult legal and technical terms in parentheses immediately after the term.

Focus on what the document means for an ordinary user: what rights the user has, what permissions the platform receives, what information is collected or shared (where relevant), what restrictions apply, what risks exist, and what choices the user can make.

Use clear headings, short paragraphs, and bullet points. Support your explanations with section headings or clause numbers from the supplied text wherever possible.

Do not invent information, assume a provision exists, or confuse a platform's contractual claim with a legal rule that applies everywhere. If something is missing, ambiguous, region-specific, or unsupported by the supplied text, say so explicitly.

End with:
1. What This Means for You
2. Important Things to Watch Out For
3. Questions You Should Ask Before Accepting
4. A short overall assessment of the policy's practical implications, supported by the text.

Policy text:
[PASTE THE COMPLETE POLICY TEXT HERE]"""

PRIVACY_PROMPT_TEMPLATE = """You are a privacy-focused legal-document explainer for {platform}'s Privacy Policy.

Read the complete Privacy Policy text I paste below. Explain it in simple English that a Grade 10 student can understand. Define legal and technical terms in parentheses.

Answer these questions using only what is in the supplied text:
1. What personal information is collected? (profile details, location, device info, browsing activity, uploaded content, contacts, etc.)
2. Why is the information collected?
3. How is the information used internally?
4. Is information shared with advertisers, business partners, service providers, affiliated companies, or other users? If yes, how and why?
5. Is information used for advertising, personalisation, recommendations, or AI training/features?
6. What controls can users exercise? (access, download, correct, delete)
7. How long is information retained? What happens after account deletion?
8. What security protections and limitations does the policy describe?
9. What are the most important privacy risks a user should know about?
10. Does the policy differ by region (e.g. India vs USA)?

Use headings and bullet points. Cite section headings or clause numbers from the text.
Do not invent facts. If information is missing or ambiguous, say so.

End with:
- What This Means for You
- Important Things to Watch Out For
- Questions You Should Ask Before Accepting

Policy text:
[PASTE THE COMPLETE PRIVACY POLICY TEXT HERE]"""

TOS_PROMPT_TEMPLATE = """You are a legal-document explainer for {platform}'s Terms of Service.

Read the complete Terms of Service text I paste below. Explain it in simple English that a Grade 10 student can understand. Define legal/technical terms in parentheses.

Summarise under these exact headings:
1. Who Can Use the Service
2. Rights You Grant the Platform (explain the content licence — what permissions the user grants, how broad, for how long, and for what purpose — without confusing a licence with ownership transfer)
3. Privacy
4. Personalisation and Recommendations
5. Moderation, Enforcement and Appeals
6. User Responsibilities and Prohibited Activities
7. Account Suspension and Termination
8. Payments, Purchases and Subscriptions (if applicable)
9. Third-Party Services and External Links
10. Intellectual Property and Ownership
11. Changes to the Terms
12. Disputes, Governing Law and Jurisdiction
13. Liability and Disclaimers
14. What These Terms Mean for an Ordinary User

Do not invent provisions. If a heading has no corresponding content in the supplied text, write "Not addressed in the supplied document."
Cite section headings or clause numbers from the text.

End with:
- What This Means for You
- Important Things to Watch Out For
- Questions You Should Ask Before Accepting

Terms of Service text:
[PASTE THE COMPLETE TERMS OF SERVICE TEXT HERE]"""

COMMUNITY_PROMPT_TEMPLATE = """You are a legal-document explainer for {platform}'s Community Guidelines / Acceptable Use Policy.

Read the complete document text I paste below. Explain it in simple English that a Grade 10 student can understand. Define terms in parentheses.

Cover:
1. What content is allowed?
2. What content is prohibited or restricted? (harassment, hate, threats, scams, spam, impersonation, illegal activity, misinformation, adult content, graphic content)
3. How are reports reviewed?
4. What actions can the platform take? (removal, reach restriction, suspension, permanent ban)
5. Is there an appeal process? How does it work?
6. What can a normal user do if content violates the rules?
7. Is this a standalone Community Guidelines document, part of the Terms of Service, or something else?

Cite section headings or clause numbers. Note if a topic is not addressed.

End with:
- What This Means for You
- Important Things to Watch Out For
- Questions You Should Ask Before Accepting

Policy text:
[PASTE THE COMPLETE COMMUNITY GUIDELINES / ACCEPTABLE USE POLICY TEXT HERE]"""

THIRD_PARTY_PROMPT_TEMPLATE = """You are a legal-document explainer for {platform}'s third-party material and services provisions.

Read the supplied text. Explain it in simple English that a Grade 10 student can understand. Define terms in parentheses.

Cover:
1. What counts as third-party content or services? (external websites, ads, bots, integrations, apps, marketplace sellers)
2. Who is responsible for third-party products, content, or services?
3. Does the platform endorse or guarantee third-party material?
4. What information might be shared when the user interacts with a third party?
5. What privacy or security risks may arise?
6. What happens when a user follows an external link?
7. What responsibility (if any) does the platform accept for third-party conduct or failures?
8. What precautions should ordinary users take?

Only include issues addressed by the actual policy. Label practical safety recommendations as recommendations, not contractual requirements.
Cite section headings or clause numbers.

End with:
- What This Means for You
- Important Things to Watch Out For
- Questions You Should Ask Before Accepting

Policy text:
[PASTE THE RELEVANT POLICY TEXT HERE]"""

LIABILITY_PROMPT_TEMPLATE = """You are a legal-document explainer for {platform}'s Limitation of Liability clause.

Read the supplied text. Explain it in simple English that a Grade 10 student can understand. Define all legal terms in parentheses (e.g. "consequential damages" means certain indirect financial losses caused by an event).

Cover:
1. What types of losses or damages does the platform say it is responsible for?
2. What types of losses or damages does it seek to exclude or limit?
3. Are there financial caps on liability?
4. Are indirect, incidental, special, punitive, or consequential damages discussed?
5. Does the platform disclaim warranties or guarantee of uninterrupted service?
6. Are there exceptions, or mandatory legal rights that may remain?
7. How could this provision affect an ordinary user in a practical situation?
8. Does the provision differ for users in India vs the United States?

Note: Do not assume every disclaimer is enforceable in every country. Distinguish between what the contract says and what applicable law may permit.
Cite section headings or clause numbers.

End with:
- What This Means for You
- Important Things to Watch Out For
- Questions You Should Ask Before Accepting

Policy text:
[PASTE THE LIMITATION OF LIABILITY CLAUSE TEXT HERE]"""

ARBITRATION_PROMPT_TEMPLATE = """You are a legal-document explainer for {platform}'s Arbitration and Dispute Resolution provisions.

Read the supplied text. Explain it in simple English that a Grade 10 student can understand. Define all legal terms in parentheses:
- Arbitration: a private process for resolving a dispute outside the ordinary court system
- Class action waiver: a provision that may restrict participation in a group lawsuit
- Jury trial waiver: a provision that may waive the right to have certain disputes decided by a jury
- Opt-out: a permitted process for declining an agreement or provision within the stated conditions

Cover:
1. Is arbitration mandatory or optional?
2. Must disputes be resolved individually (no class actions)?
3. Is there a jury trial waiver?
4. Are there exceptions to arbitration (e.g. small-claims court)?
5. Is there an opt-out procedure? What are the conditions and deadline?
6. What are the notice requirements and dispute-resolution steps before arbitration?
7. What is the governing law and jurisdiction?
8. Does this provision apply to users in India? Or only to users in specific countries (e.g. the United States)?

IMPORTANT: Do not present a US-specific arbitration or class-action waiver clause as applicable to Indian users without documentary support. If the provision is absent, write: "No applicable provision was identified in the official document reviewed." If applicability cannot be determined, write: "Not verified — review the current official terms."

Cite section headings or clause numbers.

End with:
- What This Means for You
- Important Things to Watch Out For
- Questions You Should Ask Before Accepting

Policy text:
[PASTE THE DISPUTE RESOLUTION / ARBITRATION CLAUSE TEXT HERE]"""


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


# ── Platform data ─────────────────────────────────────────────────────────────
# availability_status values:
#   "Verified"           — URL confirmed to load the correct document
#   "Partially verified" — Landing page confirmed; exact section may vary
#   "Embedded"           — Clause lives inside a larger document
#   "Not found"          — No standalone document found
#   "Region-specific"    — Document exists only for certain regions

PLATFORMS = {
    "WhatsApp": {
        "icon": "💬",
        "category": "Messaging & Social Networking",
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
                "notes": "Third-party provisions are embedded in the Terms of Service. Look for sections on 'Third-Party Services'.",
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
                "notes": "⚠️ Arbitration and class-action waiver provisions in WhatsApp's ToS are specifically applicable to US users. Indian users are subject to Indian law dispute resolution. Do not assume US clauses apply in India.",
            },
        },
    },

    "Instagram": {
        "icon": "📸",
        "category": "Messaging & Social Networking",
        "developer": "Meta Platforms, Inc.",
        "description": "Photo and video sharing social network.",
        "official_home": "https://help.instagram.com/",
        "policies": {
            "privacy_policy": {
                "title": "Instagram Privacy Policy (Meta Privacy Policy)",
                "url": "https://privacycenter.instagram.com/policy/",
                "region_urls": {
                    "India": "https://privacycenter.instagram.com/policy/",
                    "United States": "https://privacycenter.instagram.com/policy/",
                    "Global": "https://privacycenter.instagram.com/policy/",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "September 2023",
                "last_verified": "June 2025",
                "notes": "Instagram shares its Privacy Policy with Meta. The same document covers Facebook and other Meta products.",
            },
            "terms_of_service": {
                "title": "Instagram Terms of Use",
                "url": "https://help.instagram.com/581066165581870",
                "region_urls": {
                    "India": "https://help.instagram.com/581066165581870",
                    "United States": "https://help.instagram.com/581066165581870",
                    "Global": "https://help.instagram.com/581066165581870",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "January 2023",
                "last_verified": "June 2025",
                "notes": "Instagram-specific Terms of Use. Also references Meta Platform Terms.",
            },
            "community_guidelines": {
                "title": "Instagram Community Guidelines",
                "url": "https://help.instagram.com/477434105621119",
                "region_urls": {
                    "India": "https://help.instagram.com/477434105621119",
                    "Global": "https://help.instagram.com/477434105621119",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "Not specified",
                "last_verified": "June 2025",
                "notes": "Standalone Community Guidelines page on Instagram Help Centre.",
            },
            "third_party": {
                "title": "Third-Party Content — Instagram Terms of Use",
                "url": "https://help.instagram.com/581066165581870",
                "region_urls": {
                    "India": "https://help.instagram.com/581066165581870",
                    "Global": "https://help.instagram.com/581066165581870",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "January 2023",
                "last_verified": "June 2025",
                "notes": "Third-party provisions embedded in Terms of Use.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Instagram Terms of Use",
                "url": "https://help.instagram.com/581066165581870",
                "region_urls": {
                    "India": "https://help.instagram.com/581066165581870",
                    "Global": "https://help.instagram.com/581066165581870",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "January 2023",
                "last_verified": "June 2025",
                "notes": "Embedded in Terms of Use.",
            },
            "arbitration": {
                "title": "Dispute Resolution — Instagram Terms of Use",
                "url": "https://help.instagram.com/581066165581870",
                "region_urls": {
                    "India": "https://help.instagram.com/581066165581870",
                    "United States": "https://help.instagram.com/581066165581870",
                    "Global": "https://help.instagram.com/581066165581870",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global (US-specific arbitration provisions)",
                "last_updated": "January 2023",
                "last_verified": "June 2025",
                "notes": "⚠️ Arbitration/class-action waiver provisions are US-specific. Indian users are subject to Indian law. Do not assume US arbitration clauses apply in India.",
            },
        },
    },

    "Facebook": {
        "icon": "📘",
        "category": "Messaging & Social Networking",
        "developer": "Meta Platforms, Inc.",
        "description": "Social networking platform.",
        "official_home": "https://www.facebook.com/terms/",
        "policies": {
            "privacy_policy": {
                "title": "Meta Privacy Policy",
                "url": "https://www.facebook.com/privacy/policy/",
                "region_urls": {
                    "India": "https://www.facebook.com/privacy/policy/",
                    "United States": "https://www.facebook.com/privacy/policy/",
                    "Global": "https://www.facebook.com/privacy/policy/",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "September 2023",
                "last_verified": "June 2025",
                "notes": "Covers Facebook, Instagram, and other Meta products.",
            },
            "terms_of_service": {
                "title": "Facebook Terms of Service",
                "url": "https://www.facebook.com/terms/",
                "region_urls": {
                    "India": "https://www.facebook.com/terms/",
                    "United States": "https://www.facebook.com/terms/",
                    "Global": "https://www.facebook.com/terms/",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "September 2023",
                "last_verified": "June 2025",
                "notes": "Facebook-specific Terms. Also see Meta Platform Terms for developers.",
            },
            "community_guidelines": {
                "title": "Facebook Community Standards",
                "url": "https://transparency.fb.com/policies/community-standards/",
                "region_urls": {
                    "India": "https://transparency.fb.com/policies/community-standards/",
                    "Global": "https://transparency.fb.com/policies/community-standards/",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "Updated regularly",
                "last_verified": "June 2025",
                "notes": "Facebook uses 'Community Standards' as its equivalent to community guidelines. This is a separate, detailed document.",
            },
            "third_party": {
                "title": "Third-Party Content — Facebook Terms of Service",
                "url": "https://www.facebook.com/terms/",
                "region_urls": {
                    "India": "https://www.facebook.com/terms/",
                    "Global": "https://www.facebook.com/terms/",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "September 2023",
                "last_verified": "June 2025",
                "notes": "Embedded in Terms of Service.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Facebook Terms of Service",
                "url": "https://www.facebook.com/terms/",
                "region_urls": {
                    "India": "https://www.facebook.com/terms/",
                    "Global": "https://www.facebook.com/terms/",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "September 2023",
                "last_verified": "June 2025",
                "notes": "Embedded in Terms of Service.",
            },
            "arbitration": {
                "title": "Dispute Resolution — Facebook Terms of Service",
                "url": "https://www.facebook.com/terms/",
                "region_urls": {
                    "India": "https://www.facebook.com/terms/",
                    "United States": "https://www.facebook.com/terms/",
                    "Global": "https://www.facebook.com/terms/",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global (US-specific arbitration clause)",
                "last_updated": "September 2023",
                "last_verified": "June 2025",
                "notes": "⚠️ Arbitration/class-action waiver is US-specific. Indian users dispute under Indian law.",
            },
        },
    },

    "Telegram": {
        "icon": "✈️",
        "category": "Messaging & Social Networking",
        "developer": "Telegram FZ-LLC",
        "description": "Cloud-based messaging and broadcasting platform.",
        "official_home": "https://telegram.org/",
        "policies": {
            "privacy_policy": {
                "title": "Telegram Privacy Policy",
                "url": "https://telegram.org/privacy",
                "region_urls": {
                    "India": "https://telegram.org/privacy",
                    "United States": "https://telegram.org/privacy",
                    "Global": "https://telegram.org/privacy",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "August 2023",
                "last_verified": "June 2025",
                "notes": "Single global privacy policy.",
            },
            "terms_of_service": {
                "title": "Telegram Terms of Service",
                "url": "https://telegram.org/tos",
                "region_urls": {
                    "India": "https://telegram.org/tos",
                    "United States": "https://telegram.org/tos",
                    "Global": "https://telegram.org/tos",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "September 2022",
                "last_verified": "June 2025",
                "notes": "Main Telegram Terms of Service. Separate API terms exist for developers.",
            },
            "community_guidelines": {
                "title": "Telegram Usage Guidelines (within ToS)",
                "url": "https://telegram.org/tos",
                "region_urls": {
                    "India": "https://telegram.org/tos",
                    "Global": "https://telegram.org/tos",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "September 2022",
                "last_verified": "June 2025",
                "notes": "Telegram does not publish a separate Community Guidelines document. Acceptable use rules are embedded in the Terms of Service.",
            },
            "third_party": {
                "title": "Third-Party Content — Telegram Privacy Policy & ToS",
                "url": "https://telegram.org/privacy",
                "region_urls": {
                    "India": "https://telegram.org/privacy",
                    "Global": "https://telegram.org/privacy",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "August 2023",
                "last_verified": "June 2025",
                "notes": "Third-party references embedded in Privacy Policy and ToS. Also see Bot API terms.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Telegram Terms of Service",
                "url": "https://telegram.org/tos",
                "region_urls": {
                    "India": "https://telegram.org/tos",
                    "Global": "https://telegram.org/tos",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "September 2022",
                "last_verified": "June 2025",
                "notes": "Embedded in Terms of Service.",
            },
            "arbitration": {
                "title": "Dispute Resolution — Telegram Terms of Service",
                "url": "https://telegram.org/tos",
                "region_urls": {
                    "India": "https://telegram.org/tos",
                    "Global": "https://telegram.org/tos",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "September 2022",
                "last_verified": "June 2025",
                "notes": "Telegram's ToS specifies governing law and jurisdiction. Review current document for arbitration/class-action waiver applicability to Indian users.",
            },
        },
    },

    "Snapchat": {
        "icon": "👻",
        "category": "Messaging & Social Networking",
        "developer": "Snap Inc.",
        "description": "Multimedia messaging and social media app.",
        "official_home": "https://values.snap.com/",
        "policies": {
            "privacy_policy": {
                "title": "Snap Privacy Policy",
                "url": "https://values.snap.com/privacy/privacy-policy",
                "region_urls": {
                    "India": "https://values.snap.com/privacy/privacy-policy",
                    "United States": "https://values.snap.com/privacy/privacy-policy",
                    "Global": "https://values.snap.com/privacy/privacy-policy",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "February 2024",
                "last_verified": "June 2025",
                "notes": "Single global Privacy Policy covering Snapchat and other Snap services.",
            },
            "terms_of_service": {
                "title": "Snap Terms of Service",
                "url": "https://values.snap.com/privacy/terms-of-service",
                "region_urls": {
                    "India": "https://values.snap.com/privacy/terms-of-service",
                    "United States": "https://values.snap.com/privacy/terms-of-service",
                    "Global": "https://values.snap.com/privacy/terms-of-service",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "February 2024",
                "last_verified": "June 2025",
                "notes": "Includes arbitration clause applicable to US users.",
            },
            "community_guidelines": {
                "title": "Snap Community Guidelines",
                "url": "https://values.snap.com/privacy/transparency/community-guidelines",
                "region_urls": {
                    "India": "https://values.snap.com/privacy/transparency/community-guidelines",
                    "Global": "https://values.snap.com/privacy/transparency/community-guidelines",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "Not specified",
                "last_verified": "June 2025",
                "notes": "Standalone Community Guidelines document.",
            },
            "third_party": {
                "title": "Third-Party Content — Snap Terms of Service",
                "url": "https://values.snap.com/privacy/terms-of-service",
                "region_urls": {
                    "India": "https://values.snap.com/privacy/terms-of-service",
                    "Global": "https://values.snap.com/privacy/terms-of-service",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "February 2024",
                "last_verified": "June 2025",
                "notes": "Embedded in Terms of Service.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Snap Terms of Service",
                "url": "https://values.snap.com/privacy/terms-of-service",
                "region_urls": {
                    "India": "https://values.snap.com/privacy/terms-of-service",
                    "Global": "https://values.snap.com/privacy/terms-of-service",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "February 2024",
                "last_verified": "June 2025",
                "notes": "Embedded in Terms of Service.",
            },
            "arbitration": {
                "title": "Arbitration and Class Action Waiver — Snap Terms of Service",
                "url": "https://values.snap.com/privacy/terms-of-service",
                "region_urls": {
                    "India": "https://values.snap.com/privacy/terms-of-service",
                    "United States": "https://values.snap.com/privacy/terms-of-service",
                    "Global": "https://values.snap.com/privacy/terms-of-service",
                },
                "availability_status": "Embedded",
                "applicable_region": "United States — specific arbitration and class action waiver",
                "last_updated": "February 2024",
                "last_verified": "June 2025",
                "notes": "⚠️ Snap's arbitration and class-action waiver provisions are explicitly for US users. Indian users are subject to Indian law and the jurisdiction specified in their regional terms.",
            },
        },
    },

    "Flipkart": {
        "icon": "🛍️",
        "category": "E-Commerce",
        "developer": "Flipkart Internet Pvt. Ltd. (Walmart Group)",
        "description": "Major Indian e-commerce marketplace.",
        "official_home": "https://www.flipkart.com/",
        "policies": {
            "privacy_policy": {
                "title": "Flipkart Privacy Policy",
                "url": "https://www.flipkart.com/pages/privacypolicy",
                "region_urls": {
                    "India": "https://www.flipkart.com/pages/privacypolicy",
                    "Global": "https://www.flipkart.com/pages/privacypolicy",
                },
                "availability_status": "Verified",
                "applicable_region": "India (primary market)",
                "last_updated": "2023 (approximate)",
                "last_verified": "June 2025",
                "notes": "Flipkart primarily operates in India. This is the India-applicable Privacy Policy.",
            },
            "terms_of_service": {
                "title": "Flipkart Terms of Use",
                "url": "https://www.flipkart.com/pages/terms",
                "region_urls": {
                    "India": "https://www.flipkart.com/pages/terms",
                },
                "availability_status": "Verified",
                "applicable_region": "India",
                "last_updated": "2023 (approximate)",
                "last_verified": "June 2025",
                "notes": "India-specific Terms of Use.",
            },
            "community_guidelines": {
                "title": "Flipkart Marketplace Seller / User Conduct Terms",
                "url": "https://www.flipkart.com/pages/terms",
                "region_urls": {
                    "India": "https://www.flipkart.com/pages/terms",
                },
                "availability_status": "Embedded",
                "applicable_region": "India",
                "last_updated": "2023 (approximate)",
                "last_verified": "June 2025",
                "notes": "Flipkart is an e-commerce platform. Acceptable use and conduct rules are embedded in the Terms of Use rather than a separate Community Guidelines document.",
            },
            "third_party": {
                "title": "Third-Party Services — Flipkart Terms of Use",
                "url": "https://www.flipkart.com/pages/terms",
                "region_urls": {
                    "India": "https://www.flipkart.com/pages/terms",
                },
                "availability_status": "Embedded",
                "applicable_region": "India",
                "last_updated": "2023 (approximate)",
                "last_verified": "June 2025",
                "notes": "Third-party seller and service provisions embedded in Terms of Use.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Flipkart Terms of Use",
                "url": "https://www.flipkart.com/pages/terms",
                "region_urls": {
                    "India": "https://www.flipkart.com/pages/terms",
                },
                "availability_status": "Embedded",
                "applicable_region": "India",
                "last_updated": "2023 (approximate)",
                "last_verified": "June 2025",
                "notes": "Embedded in Terms of Use. Indian Consumer Protection Act provisions may override certain limitations.",
            },
            "arbitration": {
                "title": "Dispute Resolution — Flipkart Terms of Use",
                "url": "https://www.flipkart.com/pages/terms",
                "region_urls": {
                    "India": "https://www.flipkart.com/pages/terms",
                },
                "availability_status": "Embedded",
                "applicable_region": "India",
                "last_updated": "2023 (approximate)",
                "last_verified": "June 2025",
                "notes": "Flipkart's dispute resolution provisions are India-specific and subject to Indian Arbitration and Conciliation Act. No US-style class-action waiver applies.",
            },
        },
    },

    "Google": {
        "icon": "🔵",
        "category": "Search, Email & Online Services",
        "developer": "Google LLC (Alphabet Inc.)",
        "description": "Search engine, advertising, and cloud services platform.",
        "official_home": "https://policies.google.com/",
        "policies": {
            "privacy_policy": {
                "title": "Google Privacy Policy",
                "url": "https://policies.google.com/privacy",
                "region_urls": {
                    "India": "https://policies.google.com/privacy",
                    "United States": "https://policies.google.com/privacy",
                    "Global": "https://policies.google.com/privacy",
                },
                "availability_status": "Verified",
                "applicable_region": "Global (covers all Google services)",
                "last_updated": "Periodically updated — check page for current date",
                "last_verified": "June 2025",
                "notes": "Covers all Google services including Search, Maps, YouTube, Drive, and Gmail. Product-specific terms may supplement.",
            },
            "terms_of_service": {
                "title": "Google Terms of Service",
                "url": "https://policies.google.com/terms",
                "region_urls": {
                    "India": "https://policies.google.com/terms",
                    "United States": "https://policies.google.com/terms",
                    "Global": "https://policies.google.com/terms",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "January 2022 (major revision)",
                "last_verified": "June 2025",
                "notes": "General Google Terms covering all services. Product-specific terms may apply additionally.",
            },
            "community_guidelines": {
                "title": "Google Prohibited Content Policies",
                "url": "https://policies.google.com/",
                "region_urls": {
                    "India": "https://policies.google.com/",
                    "Global": "https://policies.google.com/",
                },
                "availability_status": "Partially verified",
                "applicable_region": "Global",
                "last_updated": "Varies by product",
                "last_verified": "June 2025",
                "notes": "Google does not publish a single 'Community Guidelines' document. Each product (YouTube, Play Store, etc.) has its own content policies. The policies.google.com landing page is the official starting point.",
            },
            "third_party": {
                "title": "Third-Party Services — Google Terms of Service",
                "url": "https://policies.google.com/terms",
                "region_urls": {
                    "India": "https://policies.google.com/terms",
                    "Global": "https://policies.google.com/terms",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "January 2022",
                "last_verified": "June 2025",
                "notes": "Third-party provisions embedded in Google Terms of Service.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Google Terms of Service",
                "url": "https://policies.google.com/terms",
                "region_urls": {
                    "India": "https://policies.google.com/terms",
                    "Global": "https://policies.google.com/terms",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "January 2022",
                "last_verified": "June 2025",
                "notes": "Embedded in Terms of Service.",
            },
            "arbitration": {
                "title": "Dispute Resolution — Google Terms of Service",
                "url": "https://policies.google.com/terms",
                "region_urls": {
                    "India": "https://policies.google.com/terms",
                    "United States": "https://policies.google.com/terms",
                    "Global": "https://policies.google.com/terms",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global (US-specific arbitration provisions)",
                "last_updated": "January 2022",
                "last_verified": "June 2025",
                "notes": "⚠️ Google's ToS contains US-specific arbitration and class-action waiver provisions that apply to users contracting with Google LLC. Indian users contract with Google India Pvt. Ltd. and are subject to Indian law dispute resolution.",
            },
        },
    },

    "Gmail": {
        "icon": "📧",
        "category": "Search, Email & Online Services",
        "developer": "Google LLC (Alphabet Inc.)",
        "description": "Google's email and communication service.",
        "official_home": "https://www.google.com/gmail/about/",
        "policies": {
            "privacy_policy": {
                "title": "Google Privacy Policy (applies to Gmail)",
                "url": "https://policies.google.com/privacy",
                "region_urls": {
                    "India": "https://policies.google.com/privacy",
                    "United States": "https://policies.google.com/privacy",
                    "Global": "https://policies.google.com/privacy",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "Periodically updated",
                "last_verified": "June 2025",
                "notes": "Gmail does not have a separate Privacy Policy. The general Google Privacy Policy governs Gmail, with Gmail-specific notes inside.",
            },
            "terms_of_service": {
                "title": "Gmail Program Policies & Google Terms of Service",
                "url": "https://policies.google.com/terms",
                "region_urls": {
                    "India": "https://policies.google.com/terms",
                    "United States": "https://policies.google.com/terms",
                    "Global": "https://policies.google.com/terms",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "January 2022",
                "last_verified": "June 2025",
                "notes": "Gmail is governed by Google's general Terms of Service, supplemented by Gmail Program Policies.",
            },
            "community_guidelines": {
                "title": "Gmail Program Policies",
                "url": "https://support.google.com/mail/answer/8984743",
                "region_urls": {
                    "India": "https://support.google.com/mail/answer/8984743",
                    "Global": "https://support.google.com/mail/answer/8984743",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "Not specified",
                "last_verified": "June 2025",
                "notes": "Gmail-specific acceptable use rules. Supplement to Google's general policies.",
            },
            "third_party": {
                "title": "Third-Party App Access — Google Account Permissions",
                "url": "https://support.google.com/accounts/answer/3466521",
                "region_urls": {
                    "India": "https://support.google.com/accounts/answer/3466521",
                    "Global": "https://support.google.com/accounts/answer/3466521",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "Not specified",
                "last_verified": "June 2025",
                "notes": "Official Google support page on third-party app access to Google account data including Gmail.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — Google Terms of Service",
                "url": "https://policies.google.com/terms",
                "region_urls": {
                    "India": "https://policies.google.com/terms",
                    "Global": "https://policies.google.com/terms",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "January 2022",
                "last_verified": "June 2025",
                "notes": "Same limitation clause as Google general Terms.",
            },
            "arbitration": {
                "title": "Dispute Resolution — Google Terms of Service",
                "url": "https://policies.google.com/terms",
                "region_urls": {
                    "India": "https://policies.google.com/terms",
                    "United States": "https://policies.google.com/terms",
                    "Global": "https://policies.google.com/terms",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global (US-specific arbitration provisions)",
                "last_updated": "January 2022",
                "last_verified": "June 2025",
                "notes": "⚠️ Same as Google general Terms. US-specific arbitration applies to users contracting with Google LLC. Indian users contract with Google India Pvt. Ltd.",
            },
        },
    },

    "GitHub": {
        "icon": "🐙",
        "category": "Developer & Collaboration Platforms",
        "developer": "GitHub, Inc. (Microsoft)",
        "description": "Code hosting, version control, and developer collaboration platform.",
        "official_home": "https://docs.github.com/en/site-policy/",
        "policies": {
            "privacy_policy": {
                "title": "GitHub Privacy Statement",
                "url": "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement",
                "region_urls": {
                    "India": "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement",
                    "United States": "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement",
                    "Global": "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "Periodically updated — check page",
                "last_verified": "June 2025",
                "notes": "GitHub calls its privacy document a 'Privacy Statement' rather than a Privacy Policy.",
            },
            "terms_of_service": {
                "title": "GitHub Terms of Service",
                "url": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                "region_urls": {
                    "India": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                    "United States": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                    "Global": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "Not specified — check page",
                "last_verified": "June 2025",
                "notes": "Main GitHub Terms of Service for individual accounts.",
            },
            "community_guidelines": {
                "title": "GitHub Community Guidelines & Acceptable Use Policies",
                "url": "https://docs.github.com/en/site-policy/github-terms/github-community-guidelines",
                "region_urls": {
                    "India": "https://docs.github.com/en/site-policy/github-terms/github-community-guidelines",
                    "Global": "https://docs.github.com/en/site-policy/github-terms/github-community-guidelines",
                },
                "availability_status": "Verified",
                "applicable_region": "Global",
                "last_updated": "Not specified — check page",
                "last_verified": "June 2025",
                "notes": "GitHub has separate Community Guidelines and a detailed Acceptable Use Policy. Both are available at docs.github.com/en/site-policy.",
            },
            "third_party": {
                "title": "Third-Party Applications — GitHub Terms of Service",
                "url": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                "region_urls": {
                    "India": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                    "Global": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "Not specified",
                "last_verified": "June 2025",
                "notes": "Third-party application provisions embedded in Terms of Service.",
            },
            "limitation_liability": {
                "title": "Limitation of Liability — GitHub Terms of Service",
                "url": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                "region_urls": {
                    "India": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                    "Global": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "Not specified",
                "last_verified": "June 2025",
                "notes": "Embedded in Terms of Service.",
            },
            "arbitration": {
                "title": "Dispute Resolution — GitHub Terms of Service",
                "url": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                "region_urls": {
                    "India": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                    "United States": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                    "Global": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
                },
                "availability_status": "Embedded",
                "applicable_region": "Global",
                "last_updated": "Not specified",
                "last_verified": "June 2025",
                "notes": "Review current GitHub Terms for dispute resolution and arbitration provisions. Note whether US-specific arbitration applies to Indian users.",
            },
        },
    },
}

# Platform categories for grouping
PLATFORM_CATEGORIES = {
    "Messaging & Social Networking": ["WhatsApp", "Instagram", "Facebook", "Telegram", "Snapchat"],
    "E-Commerce":                    ["Flipkart"],
    "Search, Email & Online Services": ["Google", "Gmail"],
    "Developer & Collaboration Platforms": ["GitHub"],
}

AVAILABILITY_STYLES = {
    "Verified":             ("status-verified", "✅ Verified"),
    "Partially verified":   ("status-review",   "🔍 Partially Verified"),
    "Embedded":             ("status-demo",      "📎 Embedded in Document"),
    "Not found":            ("badge-unknown",    "⚪ Not Found"),
    "Region-specific":      ("status-updated",   "🌍 Region-Specific"),
}
