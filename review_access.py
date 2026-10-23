"""Review My Access — Action Centre for reviewing privacy settings."""

import streamlit as st
from sections.data import APPS


# ── Action data ───────────────────────────────────────────────────────────────

DEVICE_ACTIONS = [
    {
        "id": "location_permission",
        "icon": "📍",
        "title": "Review Location Permissions",
        "description": (
            "Check which apps have access to your location and whether "
            "background ('Always On') access is granted unnecessarily."
        ),
        "android_steps": [
            "Open Settings",
            "Tap Privacy → Permission Manager",
            "Tap Location",
            "Review each app — change to 'Allow only while using the app' or 'Deny' where appropriate",
        ],
        "ios_steps": [
            "Open Settings",
            "Tap Privacy & Security → Location Services",
            "Review each app — tap to change to Never, Ask Next Time, or While Using the App",
        ],
    },
    {
        "id": "camera_permission",
        "icon": "📷",
        "title": "Review Camera Permissions",
        "description": "Check which apps can activate your camera and revoke where unnecessary.",
        "android_steps": [
            "Open Settings → Privacy → Permission Manager",
            "Tap Camera",
            "Review apps — deny camera access to apps that do not need it",
        ],
        "ios_steps": [
            "Open Settings → Privacy & Security → Camera",
            "Toggle off camera access for apps that don't require it",
        ],
    },
    {
        "id": "microphone_permission",
        "icon": "🎤",
        "title": "Review Microphone Permissions",
        "description": "Identify apps with microphone access and deny where unneeded.",
        "android_steps": [
            "Open Settings → Privacy → Permission Manager",
            "Tap Microphone",
            "Review and revoke for apps without a legitimate audio need",
        ],
        "ios_steps": [
            "Open Settings → Privacy & Security → Microphone",
            "Toggle off for apps that don't use voice features",
        ],
    },
    {
        "id": "contacts_permission",
        "icon": "👥",
        "title": "Review Contacts Permissions",
        "description": (
            "Contact access uploads your address book to the app's servers. "
            "Review which apps have this permission."
        ),
        "android_steps": [
            "Open Settings → Privacy → Permission Manager",
            "Tap Contacts",
            "Deny for apps where friend-finding is not important to you",
        ],
        "ios_steps": [
            "Open Settings → Privacy & Security → Contacts",
            "Toggle off for apps that don't need your address book",
        ],
    },
]

CONNECTED_APP_ACTIONS = [
    {
        "id": "facebook_connected",
        "icon": "📘",
        "title": "Review Facebook Connected Apps",
        "description": (
            "Third-party apps that you logged into using Facebook may still have "
            "active access to your profile, friends list, and other data. "
            "Revoking access stops future data requests but does not delete "
            "information already collected by those apps."
        ),
        "link": "https://www.facebook.com/settings?tab=applications",
        "link_label": "Open Facebook App Settings",
        "manual_steps": [
            "Go to facebook.com → Settings → Apps and Websites",
            "Review Active apps",
            "Click 'Remove' on any app you no longer use or trust",
        ],
    },
    {
        "id": "google_connected",
        "icon": "🔵",
        "title": "Review Google Connected Apps",
        "description": (
            "Apps authorised with 'Sign in with Google' may have access to your "
            "Google account data. Review and revoke unused authorisations."
        ),
        "link": "https://myaccount.google.com/permissions",
        "link_label": "Open Google Account Permissions",
        "manual_steps": [
            "Go to myaccount.google.com → Security → Third-party apps with account access",
            "Review the list — click an app to see its permissions",
            "Click 'Remove Access' for apps you no longer use",
        ],
    },
    {
        "id": "instagram_connected",
        "icon": "📸",
        "title": "Review Instagram Connected Apps",
        "description": "Check third-party apps connected to your Instagram account.",
        "link": "https://www.instagram.com/accounts/manage_access/",
        "link_label": "Open Instagram App Access Settings",
        "manual_steps": [
            "Open Instagram → Profile → Menu (☰) → Settings and Privacy",
            "Tap Account → Apps and Websites",
            "Review Active authorisations and remove unused ones",
        ],
    },
]

TRACKING_ACTIONS = [
    {
        "id": "ad_preferences_facebook",
        "icon": "🎯",
        "title": "Review Facebook Ad Preferences",
        "description": (
            "Facebook builds an interest profile based on your activity on and off the platform. "
            "You can review and clear parts of this profile."
        ),
        "link": "https://www.facebook.com/adpreferences",
        "link_label": "Open Facebook Ad Preferences",
        "manual_steps": [
            "Go to facebook.com → Settings → Ads → Ad Preferences",
            "Review 'Your interests' and 'Advertisers you've interacted with'",
            "Check 'Off-Facebook activity' and clear if desired",
        ],
    },
    {
        "id": "snap_location",
        "icon": "👻",
        "title": "Enable Snapchat Ghost Mode",
        "description": (
            "Snap Map shares your real-time location with friends by default. "
            "Ghost Mode hides your location from the map."
        ),
        "link": None,
        "link_label": None,
        "manual_steps": [
            "Open Snapchat → Tap the Map icon (bottom left)",
            "Tap the Settings icon (top right of the map)",
            "Toggle on Ghost Mode",
        ],
    },
    {
        "id": "telegram_privacy",
        "icon": "✈️",
        "title": "Set Telegram Phone Number Privacy",
        "description": (
            "By default, anyone who has your phone number may find your Telegram account. "
            "Restrict this in Privacy settings."
        ),
        "link": None,
        "link_label": None,
        "manual_steps": [
            "Open Telegram → Settings → Privacy and Security",
            "Tap Phone Number → Who can see my phone number: set to Nobody",
            "Tap Who can find me by my number: set to My Contacts or Nobody",
        ],
    },
]


