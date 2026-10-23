"""Permission Explorer — detailed per-permission educational content."""

import streamlit as st
from sections.data import PERMISSIONS, RISK_LABELS


def _risk_html(level: str) -> str:
    icon, label, cls = RISK_LABELS.get(level, RISK_LABELS["unknown"])
    return f'<span class="{cls}">{icon} {label}</span>'


def _risk_label(level: str) -> str:
    """Plain-text risk label for use in expander titles (no HTML)."""
    icon, label, _ = RISK_LABELS.get(level, RISK_LABELS["unknown"])
    return f"{icon} {label}"


def show_permission_explorer():
    st.markdown("## 🔍 Permission Explorer")
    st.markdown(
        "<div class='dg-info'>"
        "Understand what each device permission means, why an app might request it, "
        "what data it exposes, and what action is recommended. "
        "Context matters — a permission is not inherently risky or safe without considering "
        "which app is requesting it and why."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Legend ─────────────────────────────────────────────────────────────────
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

    st.markdown(
        "<div class='dg-warn'>"
        "These ratings reflect general patterns based on documented privacy practices. "
        "A permission labelled 'Review Recommended' is not proof of misuse — it is an invitation "
        "to think about whether granting it makes sense for your usage."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Filter ─────────────────────────────────────────────────────────────────
    risk_filter = st.selectbox(
        "Filter by concern level",
        ["All", "🟢 Lower Concern", "🟡 Review Recommended", "🔴 Higher Concern"],
        key="perm_filter",
    )
    risk_map = {
        "🟢 Lower Concern": "low",
        "🟡 Review Recommended": "review",
        "🔴 Higher Concern": "high",
    }
    selected_risk = risk_map.get(risk_filter)

    for perm_name, perm in PERMISSIONS.items():
        level = perm.get("risk_level", "unknown")
        if selected_risk and level != selected_risk:
            continue

        with st.expander(
            f"{perm['icon']}  {perm_name}   —   {_risk_label(level)}",
            expanded=False,
        ):
            col_a, col_b = st.columns([1, 1])

            with col_a:
                st.markdown("##### 📖 What it means")
                st.markdown(
                    f"<div class='dg-card-body'>{perm['what_it_means']}</div>",
                    unsafe_allow_html=True,
                )

                st.markdown("##### ✅ Why an app might request it")
                for reason in perm["why_requested"]:
                    st.markdown(f"- {reason}")

                st.markdown("##### 🗂️ Data that may become accessible")
                st.markdown(
                    f"<div class='dg-card-body'>{perm['data_exposed']}</div>",
                    unsafe_allow_html=True,
                )

            with col_b:
                st.markdown("##### ❌ When it may be unnecessary")
                st.markdown(
                    f"<div class='dg-card-body'>{perm['when_unnecessary']}</div>",
                    unsafe_allow_html=True,
                )

                st.markdown("##### ⚠️ Potential privacy risks")
                st.markdown(
                    f"<div class='dg-warn'>{perm['risks']}</div>",
                    unsafe_allow_html=True,
                )

                st.markdown("##### 💡 Recommended action")
                action_cls = {
                    "low": "dg-ok",
                    "review": "dg-warn",
                    "high": "dg-danger",
                }.get(level, "dg-info")
                st.markdown(
                    f"<div class='{action_cls}'>{perm['action_text']}</div>",
                    unsafe_allow_html=True,
                )

            st.markdown(
                "<div class='dg-info' style='margin-top:0.5rem;'>"
                "📎 <strong>Evidence & limitations:</strong> This explanation is based on general "
                "platform documentation and documented privacy practices. "
                "Actual permission behaviour varies by OS version, app version, and device."
                "</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### 📱 How to Review Permissions on Your Device")

    with st.expander("Android — Reviewing App Permissions"):
        st.markdown(
            """
            1. Open **Settings** on your Android device.
            2. Tap **Apps** (or **Application Manager**).
            3. Select the app you want to review.
            4. Tap **Permissions**.
            5. Review each permission — tap to Allow, Deny, or set to **Allow only while using**.
            6. For a full overview, go to **Settings → Privacy → Permission Manager**.
            """
        )
        st.markdown(
            "<div class='dg-info'>Data Guardian cannot open these settings screens directly. "
            "You must navigate to them yourself.</div>",
            unsafe_allow_html=True,
        )

    with st.expander("iOS — Reviewing App Permissions"):
        st.markdown(
            """
            1. Open **Settings** on your iPhone or iPad.
            2. Scroll down and tap the app name (e.g. Instagram).
            3. Review each permission listed — tap to change between Never, Ask, or Allow.
            4. For a category-level view, go to **Settings → Privacy & Security**
               and select a permission type (e.g. Location Services).
            """
        )
        st.markdown(
            "<div class='dg-info'>Data Guardian cannot open iOS permission screens. "
            "You must navigate to them yourself.</div>",
            unsafe_allow_html=True,
        )
