"""Privacy Policy Changes — monitor and explain policy updates."""

import streamlit as st
from sections.data import POLICY_CHANGES, APPS


STATUS_DISPLAY = {
    "change_detected": ("status-updated", "📋 Change Detected"),
    "no_change":       ("status-verified", "✅ No Change Detected"),
    "not_configured":  ("status-demo",     "⚠️ Monitoring Not Configured"),
    "unavailable":     ("badge-unknown",   "⚪ Unable to Retrieve"),
}


def show_policy_changes():
    st.markdown("## 📋 Privacy Policy Changes")
    st.markdown(
        "<div class='dg-info'>"
        "This section helps you understand when and how app privacy policies change. "
        "Keeping track of policy changes is important — a new policy might introduce "
        "different data sharing practices, advertising purposes, or AI training clauses."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='dg-warn'>"
        "⚠️ <strong>Prototype notice:</strong> Live policy monitoring is not active. "
        "The comparisons below are demonstration examples based on publicly reported "
        "updates. They are not real-time comparisons and should not be treated as "
        "current policy alerts."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── How monitoring works ───────────────────────────────────────────────────
    with st.expander("ℹ️ How Does Policy Monitoring Work?"):
        st.markdown(
            """
            A policy monitoring system would work as follows:

            1. **Retrieve** the current privacy policy from the official URL on a regular schedule.
            2. **Record** the retrieval date and the policy version or 'last updated' date.
            3. **Compare** the current text with a previously saved version using text-difference algorithms.
            4. **Identify** additions (new text), removals (deleted text), and changed passages.
            5. **Explain** the differences in plain language.
            6. **Alert** users to changes that may affect their privacy choices.

            **In this prototype:**
            - No automated retrieval is active.
            - The sample comparisons below use publicly reported changes as demonstration content.
            - A production implementation would require a scheduled backend process,
              a database to store historical versions, and appropriate access to official policy URLs.
            """
        )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── All apps status overview ───────────────────────────────────────────────
    st.markdown("#### Monitoring Status Overview")
    monitored_apps = {pc["app"] for pc in POLICY_CHANGES}

    rows = []
    for app_name, app_info in APPS.items():
        if app_name in monitored_apps:
            pc = next(p for p in POLICY_CHANGES if p["app"] == app_name)
            status_key = pc["status"]
        else:
            status_key = "not_configured"
            pc = None

        status_cls, status_text = STATUS_DISPLAY.get(status_key, STATUS_DISPLAY["not_configured"])
        rows.append((app_info["icon"], app_name, status_cls, status_text,
                     pc["date"] if pc else "N/A", app_info["privacy_policy"]))

    cols = st.columns(3)
    for i, (icon, name, status_cls, status_text, date, policy_url) in enumerate(rows):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="dg-card">
                    <div style="font-size:1.8rem;">{icon}</div>
                    <div class="dg-card-title" style="margin-bottom:0.3rem;">{name}</div>
                    <span class="{status_cls}">{status_text}</span>
                    <div style="font-size:0.8rem;color:#557788;margin-top:0.4rem;">
                        Last check: {date}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Detailed change cards ──────────────────────────────────────────────────
    st.markdown("#### Demonstration Policy Change Details")

    for pc in POLICY_CHANGES:
        app_info = APPS.get(pc["app"], {})
        icon = app_info.get("icon", "📄")
        status_cls, status_text = STATUS_DISPLAY.get(pc["status"], STATUS_DISPLAY["not_configured"])

        with st.expander(f"{icon}  {pc['app']} — {status_text}", expanded=(pc["status"] == "change_detected")):
            st.markdown(
                f"<div class='dg-warn'>⚠️ {pc['note']}</div>",
                unsafe_allow_html=True,
            )

            st.markdown(f"**Date of detected change:** {pc['date']}")
            st.markdown(f"**Summary:** {pc['summary']}")

            if pc.get("old_excerpt") and pc.get("new_excerpt"):
                col_old, col_new = st.columns(2)
                with col_old:
                    st.markdown("**Previous version excerpt:**")
                    st.markdown(
                        f"""
                        <div style="background:#2a0a0a;border-left:3px solid #cc2222;
                                    border-radius:6px;padding:0.7rem;color:#ff9090;
                                    font-size:0.9rem;">
                            ❌ {pc['old_excerpt']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_new:
                    st.markdown("**Updated version excerpt:**")
                    st.markdown(
                        f"""
                        <div style="background:#0a2a0a;border-left:3px solid #00cc66;
                                    border-radius:6px;padding:0.7rem;color:#80ffb0;
                                    font-size:0.9rem;">
                            ✅ {pc['new_excerpt']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.markdown(
                f"🔗 [View Official Privacy Policy]({pc['policy_link']})"
            )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── What to do when a policy changes ──────────────────────────────────────
    st.markdown("#### 💡 What To Do When a Privacy Policy Changes")
    st.markdown(
        """
        When an app updates its privacy policy:

        1. **Read the summary of changes** — most platforms now highlight key changes.
        2. **Look for new data-sharing purposes** — especially advertising, AI training, or new partners.
        3. **Check whether your settings still reflect your preferences** — some changes may reset or alter defaults.
        4. **Decide whether you accept the new terms** — if not, you may need to delete your account.
        5. **Review connected app authorisations** — policy changes sometimes affect what third-party apps can access.
        """
    )
    st.markdown(
        "<div class='dg-info'>"
        "You can set up free third-party policy-tracking services such as "
        "<a href='https://tosdr.org' target='_blank' style='color:#00d4aa;'>Terms of Service; Didn't Read (ToS;DR)</a> "
        "to receive plain-language summaries of terms and policy changes."
        "</div>",
        unsafe_allow_html=True,
    )
