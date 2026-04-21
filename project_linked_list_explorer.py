import streamlit as st
from dataclasses import dataclass
from typing import Optional, List, Any, Tuple
import time
import uuid

#  Data Structures

@dataclass
class Node:
    value: Any
    next: Optional["Node"] = None
    id: str = None
    address: str = None

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())[:8]
        if self.address is None:
            base = 0x55A3B000 + (hash(self.id) & 0xFFFF) * 0x10
            self.address = f"0x{base:08X}"


class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None

    def to_list(self) -> List[Any]:
        res, cur = [], self.head
        while cur:
            res.append(cur.value)
            cur = cur.next
        return res

    def snapshot(self) -> List[dict]:
        res, cur = [], self.head
        while cur:
            res.append({
                "value":      cur.value,
                "id":         cur.id,
                "address":    cur.address,
                "next_addr":  cur.next.address if cur.next else "NULL",
            })
            cur = cur.next
        return res

    def insert_head(self, value) -> Node:
        node = Node(value)
        node.next = self.head
        self.head = node
        return node

    def insert_tail(self, value) -> Tuple[Node, int]:
        node = Node(value)
        if not self.head:
            self.head = node
            return node, 0
        cur, idx = self.head, 0
        while cur.next:
            cur = cur.next
            idx += 1
        cur.next = node
        return node, idx + 1

    def insert_at_index(self, index: int, value) -> Tuple[Node, int, bool]:
        if index <= 0 or not self.head:
            node = self.insert_head(value)
            return node, 0, True
        cur, i = self.head, 0
        while cur and i < index - 1:
            cur = cur.next
            i += 1
        if cur is None:
            node, tail_idx = self.insert_tail(value)
            return node, tail_idx, False
        node = Node(value)
        node.next = cur.next
        cur.next = node
        return node, index, True

    def delete_at_index(self, index: int) -> Tuple[bool, Any, Any]:
        if not self.head:
            return False, None, None
        if index <= 0:
            removed = self.head
            self.head = self.head.next
            return True, removed.value, removed.address
        cur, i = self.head, 0
        while cur.next and i < index - 1:
            cur = cur.next
            i += 1
        if cur.next is None:
            return False, None, None
        removed = cur.next
        cur.next = cur.next.next
        return True, removed.value, removed.address

    def delete_by_value(self, value) -> Tuple[bool, Any]:
        if not self.head:
            return False, None
        if self.head.value == value:
            addr = self.head.address
            self.head = self.head.next
            return True, addr
        prev, cur = self.head, self.head.next
        while cur:
            if cur.value == value:
                prev.next = cur.next
                return True, cur.address
            prev, cur = cur, cur.next
        return False, None

    def find_nodes_with_indices(self) -> List[Tuple[Node, int]]:
        res, cur, i = [], self.head, 0
        while cur:
            res.append((cur, i))
            cur = cur.next
            i += 1
        return res

    def generate_dot(self, highlight_ids: List[str] = None) -> str:
        if highlight_ids is None:
            highlight_ids = []
        nodes, edges = [], []
        cur, idx = self.head, 0
        while cur:
            color     = "#00ff88" if cur.id in highlight_ids else "#1a2e1a"
            fontcolor = "#0d0d0d" if cur.id in highlight_ids else "#e0e0e0"
            border    = "#00ff88" if cur.id in highlight_ids else "#2a5a2a"
            label = f"{cur.value}\\n{cur.address}"
            nodes.append(
                f'"{cur.id}" [label="{label}", style="filled,bold", '
                f'fillcolor="{color}", fontcolor="{fontcolor}", color="{border}", '
                f'shape=ellipse, fontname="Courier Bold", fontsize=18, '
                f'width=1.8, height=1.0, fixedsize=false, margin="0.3,0.2"];'
            )
            if cur.next:
                edges.append(
                    f'"{cur.id}" -> "{cur.next.id}" '
                    f'[color="#00b4ff", penwidth=2.5, arrowsize=1.2];'
                )
            else:
                null_id = f"null_{cur.id}"
                nodes.append(
                    f'"{null_id}" [label="NULL", shape=plaintext, '
                    f'fontcolor="#888888", fontname="Courier Bold", fontsize=15];'
                )
                edges.append(
                    f'"{cur.id}" -> "{null_id}" '
                    f'[style=dashed, color="#444444", penwidth=1.5, arrowsize=1.0];'
                )
            cur = cur.next
            idx += 1
        return (
            'digraph G {\nrankdir=LR;\nbgcolor="#0d0d0d";\n'
            'graph [pad="0.4", nodesep="0.6", ranksep="0.8"];\n'
            'node [fontsize=18];\n'
            + "\n".join(nodes) + "\n" + "\n".join(edges) + "\n}"
        )

    def ascii_visual(self, highlight_id=None) -> str:
        parts, cur = [], self.head
        while cur:
            v = f"[{cur.value}]"
            parts.append(f">>>{v}<<<" if cur.id == highlight_id else v)
            cur = cur.next
        parts.append("NULL")
        return " -> ".join(parts)



