"""App Privacy Library — browse and view detailed app profiles."""

import streamlit as st
from sections.data import APPS, PERMISSIONS, RISK_LABELS, STATUS_LABELS


def _risk_badge(level: str) -> str:
    icon, label, cls = RISK_LABELS.get(level, RISK_LABELS["unknown"])
    return f'<span class="{cls}">{icon} {label}</span>'


def _risk_label(level: str) -> str:
    """Plain-text label for expander titles."""
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

    # If an app is pre-selected from the Home dashboard, go straight to profile
    if st.session_state.get("selected_app") and st.session_state.selected_app in APPS:
        _show_app_profile(st.session_state.selected_app)
        if st.button("← Back to App Library"):
            st.session_state.selected_app = None
            st.rerun()
        return

    # ── Search & filter ────────────────────────────────────────────────────────
    col_s, col_c = st.columns([3, 1])
    with col_s:
        search = st.text_input("🔎 Search apps…", placeholder="App name…", key="lib_search")
    with col_c:
        cat = st.selectbox(
            "Category",
            ["All", "Social Media", "Messaging", "E-Commerce", "Ride-Hailing"],
            key="lib_cat",
        )

    filtered = {
        name: info
        for name, info in APPS.items()
        if (search.lower() in name.lower() or not search)
        and (cat == "All" or info["category"] == cat)
    }

    if not filtered:
        st.markdown(
            "<div class='dg-warn'>No apps match your search.</div>",
            unsafe_allow_html=True,
        )
        return

    cols = st.columns(3)
    for i, (name, info) in enumerate(filtered.items()):
        status_class, status_text = STATUS_LABELS[info["status"]]
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="dg-card">
                    <div style="font-size:2.4rem;">{info['icon']}</div>
                    <div class="dg-card-title">{name}</div>
                    <div style="font-size:0.82rem;color:#7a9ab0;margin-bottom:0.4rem;">
                        {info['category']}
                    </div>
                    <div style="font-size:0.82rem;color:#a0b8c8;margin-bottom:0.6rem;">
                        {info['developer']}
                    </div>
                    <span class="{status_class}">{status_text}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open {name} Profile", key=f"lib_open_{name}", use_container_width=True):
                st.session_state.selected_app = name
                st.rerun()


