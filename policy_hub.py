"""Social Media Policy Research Hub — browse all 9 platforms × 6 policy categories."""

import streamlit as st
import streamlit.components.v1 as components
from sections.policy_data import (
    PLATFORMS, POLICY_CATEGORIES, PLATFORM_CATEGORIES,
    AVAILABILITY_STYLES,
)
from sections.summarizer import summarize, AI_CONFIGURED


def _avail_badge(status: str) -> str:
    cls, text = AVAILABILITY_STYLES.get(status, ("badge-unknown", "⚪ Unknown"))
    return f'<span class="{cls}">{text}</span>'


def _policy_card(platform_name: str, cat_key: str, cat_label: str,
                 policy: dict, region: str):
    """Render a full policy card with link, prompt, and paste areas."""
    avail = policy.get("availability_status", "Not found")
    avail_cls, avail_text = AVAILABILITY_STYLES.get(avail, ("badge-unknown", "⚪ Unknown"))

    region_urls = policy.get("region_urls", {})
    url = region_urls.get(region) or policy.get("url", "")

    # Header
    st.markdown(
        f"""
        <div style="background:#091e2e;border:1px solid #1e3a5f;border-radius:10px;
                    padding:0.8rem 1.1rem;margin-bottom:0.3rem;">
            <div style="display:flex;align-items:center;flex-wrap:wrap;gap:0.6rem;">
                <strong style="color:#e8f0f7;font-size:0.97rem;">{policy.get('title', cat_label)}</strong>
                <span class="{avail_cls}">{avail_text}</span>
            </div>
            <div style="font-size:0.82rem;color:#7a9ab0;margin-top:0.3rem;">
                Region: {policy.get('applicable_region','–')} &nbsp;|&nbsp;
                Last updated: {policy.get('last_updated','–')} &nbsp;|&nbsp;
                Verified: {policy.get('last_verified','–')}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if policy.get("notes"):
        st.markdown(
            f"<div class='dg-warn' style='font-size:0.85rem;padding:0.5rem 0.8rem;'>"
            f"📎 {policy['notes']}</div>",
            unsafe_allow_html=True,
        )

    # Official link
    if url:
        st.markdown(f"🔗 **[Open Official Policy — {cat_label}]({url})**")
    else:
        official_home = PLATFORMS[platform_name]["official_home"]
        st.markdown(
            "<div class='dg-danger' style='font-size:0.85rem;'>⚠️ Verified direct URL not available. "
            f"Start from: <a href='{official_home}' target='_blank' "
            f"style='color:#00d4aa;'>{official_home}</a></div>",
            unsafe_allow_html=True,
        )

    # ── Paste Policy Text ─────────────────────────────────────────────────────
    paste_key = f"hub_paste_{platform_name}_{cat_key}"
    if paste_key not in st.session_state:
        st.session_state[paste_key] = ""
    pasted = st.text_area(
        "Paste Policy Text",
        value=st.session_state[paste_key],
        height=200,
        key=f"ta_{paste_key}",
        placeholder="Paste the complete official policy text here...",
        label_visibility="visible",
    )
    st.session_state[paste_key] = pasted

    if pasted and len(pasted.strip()) < 200:
        st.markdown(
            "<div class='dg-warn-light' style='font-size:0.85rem;'>⚠️ Text looks too short — paste the full document.</div>",
            unsafe_allow_html=True,
        )

    # ── Summarize Policy button ───────────────────────────────────────────────
    sum_key = f"hub_sum_{platform_name}_{cat_key}"
    if sum_key not in st.session_state:
        st.session_state[sum_key] = ""

    col_s, col_c = st.columns([2, 1])
    with col_s:
        if st.button("🔍 Summarize Policy", key=f"hub_sum_btn_{platform_name}_{cat_key}", type="primary"):
            if not st.session_state[paste_key].strip():
                st.markdown(
                    "<div class='dg-danger-light' style='font-size:0.85rem;'>❌ Paste policy text above first.</div>",
                    unsafe_allow_html=True,
                )
            else:
                with st.spinner("Summarizing…"):
                    result = summarize(platform_name, cat_key, st.session_state[paste_key])
                if result["ok"]:
                    st.session_state[sum_key] = result["summary"]
                    st.rerun()
                else:
                    st.markdown(
                        f"<div class='dg-danger-light' style='font-size:0.85rem;'>❌ {result['error']}</div>",
                        unsafe_allow_html=True,
                    )
    with col_c:
        if st.button("🗑️ Clear", key=f"clr_{platform_name}_{cat_key}"):
            st.session_state[paste_key] = ""
            st.session_state[sum_key] = ""
            st.rerun()

    # ── Policy Summary display ────────────────────────────────────────────────
    generated = st.session_state.get(sum_key, "")
    if generated:
        st.markdown("**📋 Policy Summary**")
        st.markdown(
            "<div class='dg-ok-light' style='font-size:0.82rem;margin-bottom:0.5rem;'>✅ Not legal advice — verify against the official document.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='dg-summary-box'>{generated}</div>",
            unsafe_allow_html=True,
        )
        cp_key = f"hub_cp_sum_{platform_name}_{cat_key}"
        col_cp, _ = st.columns([1, 3])
        with col_cp:
            if st.button("📋 Copy Summary", key=cp_key, use_container_width=True):
                escaped = generated.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
                components.html(
                    f"<script>navigator.clipboard.writeText(`{escaped}`);</script>",
                    height=0,
                )
                st.session_state[f"copied_{cp_key}"] = True
                st.rerun()
        if st.session_state.get(f"copied_{cp_key}"):
            st.markdown(
                "<div class='dg-ok-light' style='font-size:0.82rem;padding:0.3rem 0.6rem;'>✅ Copied!</div>",
                unsafe_allow_html=True,
            )


def show_policy_hub():
    st.markdown("## 🔬 Social Media Policy Research Hub")
    st.markdown(
        "<div class='dg-info'>"
        "Browse official legal policy documents for all 9 platforms across 6 policy categories. "
        "Use the search, region selector, and platform/category filters to find the information you need. "
        "Every policy card provides a direct official link, a copy-ready AI summarization prompt, "
        "and areas to paste the policy text and summary."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Controls bar ───────────────────────────────────────────────────────────
    ctrl1, ctrl2, ctrl3 = st.columns([2, 2, 2])
    with ctrl1:
        region = st.selectbox(
            "🌍 Applicable Region",
            ["India", "United States", "Global"],
            index=0,
            key="hub_region",
        )
    with ctrl2:
        search = st.text_input(
            "🔎 Search platform or policy",
            placeholder="e.g. WhatsApp, arbitration…",
            key="hub_search",
        )
    with ctrl3:
        cat_filter = st.selectbox(
            "📂 Filter by category",
            ["All Categories"] + [lbl for _, lbl in POLICY_CATEGORIES],
            key="hub_cat_filter",
        )

    if region == "India":
        st.markdown(
            "<div class='dg-warn'>"
            "🇮🇳 <strong>India selected.</strong> "
            "US-specific arbitration clauses, class-action waivers, and jury-waiver provisions "
            "are <strong>not automatically applicable to Indian users</strong>. "
            "Where a platform distinguishes Indian users from US users, this is noted on the relevant card."
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Platform sections ──────────────────────────────────────────────────────
    shown_any = False
    for group_name, group_platforms in PLATFORM_CATEGORIES.items():
        # Filter platforms in this group
        matching_platforms = [
            p for p in group_platforms
            if not search or search.lower() in p.lower()
            or any(
                search.lower() in (lbl.lower() + cat_k.lower())
                for cat_k, lbl in POLICY_CATEGORIES
            )
        ]
        if not matching_platforms:
            continue

        st.markdown(f"### 📂 {group_name}")

        for platform_name in matching_platforms:
            plat = PLATFORMS[platform_name]
            shown_any = True

            with st.expander(
                f"{plat['icon']}  {platform_name}  —  {plat['developer']}",
                expanded=False,
            ):
                st.markdown(
                    f"""
                    <div style="background:#091e2e;border:1px solid #1e3a5f;border-radius:8px;
                                padding:0.6rem 1rem;margin-bottom:0.7rem;">
                        <span style="color:#8ab0cc;font-size:0.87rem;">{plat['description']}</span>
                        &nbsp;|&nbsp;
                        <a href="{plat['official_home']}" target="_blank"
                           style="color:#00d4aa;font-size:0.85rem;">Official Legal Home ↗</a>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Policy category tabs
                tab_keys = [cat_k for cat_k, _ in POLICY_CATEGORIES]
                tab_labels = [lbl for _, lbl in POLICY_CATEGORIES]

                # Apply category filter
                if cat_filter != "All Categories":
                    filtered_tabs = [
                        (k, l) for k, l in POLICY_CATEGORIES if l == cat_filter
                    ]
                else:
                    filtered_tabs = list(POLICY_CATEGORIES)

                if not filtered_tabs:
                    st.info("No categories match the current filter.")
                    continue

                tabs = st.tabs([lbl for _, lbl in filtered_tabs])
                for tab_obj, (cat_key, cat_label) in zip(tabs, filtered_tabs):
                    with tab_obj:
                        policy = plat["policies"].get(cat_key)
                        if not policy:
                            st.markdown(
                                "<div class='dg-warn'>No policy record available for this category.</div>",
                                unsafe_allow_html=True,
                            )
                            continue
                        _policy_card(platform_name, cat_key, cat_label, policy, region)

    if not shown_any:
        st.markdown(
            "<div class='dg-warn'>No platforms match your search. Try clearing the search field.</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Quick reference table ──────────────────────────────────────────────────
    st.markdown("### 📊 Quick Reference: Policy Availability")
    st.markdown(
        "This table shows the availability status of each policy category across all 9 platforms."
    )

    header_cols = st.columns([2] + [1] * 6)
    header_cols[0].markdown("**Platform**")
    for i, (_, lbl) in enumerate(POLICY_CATEGORIES):
        header_cols[i + 1].markdown(f"**{lbl[:18]}…**" if len(lbl) > 18 else f"**{lbl}**")

    st.markdown("<hr style='margin:0.3rem 0;'/>", unsafe_allow_html=True)

    for platform_name, plat in PLATFORMS.items():
        row_cols = st.columns([2] + [1] * 6)
        row_cols[0].markdown(f"{plat['icon']} **{platform_name}**")
        for i, (cat_k, _) in enumerate(POLICY_CATEGORIES):
            pol = plat["policies"].get(cat_k, {})
            avail = pol.get("availability_status", "Not found")
            _, avail_text = AVAILABILITY_STYLES.get(avail, ("badge-unknown", "⚪"))
            row_cols[i + 1].markdown(
                f"<span style='font-size:0.75rem;'>{avail_text}</span>",
                unsafe_allow_html=True,
            )
