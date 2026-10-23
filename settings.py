"""Settings & About page."""

import streamlit as st


def show_settings():
    st.markdown("## ⚙️ Settings & About")

    tab_about, tab_data, tab_settings = st.tabs(
        ["ℹ️ About Data Guardian", "📊 Data & Privacy", "🛠️ Settings"]
    )

    # ── About ──────────────────────────────────────────────────────────────────
    with tab_about:
        st.markdown(
            """
            <div style="background:#0d2236;border:1px solid #1e3a5f;border-radius:14px;
                        padding:1.8rem 2rem;margin-bottom:1rem;">
                <div style="font-size:3rem;margin-bottom:0.5rem;">🛡️</div>
                <h2 style="color:#00d4aa;margin:0 0 0.5rem 0;">Data Guardian</h2>
                <p style="color:#b0cce0;font-size:1rem;line-height:1.7;margin:0;">
                    An AI-powered privacy and cybersecurity awareness dashboard that helps users
                    understand application permissions, third-party data access, privacy risks,
                    and guides them towards appropriate security actions using evidence-based explanations.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### Product Vision")
        st.markdown(
            """
            Data Guardian helps users answer five key questions:

            1. 📌 **What information can an application potentially access?**
            2. ❓ **Why might the application need that information?**
            3. 👥 **Who else might receive or process that information?**
            4. ⚠️ **What privacy or cybersecurity risks could arise?**
            5. ✅ **What practical steps can I take to review or reduce those risks?**
            """
        )

        st.markdown(
            "<div class='dg-info'>"
            "<strong>What Data Guardian is:</strong> An educational awareness tool that explains "
            "app permissions, third-party data flows, and cybersecurity risks in plain language."
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='dg-warn'>"
            "<strong>What Data Guardian is not:</strong> An antivirus, firewall, vulnerability scanner, "
            "guaranteed threat-prevention system, or live device monitoring tool. "
            "It does not inspect your device, change permissions, or revoke authorisations."
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown("#### Technology Stack")
        st.markdown(
            """
            | Component | Technology |
            |-----------|-----------|
            | Frontend & UI | Streamlit (Python) |
            | Data & Logic | Python (built-in modules only) |
            | Charts | Streamlit native metrics |
            | Deployment | Local / Streamlit Community Cloud |
            | External APIs | None (educational prototype) |
            | AI Service | Not connected — demo explanations only |
            """
        )

        st.markdown("#### Version")
        st.markdown(
            """
            | Field | Value |
            |-------|-------|
            | Version | 1.0 (Prototype) |
            | Built for | Academic / educational demonstration |
            | Author | Prekchha Thakur |
            | Data status | All app profiles are demonstration data |
            | Live monitoring | Not active |
            """
        )

    # ── Data & Privacy ─────────────────────────────────────────────────────────
    with tab_data:
        st.markdown("#### What Data Does This Dashboard Store?")
        st.markdown(
            "<div class='dg-info'>"
            "Data Guardian follows a privacy-by-design approach."
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            | Data type | Where stored | When deleted |
            |-----------|-------------|--------------|
            | Review progress (items marked as reviewed) | Browser session state only | When you close the browser tab or clear session |
            | Selected app and navigation state | Browser session state only | When you close the tab |
            | No personal account data | Not collected | N/A |
            | No social media credentials | Never requested | N/A |
            | No device permissions | Not inspected | N/A |
            | No contact lists or photos | Never collected | N/A |
            | No API keys in frontend code | Keys kept server-side if used | N/A |
            """
        )

        st.markdown(
            "<div class='dg-ok'>"
            "✅ This prototype does not require you to connect any account, "
            "does not store any personal data, and does not access your device's "
            "permissions, files, or sensors."
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown("#### Clear Session Data")
        if st.button("🗑️ Clear All Review Progress & Session Data", type="primary"):
            st.session_state.reviewed_items = {}
            st.session_state.selected_app = None
            st.success("✅ Session data cleared. All review progress has been reset.")

    # ── Settings ───────────────────────────────────────────────────────────────
    with tab_settings:
        st.markdown("#### Display Settings")
        st.info(
            "The dashboard uses a high-contrast dark theme designed for accessibility. "
            "The colour scheme uses dark navy backgrounds with bright teal accents, "
            "amber warnings, and red alerts — chosen for maximum readability, "
            "including for users with low vision."
        )

        st.markdown("#### AI Explainer Status")
        st.markdown(
            "<div class='dg-warn'>"
            "⚠️ The AI Privacy Explainer feature requires a configured AI service (e.g. OpenAI API key). "
            "No AI service is connected in this prototype. "
            "To enable it, add your API key as an environment variable and configure the service "
            "in a backend module — do not add API keys to the frontend code."
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown("**To configure an AI service:**")
        st.code(
            """
# Set environment variable before running:
# Linux / macOS:
export OPENAI_API_KEY=your_key_here
streamlit run data_guardian_app.py

# Windows PowerShell:
$env:OPENAI_API_KEY="your_key_here"
streamlit run data_guardian_app.py
            """,
            language="bash",
        )
        st.markdown(
            "<div class='dg-danger'>"
            "🚫 Never put API keys directly in your Python source code or Streamlit secrets "
            "files that are committed to public repositories."
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown("#### Known Limitations")
        limitations = [
            ("Live monitoring", "Policy change monitoring is not active. Shown changes are demonstration data."),
            ("Live AI", "No AI model is connected. A real deployment would require a backend AI service."),
            ("Device permissions", "The dashboard cannot inspect or change your device's permissions."),
            ("OAuth revocation", "The dashboard cannot revoke connected app authorisations — only link to official settings."),
            ("Source verification", "All app profiles are demonstration data — policy URLs are correct but content is not live-scraped."),
            ("Mobile native features", "No native Android/iOS integration is present. Instructions are manual guidance only."),
        ]
        for feature, note in limitations:
            st.markdown(
                f"""
                <div class='dg-card' style='margin-bottom:0.4rem;'>
                    <strong style='color:#ffd54f;'>⚠️ {feature}:</strong>
                    <span style='color:#b0c8e0;'> {note}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
