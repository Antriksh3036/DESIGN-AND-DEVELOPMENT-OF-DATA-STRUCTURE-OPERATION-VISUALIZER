import streamlit as st
import time
import graphviz

st.set_page_config(page_title="Stacks using Linked List", layout="wide")

st.markdown("""

""", unsafe_allow_html=True)

if 'll_stack' not in st.session_state:
    st.session_state.ll_stack = []
if 'current_line' not in st.session_state:
    st.session_state.current_line = -1

page = st.sidebar.radio("Navigation", ["Theory", "Visualizer", "Quiz"])

if page == "Theory":
    st.title("Stacks using Linked List")

    with st.container():
        st.markdown('', unsafe_allow_html=True)
        st.subheader("What is a Linked Stack?")
        st.write("""
        A Stack implemented using a Linked List is a dynamic data structure. Unlike array-based stacks,
        it does not require a pre-defined capacity. Each element is a **Node** consisting of two parts:
        1. **Data**: The value stored in the stack.
        2. **Node Pointer**: A reference to the next **Node** in the stack.
        """)
        st.markdown('', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Core Operations")
        st.write("""
        - **Push**: A new **Node** is created. Its pointer points to the current Top, and Top is updated to this new **Node**.
        - **Pop**: The Top pointer is moved to the next **Node** in the sequence (Top = Top->Node). The old memory is freed.
        - **Is Empty**: If the Top pointer is NULL, the stack is empty.
        """)

    with col2:
        st.subheader("Advantages")
        st.write("Dynamic Size: Grows and shrinks at runtime.")
        st.write("No Overflow: Overflow only occurs if the system runs out of heap memory.")
        st.write("Efficiency: Insertion and deletion are always 
.")

elif page == "Visualizer":
    st.title("Interactive Linked Stack")

    def generate_stack_image():
        dot = graphviz.Digraph(format='png')
        dot.attr(rankdir='LR', bgcolor='transparent')
        dot.attr('node', fontname='Helvetica', fontcolor='white', color='white')

        if not st.session_state.ll_stack:
            dot.node('Top', 'Top', shape='none')
            dot.node('n_null', 'NULL', shape='none')
            dot.edge('Top', 'n_null', color='#FF4B4B', penwidth='2')
        else:
            dot.node('Top', 'Top', shape='none')
            for i, val in enumerate(st.session_state.ll_stack):
                dot.node(f'node{i}', f'{{ {val} | node }}', shape='record',
                         style='filled', fillcolor='#458588')

            dot.edge('Top', 'node0', color='#FF4B4B', penwidth='2')
            for i in range(len(st.session_state.ll_stack) - 1):
                dot.edge(f'node{i}', f'node{i+1}')

            dot.node('null_end', 'NULL', shape='none')
            dot.edge(f'node{len(st.session_state.ll_stack)-1}', 'null_end')

        return dot.pipe()

    c_vis, c_code = st.columns([1.5, 1])

    with c_vis:
        st.subheader("Memory Visualization")
        st.image(generate_stack_image(), use_container_width=True)

    with c_code:
        st.subheader("Pseudocode Execution")
        logic = [
            "Structure Node: { data, Node* next }",
            "Procedure PUSH(value):",
            "  Create newNode with value",
            "  newNode.next = Top",
            "  Top = newNode",
            "End Procedure",
            "Procedure POP():",
            "  If Top is NULL: Return UNDERFLOW",
            "  temp = Top",
            "  Top = Top.next",
            "  Free temp",
            "End Procedure"
        ]
        for i, line in enumerate(logic):
            style = "highlight-code" if st.session_state.current_line == i else "standard-code"
            st.markdown(f'{line}', unsafe_allow_html=True)

    st.divider()
    val = st.text_input("Enter node value:", placeholder="Data...")
    b1, b2, b3 = st.columns(3)

    if b1.button("EXECUTE PUSH", use_container_width=True):
        if val:
            st.session_state.current_line = 2
            time.sleep(0.3)
            st.session_state.current_line = 4
            st.session_state.ll_stack.insert(0, val)
            st.rerun()

    if b2.button("EXECUTE POP", use_container_width=True):
        if st.session_state.ll_stack:
            st.session_state.current_line = 8
            time.sleep(0.3)
            st.session_state.current_line = 10
            st.session_state.ll_stack.pop(0)
            st.rerun()
        else:
            st.error("Underflow: No nodes to remove!")

    if b3.button("RESET STACK", use_container_width=True):
        st.session_state.ll_stack = []
        st.session_state.current_line = -1
        st.rerun()

elif page == "Quiz":
    st.title("Test Your Knowledge")
    with st.form("quiz_form"):
        q1 = st.radio("1. What is the time complexity of pushing a node in a Linked Stack?", ["O(1)", "O(n)", "O(log n)"])
        q2 = st.radio("2. Where does the pointer of the last Node in the stack point?", ["Top", "The previous Node", "NULL"])
        q3 = st.radio("3. Which pointer is updated during a POP operation?", ["Bottom", "Top", "Both"])
        q4 = st.radio("4. In a Linked List implementation, 'Overflow' usually happens when:", ["The array is full", "Heap memory is exhausted", "Top reaches 0"])
        q5 = st.radio("5. Does a Linked Stack require contiguous memory locations?", ["Yes", "No"])

        submitted = st.form_submit_button("Submit Answers")

        if submitted:
            score = 0
            if q1 == "O(1)": score += 1
            if q2 == "NULL": score += 1
            if q3 == "Top": score += 1
            if q4 == "Heap memory is exhausted": score += 1
            if q5 == "No": score += 1

            if score == 5:
                st.balloons()
                st.success("Perfect Score! 5/5")
            else:
                st.warning(f"You got {score}/5 correct. Review the theory and try again!")
