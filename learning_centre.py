"""Cybersecurity Learning Centre — educational topics and case studies."""

import streamlit as st


TOPICS = [
    {
        "id": "excessive_permissions",
        "title": "Excessive Permissions & Least Privilege",
        "icon": "🔒",
        "explanation": (
            "The 'least privilege' principle means an app should only request the access "
            "it genuinely needs to perform its function. When an app requests more permissions "
            "than necessary, it collects more data than intended — increasing the potential harm "
            "if the app is compromised or misuses the data."
        ),
        "example": (
            "A torch (flashlight) app that requests access to your contacts, microphone, "
            "and precise location has no obvious legitimate reason for those permissions. "
            "A messaging app only needs microphone access when you are in a call."
        ),
        "consequence": (
            "Over-privileged apps collect more data, increasing exposure in the event of a breach, "
            "a company acquisition, a policy change, or a malicious update."
        ),
        "prevention": (
            "Review permissions before and after installing apps. "
            "Deny permissions that are not clearly needed. "
            "On Android 6+ and iOS, you can grant permissions selectively without uninstalling the app."
        ),
    },
    {
        "id": "oauth_api",
        "title": "OAuth & API Authorization",
        "icon": "🔑",
        "explanation": (
            "OAuth is an open standard that lets you authorize a third-party app to access "
            "your account on another service — without sharing your password. "
            "When you click 'Login with Google' or 'Connect with Facebook', you are using OAuth. "
            "The app receives an access token that grants it specific, defined permissions (scopes)."
        ),
        "example": (
            "You authorize a fitness app to access your Google account. "
            "If the app requests the 'email' and 'calendar.read' scopes, "
            "it can read your email address and calendar events — even if you only wanted step tracking. "
            "The 2014 Cambridge Analytica situation began with a quiz app that used Facebook Login "
            "to request access to users' friends lists — a scope that was permitted at the time."
        ),
        "consequence": (
            "Overly broad OAuth scopes mean third-party apps can access more of your account than necessary. "
            "If a third-party app is compromised, that data may be exposed. "
            "Access tokens persist until revoked — apps may retain access years after you stop using them."
        ),
        "prevention": (
            "Review which scopes an app is requesting before authorizing. "
            "Regularly audit and revoke connected apps in your account settings. "
            "Prefer apps that request minimal, specific permissions."
        ),
    },
    {
        "id": "third_party_app_risks",
        "title": "Third-Party Application Risks",
        "icon": "🌐",
        "explanation": (
            "Third-party apps connect to social media platforms, cloud services, and email providers "
            "through APIs and OAuth. They extend the platform's functionality but also extend "
            "its data-sharing surface. A connected app can access your data even if it is "
            "insecure, acquired by another company, or operated with different privacy practices."
        ),
        "example": (
            "A social media scheduling tool authorised to post on your behalf "
            "also receives read access to your messages if that scope was granted. "
            "If the scheduling tool is hacked or sold, your message data may be exposed."
        ),
        "consequence": "Data exposure, account takeover, or privacy violations through a less-secure connected app.",
        "prevention": (
            "Authorize only apps you currently use and trust. "
            "Regularly review and revoke unused connected apps. "
            "Prefer apps with clear, narrow permission requests."
        ),
    },
    {
        "id": "token_theft",
        "title": "Access Token & Session Token Theft",
        "icon": "🪙",
        "explanation": (
            "An access token or session cookie is a credential that proves your identity to a service. "
            "After you log in, your browser or app holds a session token so you don't have to "
            "re-enter your password constantly. If this token is stolen, "
            "an attacker can use it to access your account — without knowing your password."
        ),
        "example": (
            "An attacker sends you a phishing link that looks like a Facebook login page. "
            "You enter your credentials. The attacker captures your session token "
            "and can now read your messages, post content, and change your settings — "
            "even if you later change your password (until the token is invalidated)."
        ),
        "consequence": "Full account access for an attacker until the token expires or is revoked.",
        "prevention": (
            "Enable multi-factor authentication. "
            "Regularly review active sessions in account security settings and log out unknown sessions. "
            "Avoid clicking suspicious links. "
            "Log out of accounts on shared or public devices."
        ),
    },
    {
        "id": "phishing",
        "title": "Phishing & Fake Login Pages",
        "icon": "🎣",
        "explanation": (
            "Phishing is a social engineering attack where an adversary impersonates a trusted entity — "
            "a bank, a social media platform, an IT department — to trick users into revealing "
            "login credentials, installing malware, or authorizing transactions."
        ),
        "example": (
            "You receive a message saying your Instagram account will be disabled unless you verify "
            "your email. The link leads to a convincing-looking but fake Instagram login page. "
            "You enter your username and password. The attacker captures them instantly."
        ),
        "consequence": "Account takeover, identity theft, financial loss, or deployment of further attacks.",
        "prevention": (
            "Check the URL before entering credentials — look for HTTPS and the correct domain. "
            "Enable multi-factor authentication so a stolen password alone is not sufficient. "
            "Be suspicious of urgency-based messages. "
            "Report phishing attempts to the platform."
        ),
    },
    {
        "id": "xss",
        "title": "Cross-Site Scripting (XSS)",
        "icon": "💻",
        "explanation": (
            "XSS is an attack where malicious scripts are injected into a trusted website. "
            "When a victim's browser loads the page, the script runs in the context of that site — "
            "potentially stealing session cookies, redirecting the user, or modifying content."
        ),
        "example": (
            "An attacker posts a comment on a forum that contains a hidden script. "
            "When other users view the comment, the script runs in their browser "
            "and sends their session cookie to the attacker's server."
        ),
        "consequence": "Session hijacking, credential theft, or malicious actions performed as the user.",
        "prevention": (
            "Use browsers with XSS protection. "
            "Keep browsers and extensions updated. "
            "For developers: sanitize and escape all user-supplied input before rendering it."
        ),
    },
    {
        "id": "csrf",
        "title": "Cross-Site Request Forgery (CSRF)",
        "icon": "🔄",
        "explanation": (
            "CSRF tricks your browser into making an unintended request to a site where "
            "you are already authenticated — without your knowledge. "
            "Because the browser automatically includes your cookies with requests to that site, "
            "the forged request appears legitimate."
        ),
        "example": (
            "You are logged into your bank. You visit a malicious website that contains a hidden form "
            "that submits a transfer request to your bank. "
            "Your browser sends the request with your bank's session cookie, "
            "and the transfer is processed."
        ),
        "consequence": "Unauthorized account actions — changing settings, posting content, or financial transactions.",
        "prevention": (
            "Log out of sensitive accounts when not in use. "
            "Avoid visiting untrusted sites while logged into important accounts. "
            "Modern browsers and well-implemented sites include CSRF protections."
        ),
    },
    {
        "id": "sdks",
        "title": "Malicious or Poorly Configured SDKs",
        "icon": "📦",
        "explanation": (
            "Developers embed third-party SDKs (Software Development Kits) to add features "
            "like analytics, advertising, or payments. These SDKs run inside the app "
            "with the same permissions as the app itself. "
            "A poorly configured or malicious SDK can collect more data than the developer intended."
        ),
        "example": (
            "An app embeds an advertising SDK that also collects device location, "
            "unique device identifiers, and app usage patterns — "
            "even if the developer only intended to show ads."
        ),
        "consequence": (
            "Users' data collected beyond what the app's stated purpose requires. "
            "Data may be sent to the SDK provider's servers."
        ),
        "prevention": (
            "Prefer apps from developers who are transparent about which SDKs they use. "
            "Check app privacy labels (available on iOS App Store and some Android listings). "
            "For developers: audit SDK permissions and data collection practices before embedding."
        ),
    },
    {
        "id": "tracking_pixels",
        "title": "Cookies & Tracking Pixels",
        "icon": "🍪",
        "explanation": (
            "Cookies are small files stored by your browser that can track your session and activity. "
            "Third-party cookies set by advertising networks track you across many websites. "
            "A tracking pixel is a tiny invisible image that, when loaded, signals to a remote server "
            "that you visited a page or opened an email — including your IP address and browser details."
        ),
        "example": (
            "The Meta Pixel (formerly Facebook Pixel) is a JavaScript snippet placed on external websites. "
            "When you visit a site with the Meta Pixel, it reports your visit to Meta — "
            "even if you are not currently using Facebook. "
            "This data contributes to the advertising profile Meta maintains about you."
        ),
        "consequence": "Cross-site browsing profiles built without direct interaction with the tracking platform.",
        "prevention": (
            "Use a browser with third-party cookie blocking (e.g. Firefox, Safari) or privacy extensions. "
            "Opt out of personalised advertising in Facebook's Off-Facebook Activity settings. "
            "Use a content blocker that blocks known tracking scripts."
        ),
    },
    {
        "id": "data_profiling",
        "title": "Data Profiling & Data Brokerage",
        "icon": "📊",
        "explanation": (
            "Data profiling involves combining data from multiple sources — apps, websites, "
            "public records, purchase history — to build a detailed picture of an individual. "
            "Data brokers are companies that collect and sell these profiles "
            "to advertisers, insurers, employers, and others."
        ),
        "example": (
            "Your location data from a ride-hailing app, your purchase history from a shopping app, "
            "and your social media interests may be separately sold to data brokers. "
            "Brokers combine these into a profile that is resold to advertisers or other buyers."
        ),
        "consequence": (
            "Loss of privacy, discriminatory profiling, targeted manipulation, "
            "or exposure of sensitive information (health, financial status, political views)."
        ),
        "prevention": (
            "Limit the data you share with apps by reviewing permissions and account settings. "
            "Use opt-out registries where available (e.g. NAI opt-out, Digital Advertising Alliance). "
            "Be aware that once data is sold to a broker, it is very difficult to delete."
        ),
    },
    {
        "id": "e2ee",
        "title": "End-to-End Encryption & Metadata",
        "icon": "🔐",
        "explanation": (
            "End-to-end encryption (E2EE) means only the sender and recipient can read a message — "
            "not even the service provider. However, E2EE protects message content, not metadata. "
            "Metadata — who you communicated with, when, how often, and from where — "
            "can still be collected and can reveal sensitive information."
        ),
        "example": (
            "WhatsApp encrypts message content by default. "
            "However, Meta can still see: who you message, how often, when, "
            "from which device, and from which IP address. "
            "WhatsApp backups on Google Drive or iCloud are not covered by WhatsApp's E2EE "
            "unless encrypted backup is explicitly enabled."
        ),
        "consequence": (
            "Metadata reveals social networks, relationships, routines, and potentially sensitive associations "
            "even without access to message content."
        ),
        "prevention": (
            "Enable E2EE backup in WhatsApp. "
            "For highly sensitive communications, use Signal, which collects minimal metadata. "
            "Be aware that no messaging system can protect metadata completely."
        ),
    },
    {
        "id": "account_security",
        "title": "Basic Account Security & Multi-Factor Authentication",
        "icon": "🛡️",
        "explanation": (
            "Strong account security reduces the risk of unauthorized access even when credentials "
            "are stolen. Multi-factor authentication (MFA) requires a second proof of identity "
            "(e.g. a one-time code, an authenticator app, or a hardware key) in addition to your password."
        ),
        "example": (
            "An attacker obtains your password via a data breach. "
            "Without MFA, they can immediately log in. "
            "With MFA enabled, they also need your second factor — "
            "a code from your authenticator app — which they don't have."
        ),
        "consequence": (
            "Without MFA, a stolen or guessed password is sufficient for account takeover. "
            "Reusing passwords across sites means a breach on one site exposes all others."
        ),
        "prevention": (
            "Enable MFA on all important accounts — especially email, social media, and banking. "
            "Use an authenticator app (e.g. Google Authenticator, Authy) rather than SMS where possible, "
            "as SMS codes can be intercepted. "
            "Use a unique, strong password for each account — a password manager helps."
        ),
    },
]