def _show_app_profile(name: str):
    info = APPS[name]
    status_class, status_text = STATUS_LABELS[info["status"]]

    # ── App header ─────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="background:#0d2236;border:1px solid #1e3a5f;border-radius:14px;
                    padding:1.5rem 2rem;margin-bottom:1rem;">
            <div style="font-size:3rem;margin-bottom:0.3rem;">{info['icon']}</div>
            <h2 style="margin:0;color:#00d4aa;">{name}</h2>
            <div style="color:#8ab0cc;font-size:0.92rem;margin:0.3rem 0;">
                {info['developer']}
            </div>
            <div style="margin-top:0.5rem;">
                <span class="{status_class}">{status_text}</span>
                &nbsp;
                <span style="font-size:0.82rem;color:#557788;">
                    Source: {info['source_date']}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("← Back to App Library", key="back_lib"):
        st.session_state.selected_app = None
        st.rerun()

    # ── Tabs ───────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📋 Overview", "🔑 Permissions", "🌐 Data Sharing", "⚠️ Security Risks", "📎 Sources"]
    )

    # ── Tab 1: Overview ────────────────────────────────────────────────────────
    with tab1:
        st.markdown("#### Plain-Language Summary")
        st.markdown(
            f"<div class='dg-card'><div class='dg-card-body'>{info['summary']}</div></div>",
            unsafe_allow_html=True,
        )

        st.markdown("#### Key Data Categories Collected")
        for item in info["data_categories"]:
            st.markdown(f"- {item}")

        st.markdown("#### Recommended User Actions")
        for action in info["actions"]:
            st.markdown(f"✅ {action}")

        if info.get("official_settings"):
            st.markdown(
                f"🔗 [Open Official Settings Page]({info['official_settings']})",
            )

    # ── Tab 2: Permissions ─────────────────────────────────────────────────────
    with tab2:
        st.markdown(
            "<div class='dg-info'>Permissions listed here reflect what the app <em>may</em> request "
            "based on available documentation. Actual permissions vary by OS version, device, "
            "region, and enabled features. Granting a permission does not automatically mean "
            "the data is collected or misused.</div>",
            unsafe_allow_html=True,
        )
        for perm_name in info["permissions"]:
            perm = PERMISSIONS.get(perm_name, {})
            icon = perm.get("icon", "🔒")
            risk = perm.get("risk_level", "unknown")
            with st.expander(f"{icon} {perm_name} — {_risk_label(risk)}", expanded=False):
                if perm:
                    st.markdown(f"**What it means:** {perm['what_it_means']}")
                    st.markdown(f"**Data potentially accessible:** {perm['data_exposed']}")
                    st.markdown(f"**Recommended action:** {perm['action_text']}")
                    if st.button(
                        f"Full details for {perm_name} →",
                        key=f"perm_link_{name}_{perm_name}",
                    ):
                        st.session_state.nav = "Permission Explorer"
                        st.rerun()
                else:
                    st.markdown("Detailed information for this permission is not yet available.")

    # ── Tab 3: Data Sharing ────────────────────────────────────────────────────
    with tab3:
        st.markdown("#### Third-Party Data Sharing")
        st.markdown(
            f"<div class='dg-card'><div class='dg-card-body'>{info['third_party_sharing']}</div></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='dg-warn'>The description above is derived from the app's privacy policy "
            "documentation. The actual scope of sharing depends on user settings, "
            "platform controls, and regulatory requirements at the time of use.</div>",
            unsafe_allow_html=True,
        )
        if info.get("connected_apps_link"):
            st.markdown(
                f"🔗 [Review Connected Applications]({info['connected_apps_link']})"
            )
        if st.button("Explore Third-Party Data Access in depth →", key=f"tpa_{name}"):
            st.session_state.nav = "Third-Party Data Access"
            st.rerun()

    # ── Tab 4: Security Risks ──────────────────────────────────────────────────
    with tab4:
        st.markdown("#### Potential Privacy & Security Risks")
        st.markdown(
            "<div class='dg-info'>These risks are identified based on the app's documented "
            "data practices and, where applicable, publicly reported security incidents. "
            "Their presence does not mean the app is actively exploiting them or that "
            "your account is currently affected.</div>",
            unsafe_allow_html=True,
        )
        for risk in info["risks"]:
            st.markdown(
                f"<div class='dg-warn'>⚠️ {risk}</div>",
                unsafe_allow_html=True,
            )

    # ── Tab 5: Sources ─────────────────────────────────────────────────────────
    with tab5:
        st.markdown("#### Source Information")
        st.markdown(
            f"""
            <div class='dg-card'>
                <div class='dg-card-title'>Privacy Policy</div>
                <div class='dg-card-body'>
                    <strong>Publisher:</strong> {info['developer']}<br/>
                    <strong>URL:</strong> <a href="{info['privacy_policy']}" target="_blank"
                        style="color:#00d4aa;">{info['privacy_policy']}</a><br/>
                    <strong>Policy last updated:</strong> {info['policy_updated']}<br/>
                    <strong>Source date in this prototype:</strong> {info['source_date']}<br/>
                    <strong>Verification status:</strong>
                    <span class="status-demo">⚠️ Demonstration Data</span>
                </div>
            </div>
            <div class='dg-warn'>
                All data in this prototype is for educational demonstration. Policy details
                should be verified directly from the official link above before relying on them
                for personal decisions. No automated scraping or live monitoring is active.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f"🔗 [View Official Privacy Policy]({info['privacy_policy']})")
