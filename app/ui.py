import streamlit as st
import requests
from datetime import datetime

# ----------------------------------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="ParcelPilot AI Support",
    page_icon="📦",
    layout="centered",
    initial_sidebar_state="expanded",
)

API_URL = "http://127.0.0.1:8000/chat"
STATUS_STEPS = ["BOOKED", "PICKED UP", "IN TRANSIT", "DELIVERED"]

# ----------------------------------------------------------------------------
# ENTERPRISE UI STYLING
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        :root {
            --pp-primary: #1E40AF;
            --pp-primary-light: #EFF6FF;
            --pp-accent: #0284C7;
            --pp-success: #16A34A;
            --pp-warning: #D97706;
            --pp-danger: #DC2626;
            --pp-text-main: #0F172A;
            --pp-text-muted: #64748B;
            --pp-border: #E2E8F0;
            --pp-card-bg: #FFFFFF;
            --pp-bg: #F8FAFC;
        }

        .stApp {
            background-color: var(--pp-bg);
        }

        #MainMenu, footer, header { visibility: hidden; }

        /* ---------- Header Container ---------- */
        .pp-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 1.25rem;
            background: var(--pp-card-bg);
            border: 1px solid var(--pp-border);
            border-radius: 16px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
        }
        .pp-header-left {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .pp-logo {
            font-size: 1.6rem;
            background: var(--pp-primary-light);
            border-radius: 12px;
            padding: 0.5rem 0.75rem;
            border: 1px solid #DBEAFE;
        }
        .pp-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--pp-text-main);
            margin: 0;
            line-height: 1.2;
        }
        .pp-subtitle {
            font-size: 0.825rem;
            color: var(--pp-text-muted);
            margin-top: 0.2rem;
            font-weight: 500;
        }
        .pp-status {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.8rem;
            color: var(--pp-success);
            font-weight: 600;
            background: #DCFCE7;
            padding: 0.35rem 0.75rem;
            border-radius: 9999px;
        }
        .pp-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--pp-success);
        }

        /* ---------- Cards & Banner ---------- */
        .pp-welcome {
            background: var(--pp-card-bg);
            border: 1px solid var(--pp-border);
            border-left: 5px solid var(--pp-primary);
            border-radius: 14px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        }
        .pp-welcome h4 {
            margin: 0 0 0.5rem 0;
            color: var(--pp-text-main);
            font-size: 1.15rem;
            font-weight: 700;
        }
        .pp-welcome p {
            margin: 0;
            color: var(--pp-text-muted);
            font-size: 0.925rem;
            line-height: 1.6;
        }

        /* ---------- Order Card & Badges ---------- */
        .pp-order-card {
            background: var(--pp-card-bg);
            border: 1px solid var(--pp-border);
            border-radius: 14px;
            padding: 1.25rem;
            margin: 0.75rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
        }
        .pp-order-title {
            font-weight: 700;
            font-size: 1rem;
            color: var(--pp-text-main);
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .pp-order-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.4rem 0;
            font-size: 0.875rem;
            border-bottom: 1px dashed var(--pp-border);
        }
        .pp-order-row:last-of-type { border-bottom: none; }
        .pp-order-label { color: var(--pp-text-muted); font-weight: 500; }
        .pp-order-value { color: var(--pp-text-main); font-weight: 600; }

        .pp-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.2rem 0.65rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.01em;
        }
        .pp-badge-booked { background: #EFF6FF; color: #1E40AF; }
        .pp-badge-picked { background: #FEF3C7; color: #92400E; }
        .pp-badge-transit { background: #FFEDD5; color: #C2410C; }
        .pp-badge-delivered { background: #DCFCE7; color: #166534; }
        .pp-badge-cancelled { background: #FEE2E2; color: #991B1B; }

        /* ---------- Progress Timeline ---------- */
        .pp-timeline {
            display: flex;
            align-items: center;
            margin-top: 1.2rem;
            padding-top: 0.5rem;
        }
        .pp-step {
            font-size: 0.725rem;
            color: var(--pp-text-muted);
            text-align: center;
            flex: 1;
            position: relative;
        }
        .pp-step-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--pp-border);
            margin: 0 auto 0.4rem auto;
            transition: all 0.2s ease;
        }
        .pp-step-dot.active { background: var(--pp-primary); box-shadow: 0 0 0 3px #DBEAFE; }
        .pp-step.active-label { color: var(--pp-text-main); font-weight: 700; }

        /* ---------- Confirm Cards ---------- */
        .pp-confirm-card {
            background: #FFFBEB;
            border: 1px solid #FDE68A;
            border-radius: 14px;
            padding: 1.25rem;
            margin: 0.75rem 0;
        }
        .pp-confirm-title {
            font-weight: 700;
            color: #92400E;
            margin-bottom: 0.5rem;
        }

        /* ---------- Chat Customization ---------- */
        .pp-bubble {
            border-radius: 12px;
            padding: 0.85rem 1.1rem;
            font-size: 0.95rem;
            line-height: 1.6;
            margin-top: 0.25rem;
        }
        .pp-bubble-user {
            background: #FFFFFF !important;
            border: 1px solid var(--pp-border);
            color: var(--pp-text-main) !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
        }
        .pp-bubble-assistant {
            background: #EFF6FF !important;
            border: 1px solid #BFDBFE;
            color: #1E3A8A !important;
        }
        .pp-processing {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--pp-text-muted);
            font-style: italic;
        }

        /* ---------- Sidebar Redesign ---------- */
        section[data-testid="stSidebar"] {
            background: #0F172A;
        }
        section[data-testid="stSidebar"] * {
            color: #F8FAFC !important;
        }
        section[data-testid="stSidebar"] input {
            color: #0F172A !important;
            background-color: #FFFFFF !important;
            border-radius: 8px !important;
        }
        .pp-sidebar-brand {
            font-weight: 800;
            font-size: 1.15rem;
            letter-spacing: 0.04em;
        }
        .pp-sidebar-sub {
            font-size: 0.75rem;
            color: #94A3B8 !important;
            letter-spacing: 0.05em;
        }
        .pp-sidebar-section-label {
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            color: #94A3B8 !important;
            margin-top: 1rem;
            margin-bottom: 0.4rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# SESSION STATE MANAGEMENT
# ----------------------------------------------------------------------------
def reset_to_home():
    """Resets chat context and sends user back to home landing state."""
    st.session_state.messages = []
    st.session_state.queued_prompt = None
    st.session_state.pending_request = None
    st.session_state.cancel_flow_step = None
    st.session_state.cancel_order_id = ""

if "messages" not in st.session_state:
    st.session_state.messages = []
if "queued_prompt" not in st.session_state:
    st.session_state.queued_prompt = None
if "pending_request" not in st.session_state:
    st.session_state.pending_request = None
if "cancel_flow_step" not in st.session_state:
    st.session_state.cancel_flow_step = None
if "cancel_order_id" not in st.session_state:
    st.session_state.cancel_order_id = ""
if "account_id" not in st.session_state:
    st.session_state.account_id = "ACCT-001"

# ----------------------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------------------
def status_badge_class(status: str) -> str:
    status = (status or "").upper()
    if status == "DELIVERED":
        return "pp-badge-delivered"
    if status in ("CANCELLED", "CANCELED"):
        return "pp-badge-cancelled"
    if status == "PICKED UP":
        return "pp-badge-picked"
    if status == "IN TRANSIT":
        return "pp-badge-transit"
    return "pp-badge-booked"

def status_badge_emoji(status: str) -> str:
    status = (status or "").upper()
    if status == "DELIVERED":
        return "🟢"
    if status in ("CANCELLED", "CANCELED"):
        return "🔴"
    if status == "PICKED UP":
        return "🟡"
    if status == "IN TRANSIT":
        return "🟠"
    return "🔵"

def render_order_card(order: dict):
    order_id = order.get("order_id", "N/A")
    status = (order.get("status", "UNKNOWN") or "UNKNOWN").upper()
    carrier = order.get("carrier", "—")
    acct = order.get("account_id", "—")

    current_index = STATUS_STEPS.index(status) if status in STATUS_STEPS else -1

    rows = f"""
        <div class="pp-order-row">
            <span class="pp-order-label">Status</span>
            <span><span class="pp-badge {status_badge_class(status)}">{status_badge_emoji(status)} {status}</span></span>
        </div>
        <div class="pp-order-row">
            <span class="pp-order-label">Carrier</span>
            <span class="pp-order-value">{carrier}</span>
        </div>
        <div class="pp-order-row">
            <span class="pp-order-label">Account</span>
            <span class="pp-order-value">{acct}</span>
        </div>
    """

    timeline = ""
    if status not in ("CANCELLED", "CANCELED"):
        steps_html = ""
        for i, step in enumerate(STATUS_STEPS):
            active = i <= current_index
            steps_html += f"""
                <div class="pp-step">
                    <div class="pp-step-dot {'active' if active else ''}"></div>
                    <span class="{'active-label' if i == current_index else ''}">{step}</span>
                </div>
            """
        timeline = f'<div class="pp-timeline">{steps_html}</div>'

    st.markdown(
        f"""
        <div class="pp-order-card">
            <div class="pp-order-title">📦 Order Summary: {order_id}</div>
            {rows}
            {timeline}
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_tool_activity(tools_used: list):
    if not tools_used:
        return
    with st.expander("🔧 Agent Activity Diagnostics", expanded=False):
        for tool in tools_used:
            st.markdown(f"✓ `{tool}`")

TECHNICAL_ERROR_MARKERS = [
    "httpconnectionpool", "read timed out", "connection refused",
    "traceback", "resource_exhausted", "429", "5xx", "500",
    "internal server error", "timeout", "connectionerror", "max retries exceeded",
]
ACCESS_DENIED_MARKERS = [
    "access denied", "not authorized", "permission denied",
    "unauthorized", "access restricted", "forbidden",
]

def humanize_response(text: str) -> str:
    if not text:
        return text
    lower = text.lower()

    if any(marker in lower for marker in TECHNICAL_ERROR_MARKERS):
        return (
            "⚠️ **Service Temporarily Unavailable**\n\n"
            "We are currently experiencing technical difficulty processing your request. Please try again shortly."
        )

    if any(marker in lower for marker in ACCESS_DENIED_MARKERS):
        return (
            "🔒 **Access Restricted**\n\n"
            "This order record is not accessible under your current account credentials.\n\n"
            "If you require assistance, please contact ParcelPilot Support."
        )

    return text

def call_agent_api(message: str, account_id: str) -> dict:
    payload = {
        "message": message,
        "user_context": {"account_id": account_id},
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ParcelPilot API Error] {e}")
        return {"answer": "⚠️ **Service Temporarily Unavailable**\n\nUnable to process your request at this time."}

def start_request(text: str):
    st.session_state.messages.append({"role": "user", "content": text})
    st.session_state.pending_request = text

def queue_prompt(text: str):
    st.session_state.queued_prompt = text

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="pp-sidebar-brand">📦 PARCELPILOT</div>', unsafe_allow_html=True)
    st.markdown('<div class="pp-sidebar-sub">ENTERPRISE ASSISTANT</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Navigation / Home Option
    st.markdown('<div class="pp-sidebar-section-label">NAVIGATION</div>', unsafe_allow_html=True)
    if st.button("🏠 Home / Finish Session", use_container_width=True, type="primary"):
        reset_to_home()
        st.rerun()

    st.markdown('<div class="pp-sidebar-section-label">ACCOUNT SETTINGS</div>', unsafe_allow_html=True)
    account_id_input = st.text_input(
        "Account ID", value=st.session_state.account_id, label_visibility="collapsed"
    )
    st.session_state.account_id = account_id_input
    st.caption("Connected: Northstar Logistics")

    st.markdown("---")
    st.markdown('<div class="pp-sidebar-section-label">QUICK ACTIONS</div>', unsafe_allow_html=True)

    if st.button("📦 Track Order", use_container_width=True):
        queue_prompt("I'd like to track my order.")
    if st.button("❌ Cancel Order", use_container_width=True):
        st.session_state.cancel_flow_step = "input"
    if st.button("📋 Policies", use_container_width=True):
        queue_prompt("What is your cancellation policy?")
    if st.button("👨‍💼 Escalate to Agent", use_container_width=True):
        queue_prompt("I'd like to speak with a human support agent.")

    st.markdown("---")
    if st.button("🗑 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.cancel_flow_step = None
        st.rerun()

# ----------------------------------------------------------------------------
# HEADER & HOME ACTION
# ----------------------------------------------------------------------------
header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    st.markdown(
        f"""
        <div class="pp-header">
            <div class="pp-header-left">
                <div class="pp-logo">📦</div>
                <div>
                    <p class="pp-title">ParcelPilot AI Agent</p>
                    <p class="pp-subtitle">Customer Support Portal · Account: <b>{st.session_state.account_id}</b></p>
                </div>
            </div>
            <div class="pp-status"><span class="pp-dot"></span> System Online</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_col2:
    if st.button("🏠 Finish & Home", help="Reset chat and return to main screen", use_container_width=True):
        reset_to_home()
        st.rerun()

# ----------------------------------------------------------------------------
# WELCOME SCREEN (Rendered when no active conversation)
# ----------------------------------------------------------------------------
if not st.session_state.messages:
    st.markdown(
        """
        <div class="pp-welcome">
            <h4>👋 Welcome to ParcelPilot Intelligent Support</h4>
            <p>I am your automated logistics concierge. I can assist you with real-time package tracking, 
            order modifications, cancellations, and enterprise shipping policies.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("📦 Track Order", use_container_width=True):
            queue_prompt("I'd like to track my order.")
    with c2:
        if st.button("❌ Cancel Order", use_container_width=True):
            st.session_state.cancel_flow_step = "input"
    with c3:
        if st.button("📋 Cancellation Policy", use_container_width=True):
            queue_prompt("What is your cancellation policy?")
    with c4:
        if st.button("👨‍💼 Live Support", use_container_width=True):
            queue_prompt("I'd like to speak with a human support agent.")

# ----------------------------------------------------------------------------
# CANCELLATION DIALOG WORKFLOW
# ----------------------------------------------------------------------------
if st.session_state.cancel_flow_step == "input":
    with st.container():
        st.markdown(
            """
            <div class="pp-confirm-card">
                <div class="pp-confirm-title">❌ Cancel an Order</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        order_id_input = st.text_input("Enter Order ID", placeholder="e.g. ORD-1001")
        cc1, cc2 = st.columns(2)
        with cc1:
            if st.button("Review Cancellation Request", use_container_width=True, disabled=not order_id_input):
                st.session_state.cancel_order_id = order_id_input
                st.session_state.cancel_flow_step = "confirm"
                st.rerun()
        with cc2:
            if st.button("Dismiss", use_container_width=True):
                st.session_state.cancel_flow_step = None
                st.rerun()

if st.session_state.cancel_flow_step == "confirm":
    order_id = st.session_state.cancel_order_id
    st.markdown(
        f"""
        <div class="pp-confirm-card">
            <div class="pp-confirm-title">⚠️ Confirm Cancellation</div>
            <div class="pp-order-row"><span class="pp-order-label">Target Order:</span>
                <span class="pp-order-value">{order_id}</span></div>
            <div class="pp-order-row"><span class="pp-order-label">Account Context:</span>
                <span class="pp-order-value">{st.session_state.account_id}</span></div>
            <p style="margin-top:0.75rem; font-size:0.875rem; color:#92400E;">
                Are you sure you want to cancel this order? Once confirmed, this action cannot be reversed.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cc1, cc2 = st.columns(2)
    with cc1:
        if st.button("Keep Order", use_container_width=True):
            st.session_state.cancel_flow_step = None
            st.rerun()
    with cc2:
        if st.button("Confirm Cancellation", use_container_width=True, type="primary"):
            start_request(f"Please cancel order {order_id}.")
            st.session_state.cancel_flow_step = None
            st.rerun()

# ----------------------------------------------------------------------------
# CHAT HISTORY DISPLAY
# ----------------------------------------------------------------------------
for message in st.session_state.messages:
    role = message["role"]
    label = "👤 You" if role == "user" else "🤖 ParcelPilot AI"
    with st.chat_message(role):
        st.markdown(f"**{label}**")
        st.markdown(
            f'<div class="pp-bubble pp-bubble-{role}">{message["content"]}</div>',
            unsafe_allow_html=True,
        )
        if role == "assistant":
            if message.get("order"):
                render_order_card(message["order"])
            if message.get("tools_used"):
                render_tool_activity(message["tools_used"])

# ----------------------------------------------------------------------------
# ASYNCHRONOUS PENDING REQUEST HANDLER
# ----------------------------------------------------------------------------
if st.session_state.pending_request:
    with st.chat_message("assistant"):
        st.markdown("**🤖 ParcelPilot AI**")
        st.markdown(
            '<div class="pp-bubble pp-bubble-assistant pp-processing">⏳ Processing your request...</div>',
            unsafe_allow_html=True,
        )

    text = st.session_state.pending_request
    st.session_state.pending_request = None
    result = call_agent_api(text, st.session_state.account_id)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": humanize_response(result.get("answer", "Sorry, I could not process your request.")),
            "order": result.get("order"),
            "tools_used": result.get("tools_used"),
        }
    )
    st.rerun()

# ----------------------------------------------------------------------------
# QUEUED PROMPTS & USER INPUT
# ----------------------------------------------------------------------------
if st.session_state.queued_prompt:
    prompt = st.session_state.queued_prompt
    st.session_state.queued_prompt = None
    start_request(prompt)
    st.rerun()

user_message = st.chat_input("Ask ParcelPilot AI about your shipment...")
if user_message:
    start_request(user_message)
    st.rerun()