#  Session control


def get_ll() -> LinkedList:
    if "ll" not in st.session_state:
        st.session_state.ll = LinkedList()
    return st.session_state.ll

def reset_ll():
    st.session_state.ll = LinkedList()

def append_log(msg: str, kind: str = ""):
    if "op_log" not in st.session_state:
        st.session_state.op_log = []
    st.session_state.op_log.append((msg, kind))


# Explanation tab(3rd_column)

def build_narrative(op: str, ll: LinkedList, result=None) -> List[Tuple[str, str, str]]:
    snap = ll.snapshot()
    size = len(snap)

    if op == "Insert Head" and result:
        node, val = result
        return [
            ("🧱", "Step 1 — malloc()",
             f"C called malloc(sizeof(Node)) and allocated\n"
             f"memory for a new node.\n\n"
             f"New node address : {node.address}\n"
             f"Node stores value: '{val}'"),
            ("🔗", "Step 2 — rewire head pointer",
             f"new_node->next = head\n"
             f"  (new node inherits the old head)\n\n"
             f"head = new_node\n"
             f"  (head now points to {node.address})"),
            ("✅", "Result",
             f"'{val}' is now at index 0.\n"
             f"List size: {size} node(s)."),
        ]

    if op == "Insert Tail" and result:
        node, idx, val = result
        return [
            ("🚶", "Step 1 — walk to end",
             f"Started at head, followed ->next pointers\n"
             f"until reaching a node where next == NULL.\n\n"
             f"Took {idx} hop(s) to reach the tail."),
            ("🧱", "Step 2 — malloc() and attach",
             f"malloc() returned: {node.address}\n\n"
             f"last_node->next = new_node\n"
             f"new_node->next  = NULL\n"
             f"  (new node is the new tail)"),
            ("✅", "Result",
             f"'{val}' appended at index {idx}.\n"
             f"List size: {size} node(s)."),
        ]

    if op == "Insert At Index" and result:
        node, idx, val, exact = result
        return [
            ("🚶", "Step 1 — walk to index - 1",
             f"Traversed {max(idx - 1, 0)} node(s) to reach\n"
             f"the node just before position {idx}."),
            ("🔀", "Step 2 — splice new node in",
             f"new_node->next = cur->next\n"
             f"  (new node takes the forward link)\n\n"
             f"cur->next = new_node\n"
             f"  (predecessor points to new node)\n\n"
             f"New node at: {node.address}"),
            ("✅", "Result",
             (f"'{val}' inserted at index {idx}.\n"
              f"List size: {size} node(s).")
             if exact else
             (f"Index was out of bounds.\n"
              f"'{val}' appended to tail instead.\n"
              f"List size: {size} node(s).")),
        ]

    if op == "Delete At Index" and result:
        ok, val, addr, idx = result
        if not ok:
            return [("⚠️", "Nothing deleted",
                     "Index was out of bounds or list was empty.\n"
                     "No pointers were changed.")]
        return [
            ("🚶", "Step 1 — walk to index - 1",
             f"Followed ->next pointers until reaching\n"
             f"the node just before index {idx}."),
            ("✂️", "Step 2 — bypass and free()",
             f"cur->next = cur->next->next\n"
             f"  (predecessor skips the target node)\n\n"
             f"free() released memory at {addr}"),
            ("✅", "Result",
             f"Node '{val}' at {addr} removed.\n"
             f"List size: {size} node(s)."),
        ]

    if op == "Delete By Value" and result:
        ok, val, addr = result
        if not ok:
            return [("🔍", "Value not found",
                     f"Walked entire list comparing each node\n"
                     f"using strcmp().\n\n"
                     f"No node held '{val}'.\n"
                     f"Nothing changed.")]
        return [
            ("🔍", "Step 1 — linear search",
             f"Compared each node's value using strcmp()\n"
             f"until finding '{val}' at {addr}."),
            ("✂️", "Step 2 — bypass and free()",
             f"prev->next = cur->next\n"
             f"  (predecessor links around matched node)\n\n"
             f"free() called on {addr}"),
            ("✅", "Result",
             f"First occurrence of '{val}' removed.\n"
             f"List size: {size} node(s)."),
        ]

    if op == "Reset List":
        return [
            ("💣", "Step 1 — walk and free() every node",
             "Iterated from head to NULL.\n"
             "Called free(node->value) and free(node)\n"
             "on every node in the list."),
            ("🔄", "Step 2 — reset head to NULL",
             "head = NULL\n\n"
             "List is completely empty.\n"
             "All heap memory has been released."),
            ("✅", "Result",
             "List is empty. Ready for new operations."),
        ]

    if op == "Traverse":
        if not snap:
            return [("📭", "Empty list",
                     "head == NULL.\nNothing to traverse.")]
        addr_chain = " -> ".join(n["address"] for n in snap) + " -> NULL"
        return [
            ("👁️", "How traverse works",
             f"Starts at head, reads the value,\n"
             f"then follows ->next until NULL.\n"
             f"Visits {size} node(s) total."),
            ("🗺️", "Memory address path visited",
             addr_chain),
            ("💡", "Complexity",
             "Time : O(n)  — must visit every node.\n"
             "Space: O(1)  — only one pointer used."),
        ]

    return [("💡", "Run an operation",
             "Execute an operation on the left.\n\n"
             "This panel will explain exactly what\n"
             "changed in memory, step by step.")]