CASE_STUDIES = [
    {
        "id": "cambridge_analytica",
        "title": "Facebook & Cambridge Analytica (2014–2018)",
        "icon": "📘",
        "what_happened": (
            "A personality quiz app called 'This Is Your Digital Life' was connected to Facebook "
            "via Facebook Login. Approximately 270,000 users consented to share their profile data "
            "with the app. Due to Facebook's API permissions at the time, the app could also access "
            "the profile data of those users' Facebook friends — without those friends' explicit consent. "
            "This reportedly resulted in the data of approximately 87 million users being harvested. "
            "The data was later used by Cambridge Analytica for political profiling purposes."
        ),
        "weakness": (
            "Facebook's API at the time allowed apps to access friends' data through a single consenting user. "
            "This is an example of overly broad OAuth/API scopes and insufficient enforcement "
            "of third-party data use restrictions."
        ),
        "why_it_matters": (
            "The incident highlighted that consenting to one app's data access can expose "
            "your friends' data without their knowledge. It demonstrated the risks of "
            "permissive API design and insufficient oversight of third-party developers."
        ),
        "what_users_can_learn": (
            "Review which apps are connected to your social media accounts. "
            "Consider what data you are sharing — and what data about others you may be indirectly sharing. "
            "Be cautious about authorizing apps that request access to your friends list."
        ),
        "what_dashboard_helps": (
            "Data Guardian can help you understand OAuth permissions, review connected apps, "
            "and follow the steps to revoke unused third-party authorisations."
        ),
        "what_dashboard_cannot_do": (
            "Data Guardian cannot detect whether an app has already harvested data, "
            "reverse data that has already been collected, or guarantee that similar practices "
            "are not occurring with other connected apps."
        ),
        "source": "Multiple news reports; Meta's own disclosures (2018). The approximately 87 million figure is from Meta's public statements in 2018.",
        "source_link": "https://about.fb.com/news/2018/04/restricting-data-access/",
    },
    {
        "id": "snapchat_findfriends",
        "title": "Snapchat Find Friends Incident (2014)",
        "icon": "👻",
        "what_happened": (
            "In December 2013, security researchers at Gibson Security published a warning "
            "that Snapchat's Find Friends API could be exploited to match phone numbers "
            "to usernames at scale. Snapchat did not immediately address the vulnerability. "
            "In early January 2014, attackers exploited the API and published a database "
            "containing approximately 4.6 million Snapchat usernames paired with "
            "partial phone numbers."
        ),
        "weakness": (
            "Snapchat's Find Friends API did not implement adequate rate limiting or "
            "abuse detection. This allowed automated requests to enumerate a large portion "
            "of the user base — exposing usernames and partial phone numbers in bulk."
        ),
        "why_it_matters": (
            "This incident illustrates how an API designed for a legitimate user feature "
            "(finding friends) can be abused at scale when appropriate controls are absent. "
            "Contact-matching features create a large, valuable dataset that can be exposed "
            "if the API is not properly secured."
        ),
        "what_users_can_learn": (
            "Contact access on apps contributes to databases that can be targeted. "
            "Limiting contact access and restricting who can find you by phone number "
            "reduces exposure. Review your discoverability settings."
        ),
        "what_dashboard_helps": (
            "Data Guardian explains contact permission risks, describes the Snapchat incident, "
            "and guides users to review Snapchat's discoverability settings."
        ),
        "what_dashboard_cannot_do": (
            "Data Guardian cannot prevent API abuse at the platform level or "
            "detect whether your data has already been included in a harvested dataset."
        ),
        "source": "Gibson Security disclosure (December 2013); widespread media reporting (January 2014).",
        "source_link": "https://gibsonsec.org/snapchat/",
    },
    {
        "id": "cross_site_tracking",
        "title": "Cross-Site Tracking via Embedded Social Plugins",
        "icon": "🌐",
        "what_happened": (
            "Social media platforms provide website owners with embedded 'Like' buttons, "
            "share widgets, and comment boxes. These elements load scripts from the social "
            "platform's servers. When a user visits a website with these plugins, "
            "the social platform may receive a signal that includes the page URL, "
            "the user's IP address, and — if the user is logged in — their account identity. "
            "Tracking pixels work similarly: a 1×1 pixel image triggers a request to a "
            "tracking server when the page loads."
        ),
        "weakness": (
            "The HTTP protocol sends browser cookies and headers with every request to a domain. "
            "Third-party scripts embedded across many websites can build a browsing profile "
            "that spans many unrelated sites — often without the user's awareness."
        ),
        "why_it_matters": (
            "Users may not realize that visiting a health information website, "
            "reading a news article, or browsing an online shop shares that activity "
            "with social media companies or advertising networks via embedded trackers."
        ),
        "what_users_can_learn": (
            "Use browsers with built-in tracking protection (Firefox, Safari, Brave). "
            "Install content-blocking extensions. "
            "Opt out of off-platform data use in social media ad settings."
        ),
        "what_dashboard_helps": (
            "Data Guardian explains how tracking pixels and cookies work, "
            "describes the Meta Pixel specifically, and points users towards "
            "Facebook's Off-Facebook Activity settings."
        ),
        "what_dashboard_cannot_do": (
            "Data Guardian cannot block trackers on your device or confirm "
            "how many tracking scripts you currently encounter."
        ),
        "source": "General cybersecurity and privacy research. No specific single incident — this is an ongoing, documented practice.",
        "source_link": "https://www.eff.org/issues/trackers",
    },
]


