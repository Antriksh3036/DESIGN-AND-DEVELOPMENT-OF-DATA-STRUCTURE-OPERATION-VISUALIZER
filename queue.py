import streamlit as st
import subprocess
import tempfile
import os

st.set_page_config(page_title="Data Structure : Queue", layout="wide")
MAX_SIZE = 6

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #fafafa; }
    .stSidebar, [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 2px solid #58a6ff !important; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #c9d1d9 !important; }
    [data-testid="stSidebar"] .stRadio label { color: #c9d1d9 !important; font-weight: 500; }
    [data-testid="stSidebar"] .stRadio label:hover { color: #58a6ff !important; }
    [data-testid="stSidebar"] .stRadio [role="radiogroup"] label[data-checked="true"] { color: #58a6ff !important; font-weight: 700; }
    header[data-testid="stHeader"] { background-color: #0e1117 !important; }
    .stButton > button { background-color: #21262d !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
    .stButton > button:hover { background-color: #30363d !important; border-color: #58a6ff !important; }
    .highlight-code { background-color: #ffff00; color: black; padding: 5px; border-radius: 5px; font-weight: bold; }

    .backend-panel { background: #161b22; border: 1px solid #30363d; border-radius: 8px; font-family: 'Courier New', monospace; overflow: hidden; margin-bottom: 16px; }
    .backend-header { background: #21262d; padding: 10px 16px; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid #30363d; }
    .backend-header-title { color: #8b949e; font-size: 13px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }
    .backend-body { padding: 16px 18px; font-size: 12.5px; line-height: 1.8; max-height: 600px; overflow-y: auto; color: #c9d1d9; }
    .step-num { display: inline-block; background: #58a6ff; color: #0e1117; font-size: 10px; font-weight: 700; padding: 1px 7px; border-radius: 4px; margin-right: 8px; }
    .step-action { color: #c9d1d9; font-weight: 600; }
    .step-detail { color: #8b949e; font-style: italic; margin-left: 36px; display: block; }
    .step-success { color: #3fb950; font-weight: 700; }
    .step-error { color: #f85149; font-weight: 700; }
    .step-warn { color: #d29922; font-weight: 600; }
    .step-divider { border: none; border-top: 1px dashed #30363d; margin: 10px 0; }
    .state-box { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 10px 14px; margin: 8px 0 4px 0; color: #8b949e; font-size: 12px; }
    .state-label { color: #58a6ff; font-weight: 700; margin-right: 6px; }

    .q-cell { text-align: center; padding: 14px 10px; border-radius: 8px; font-family: 'Courier New', monospace; font-weight: 700; font-size: 18px; min-width: 60px; display: inline-block; margin: 0 4px; }
    .q-front-rear { background: #1f6feb; color: #fff; border: 2px solid #58a6ff; }
    .q-front { background: #238636; color: #fff; border: 2px solid #3fb950; }
    .q-rear { background: #8957e5; color: #fff; border: 2px solid #bc8cff; }
    .q-mid { background: #21262d; color: #c9d1d9; border: 2px solid #30363d; }
    .q-empty-slot { background: #0d1117; color: #484f58; border: 2px dashed #30363d; }
    .q-label { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; margin-top: 6px; color: #8b949e; }
    .queue-container { display: flex; align-items: flex-end; gap: 6px; padding: 20px 0; overflow-x: auto; }
    .queue-arrow { color: #58a6ff; font-size: 22px; display: flex; align-items: center; padding-bottom: 26px; }

    .stCodeBlock, pre, code { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
    .stCodeBlock code span { color: #c9d1d9 !important; }
    code .token.keyword, code .hljs-keyword, code .hljs-type { color: #ff7b72 !important; }
    code .token.function, code .hljs-title { color: #d2a8ff !important; }
    code .token.string, code .hljs-string { color: #a5d6ff !important; }
    code .token.number, code .hljs-number { color: #79c0ff !important; }
    code .token.comment, code .hljs-comment { color: #8b949e !important; }
    code .token.preprocessor, code .hljs-meta { color: #f85149 !important; }
</style>
""", unsafe_allow_html=True)

if 'queue_data' not in st.session_state:
    st.session_state['queue_data'] = []
if 'element_counter' not in st.session_state:
    st.session_state['element_counter'] = 1
if 'front' not in st.session_state:
    st.session_state['front'] = -1
if 'rear' not in st.session_state:
    st.session_state['rear'] = -1
if 'op_log' not in st.session_state:
    st.session_state['op_log'] = []

def _log_step(num, action, detail=None, kind="normal"):
    cls = {"normal": "step-action", "success": "step-success", "error": "step-error", "warn": "step-warn"}.get(kind, "step-action")
    html = f'<span class="step-num">{num}</span><span class="{cls}">{action}</span>'
    if detail:
        html += f'<span class="step-detail">{detail}</span>'
    st.session_state['op_log'].append(html)

def _log_divider():
    st.session_state['op_log'].append('<hr class="step-divider">')

def _log_state():
    q = st.session_state['queue_data']
    f = st.session_state['front']
    r = st.session_state['rear']
    items = ", ".join(str(v) for v in q) if q else "(empty)"
    st.session_state['op_log'].append(
        f'<div class="state-box"><span class="state-label">front</span>= {f} &nbsp;&nbsp; '
        f'<span class="state-label">rear</span>= {r} &nbsp;&nbsp; '
        f'<span class="state-label">items</span>= [ {items} ]</div>'
    )

def enqueue():
    val = st.session_state['element_counter']
    st.session_state['op_log'] = []
    _log_step(1, f"ENQUEUE({val})  — operation starts")
    _log_step(2, "Check overflow: rear == MAX-1 ?", f"rear = {st.session_state['rear']}, MAX-1 = {MAX_SIZE - 1}")
    if st.session_state['rear'] == MAX_SIZE - 1:
        _log_step(3, "Queue Overflow! Cannot insert.", kind="error")
        _log_state()
        return
    _log_step(3, "No overflow, proceed.", kind="success")
    if st.session_state['front'] == -1:
        st.session_state['front'] = 0
        _log_step(4, "Queue was empty, set front = 0", kind="warn")
    else:
        _log_step(4, "Queue not empty, front unchanged.")
    st.session_state['rear'] += 1
    _log_step(5, f"rear++ = {st.session_state['rear']}")
    st.session_state['queue_data'].append(val)
    _log_step(6, f"items[{st.session_state['rear']}] = {val}")
    st.session_state['element_counter'] += 1
    _log_step(7, f"Enqueue complete, {val} inserted.", kind="success")
    _log_divider()
    _log_state()

def dequeue():
    st.session_state['op_log'] = []
    _log_step(1, "DEQUEUE() — operation starts")
    if st.session_state['front'] == -1:
        _log_step(2, "Queue Underflow! Nothing to remove.", kind="error")
        _log_state()
        return
    removed = st.session_state['queue_data'].pop(0)
    _log_step(2, f"Removed items[{st.session_state['front']}] = {removed}")
    st.session_state['front'] += 1
    _log_step(3, f"front++ = {st.session_state['front']}")
    if st.session_state['front'] > st.session_state['rear']:
        st.session_state['front'] = -1
        st.session_state['rear'] = -1
        _log_step(4, "Queue empty, reset front = rear = -1", kind="warn")
    else:
        _log_step(4, "Queue still has elements.", kind="success")
    _log_step(5, f"Dequeue complete, {removed} removed.", kind="success")
    _log_divider()
    _log_state()

def display():
    st.session_state['op_log'] = []
    _log_step(1, "DISPLAY() — operation starts")
    if st.session_state['rear'] == -1:
        _log_step(2, "Queue is empty.", kind="warn")
        _log_state()
        return
    for idx, val in enumerate(st.session_state['queue_data']):
        _log_step(2 + idx, f"items[{st.session_state['front'] + idx}] = {val}")
    _log_step(2 + len(st.session_state['queue_data']), f"Display complete.", kind="success")
    _log_divider()
    _log_state()

def reset():
    st.session_state['queue_data'] = []
    st.session_state['element_counter'] = 1
    st.session_state['front'] = -1
    st.session_state['rear'] = -1
    st.session_state['op_log'] = []
    _log_step(1, "RESET — queue cleared", kind="warn")
    _log_state()

# Sidebar
page = st.sidebar.radio("Go to", [" Theory", " Visualizer"])

# Theory
if page == " Theory":
    st.title("Queue Data Structure")
    st.markdown("""
    ### What is a Queue?
    A **Queue** is a linear data structure that follows a particular order in which operations are performed.
    The order is **FIFO (First In First Out)**. The element that is inserted first comes out first.
    It is an abstract data type with two main operations:
    * **Enqueue**: Adds an element to the rear of the queue.
    * **Dequeue**: Removes an element from the front of the queue.
    * Other queue operations include:
    * **Peek/Front**: Returns the front element without removing it.
    """)

    st.info("The order in which elements come out of a queue gives rise to its alternative name, **FIFO** (first in, first out).")

    with st.expander("See Real-world Relation"):
        st.write("Think of a queue at a ticket counter. The first person in line is the first to be served. New arrivals join at the **rear**, and service happens at the **front**.")

    st.divider()
    st.subheader("C Code Implementation")

    c_code = """\
#include <stdio.h>
#define MAX 5

int items[MAX];
int front = -1, rear = -1;

void enqueue(int value) {
    if (rear == MAX - 1)
        printf("Queue Overflow\\n");
    else {
        if (front == -1)
            front = 0;
        rear++;
        items[rear] = value;
        printf("Inserted -> %d\\n", value);
    }
}

void dequeue() {
    if (front == -1)
        printf("Queue Underflow\\n");
    else {
        printf("Deleted -> %d\\n", items[front]);
        front++;
        if (front > rear)
            front = rear = -1;
    }
}

void display() {
    if (rear == -1)
        printf("Queue is empty\\n");
    else {
        int i;
        printf("Queue elements are:\\n");
        for (i = front; i <= rear; i++)
            printf("%d ", items[i]);
        printf("\\n");
    }
}

int main() {
    enqueue(10);
    enqueue(20);
    enqueue(30);
    display();
    dequeue();
    display();
    return 0;
}
"""
    st.code(c_code, language='c')

    if st.button("Run Code", use_container_width=True):
        with st.spinner("Compiling & running..."):
            try:
                tmp_dir = tempfile.mkdtemp()
                src = os.path.join(tmp_dir, "queue.c")
                exe = os.path.join(tmp_dir, "queue.exe")
                with open(src, "w") as f:
                    f.write(c_code)
                comp = subprocess.run(["gcc", src, "-o", exe], capture_output=True, text=True, timeout=15)
                if comp.returncode != 0:
                    st.error("Compilation failed!")
                    st.code(comp.stderr)
                else:
                    run = subprocess.run([exe], capture_output=True, text=True, timeout=10)
                    st.success("Compiled and ran successfully!")
                    st.code(run.stdout if run.stdout else "(no output)")
            except FileNotFoundError:
                st.error("GCC compiler not found. Install MinGW / GCC to compile C code.")
            except subprocess.TimeoutExpired:
                st.error("Process timed out.")
            except Exception as e:
                st.error(f"Error: {e}")

# Visualizer
elif page == " Visualizer":
    st.title("Interactive Queue Visualization")
    st.caption("Each operation is broken into micro-steps so you can see exactly what happens inside the queue.")

    c1, c2, c3, c4 = st.columns(4)
    btn_enqueue = c1.button("Enqueue", use_container_width=True)
    btn_dequeue = c2.button("Dequeue", use_container_width=True)
    btn_display = c3.button("Display", use_container_width=True)
    btn_reset = c4.button("Reset", use_container_width=True)

    if btn_enqueue: enqueue()
    elif btn_dequeue: dequeue()
    elif btn_display: display()
    elif btn_reset: reset()

    col_vis, col_backend = st.columns([3, 2])

    with col_vis:
        st.markdown("#### Current Queue State")
        q = st.session_state['queue_data']
        front = st.session_state['front']
        rear = st.session_state['rear']

        cells_html = ""
        for i in range(MAX_SIZE):
            if i < len(q):
                val = q[i]
                if len(q) == 1:
                    cls, label = "q-front-rear", "Front & Rear"
                elif i == 0:
                    cls, label = "q-front", "Front"
                elif i == len(q) - 1:
                    cls, label = "q-rear", "Rear"
                else:
                    cls, label = "q-mid", f"[ {front + i} ]"
                cells_html += f'<div class="q-cell {cls}">{val}<div class="q-label">{label}</div></div>'
            else:
                cells_html += f'<div class="q-cell q-empty-slot">—<div class="q-label">[ {i} ]</div></div>'
            if i < MAX_SIZE - 1:
                cells_html += '<div class="queue-arrow">→</div>'

        st.markdown(f'<div class="queue-container">{cells_html}</div>', unsafe_allow_html=True)

        if not q:
            st.info("Queue is **empty**  ·  front = -1  ·  rear = -1")
        else:
            st.markdown(f"**Elements:** {len(q)} / {MAX_SIZE} | **front** = {front} | **rear** = {rear}")

    with col_backend:
        st.markdown("#### Backend Output")
        log = st.session_state.get('op_log', [])
        if not log:
            body = '<span style="color:#8b949e;">No operation executed yet. Click a button above.</span>'
        else:
            body = "<br>".join(log)
        st.markdown(f"""
        <div class="backend-panel">
            <div class="backend-header">
                <span class="backend-header-title">Execution Trace</span>
            </div>
            <div class="backend-body">{body}</div>
        </div>
        """, unsafe_allow_html=True)