# C codes for understanding 

C_SNIPPETS = {
    "Insert Head": r"""void insert_head(Node **head_ref, const char *val) {
    Node *n   = create_node(val);
    n->next   = *head_ref;   // point to old head
    *head_ref = n;           // update head
}""",
    "Insert Tail": r"""void insert_tail(Node **head_ref, const char *val) {
    Node *n = create_node(val);
    if (!*head_ref) { *head_ref = n; return; }
    Node *cur = *head_ref;
    while (cur->next)        // walk to last node
        cur = cur->next;
    cur->next = n;           // attach at end
}""",
    "Insert At Index": r"""int insert_at_index(Node **head_ref,
                           int idx, const char *val) {
    if (idx <= 0 || !*head_ref) {
        insert_head(head_ref, val); return 1;
    }
    Node *cur = *head_ref; int i = 0;
    while (cur && i < idx - 1) {
        cur = cur->next; i++;
    }
    if (!cur) { insert_tail(head_ref, val); return 0; }
    Node *n   = create_node(val);
    n->next   = cur->next;   // splice forward
    cur->next = n;           // splice backward
    return 1;
}""",
    "Delete At Index": r"""int delete_at_index(Node **head_ref, int idx) {
    if (!*head_ref) return 0;
    if (idx <= 0) {
        Node *tmp = *head_ref;
        *head_ref = tmp->next;
        free(tmp); return 1;
    }
    Node *cur = *head_ref; int i = 0;
    while (cur->next && i < idx - 1) {
        cur = cur->next; i++;
    }
    if (!cur->next) return 0;
    Node *del  = cur->next;
    cur->next  = del->next;  // bypass
    free(del); return 1;
}""",
    "Delete By Value": r"""int delete_by_value(Node **head_ref,
                          const char *val) {
    if (!*head_ref) return 0;
    if (strcmp((*head_ref)->value, val) == 0) {
        Node *tmp = *head_ref;
        *head_ref = tmp->next;
        free(tmp); return 1;
    }
    Node *prev = *head_ref, *cur = prev->next;
    while (cur) {
        if (strcmp(cur->value, val) == 0) {
            prev->next = cur->next;
            free(cur); return 1;
        }
        prev = cur; cur = cur->next;
    }
    return 0;
}""",
    "Traverse": r"""void traverse(Node *head) {
    Node *cur = head;
    while (cur) {
        printf("%s -> ", cur->value);
        cur = cur->next;
    }
    printf("NULL\n");
}""",
    "Reset List": r"""void free_list(Node **head_ref) {
    Node *cur = *head_ref;
    while (cur) {
        Node *tmp = cur;
        cur = cur->next;
        free(tmp->value);
        free(tmp);
    }
    *head_ref = NULL;
}""",
}

