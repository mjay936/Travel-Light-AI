import streamlit as st
from datetime import date
import os
from dotenv import load_dotenv
from streamlit.components.v1 import html as st_html
from api_server import start_server_in_thread

# Load environment variables
load_dotenv()
start_server_in_thread()

# --- Floating Shortcut Button CSS ---
st.markdown("", unsafe_allow_html=True)

# --- Floating Shortcut Button (no-JS using details/summary) ---
st.markdown("", unsafe_allow_html=True)

# --- Hero Section with Background ---
st.markdown("""
    <style>
    .hero {
        background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        padding: 3em 2em 2em 2em;
        border-radius: 18px;
        margin-bottom: 2em;
        color: white;
        box-shadow: 0 4px 24px rgba(0,0,0,0.15);
    }
    .hero h1, .hero h3, .hero p {
        color: white !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }
    .hero h1 {margin-bottom: 0.2em;}
    </style>
    <div class="hero">
        <h1>✈️ Travel Light</h1>
        <h3>Book Flights, Hotels, Trains, Cabs, or Chat with AI</h3>
        <p>Find the best deals or get personalized travel advice!</p>
    </div>
""", unsafe_allow_html=True)

# --- Tabbed Navigation ---
tabs = st.tabs(["Flights", "Hotels", "Trains", "Cabs", "AI Chat"])

# --- Flights Tab ---
with tabs[0]:
    st.markdown("#### Search Flights")
    col1, col2, col3 = st.columns(3)
    with col1:
        from_city = st.text_input("From", "New York", key="flight_from")
    with col2:
        to_city = st.text_input("To", "London", key="flight_to")
    with col3:
        depart_date = st.date_input("Departure", date.today(), key="flight_depart")
    col4, col5 = st.columns(2)
    with col4:
        passengers = st.number_input("Passengers", 1, 10, 1, key="flight_pass")
    with col5:
        flight_class = st.selectbox("Class", ["Economy", "Business", "First"], key="flight_class")
    if st.button("🔍 Search Flights", key="flight_search"):
        st.success(f"Searching flights from {from_city} to {to_city} on {depart_date} for {passengers} passenger(s) in {flight_class} class.")

# --- Hotels Tab ---
with tabs[1]:
    st.markdown("#### Search Hotels")
    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("City", "Paris", key="hotel_city")
    with col2:
        check_in = st.date_input("Check-in", date.today(), key="hotel_checkin")
    col3, col4 = st.columns(2)
    with col3:
        check_out = st.date_input("Check-out", date.today(), key="hotel_checkout")
    with col4:
        guests = st.number_input("Guests", 1, 10, 1, key="hotel_guests")
    if st.button("🔍 Search Hotels", key="hotel_search"):
        st.success(f"Searching hotels in {city} from {check_in} to {check_out} for {guests} guest(s).")

# --- Trains Tab ---
with tabs[2]:
    st.markdown("#### Search Trains")
    col1, col2 = st.columns(2)
    with col1:
        from_station = st.text_input("From Station", "Delhi", key="train_from")
    with col2:
        to_station = st.text_input("To Station", "Mumbai", key="train_to")
    col3, col4 = st.columns(2)
    with col3:
        train_date = st.date_input("Travel Date", date.today(), key="train_date")
    with col4:
        train_class = st.selectbox("Class", ["Sleeper", "AC", "First Class"], key="train_class")
    if st.button("🔍 Search Trains", key="train_search"):
        st.success(f"Searching trains from {from_station} to {to_station} on {train_date} in {train_class} class.")

# --- Cabs Tab ---
with tabs[3]:
    st.markdown("#### Book a Cab")
    col1, col2 = st.columns(2)
    with col1:
        pickup = st.text_input("Pickup Location", "Airport", key="cab_pickup")
    with col2:
        drop = st.text_input("Drop Location", "Hotel", key="cab_drop")
    col3, col4 = st.columns(2)
    with col3:
        cab_date = st.date_input("Pickup Date", date.today(), key="cab_date")
    with col4:
        cab_time = st.time_input("Pickup Time", key="cab_time")
    if st.button("🚕 Book Cab", key="cab_book"):
        st.success(f"Booking cab from {pickup} to {drop} on {cab_date} at {cab_time}.")

