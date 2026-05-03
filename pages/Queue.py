import streamlit as st
import subprocess
import tempfile
import os

st.set_page_config(page_title="Data Structure : Queue & Circular Queue", layout="wide")
DEFAULT_SIZE = 6

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

    .cq-ring { position: relative; width: 340px; height: 340px; margin: 20px auto; }
    .cq-node { position: absolute; width: 62px; height: 62px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: 'Courier New', monospace; font-weight: 700; font-size: 16px; transition: all 0.3s ease; }
    .cq-node-empty { background: #0d1117; color: #484f58; border: 2px dashed #30363d; }
    .cq-node-front-rear { background: linear-gradient(135deg, #238636, #8957e5); color: #fff; border: 2px solid #58a6ff; box-shadow: 0 0 14px rgba(88,166,255,0.5); }
    .cq-node-front { background: #238636; color: #fff; border: 2px solid #3fb950; box-shadow: 0 0 10px rgba(63,185,80,0.4); }
    .cq-node-rear { background: #8957e5; color: #fff; border: 2px solid #bc8cff; box-shadow: 0 0 10px rgba(137,87,229,0.4); }
    .cq-node-mid { background: #21262d; color: #c9d1d9; border: 2px solid #30363d; }
    .cq-node-label { font-size: 8px; text-transform: uppercase; letter-spacing: 1px; color: #8b949e; margin-top: 2px; }
    .cq-center-label { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; color: #8b949e; font-size: 12px; font-family: 'Courier New', monospace; }

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

if 'q_size' not in st.session_state:
    st.session_state['q_size'] = DEFAULT_SIZE
if 'queue_data' not in st.session_state:
    st.session_state['queue_data'] = []
if 'front' not in st.session_state:
    st.session_state['front'] = -1
if 'rear' not in st.session_state:
    st.session_state['rear'] = -1
if 'op_log' not in st.session_state:
    st.session_state['op_log'] = []

# Circular Queue state
if 'cq_size' not in st.session_state:
    st.session_state['cq_size'] = DEFAULT_SIZE
if 'cq_data' not in st.session_state:
    st.session_state['cq_data'] = [None] * st.session_state['cq_size']
if 'cq_front' not in st.session_state:
    st.session_state['cq_front'] = -1
if 'cq_rear' not in st.session_state:
    st.session_state['cq_rear'] = -1
if 'cq_count' not in st.session_state:
    st.session_state['cq_count'] = 0
if 'cq_log' not in st.session_state:
    st.session_state['cq_log'] = []

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

def enqueue(val):
    max_sz = st.session_state['q_size']
    st.session_state['op_log'] = []
    _log_step(1, f"ENQUEUE({val})  — operation starts")
    _log_step(2, "Check overflow: rear == MAX-1 ?", f"rear = {st.session_state['rear']}, MAX-1 = {max_sz - 1}")
    if st.session_state['rear'] == max_sz - 1:
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
    st.session_state['front'] = -1
    st.session_state['rear'] = -1
    st.session_state['op_log'] = []
    _log_step(1, "RESET — queue cleared", kind="warn")
    _log_state()

# ───── Circular Queue operations ─────
def _cq_log_step(num, action, detail=None, kind="normal"):
    cls = {"normal": "step-action", "success": "step-success", "error": "step-error", "warn": "step-warn"}.get(kind, "step-action")
    html = f'<span class="step-num">{num}</span><span class="{cls}">{action}</span>'
    if detail:
        html += f'<span class="step-detail">{detail}</span>'
    st.session_state['cq_log'].append(html)

def _cq_log_divider():
    st.session_state['cq_log'].append('<hr class="step-divider">')

def _cq_log_state():
    max_sz = st.session_state['cq_size']
    f = st.session_state['cq_front']
    r = st.session_state['cq_rear']
    cnt = st.session_state['cq_count']
    items_str = ", ".join(str(v) for v in st.session_state['cq_data'] if v is not None) if cnt > 0 else "(empty)"
    st.session_state['cq_log'].append(
        f'<div class="state-box"><span class="state-label">front</span>= {f} &nbsp;&nbsp; '
        f'<span class="state-label">rear</span>= {r} &nbsp;&nbsp; '
        f'<span class="state-label">count</span>= {cnt}/{max_sz} &nbsp;&nbsp; '
        f'<span class="state-label">items</span>= [ {items_str} ]</div>'
    )

def cq_enqueue(val):
    max_sz = st.session_state['cq_size']
    st.session_state['cq_log'] = []
    _cq_log_step(1, f"CQ_ENQUEUE({val}) — operation starts")
    _cq_log_step(2, "Check full: count == MAX ?", f"count = {st.session_state['cq_count']}, MAX = {max_sz}")
    if st.session_state['cq_count'] == max_sz:
        _cq_log_step(3, "Circular Queue is FULL! Cannot insert.", kind="error")
        _cq_log_state()
        return
    _cq_log_step(3, "Not full, proceed.", kind="success")
    if st.session_state['cq_front'] == -1:
        st.session_state['cq_front'] = 0
        _cq_log_step(4, "Queue was empty, set front = 0", kind="warn")
    else:
        _cq_log_step(4, "Queue not empty, front unchanged.")
    st.session_state['cq_rear'] = (st.session_state['cq_rear'] + 1) % max_sz
    _cq_log_step(5, f"rear = (rear + 1) % MAX = {st.session_state['cq_rear']}")
    st.session_state['cq_data'][st.session_state['cq_rear']] = val
    st.session_state['cq_count'] += 1
    _cq_log_step(6, f"items[{st.session_state['cq_rear']}] = {val}")
    _cq_log_step(7, f"Enqueue complete. {val} inserted.", kind="success")
    _cq_log_divider()
    _cq_log_state()

def cq_dequeue():
    max_sz = st.session_state['cq_size']
    st.session_state['cq_log'] = []
    _cq_log_step(1, "CQ_DEQUEUE() — operation starts")
    if st.session_state['cq_count'] == 0:
        _cq_log_step(2, "Circular Queue Underflow! Nothing to remove.", kind="error")
        _cq_log_state()
        return
    removed = st.session_state['cq_data'][st.session_state['cq_front']]
    _cq_log_step(2, f"Removed items[{st.session_state['cq_front']}] = {removed}")
    st.session_state['cq_data'][st.session_state['cq_front']] = None
    st.session_state['cq_count'] -= 1
    if st.session_state['cq_count'] == 0:
        st.session_state['cq_front'] = -1
        st.session_state['cq_rear'] = -1
        _cq_log_step(3, "Queue now empty, reset front = rear = -1", kind="warn")
    else:
        st.session_state['cq_front'] = (st.session_state['cq_front'] + 1) % max_sz
        _cq_log_step(3, f"front = (front + 1) % MAX = {st.session_state['cq_front']}")
    _cq_log_step(4, f"Dequeue complete. {removed} removed.", kind="success")
    _cq_log_divider()
    _cq_log_state()

def cq_display():
    max_sz = st.session_state['cq_size']
    st.session_state['cq_log'] = []
    _cq_log_step(1, "CQ_DISPLAY() — operation starts")
    if st.session_state['cq_count'] == 0:
        _cq_log_step(2, "Circular Queue is empty.", kind="warn")
        _cq_log_state()
        return
    idx = st.session_state['cq_front']
    for i in range(st.session_state['cq_count']):
        _cq_log_step(2 + i, f"items[{idx}] = {st.session_state['cq_data'][idx]}")
        idx = (idx + 1) % max_sz
    _cq_log_step(2 + st.session_state['cq_count'], "Display complete.", kind="success")
    _cq_log_divider()
    _cq_log_state()

def cq_reset():
    max_sz = st.session_state['cq_size']
    st.session_state['cq_data'] = [None] * max_sz
    st.session_state['cq_front'] = -1
    st.session_state['cq_rear'] = -1
    st.session_state['cq_count'] = 0
    st.session_state['cq_log'] = []
    _cq_log_step(1, "RESET — circular queue cleared", kind="warn")
    _cq_log_state()

# Sidebar
page = st.sidebar.radio("Go to", [" Queue Theory", " Queue Visualizer", " Circular Queue Theory", " Circular Queue Visualizer"])

# Theory
if page == " Queue Theory":
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
elif page == " Queue Visualizer":
    st.title("Interactive Queue Visualization")
    st.caption("Each operation is broken into micro-steps so you can see exactly what happens inside the queue.")

    # Queue size selector
    def _on_q_size_change():
        new_size = st.session_state['q_size_slider']
        st.session_state['q_size'] = new_size
        st.session_state['queue_data'] = []
        st.session_state['front'] = -1
        st.session_state['rear'] = -1
        st.session_state['op_log'] = []

    q_size = st.slider("Queue Size (MAX)", min_value=3, max_value=10, value=st.session_state['q_size'], key="q_size_slider", on_change=_on_q_size_change)
    st.session_state['q_size'] = q_size

    enqueue_val = st.number_input("Enter value to enqueue", value=0, step=1, key="enqueue_input")

    c1, c2, c3, c4 = st.columns(4)
    btn_enqueue = c1.button("Enqueue", use_container_width=True)
    btn_dequeue = c2.button("Dequeue", use_container_width=True)
    btn_display = c3.button("Display", use_container_width=True)
    btn_reset = c4.button("Reset", use_container_width=True)

    if btn_enqueue: enqueue(enqueue_val)
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
        q_max = st.session_state['q_size']
        for i in range(q_max):
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
            if i < q_max - 1:
                cells_html += '<div class="queue-arrow">→</div>'

        st.markdown(f'<div class="queue-container">{cells_html}</div>', unsafe_allow_html=True)

        if not q:
            st.info("Queue is **empty**  ·  front = -1  ·  rear = -1")
        else:
            st.markdown(f"**Elements:** {len(q)} / {q_max} | **front** = {front} | **rear** = {rear}")

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

# ───── Circular Queue Theory ─────
elif page == " Circular Queue Theory":
    st.title("Circular Queue Data Structure")
    st.markdown("""
    ### What is a Circular Queue?
    A **Circular Queue** is a linear data structure that follows **FIFO** but the last position is connected
    back to the first position to make a circle. It is also called a **Ring Buffer**.

    **Key advantage:** In a simple linear queue, once the queue is full and elements are dequeued, the spaces
    at the front cannot be reused. A circular queue **reuses** those empty spaces by wrapping around.

    * **Enqueue**: Inserts at `(rear + 1) % MAX`.
    * **Dequeue**: Removes from `front`, then `front = (front + 1) % MAX`.
    * **Full condition**: `count == MAX`.
    * **Empty condition**: `count == 0` (or `front == -1`).
    """)

    st.info("The circular queue is widely used in **CPU scheduling**, **memory management**, and **buffering** (e.g., streaming data buffers).")

    with st.expander("See Real-world Relation"):
        st.write("Imagine a revolving door — people enter and exit in order, and the door keeps rotating. "
                 "Once a slot is vacated, the next person can use it. That's how a circular queue reuses space!")

    st.divider()
    st.subheader("C Code Implementation")

    cq_c_code = """\
#include <stdio.h>
#define MAX 5

int items[MAX];
int front = -1, rear = -1, count = 0;

void enqueue(int value) {
    if (count == MAX) {
        printf("Circular Queue Overflow\\n");
        return;
    }
    if (front == -1)
        front = 0;
    rear = (rear + 1) % MAX;
    items[rear] = value;
    count++;
    printf("Inserted -> %d at index %d\\n", value, rear);
}

void dequeue() {
    if (count == 0) {
        printf("Circular Queue Underflow\\n");
        return;
    }
    printf("Deleted -> %d from index %d\\n", items[front], front);
    count--;
    if (count == 0) {
        front = rear = -1;
    } else {
        front = (front + 1) % MAX;
    }
}

void display() {
    if (count == 0) {
        printf("Circular Queue is empty\\n");
        return;
    }
    int i, idx = front;
    printf("Queue elements are:\\n");
    for (i = 0; i < count; i++) {
        printf("%d ", items[idx]);
        idx = (idx + 1) % MAX;
    }
    printf("\\n");
}

int main() {
    enqueue(10);
    enqueue(20);
    enqueue(30);
    enqueue(40);
    enqueue(50);
    display();
    dequeue();
    dequeue();
    enqueue(60);
    enqueue(70);
    display();
    return 0;
}
"""
    st.code(cq_c_code, language='c')

    if st.button("Run Code", use_container_width=True, key="cq_run"):
        with st.spinner("Compiling & running..."):
            try:
                tmp_dir = tempfile.mkdtemp()
                src = os.path.join(tmp_dir, "cqueue.c")
                exe = os.path.join(tmp_dir, "cqueue.exe")
                with open(src, "w") as f:
                    f.write(cq_c_code)
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

# ───── Circular Queue Visualizer ─────
elif page == " Circular Queue Visualizer":
    st.title("Interactive Circular Queue Visualization")
    st.caption("Each operation shows micro-steps. The ring layout shows how indices wrap around.")

    # Circular queue size selector
    def _on_cq_size_change():
        new_size = st.session_state['cq_size_slider']
        st.session_state['cq_size'] = new_size
        st.session_state['cq_data'] = [None] * new_size
        st.session_state['cq_front'] = -1
        st.session_state['cq_rear'] = -1
        st.session_state['cq_count'] = 0
        st.session_state['cq_log'] = []

    cq_sz = st.slider("Queue Size (MAX)", min_value=3, max_value=10, value=st.session_state['cq_size'], key="cq_size_slider", on_change=_on_cq_size_change)
    st.session_state['cq_size'] = cq_sz

    cq_enqueue_val = st.number_input("Enter value to enqueue", value=0, step=1, key="cq_enqueue_input")

    c1, c2, c3, c4 = st.columns(4)
    btn_cq_enqueue = c1.button("Enqueue", use_container_width=True, key="cq_btn_enqueue")
    btn_cq_dequeue = c2.button("Dequeue", use_container_width=True, key="cq_btn_dequeue")
    btn_cq_display = c3.button("Display", use_container_width=True, key="cq_btn_display")
    btn_cq_reset = c4.button("Reset", use_container_width=True, key="cq_btn_reset")

    if btn_cq_enqueue: cq_enqueue(cq_enqueue_val)
    elif btn_cq_dequeue: cq_dequeue()
    elif btn_cq_display: cq_display()
    elif btn_cq_reset: cq_reset()

    col_vis, col_backend = st.columns([3, 2])

    with col_vis:
        st.markdown("#### Circular Queue Ring")
        import math
        cq = st.session_state['cq_data']
        cq_f = st.session_state['cq_front']
        cq_r = st.session_state['cq_rear']
        cq_cnt = st.session_state['cq_count']

        # Build ring visualization using positioned divs
        ring_size = 340
        center = ring_size // 2
        radius = 120
        node_size = 62

        nodes_html = ""
        cq_max = st.session_state['cq_size']
        for i in range(cq_max):
            angle = (2 * math.pi * i / cq_max) - (math.pi / 2)  # start from top
            x = center + radius * math.cos(angle) - node_size // 2
            y = center + radius * math.sin(angle) - node_size // 2

            val = cq[i]
            if val is not None:
                if cq_f == cq_r and cq_f == i:
                    cls = "cq-node-front-rear"
                    label = "F & R"
                elif i == cq_f:
                    cls = "cq-node-front"
                    label = "Front"
                elif i == cq_r:
                    cls = "cq-node-rear"
                    label = "Rear"
                else:
                    cls = "cq-node-mid"
                    label = f"[{i}]"
                display_val = val
            else:
                cls = "cq-node-empty"
                label = f"[{i}]"
                display_val = "—"

            nodes_html += (
                f'<div class="cq-node {cls}" style="left:{x:.0f}px; top:{y:.0f}px;">'
                f'{display_val}<div class="cq-node-label">{label}</div></div>'
            )

        # Center info
        center_info = f'<div class="cq-center-label">F={cq_f}<br>R={cq_r}<br>{cq_cnt}/{cq_max}</div>'

        st.markdown(
            f'<div class="cq-ring" style="width:{ring_size}px; height:{ring_size}px;">{nodes_html}{center_info}</div>',
            unsafe_allow_html=True
        )

        if cq_cnt == 0:
            st.info("Circular Queue is **empty**  ·  front = -1  ·  rear = -1")
        else:
            st.markdown(f"**Elements:** {cq_cnt} / {cq_max} | **front** = {cq_f} | **rear** = {cq_r}")

    with col_backend:
        st.markdown("#### Backend Output")
        log = st.session_state.get('cq_log', [])
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