COMPLEXITY = {
    "Insert Head":     ("O(1)", "O(1)"),
    "Insert Tail":     ("O(n)", "O(1)"),
    "Insert At Index": ("O(n)", "O(1)"),
    "Delete At Index": ("O(n)", "O(1)"),
    "Delete By Value": ("O(n)", "O(1)"),
    "Traverse":        ("O(n)", "O(1)"),
    "Reset List":      ("O(n)", "O(1)"),
}


# ─────────────────────────────────────────────────────────────────────────────
#  Page layout
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Linked List Explorer", layout="wide")

st.title("🔗 Linked List Explorer")
st.caption("Interactive visualizer  |  C-style memory addresses  |  Step-by-step explanation")

ll       = get_ll()
snap_top = ll.snapshot()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Nodes in list",    len(snap_top))
m2.metric("Operations done",  len(st.session_state.get("op_log", [])))
m3.metric("Head value",       snap_top[0]["value"]  if snap_top else "—")
m4.metric("Tail value",       snap_top[-1]["value"] if snap_top else "—")

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])


# ─────────────────────────────────────────────────────────────────────────────
#  LEFT — Controls
# ─────────────────────────────────────────────────────────────────────────────

with col1:
    st.subheader("Operations")

    op = st.selectbox("Choose operation", [
        "Insert Head", "Insert Tail", "Insert At Index",
        "Delete At Index", "Delete By Value",
        "Traverse", "Reset List",
    ])

    value_input    = st.text_input("Value", placeholder="e.g. 42 or hello")
    index_input    = st.number_input("Index", min_value=0, step=1, value=0)
    traverse_speed = st.slider("Traversal speed (s / node)", 0.1, 2.0, 0.7, 0.1)
    show_pseudo    = st.checkbox("Show pseudocode", value=True)

    if st.button("▶  Execute", use_container_width=True):
        ll = get_ll()

        if op == "Insert Head":
            if not value_input:
                st.warning("Enter a value.")
            else:
                node = ll.insert_head(value_input)
                append_log(f"insert_head('{value_input}')", "insert")
                st.success(f"'{value_input}' inserted at head.")
                st.session_state.narrative = build_narrative(op, ll, (node, value_input))

        elif op == "Insert Tail":
            if not value_input:
                st.warning("Enter a value.")
            else:
                node, idx = ll.insert_tail(value_input)
                append_log(f"insert_tail('{value_input}')", "insert")
                st.success(f"'{value_input}' inserted at tail (index {idx}).")
                st.session_state.narrative = build_narrative(op, ll, (node, idx, value_input))

        elif op == "Insert At Index":
            if not value_input:
                st.warning("Enter a value.")
            else:
                node, idx, exact = ll.insert_at_index(int(index_input), value_input)
                append_log(f"insert_at_index({int(index_input)}, '{value_input}')", "insert")
                if exact:
                    st.success(f"'{value_input}' inserted at index {idx}.")
                else:
                    st.info(f"Index out of bounds — '{value_input}' appended to tail.")
                st.session_state.narrative = build_narrative(op, ll, (node, idx, value_input, exact))

        elif op == "Delete At Index":
            ok, val, addr = ll.delete_at_index(int(index_input))
            if ok:
                append_log(f"delete_at_index({int(index_input)}) removed '{val}'", "delete")
                st.success(f"Deleted '{val}' at index {int(index_input)}.")
            else:
                st.warning("Delete failed — index out of bounds or list empty.")
            st.session_state.narrative = build_narrative(op, ll, (ok, val, addr, int(index_input)))

        elif op == "Delete By Value":
            if not value_input:
                st.warning("Enter a value.")
            else:
                ok, addr = ll.delete_by_value(value_input)
                if ok:
                    append_log(f"delete_by_value('{value_input}')", "delete")
                    st.success(f"Deleted '{value_input}'.")
                else:
                    st.warning(f"'{value_input}' not found.")
                st.session_state.narrative = build_narrative(op, ll, (ok, value_input, addr))

        elif op == "Traverse":
            st.session_state.do_traverse = True
            append_log("traverse()", "traverse")
            st.session_state.narrative = build_narrative(op, ll)

        elif op == "Reset List":
            reset_ll()
            append_log("reset()", "reset")
            st.success("List reset.")
            st.session_state.narrative = build_narrative(op, get_ll())

    st.divider()
    st.subheader("Quick presets")

    if st.button("🔤  Load [A, B, C, D]", use_container_width=True):
        ll = get_ll()
        for v in ["A", "B", "C", "D"]:
            ll.insert_tail(v)
        append_log("preset A->B->C->D", "insert")
        st.rerun()

    if st.button("🔢  Load [1 to 5]", use_container_width=True):
        reset_ll()
        ll = get_ll()
        for i in range(1, 6):
            ll.insert_tail(str(i))
        append_log("preset 1..5", "insert")
        st.rerun()


    if st.button("🗑️  Clear list", use_container_width=True):
        reset_ll()
        append_log("clear()", "reset")
        st.rerun()