# --- AI Chat Tab ---
with tabs[4]:
    # --- Destination Image Mapping ---
    DEST_IMAGES = {
        "bali": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
        "paris": "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=800&q=80",
        "tokyo": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80",
        "new york": "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=800&q=80",
        "default": "https://images.unsplash.com/photo-1465101178521-c1a9136a3b41?auto=format&fit=crop&w=800&q=80"
    }
    def get_destination_image(messages):
        for msg in reversed(messages):
            if msg["role"] == "user":
                for dest in DEST_IMAGES:
                    if dest in msg["content"].lower():
                        return DEST_IMAGES[dest]
        return DEST_IMAGES["default"]

    # --- Session State ---
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "graph_state" not in st.session_state:
        st.session_state["graph_state"] = {"messages": []}
    if "summary" not in st.session_state:
        st.session_state["summary"] = ""
        if not st.session_state["messages"]:
            # Buddy introduces itself at the start
            buddy_intro = {"role": "assistant", "content": "Hey there! I'm <b>Buddy</b> 🧑‍🚀, your AI travel companion! I'm here to help you plan the perfect trip. Whether you need itinerary suggestions, travel tips, or just want to chat about destinations, I've got you covered! What's on your mind today?"}
            st.session_state["messages"].append(buddy_intro)
            st.session_state["graph_state"]["messages"].append(buddy_intro)

    # --- Buddy Avatar and Tips ---
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div style='text-align:center;margin-bottom:1em;'>
            <img src='https://cdn-icons-png.flaticon.com/512/4712/4712035.png' width='80' style='border-radius:50%;box-shadow:0 2px 12px rgba(0,0,0,0.12);'>
            <div style='font-size:1.2em;margin-top:0.5em;'><b>Buddy</b> <span style='font-size:1.2em;'>🧑‍🚀</span></div>
            <div style='color:#888;font-size:0.95em;'>Your AI Travel Assistant</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("### 💡 Quick Tips from Buddy")
        st.info("""
        🎯 **Try asking me:**
        - "Plan a 3-day budget trip to Bali"
        - "What's the best time to visit Paris?"
        - "Give me travel tips for Tokyo"
        - "Help me find cheap flights to New York"
        """)

    # --- Quick Reply Buttons ---
    st.markdown("### 🚀 Quick Actions")
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
    with quick_col1:
        if st.button("🗺️ Plan Trip", key="quick_plan"):
            st.session_state["quick_action"] = "Plan a trip for me"
    with quick_col2:
        if st.button("🏨 Find Hotels", key="quick_hotels"):
            st.session_state["quick_action"] = "Help me find hotels"
    with quick_col3:
        if st.button("✈️ Flight Tips", key="quick_flights"):
            st.session_state["quick_action"] = "Give me flight booking tips"
    with quick_col4:
        if st.button("🌍 Travel Tips", key="quick_tips"):
            st.session_state["quick_action"] = "Share some travel tips"

    # --- Chat Section with Visual Bubbles ---
    st.markdown("### 💬 Chat with Buddy")
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style='background-color:#e1f5fe;padding:12px 16px;border-radius:12px;margin-bottom:8px;max-width:80%;margin-left:auto;text-align:right;'>
                <b>🧑‍💼 You:</b> {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background-color:#fffbe7;padding:12px 16px;border-radius:12px;margin-bottom:8px;max-width:80%;margin-right:auto;text-align:left;'>
                <b>🧑‍🚀 Buddy:</b> {msg['content']}
            </div>
            """, unsafe_allow_html=True)

    # --- User Input ---
    user_input = st.text_input("Ask Buddy anything about your trip!", key="ai_chat_input")
    col1, col2 = st.columns(2)
    with col1:
        reset_button = st.button("🔄 Reset Chat", key="ai_chat_reset")
    with col2:
        debug_mode = st.checkbox("🐛 Debug Mode", key="ai_chat_debug")

    # --- Handle Reset ---
    if reset_button:
        st.session_state["messages"] = []
        st.session_state["graph_state"] = {"messages": []}
        st.session_state["summary"] = ""
        st.rerun()

    # --- Handle Quick Actions ---
    if "quick_action" in st.session_state and st.session_state["quick_action"]:
        user_msg = {"role": "user", "content": st.session_state["quick_action"]}
        st.session_state["messages"].append(user_msg)
        st.session_state["graph_state"]["messages"].append(user_msg)
        del st.session_state["quick_action"]
        st.rerun()

    # --- Handle User Input ---
    if user_input and user_input.strip():
        user_msg = {"role": "user", "content": user_input.strip()}
        st.session_state["messages"].append(user_msg)
        st.session_state["graph_state"]["messages"].append(user_msg)
        with st.spinner("🧑‍🚀 Buddy is thinking..."):
            from travel_graph import build_conversation_graph
            graph = build_conversation_graph()
            result = graph.invoke(st.session_state["graph_state"])
        bot_messages = result.get("messages", [])
        if bot_messages:
            latest_bot_msg = bot_messages[-1]
            if hasattr(latest_bot_msg, 'content'):
                bot_content = latest_bot_msg.content
            elif isinstance(latest_bot_msg, dict):
                bot_content = latest_bot_msg.get("content", "")
            else:
                bot_content = str(latest_bot_msg)
            bot_msg = {"role": "assistant", "content": bot_content}
            st.session_state["messages"].append(bot_msg)
            st.session_state["graph_state"]["messages"].append(bot_msg)
            st.session_state["summary"] = "\n".join(
                getattr(m, 'content', str(m)) for m in bot_messages if getattr(m, 'role', 'assistant') == 'assistant'
            )
        else:
            st.session_state["summary"] = "Buddy didn't return a response."
            st.session_state["messages"].append({"role": "assistant", "content": st.session_state["summary"]})
            st.session_state["graph_state"]["messages"].append({"role": "assistant", "content": st.session_state["summary"]})
        st.rerun()

    # --- Show Destination Visual ---
    if st.session_state["messages"]:
        dest_img = get_destination_image(st.session_state["messages"])
        st.image(dest_img, caption="Your Dream Destination", use_column_width=True)

    # --- Show Summary ---
    if st.session_state["summary"]:
        with st.expander("📝 View Conversation Summary"):
            st.success(st.session_state["summary"])

    # --- Buddy's Mood/Status ---
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center;color:#888;font-size:0.9em;'>
        🧑‍🚀 Buddy is online and ready to help! | Status: Active
    </div>
    """, unsafe_allow_html=True)