def show_learning_centre():
    st.markdown("## 🎓 Cybersecurity Learning Centre")
    st.markdown(
        "<div class='dg-info'>"
        "This section explains privacy and cybersecurity concepts in plain language, "
        "with real examples, consequences, and prevention steps. "
        "Content is based on documented security practices and publicly reported incidents."
        "</div>",
        unsafe_allow_html=True,
    )

    tab_topics, tab_cases = st.tabs(["📖 Educational Topics", "🔍 Case Studies"])

    # ── Topics ─────────────────────────────────────────────────────────────────
    with tab_topics:
        st.markdown("### Privacy & Cybersecurity Concepts")
        st.markdown("Select any topic to expand it.")

        topic_filter = st.selectbox(
            "Jump to topic",
            ["All topics"] + [t["title"] for t in TOPICS],
            key="topic_filter",
        )

        for topic in TOPICS:
            if topic_filter != "All topics" and topic["title"] != topic_filter:
                continue

            with st.expander(f"{topic['icon']}  {topic['title']}", expanded=(topic_filter == topic["title"])):
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.markdown("#### What is it?")
                    st.markdown(
                        f"<div class='dg-card-body'>{topic['explanation']}</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown("#### Real example")
                    st.markdown(
                        f"<div class='dg-info'>{topic['example']}</div>",
                        unsafe_allow_html=True,
                    )
                with c2:
                    st.markdown("#### Potential consequence")
                    st.markdown(
                        f"<div class='dg-warn'>{topic['consequence']}</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown("#### What you can do")
                    st.markdown(
                        f"<div class='dg-ok'>{topic['prevention']}</div>",
                        unsafe_allow_html=True,
                    )

    # ── Case studies ───────────────────────────────────────────────────────────
    with tab_cases:
        st.markdown("### Case Studies")
        st.markdown(
            "<div class='dg-warn'>"
            "These are documented historical events. They are described here for educational purposes. "
            "They are not current threats and Data Guardian cannot prevent similar incidents. "
            "Figures and descriptions are based on publicly available sources cited below each study."
            "</div>",
            unsafe_allow_html=True,
        )

        for cs in CASE_STUDIES:
            with st.expander(f"{cs['icon']}  {cs['title']}", expanded=False):
                st.markdown(
                    f"""
                    <div class='dg-card'>
                        <div class='dg-card-title'>What Happened</div>
                        <div class='dg-card-body'>{cs['what_happened']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Security weakness involved**")
                    st.markdown(
                        f"<div class='dg-danger'>{cs['weakness']}</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown("**Why it matters**")
                    st.markdown(
                        f"<div class='dg-warn'>{cs['why_it_matters']}</div>",
                        unsafe_allow_html=True,
                    )
                with c2:
                    st.markdown("**What users can learn**")
                    st.markdown(
                        f"<div class='dg-ok'>{cs['what_users_can_learn']}</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown("**What Data Guardian can help with**")
                    st.markdown(
                        f"<div class='dg-info'>{cs['what_dashboard_helps']}</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown("**What the dashboard cannot do**")
                    st.markdown(
                        f"<div class='dg-card-body' style='color:#ff9090;'>"
                        f"⚠️ {cs['what_dashboard_cannot_do']}</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"📎 **Source:** {cs['source']}  \n"
                    f"🔗 [View source]({cs['source_link']})"
                )
