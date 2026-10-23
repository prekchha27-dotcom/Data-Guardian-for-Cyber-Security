"""Upload Latest Privacy Policy — main workspace section."""

import streamlit as st
import streamlit.components.v1 as components
from sections.policy_data import (
    PLATFORMS, POLICY_CATEGORIES, PLATFORM_CATEGORIES,
    AVAILABILITY_STYLES,
)
from sections.summarizer import summarize, AI_CONFIGURED


def _copy_button(label: str, text: str, key: str):
    """Render a copy-to-clipboard button using Streamlit components."""
    col_btn, col_status = st.columns([2, 3])
    with col_btn:
        clicked = st.button(label, key=key, use_container_width=True)
    with col_status:
        if st.session_state.get(f"copied_{key}"):
            st.markdown(
                "<div class='dg-ok-light' style='padding:0.3rem 0.7rem;margin:0;'>✅ Copied!</div>",
                unsafe_allow_html=True,
            )
    if clicked:
        escaped = text.replace("`", "\\`").replace("\\", "\\\\").replace("$", "\\$")
        components.html(
            f"<script>navigator.clipboard.writeText(`{escaped}`);</script>",
            height=0,
        )
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

    # ── Region selector ────────────────────────────────────────────────────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    region_col, _ = st.columns([2, 3])
    with region_col:
        selected_region = st.selectbox(
            "🌍 Applicable Region",
            ["India", "United States", "Global"],
            index=0,
            key="upload_region",
            help="Select your region. Where platforms publish different terms for different regions, the relevant document will be highlighted.",
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

    # ── Step 1: Platform selector ──────────────────────────────────────────────
    st.markdown("### Step 1 — Select a Platform")

    all_platform_names = list(PLATFORMS.keys())
    platform_cols = st.columns(5)
    for i, name in enumerate(all_platform_names[:5]):
        info = PLATFORMS[name]
        with platform_cols[i]:
            active = st.session_state.get("upload_platform") == name
            border = "border:2px solid #00d4aa;" if active else "border:1px solid #1e3a5f;"
            st.markdown(
                f"""
                <div style="background:#0d2236;{border}border-radius:10px;
                            padding:0.7rem;text-align:center;cursor:pointer;margin-bottom:0.3rem;">
                    <div style="font-size:1.8rem;">{info['icon']}</div>
                    <div style="font-size:0.82rem;color:#00d4aa;font-weight:600;">{name}</div>
                    <div style="font-size:0.7rem;color:#557788;">{info['category']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Select {name}", key=f"up_sel_{name}", use_container_width=True):
                st.session_state["upload_platform"] = name
                st.session_state["upload_policy_cat"] = None
                st.rerun()

    platform_cols2 = st.columns(4)
    for i, name in enumerate(all_platform_names[5:]):
        info = PLATFORMS[name]
        with platform_cols2[i]:
            active = st.session_state.get("upload_platform") == name
            border = "border:2px solid #00d4aa;" if active else "border:1px solid #1e3a5f;"
            st.markdown(
                f"""
                <div style="background:#0d2236;{border}border-radius:10px;
                            padding:0.7rem;text-align:center;margin-bottom:0.3rem;">
                    <div style="font-size:1.8rem;">{info['icon']}</div>
                    <div style="font-size:0.82rem;color:#00d4aa;font-weight:600;">{name}</div>
                    <div style="font-size:0.7rem;color:#557788;">{info['category']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Select {name}", key=f"up_sel_{name}", use_container_width=True):
                st.session_state["upload_platform"] = name
                st.session_state["upload_policy_cat"] = None
                st.rerun()

    selected_platform = st.session_state.get("upload_platform")

    if not selected_platform:
        st.markdown(
            "<div class='dg-card' style='text-align:center;color:#557788;'>👆 Select a platform above to begin.</div>",
            unsafe_allow_html=True,
        )
        return

    plat = PLATFORMS[selected_platform]
    st.markdown(
        f"""
        <div style="background:#0a3a2a;border:1px solid #00d4aa;border-radius:10px;
                    padding:0.7rem 1.2rem;margin:0.5rem 0;">
            <span style="font-size:1.5rem;">{plat['icon']}</span>
            <strong style="color:#00d4aa;font-size:1.1rem;margin-left:0.5rem;">{selected_platform}</strong>
            <span style="color:#8ab0cc;font-size:0.87rem;margin-left:0.8rem;">{plat['developer']}</span>
            <span style="color:#557788;font-size:0.82rem;margin-left:0.8rem;">· {plat['category']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Step 2: Policy category selector ──────────────────────────────────────
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
                f"""
                <div style="background:#0d2236;{border}border-radius:10px;
                            padding:0.7rem;margin-bottom:0.4rem;">
                    <div style="font-size:0.92rem;color:#e8f0f7;font-weight:600;margin-bottom:0.3rem;">{cat_label}</div>
                    <span class="{avail_cls}">{avail_text}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open: {cat_label[:25]}", key=f"up_cat_{cat_key}", use_container_width=True):
                st.session_state["upload_policy_cat"] = cat_key
                st.rerun()

    selected_cat = st.session_state.get("upload_policy_cat")

    if not selected_cat:
        st.markdown(
            "<div class='dg-card' style='text-align:center;color:#557788;'>👆 Select a policy category above.</div>",
            unsafe_allow_html=True,
        )
        return

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Step 3–7: Policy workspace ─────────────────────────────────────────────
    policy = plat["policies"].get(selected_cat, {})
    cat_label = dict(POLICY_CATEGORIES).get(selected_cat, selected_cat)
    avail = policy.get("availability_status", "Not found")
    avail_cls, avail_text = AVAILABILITY_STYLES.get(avail, ("badge-unknown", "⚪ Unknown"))

    # Resolve region-specific URL
    region_urls = policy.get("region_urls", {})
    policy_url = region_urls.get(selected_region) or policy.get("url", "")

    st.markdown(f"### 📄 {selected_platform} — {cat_label}")

    # Document metadata card
    st.markdown(
        f"""
        <div class="dg-card">
            <div class="dg-card-title">{policy.get('title', cat_label)}</div>
            <div class="dg-card-body">
                <strong>Official URL:</strong>
                <a href="{policy_url}" target="_blank" style="color:#00d4aa;">{policy_url}</a><br/>
                <strong>Applicable region:</strong> {policy.get('applicable_region','–')}<br/>
                <strong>Region selected:</strong> {selected_region}<br/>
                <strong>Availability:</strong> <span class="{avail_cls}">{avail_text}</span><br/>
                <strong>Last updated:</strong> {policy.get('last_updated','Not available')}<br/>
                <strong>Last verified by this dashboard:</strong> {policy.get('last_verified','Not verified')}<br/>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if policy.get("notes"):
        st.markdown(
            f"<div class='dg-warn'>📎 <strong>Note:</strong> {policy['notes']}</div>",
            unsafe_allow_html=True,
        )

    if avail == "Embedded":
        st.markdown(
            "<div class='dg-info'>📎 This policy is <strong>embedded inside a larger document</strong>. "
            "Open the official link above, search for the relevant section heading, "
            "and copy only that section's text before pasting it below.</div>",
            unsafe_allow_html=True,
        )

    # Step 3: Open official policy
    st.markdown("#### Step 3 — Open the Official Document")
    if policy_url:
        st.markdown(
            f"🔗 **[Open Official Policy]({policy_url})** ← Click to open in a new tab",
        )
    else:
        st.markdown(
            "<div class='dg-danger'>⚠️ A verified direct URL is not available for this policy. "
            f"Start from the platform's official legal page: "
            f"<a href='{plat['official_home']}' target='_blank' style='color:#00d4aa;'>{plat['official_home']}</a></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Step 4: Paste Policy Text ──────────────────────────────────────────────
    st.markdown("#### Step 4 — Paste Policy Text")
    st.markdown(
        "Open the official document above, select all text (Ctrl+A / Cmd+A), copy it, "
        "and paste it into the box below."
    )

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
            st.markdown(
                "<div class='dg-warn-light'>⚠️ The pasted text is very short. "
                "Please paste the complete policy document.</div>",
                unsafe_allow_html=True,
            )

    col_clr_paste, _ = st.columns([1, 5])
    with col_clr_paste:
        if st.button("🗑️ Clear Text", key=f"clr_{paste_key}"):
            st.session_state[paste_key] = ""
            st.session_state[f"summary_{selected_platform}_{selected_cat}"] = ""
            st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Step 5: Summarize Policy ───────────────────────────────────────────────
    st.markdown("#### Step 5 — Summarize Policy")

    summary_key = f"summary_{selected_platform}_{selected_cat}"
    if summary_key not in st.session_state:
        st.session_state[summary_key] = ""

    if st.button("🔍 Summarize Policy", key=f"sum_btn_{selected_platform}_{selected_cat}", type="primary"):
        if not st.session_state[paste_key].strip():
            st.markdown(
                "<div class='dg-danger-light'>❌ No policy text pasted. "
                "Paste the full document in Step 4 first.</div>",
                unsafe_allow_html=True,
            )
        else:
            with st.spinner("Summarizing — please wait…"):
                result = summarize(selected_platform, selected_cat, st.session_state[paste_key])
            if result["ok"]:
                st.session_state[summary_key] = result["summary"]
                st.rerun()
            else:
                st.markdown(
                    f"<div class='dg-danger-light'>❌ {result['error']}</div>",
                    unsafe_allow_html=True,
                )

    # ── Policy Summary display ─────────────────────────────────────────────────
    generated_summary = st.session_state.get(summary_key, "")
    if generated_summary:
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("#### 📋 Policy Summary")
        st.markdown(
            "<div class='dg-ok-light' style='margin-bottom:0.7rem;'>✅ Summary generated. "
            "Not legal advice — verify against the official document.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='dg-summary-box'>{generated_summary}</div>",
            unsafe_allow_html=True,
        )
        col_cp, col_clr, _ = st.columns([1, 1, 4])
        with col_cp:
            _copy_button("📋 Copy Summary", generated_summary, key=f"cp_sum_{summary_key}")
        with col_clr:
            if st.button("🗑️ Clear Summary", key=f"clr_sum_{summary_key}"):
                st.session_state[summary_key] = ""
                st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Reset button
    if st.button("↺  Reset All Fields for This Policy", key=f"reset_{selected_platform}_{selected_cat}"):
        st.session_state[paste_key] = ""
        st.session_state[summary_key] = ""
        st.rerun()