# --- Offers/Popular Destinations ---
st.markdown("### 🌟 Popular Destinations & Offers")
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80")
    st.caption("Paris - Up to 20% off")
with col2:
    st.image("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=400&q=80")
    st.caption("Tokyo - Special fares")
with col3:
    st.image("https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80")
    st.caption("New York - Last minute deals")

# --- Footer ---
st.markdown("""
    <hr>
    <div style='text-align:center;color:#888;'>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar AI Chatbot (replacing Quick Access) ---
with st.sidebar:
    st.markdown("### 🧑‍🚀 Buddy (AI Chat)")

    # Ensure session state exists (safe to re-check here)
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "graph_state" not in st.session_state:
        st.session_state["graph_state"] = {"messages": []}
    if "summary" not in st.session_state:
        st.session_state["summary"] = ""
        if not st.session_state["messages"]:
            buddy_intro = {"role": "assistant", "content": "Hey there! I'm <b>Buddy</b> 🧑‍🚀, your AI travel companion! I'm here to help you plan the perfect trip. Whether you need itinerary suggestions, travel tips, or just want to chat about destinations, I've got you covered! What's on your mind today?"}
            st.session_state["messages"].append(buddy_intro)
            st.session_state["graph_state"]["messages"].append(buddy_intro)

    # Show conversation
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style='background-color:#e1f5fe;padding:10px 12px;border-radius:10px;margin-bottom:6px;text-align:right;'>
                <b>You:</b> {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background-color:#fffbe7;padding:10px 12px;border-radius:10px;margin-bottom:6px;text-align:left;'>
                <b>Buddy:</b> {msg['content']}
            </div>
            """, unsafe_allow_html=True)

    # Input form in sidebar
    with st.form("sidebar_chat_form", clear_on_submit=True):
        sidebar_user_input = st.text_input("Ask Buddy anything...", key="sidebar_ai_chat_input")
        submitted = st.form_submit_button("Send")

    reset_sidebar = st.button("Reset Chat", key="sidebar_ai_chat_reset")

    if reset_sidebar:
        st.session_state["messages"] = []
        st.session_state["graph_state"] = {"messages": []}
        st.session_state["summary"] = ""
        st.rerun()

    if submitted and sidebar_user_input and sidebar_user_input.strip():
        user_msg = {"role": "user", "content": sidebar_user_input.strip()}
        st.session_state["messages"].append(user_msg)
        st.session_state["graph_state"]["messages"].append(user_msg)
        with st.spinner("🧑‍🚀 Buddy is thinking..."):
            from travel_graph import build_conversation_graph
            graph = build_conversation_graph()
            result = graph.invoke(st.session_state["graph_state"])
        bot_messages = result.get("messages", [])
        if bot_messages:
            latest_bot_msg = bot_messages[-1]
            if hasattr(latest_bot_msg, 'content'):
                bot_content = latest_bot_msg.content
            elif isinstance(latest_bot_msg, dict):
                bot_content = latest_bot_msg.get("content", "")
            else:
                bot_content = str(latest_bot_msg)
            bot_msg = {"role": "assistant", "content": bot_content}
            st.session_state["messages"].append(bot_msg)
            st.session_state["graph_state"]["messages"].append(bot_msg)
            st.session_state["summary"] = "\n".join(
                getattr(m, 'content', str(m)) for m in bot_messages if getattr(m, 'role', 'assistant') == 'assistant'
            )
        else:
            st.session_state["summary"] = "Buddy didn't return a response."
            st.session_state["messages"].append({"role": "assistant", "content": st.session_state["summary"]})
            st.session_state["graph_state"]["messages"].append({"role": "assistant", "content": st.session_state["summary"]})
        st.rerun()

