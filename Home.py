import streamlit as st


st.set_page_config(
    page_title="DSA Visualizer",
    layout="wide"
)


st.markdown("""
<style>

/* Main background */
.main {
    background: linear-gradient(135deg, #0f1117, #0b0c10);
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1c23, #0f1117);
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* Sidebar title */
.sidebar-title {
    font-size: 22px;
    font-weight: 600;
    color: #00ffcc;
    margin-bottom: 25px;
}

/* Radio group spacing */
div[role="radiogroup"] {
    gap: 12px;
}

/* Navigation items */
div[role="radio"] {
    background: rgba(255,255,255,0.04);
    padding: 12px 16px;
    border-radius: 12px;
    transition: all 0.25s ease;
    border: 1px solid transparent;
}

/* Hover */
div[role="radio"]:hover {
    background: rgba(0,255,204,0.12);
    border: 1px solid rgba(0,255,204,0.3);
    transform: translateX(6px);
}

/* Active */
div[aria-checked="true"] {
    background: linear-gradient(90deg, #00ffcc, #00b3ff);
    color: black !important;
    font-weight: 600;
}

/* Remove default radio circle */
div[role="radio"] > div:first-child {
    display: none;
}

/* Text */
div[role="radio"] p {
    font-size: 15px;
    margin: 0;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    transition: 0.2s;
}

.card:hover {
    background: rgba(0,255,204,0.1);
    transform: scale(1.02);
}

/* Titles */
.main-title {
    font-size: 32px;
    font-weight: 600;
    color: #ffb347;
    margin-left: 100px;
}

.section-title {
    font-size: 22px;
    color: #00ffcc;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)


with st.sidebar:

    st.markdown('<div class="sidebar-title">⚡ Data Structure Visualizer</div>', unsafe_allow_html=True)

    page = st.radio(
        "",
        [
            "🏠 Home",
            "📊 Arrays",
            "🔗 Linked Lists",
            "📚 Stacks",
            "➡️ Queue",
            "🕷️ Web Crawler(BFS)"
        ]
    )
    if page == "📊 Arrays":
        st.switch_page("pages/Array.py")

    if page == "🔗 Linked Lists":
        st.switch_page("pages/Linked_List.py")

    if page == "📚 Stacks":
        st.switch_page("pages/Stack.py")

    if page == "➡️ Queue":
        st.switch_page("pages/Queue.py")

    if page == "🕷️ Web Crawler(BFS)":
        st.switch_page("pages/Web_Crawler.py")

    st.markdown("---")
    st.caption("Interactive Learning Interface")


if page == "🏠 Home":

    col1, col2, col3 = st.columns([1,2,1])

    with col1:
        st.image("central_university_jammu_logo.png", width=200)

    with col2:
        st.markdown("<h2 style='margin-left: 100px; font-weight: 900; color:#ff2a00; display: flex; align-items: flex-end; vertical-align:bottom; height: 50px;'>Central University of Jammu</h2>", unsafe_allow_html=True)
        st.markdown('<div class="main-title">DATA STRUCTURE VISUALIZER</div>', unsafe_allow_html=True)

    st.markdown("### Learn Data Structures through interactive visualization")

    st.markdown('<div class="section-title">👥 Contributors</div>', unsafe_allow_html=True)

    contributors = [
        "Dr. Dinesh Kumar (Mentor)",
        "Antriksh Baskotra(Array)",
        "Arun Kumar(Linked List)",
        "Saksham Dubey(Stack)",
        "Sidharth Sharma(Queue)"
    ]

    for c in contributors:
        st.markdown(f'<div class="card">{c}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">⚠️ Instructions</div>', unsafe_allow_html=True)

    st.warning("Use the sidebar to navigate between visualizers.")
    st.info("Click the top-left icon to toggle the sidebar.")

# ARRAYS PAGE
elif page == "📊 Arrays":
    st.title("📊 Array Visualizer")

    try:
        import array
    except:
        st.info("array.py not connected yet")

# LINKED LIST PAGE
elif page == "🔗 Linked Lists":
    st.title("🔗 Linked List Visualizer")

    try:
        import linked_list
    except:
        st.info("Rename 'linked list.py' → 'linked_list.py'")

# STACK PAGE
elif page == "📚 Stacks":
    st.title("📚 Stack Visualizer")

    try:
        import stack
    except:
        st.info("stack.py not connected yet")