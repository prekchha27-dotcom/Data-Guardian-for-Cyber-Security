"""Third-Party Data Access — who else can access my data & data-flow diagram."""

import streamlit as st
from sections.data import GLOSSARY


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
        "risk_note": (
            "Location history can reveal home address, workplace, medical appointments, "
            "religious attendance, and daily routine. Once shared, it may be retained indefinitely."
        ),
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
        "risk_note": (
            "Your contacts have not consented to share their data. "
            "Contact data is used to build social graphs and identify relationships."
        ),
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
        "risk_note": (
            "OAuth scopes may grant third-party apps access to your profile even if you "
            "haven't explicitly shared it. Review connected apps regularly."
        ),
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
        "risk_note": (
            "Cross-site tracking via embedded pixels, SDKs, and cookies can build detailed profiles "
            "of your interests, health concerns, financial status, and political views "
            "based on what you read and click."
        ),
        "action": (
            "Use browser privacy settings, content blocking extensions, and opt out of "
            "personalised advertising in app settings where available."
        ),
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
        "risk_note": (
            "Access tokens and session cookies are the keys to your account. "
            "If stolen via phishing, XSS, or a malicious third-party app, "
            "an attacker can act as you without knowing your password."
        ),
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
        "Their access depends on the OAuth scopes you approved. "
        "An app may retain access even after you stop using it unless you explicitly revoke it."
    ),
    "Third-Party SDKs & Service Providers": (
        "Software components embedded by the developer for analytics, advertising, crash reporting, "
        "or other services. They may collect data as part of their function. "
        "Their actual access depends on the developer's implementation and configuration. "
        "Examples include analytics SDKs, advertising networks, and payment processors."
    ),
    "Business Partners & Data Recipients": (
        "Organisations that may receive information under the service's privacy practices, "
        "such as affiliated companies, advertisers, data enrichment partners, or legal authorities. "
        "The scope and basis for sharing are described (with varying clarity) in each app's privacy policy."
    ),
    "Potential Attackers": (
        "Individuals who exploit phishing, stolen session tokens, insecure OAuth implementations, "
        "XSS vulnerabilities, or other weaknesses to gain unauthorised access. "
        "They are not legitimate recipients — they exploit security weaknesses. "
        "Multi-factor authentication and regular session reviews reduce this risk."
    ),
}


def _risk_html(level: str) -> str:
    from sections.data import RISK_LABELS
    icon, label, cls = RISK_LABELS.get(level, RISK_LABELS["unknown"])
    return f'<span class="{cls}">{icon} {label}</span>'


def show_third_party():
    st.markdown("## 🌐 Third-Party Data Access")
    st.markdown("### Who Else Can Access My Data?")
    st.markdown(
        "<div class='dg-info'>"
        "When you use an app, your data may flow beyond the app itself — to service providers, "
        "advertising networks, affiliated companies, and potentially to third-party apps you "
        "have authorised. This section explains each type of recipient and lets you explore "
        "data flows by category."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Recipient types ────────────────────────────────────────────────────────
    st.markdown("#### Types of Data Recipients")
    for rtype, desc in RECIPIENT_TYPES.items():
        with st.expander(f"🔹 {rtype}"):
            st.markdown(
                f"<div class='dg-card-body'>{desc}</div>",
                unsafe_allow_html=True,
            )

    st.markdown(
        "<div class='dg-warn'>"
        "These groups do <strong>not</strong> automatically receive the same information. "
        "Access depends on permissions, authorisation scopes, service design, settings, "
        "and circumstances. The presence of an SDK does not prove it is actively collecting "
        "or misusing data."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Interactive data-flow diagram ──────────────────────────────────────────
    st.markdown("#### 🔄 Interactive Data Flow Explorer")
    st.markdown(
        "Select a data category to see how it may flow from your device to potential recipients."
    )

    selected_category = st.selectbox(
        "Choose a data category",
        list(DATA_FLOWS.keys()),
        key="df_category",
    )

    flow = DATA_FLOWS[selected_category]

    # Visual flow
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;flex-wrap:wrap;gap:0.5rem;
                    margin:1rem 0;padding:1rem;background:#0d2236;border-radius:10px;
                    border:1px solid #1e3a5f;">
            <div style="background:#1a3a5c;border-radius:8px;padding:0.5rem 0.9rem;
                        color:#e8f0f7;font-weight:600;">👤 You</div>
            <div style="color:#00d4aa;font-size:1.3rem;">→</div>
            <div style="background:#0a3a2a;border-radius:8px;padding:0.5rem 0.9rem;
                        color:#00d4aa;font-weight:600;">📱 App</div>
            <div style="color:#00d4aa;font-size:1.3rem;">→</div>
            <div style="background:#1a3a5c;border-radius:8px;padding:0.5rem 0.9rem;
                        color:#55ccff;font-weight:600;">📦 {selected_category}</div>
            <div style="color:#00d4aa;font-size:1.3rem;">→</div>
            <div style="background:#2a1a3a;border-radius:8px;padding:0.5rem 0.9rem;
                        color:#cc99ff;font-weight:600;">🌐 Possible Recipients</div>
            <div style="color:#00d4aa;font-size:1.3rem;">→</div>
            {_risk_html(flow['risk'])}
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(f"**Data description:** {flow['description']}")
        st.markdown(f"**How the app uses it:** {flow['app_use']}")

        st.markdown("**Possible recipients:**")
        for recipient, reason in flow["possible_recipients"]:
            st.markdown(
                f"""
                <div style="background:#0d2236;border:1px solid #1e3a5f;border-radius:8px;
                            padding:0.5rem 0.8rem;margin-bottom:0.4rem;">
                    <strong style="color:#00d4aa;">{recipient}</strong><br/>
                    <span style="font-size:0.88rem;color:#b0c8e0;">{reason}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with c2:
        st.markdown("**Risk explanation:**")
        st.markdown(
            f"<div class='dg-warn'>{flow['risk_note']}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("**Recommended action:**")
        st.markdown(
            f"<div class='dg-ok'>{flow['action']}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='dg-info'>"
            "📎 <strong>Evidence note:</strong> The recipient relationships shown are "
            "general illustrative examples based on common privacy policy practices and "
            "documented industry patterns. Specific relationships for specific apps are "
            "shown in the App Privacy Library."
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Concepts glossary ──────────────────────────────────────────────────────
    st.markdown("#### 📖 Key Concepts Glossary")
    st.markdown(
        "These are the technical concepts that describe how data flows, who accesses it, "
        "and what risks exist."
    )

    for term, definition in GLOSSARY.items():
        with st.expander(f"📌 {term}"):
            st.markdown(
                f"<div class='dg-card-body'>{definition}</div>",
                unsafe_allow_html=True,
            )