#  2nd Column


with col2:
    st.subheader("Visualization")

    ll      = get_ll()
    dot_ph  = st.empty()
    info_ph = st.empty()
    text_ph = st.empty()

    def render_graph(highlight_ids=None):
        dot = ll.generate_dot(highlight_ids or [])
        try:
            dot_ph.graphviz_chart(dot)
        except Exception:
            dot_ph.code(ll.ascii_visual(), language="text")
        vals = ll.to_list()
        text_ph.caption(
            "  ->  ".join(vals) + "  ->  NULL" if vals else "(empty list)"
        )

    render_graph()

    if st.session_state.get("do_traverse", False):
        st.session_state.do_traverse = False
        nodes_idx = ll.find_nodes_with_indices()
        if not nodes_idx:
            info_ph.info("List is empty — nothing to traverse.")
        else:
            for node, idx in nodes_idx:
                render_graph(highlight_ids=[node.id])
                info_ph.info(
                    f"Visiting index {idx}  |  value = '{node.value}'  |  "
                    f"address = {node.address}  |  "
                    f"next -> {node.next.address if node.next else 'NULL'}"
                )
                time.sleep(traverse_speed)
            info_ph.success("Traversal complete.")

    st.divider()
    st.subheader("Node memory table")

    snap = ll.snapshot()
    if snap:
        st.dataframe(
            {
                "Index":        list(range(len(snap))),
                "Value":        [n["value"]     for n in snap],
                "Address":      [n["address"]   for n in snap],
                "Next pointer": [n["next_addr"] for n in snap],
            },
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("List is empty.")

    st.divider()
    st.subheader("Action log")

    log = st.session_state.get("op_log", [])
    if log:
        icons = {"insert": "🟢", "delete": "🔴", "reset": "🟠", "traverse": "🔵"}
        for msg, kind in reversed(log[-30:]):
            st.caption(f"{icons.get(kind, 'o')}  {msg}")
    else:
        st.info("No operations yet.")

    if st.button("Clear log"):
        st.session_state.op_log = []
        st.rerun()


# 3rd Column c code

with col3:
    st.subheader("What just happened?")

    narrative = st.session_state.get("narrative", [])
    if not narrative:
        st.info(
            "Execute an operation on the left.\n\n"
            "This panel explains exactly what changed "
            "in memory, pointer by pointer."
        )
    else:
        for emoji, title, body in narrative:
            with st.container(border=True):
                st.markdown(f"**{emoji} {title}**")
                st.code(body, language="text")

    st.divider()
    st.subheader("C implementation")

    if op in C_SNIPPETS:
        st.code(C_SNIPPETS[op], language="c")

    if op in ("Insert Head", "Insert Tail", "Insert At Index"):
        with st.expander("Helper: create_node"):
            st.code(r"""Node* create_node(const char *val) {
    Node *n = (Node*)malloc(sizeof(Node));
    n->value = strdup(val);
    n->next  = NULL;
    return n;
}""", language="c")

    with st.expander("Struct definitions"):
        st.code(r"""typedef struct Node {
    char        *value;
    struct Node *next;
} Node;""", language="c")

    st.divider()
    st.subheader("Complexity")

    if op in COMPLEXITY:
        time_c, space_c = COMPLEXITY[op]
        t_col, s_col = st.columns(2)
        t_col.metric("Time",  time_c)
        s_col.metric("Space", space_c)

st.divider()
st.caption(
    "Tip: use Traverse to animate the pointer walk  |  "
    "right column updates after every operation  |  "
    "addresses are simulated for educational purposes"
)