# --- Floating Chatbot Widget ---
st_html("""
<div id="chatbot-widget">
  <style>
    #chatbot-widget, #chatbot-widget * { box-sizing: border-box; }
    #chatbot-widget {
      --primary: #5B6CFF;
      --accent: #10B981;
      --bg: #ffffff;
      --text: #111827;
      --muted: #6B7280;
      --border: #E5E7EB;
      --shadow: 0 12px 30px rgba(0,0,0,0.15);
      --radius: 14px;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 2147483000;
    }

    /* Floating bubble */
    #cbw-bubble {
      position: absolute;
      bottom: 0;
      right: 0;
      width: 56px;
      height: 56px;
      border-radius: 999px;
      display: grid;
      place-items: center;
      background: var(--primary);
      color: white;
      border: none;
      cursor: pointer;
      box-shadow: var(--shadow);
      transition: transform .12s ease, box-shadow .12s ease, background .2s ease;
    }
    #cbw-bubble:hover { transform: translateY(-2px); box-shadow: 0 16px 36px rgba(0,0,0,0.2); }
    #cbw-bubble:focus-visible { outline: 3px solid rgba(91,108,255,.5); outline-offset: 2px; }

    /* Panel */
    #cbw-panel {
      position: absolute;
      bottom: 72px;
      right: 0;
      width: 360px;
      height: 480px;
      max-height: calc(100vh - 96px);
      display: none;
      background: var(--bg);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow: hidden;
    }
    #cbw-panel[aria-hidden="false"] { display: grid; grid-template-rows: auto 1fr auto; }

    /* Header */
    #cbw-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      background: linear-gradient(0deg, #ffffff, #F9FAFB);
    }
    #cbw-title {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
    }
    #cbw-status {
      font-size: 12px;
      color: var(--muted);
    }
    #cbw-close {
      background: transparent;
      border: none;
      color: var(--muted);
      font-size: 18px;
      width: 32px;
      height: 32px;
      border-radius: 8px;
      cursor: pointer;
    }
    #cbw-close:hover, #cbw-close:focus-visible {
      background: #EEF2FF;
      color: var(--primary);
      outline: none;
    }

    /* Messages area */
    #cbw-messages {
      padding: 12px;
      overflow: auto;
      background: #FAFAFB;
    }
    .cbw-msg {
      max-width: 85%;
      padding: 10px 12px;
      border-radius: 12px;
      margin: 6px 0;
      line-height: 1.35;
      white-space: pre-wrap;
      word-wrap: break-word;
    }
    .cbw-user   { background: #E8ECFF; color: #1F2937; margin-left: auto; border-bottom-right-radius: 6px; }
    .cbw-bot    { background: #FFFFFF; border: 1px solid var(--border); color: #111827; margin-right: auto; border-bottom-left-radius: 6px; }
    .cbw-error  { background: #FEF2F2; color: #991B1B; border: 1px solid #FECACA; }
    .cbw-chip   { display:inline-flex; align-items:center; gap:6px; font-size:12px; color: var(--muted); }

    /* Typing indicator */
    #cbw-typing { display: none; margin: 6px 0; }
    #cbw-typing[data-active="true"] { display: inline-flex; }
    .cbw-dots { display: inline-flex; gap: 4px; margin-left: 6px; }
    .cbw-dot { width:6px; height:6px; border-radius:999px; background:#D1D5DB; animation: cbw-pulse 1s infinite ease-in-out; }
    .cbw-dot:nth-child(2){ animation-delay: .15s; } .cbw-dot:nth-child(3){ animation-delay: .3s; }
    @keyframes cbw-pulse { 0%, 80%, 100% { opacity:.3; transform: translateY(0); } 40% { opacity:1; transform: translateY(-2px); } }

    /* Composer */
    #cbw-composer {
      border-top: 1px solid var(--border);
      padding: 10px;
      background: #FFFFFF;
      display: grid;
      grid-template-columns: 1fr auto;
      grid-template-rows: auto auto;
      gap: 8px;
    }
    #cbw-label { grid-column: 1 / -1; font-size: 12px; color: var(--muted); }
    #cbw-input {
      width: 100%;
      resize: none;
      min-height: 40px;
      max-height: 120px;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid var(--border);
      font: inherit;
      line-height: 1.35;
      outline: none;
    }
    #cbw-input:focus-visible { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(91,108,255,0.2); }
    #cbw-send {
      align-self: end;
      height: 40px;
      padding: 0 14px;
      background: var(--primary);
      color: white;
      border: none;
      border-radius: 10px;
      font-weight: 600;
      cursor: pointer;
    }
    #cbw-send[disabled] { background: #A5B4FC; cursor: not-allowed; }
    #cbw-send:hover:not([disabled]) { filter: brightness(0.98); }

    /* Mobile */
    @media (max-width: 480px) {
      #cbw-panel {
        right: 0;
        bottom: 72px;
        width: calc(100vw - 24px);
        left: 12px;
        height: 60vh;
      }
    }
  </style>

  <!-- Floating Bubble -->
  <button id="cbw-bubble" aria-label="Open chat" aria-controls="cbw-panel" title="Chat with us">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M4 19.5V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H8l-4 2.5Z" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </button>

  <!-- Panel -->
  <section id="cbw-panel" role="dialog" aria-modal="true" aria-labelledby="cbw-header-title" aria-hidden="true">
    <header id="cbw-header">
      <div id="cbw-title">
        <span style="display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:999px;background:var(--primary);color:white;">🤖</span>
        <div>
          <div id="cbw-header-title">Buddy</div>
          <div id="cbw-status" aria-live="polite">Online</div>
        </div>
      </div>
      <button id="cbw-close" aria-label="Close chat" title="Close chat">✕</button>
    </header>

    <main id="cbw-messages" role="log" aria-live="polite" aria-relevant="additions" tabindex="0">
      <div class="cbw-msg cbw-bot">
        Hi! I’m Buddy. Ask me anything about your trip. I’ll help plan, suggest, and book insights for you.
      </div>
      <div id="cbw-typing" class="cbw-msg cbw-bot" aria-hidden="true">
        <span class="cbw-chip">Buddy is typing</span>
        <span class="cbw-dots" aria-hidden="true">
          <span class="cbw-dot"></span><span class="cbw-dot"></span><span class="cbw-dot"></span>
        </span>
      </div>
    </main>

    <form id="cbw-composer" aria-describedby="cbw-label">
      <label id="cbw-label" for="cbw-input">Message Buddy</label>
      <textarea id="cbw-input" name="message" rows="2" placeholder="Type a message..." aria-label="Type your message"></textarea>
      <button id="cbw-send" type="submit" aria-label="Send message">Send</button>
    </form>
  </section>

  <script>
    (function () {
      const root     = document.getElementById('chatbot-widget');
      const bubble   = root.querySelector('#cbw-bubble');
      const panel    = root.querySelector('#cbw-panel');
      const closeBtn = root.querySelector('#cbw-close');
      const messages = root.querySelector('#cbw-messages');
      const typingEl = root.querySelector('#cbw-typing');
      const form     = root.querySelector('#cbw-composer');
      const input    = root.querySelector('#cbw-input');
      const sendBtn  = root.querySelector('#cbw-send');

      const state = {
        isOpen: false,
        isStreaming: false,
        sessionId: null,
        messages: [] // {role:'user'|'assistant'|'error', content:string}
      };

      function scrollToBottom() {
        messages.scrollTop = messages.scrollHeight;
      }

      function showTyping(active) {
        typingEl.setAttribute('data-active', active ? 'true' : 'false');
        typingEl.setAttribute('aria-hidden', active ? 'false' : 'true');
        if (active) scrollToBottom();
      }

      function appendMessage(role, content) {
        const div = document.createElement('div');
        div.className = 'cbw-msg ' + (role === 'user' ? 'cbw-user' : role === 'assistant' ? 'cbw-bot' : 'cbw-error');
        div.textContent = content || '';
        messages.appendChild(div);
        scrollToBottom();
        return div;
      }

      function updateMessage(node, content) {
        node.textContent = content;
        scrollToBottom();
      }

      function setOpen(open) {
        state.isOpen = open;
        panel.setAttribute('aria-hidden', open ? 'false' : 'true');
        if (open) {
          // Focus trap: focus input
          setTimeout(() => input.focus(), 0);
        } else {
          bubble.focus();
        }
      }

      function focusTrap(e) {
        if (panel.getAttribute('aria-hidden') === 'true') return;
        if (e.key !== 'Tab') return;
        const focusable = panel.querySelectorAll('button, [href], input, textarea, select, [tabindex]:not([tabindex="-1"])');
        if (!focusable.length) return;
        const first = focusable[0];
        const last  = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          last.focus(); e.preventDefault();
        } else if (!e.shiftKey && document.activeElement === last) {
          first.focus(); e.preventDefault();
        }
      }

      async function streamAssistant(userText) {
        showTyping(true);
        state.isStreaming = true;

        // create assistant bubble to stream into
        const assistantNode = appendMessage('assistant', '');

        let buffer = '';
        try {
          const res = await fetch('http://127.0.0.1:8787/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              sessionId: state.sessionId || undefined,
              messages: state.messages.concat([{ role: 'user', content: userText }])
            })
          });
          if (!res.ok || !res.body) throw new Error('Network error');

          const reader = res.body.getReader();
          const decoder = new TextDecoder();
          let done = false;
          while (!done) {
            const chunk = await reader.read();
            done = chunk.done;
            if (chunk.value) {
              buffer += decoder.decode(chunk.value, { stream: true });
              let idx;
              while ((idx = buffer.indexOf('\n')) !== -1) {
                const line = buffer.slice(0, idx).trim();
                buffer = buffer.slice(idx + 1);
                if (!line) continue;
                // Expect lines like: data: {"delta":"...", "done":false}
                const prefix = 'data:';
                if (line.startsWith(prefix)) {
                  const payloadRaw = line.slice(prefix.length).trim();
                  try {
                    const json = JSON.parse(payloadRaw);
                    if (json.delta) {
                      assistantNode.textContent += json.delta;
                      scrollToBottom();
                    }
                    if (json.done === true) {
                      // finalize
                      state.messages.push({ role: 'assistant', content: assistantNode.textContent });
                    }
                  } catch (_) {
                    // Ignore malformed lines
                  }
                }
              }
            }
          }
        } catch (err) {
          assistantNode.classList.add('cbw-error');
          updateMessage(assistantNode, 'Sorry, something went wrong. Please try again.');
        } finally {
          showTyping(false);
          state.isStreaming = false;
        }
      }

      async function handleSend(text) {
        const userText = (text ?? input.value).trim();
        if (!userText || state.isStreaming) return;

        // Add user message
        appendMessage('user', userText);
        state.messages.push({ role: 'user', content: userText });
        input.value = '';
        input.style.height = 'auto';

        // Stream assistant
        await streamAssistant(userText);
      }

      // Public API
      window.startChat = function startChat(sessionId) {
        state.sessionId = sessionId || null;
        setOpen(true);
      };
      window.sendMessage = function sendMessage(text) {
        if (!state.isOpen) setOpen(true);
        handleSend(text);
      };

      // UI wiring
      bubble.addEventListener('click', () => setOpen(true));
      closeBtn.addEventListener('click', () => setOpen(false));
      document.addEventListener('keydown', (e) => {
        if (panel.getAttribute('aria-hidden') === 'false' && e.key === 'Escape') setOpen(false);
        focusTrap(e);
      });

      // Compose: Enter to send, Shift+Enter for newline
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          handleSend();
        }
      });

      // Auto-resize textarea
      input.addEventListener('input', () => {
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 120) + 'px';
      });

      // Form submit
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        handleSend();
      });
    })();
  </script>
</div>
""", height=120, scrolling=False)