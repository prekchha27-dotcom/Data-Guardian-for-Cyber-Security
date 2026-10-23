"""Home Dashboard section."""

import streamlit as st
from sections.data import APPS, STATUS_LABELS


def show_home():
    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#0d2236 60%,#0a3a2a 100%);
                    border:1px solid #1e3a5f; border-radius:14px;
                    padding:2rem 2.5rem; margin-bottom:1.5rem;">
            <div style="font-size:2.8rem; margin-bottom:0.4rem;">🛡️</div>
            <h1 style="color:#00d4aa; margin:0 0 0.5rem 0; font-size:2rem;">
                Take Control of Your Digital Privacy
            </h1>
            <p style="font-size:1.1rem; color:#b0cce0; max-width:680px; line-height:1.7; margin:0 0 1.2rem 0;">
                Understand what apps can access, how your information may be shared,
                and which privacy settings you should review.
            </p>
            <p style="font-size:0.82rem; color:#557788; margin:0;">
                ⚠️ <strong>Educational prototype.</strong> All app data shown here is demonstration material.
                No real device permissions are inspected.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("🔍  Explore App Privacy", type="primary", use_container_width=True):
            st.session_state.nav = "App Privacy Library"
            st.rerun()
    with col2:
        if st.button("✅  Review My Access", use_container_width=True):
            st.session_state.nav = "Review My Access"
            st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Privacy overview metrics ───────────────────────────────────────────────
    reviewed = len(st.session_state.get("reviewed_items", {}))
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📱 Apps in Library", len(APPS))
    m2.metric("🔍 Permissions Documented", 11)
    m3.metric("✅ Items Marked Reviewed", reviewed)
    m4.metric("📋 Policy Changes (Demo)", 2)

    st.markdown(
        """
        <div class="dg-info">
            📊 These figures reflect the content in this prototype. They are <strong>not</strong>
            live statistics about your device. Items marked as reviewed are stored only in
            your current browser session.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── App library overview ───────────────────────────────────────────────────
    st.markdown("### 📱 Application Library")
    search = st.text_input("🔎 Search apps…", placeholder="Type an app name…", key="home_search")
    category_filter = st.selectbox(
        "Filter by category",
        ["All", "Social Media", "Messaging", "E-Commerce", "Ride-Hailing"],
        key="home_cat",
    )

    filtered = {
        name: info
        for name, info in APPS.items()
        if (search.lower() in name.lower() or not search)
        and (category_filter == "All" or info["category"] == category_filter)
    }

    if not filtered:
        st.markdown(
            "<div class='dg-warn'>No apps match your search. Try clearing the filter.</div>",
            unsafe_allow_html=True,
        )
    else:
        cols = st.columns(3)
        for i, (name, info) in enumerate(filtered.items()):
            status_class, status_text = STATUS_LABELS[info["status"]]
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div class="dg-card">
                        <div style="font-size:2rem; margin-bottom:0.3rem;">{info['icon']}</div>
                        <div class="dg-card-title">{name}</div>
                        <div style="font-size:0.82rem; color:#7a9ab0; margin-bottom:0.5rem;">
                            {info['category']} · {info['developer'][:30]}…
                        </div>
                        <span class="{status_class}">{status_text}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"View {name}", key=f"home_app_{name}", use_container_width=True):
                    st.session_state.selected_app = name
                    st.session_state.nav = "App Privacy Library"
                    st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Recommended next steps ─────────────────────────────────────────────────
    st.markdown("### 💡 Recommended Next Steps")

    steps = [
        ("📍", "Review Location Access",
         "Many apps request location access beyond what their features require. "
         "Limiting location to 'While Using' reduces background tracking."),
        ("🌐", "Check Connected Third-Party Apps",
         "Apps you logged into using Facebook, Google, or Apple may still have active access. "
         "Review and revoke any you no longer use."),
        ("👥", "Understand Contact Access",
         "Granting contact access uploads your address book — including data about people "
         "who have not consented — to the app's servers."),
        ("🔒", "Review Account Privacy Settings",
         "Platform privacy dashboards let you control who sees your posts, "
         "whether your profile appears in search, and how your data is used for ads."),
        ("🎣", "Learn About Phishing & Session Hijacking",
         "Phishing attacks and stolen session tokens can expose your account even if "
         "your password is strong. Enable multi-factor authentication."),
    ]

    for icon, title, desc in steps:
        with st.expander(f"{icon}  {title}", expanded=False):
            st.markdown(f"<div class='dg-card-body'>{desc}</div>", unsafe_allow_html=True)
            if title == "Review Location Access":
                if st.button("Open Permission Explorer →", key=f"step_{title}"):
                    st.session_state.nav = "Permission Explorer"
                    st.rerun()
            elif title == "Check Connected Third-Party Apps":
                if st.button("Open Third-Party Data Access →", key=f"step_{title}"):
                    st.session_state.nav = "Third-Party Data Access"
                    st.rerun()
            elif title == "Learn About Phishing & Session Hijacking":
                if st.button("Open Learning Centre →", key=f"step_{title}"):
                    st.session_state.nav = "Cybersecurity Learning Centre"
                    st.rerun()