STATUS_OPTIONS = [
    "Not reviewed",
    "Instructions viewed",
    "User marked as completed",
]


def _item_key(item_id: str) -> str:
    return f"review_{item_id}"


def _status_color(status: str) -> str:
    if status == "User marked as completed":
        return "dg-ok"
    if status == "Instructions viewed":
        return "dg-info"
    return "dg-card"


def _render_action(action: dict, show_steps: bool = True):
    item_id = action["id"]
    key = _item_key(item_id)
    current_status = st.session_state.reviewed_items.get(item_id, "Not reviewed")

    status_cls = _status_color(current_status)
    st.markdown(
        f"""
        <div class="{status_cls}">
            <div class="dg-card-title">{action['icon']} {action['title']}</div>
            <div class="dg-card-body">{action['description']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:
        st.caption(f"Status: **{current_status}**")

    with c2:
        if action.get("link"):
            st.markdown(
                f"🔗 [{action['link_label']}]({action['link']})",
            )

    with c3:
        if current_status != "User marked as completed":
            if st.button("✅ Mark as Reviewed", key=f"mark_{item_id}", use_container_width=True):
                st.session_state.reviewed_items[item_id] = "User marked as completed"
                st.rerun()
        else:
            if st.button("↩️ Undo", key=f"undo_{item_id}", use_container_width=True):
                st.session_state.reviewed_items[item_id] = "Not reviewed"
                st.rerun()

    if show_steps:
        with st.expander("📋 Show Me How — Android & iOS Steps"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Android**")
                for step in action.get("android_steps", action.get("manual_steps", [])):
                    st.markdown(f"  {step}")
            with col_b:
                if action.get("ios_steps"):
                    st.markdown("**iOS**")
                    for step in action["ios_steps"]:
                        st.markdown(f"  {step}")

    st.markdown(
        "<div class='dg-info' style='margin-bottom:0.4rem;'>"
        "⚠️ <strong>Important:</strong> 'Mark as Reviewed' updates this dashboard only. "
        "It does not change any device permission, revoke any app authorisation, "
        "or verify that the action was completed on your device."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")


def show_review_access():
    st.markdown("## ✅ Review My Access — Action Centre")
    st.markdown(
        "<div class='dg-info'>"
        "This section guides you through reviewing your device permissions, "
        "connected app authorisations, and data-sharing settings. "
        "Use the instructions to make changes in your device or app settings. "
        "Mark items as reviewed to track your progress."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='dg-warn'>"
        "<strong>Limitation:</strong> Data Guardian is a web application. "
        "It cannot inspect, change, or verify your device permissions, "
        "revoke OAuth authorisations, or confirm that settings were changed. "
        "Actions marked as completed are self-reported."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Progress summary ───────────────────────────────────────────────────────
    total_actions = len(DEVICE_ACTIONS) + len(CONNECTED_APP_ACTIONS) + len(TRACKING_ACTIONS)
    completed = sum(
        1 for a in (DEVICE_ACTIONS + CONNECTED_APP_ACTIONS + TRACKING_ACTIONS)
        if st.session_state.reviewed_items.get(a["id"]) == "User marked as completed"
    )

    st.markdown(f"#### Progress: {completed} / {total_actions} items reviewed")
    st.progress(completed / total_actions if total_actions else 0)

    if st.button("🗑️ Clear All Review Progress"):
        st.session_state.reviewed_items = {}
        st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Category 1: Device permissions ────────────────────────────────────────
    st.markdown("### 📱 Category 1: Device Permissions")
    st.markdown(
        "Review which apps have access to sensitive device features. "
        "Changes must be made in your device Settings."
    )
    for action in DEVICE_ACTIONS:
        _render_action(action, show_steps=True)

    # ── Category 2: Connected apps ────────────────────────────────────────────
    st.markdown("### 🌐 Category 2: Connected Applications & Account Access")
    st.markdown(
        "Review third-party apps that are authorised to access your social media or Google accounts. "
        "Revoking access stops future requests but does not delete data already collected."
    )
    for action in CONNECTED_APP_ACTIONS:
        _render_action(action, show_steps=True)

    # ── Category 3: Data sharing & tracking ───────────────────────────────────
    st.markdown("### 🎯 Category 3: Data Sharing & Tracking Settings")
    st.markdown(
        "Review platform-level privacy settings for advertising, location sharing, and tracking. "
        "Note: changing a device permission does not automatically stop account-level tracking."
    )
    for action in TRACKING_ACTIONS:
        _render_action(action, show_steps=True)

    # ── Status legend ──────────────────────────────────────────────────────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("#### Status Key")
    st.markdown(
        """
        | Status | Meaning |
        |--------|---------|
        | Not reviewed | No action taken in this session |
        | Instructions viewed | You have expanded the step-by-step guide |
        | User marked as completed | You have self-reported completing this action |
        | Verified by integration | Not available in this prototype |
        | Unable to verify | Not available in this prototype |
        """
    )
    st.markdown(
        "<div class='dg-info'>"
        "User-reported completion is not independently verified. "
        "Data Guardian cannot confirm that a permission was changed or an app was revoked."
        "</div>",
        unsafe_allow_html=True,
    )
