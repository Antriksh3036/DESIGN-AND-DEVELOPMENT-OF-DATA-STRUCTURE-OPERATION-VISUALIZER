import streamlit as st
import time

st.set_page_config(page_title="Data Structure : Stack", layout="wide")
MAX_SIZE = 5

st.markdown("""
<style>
    .highlight-code { background-color: #ffff00; color: black; padding: 5px; border-radius: 5px; font-weight: bold; }
    .theory-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; }
</style>
""", unsafe_allow_html=True)

if 'stack' not in st.session_state:
    st.session_state.stack = []
if 'current_line' not in st.session_state:
    st.session_state.current_line = -1

page = st.sidebar.radio("Go to", [" Theory", " Visualizer", " Quiz"])

if page == " Theory":
    st.title("Stack Data Structure")
    st.markdown("""
    ### What is a Stack?
    A **Stack** A Stack is a linear data structure that follows a particular order in which the operations are performed. The order may be LIFO(Last In First Out) or FILO(First In Last Out). LIFO implies that the element that is inserted last, comes out first and FILO implies that the element that is inserted first, comes out last.It is an abstract data type that serves as a collection of elements, with two main operations:
    * **Push**: Adds an element to the collection.
    * **Pop**: Removes the most recently added element that was not yet removed.
    * Other stack operations include:
    * **Peek/Top**: Returns the most recently added element without removing it.            
    """)
    
    st.info("The order in which elements come out of a stack gives rise to its alternative name, **LIFO** (last in, first out).")
    
    with st.expander("See Real-world Relation"):
        st.write("Think of a stack of dinner plates. You add a new plate to the **top**, and when you need one, you take it off the **top**. You cannot safely take a plate from the middle!")

elif page == " Visualizer":
    st.title("Stack Visualizer")

    def get_stack_diagram():
        
        dot_code = 'digraph G {\n'
        dot_code += '  graph [bgcolor=transparent];\n'
        dot_code += '  node [shape=record, fontname="Helvetica", fontsize=18, width=4, height=0.8, style=filled];\n'
        
        if not st.session_state.stack:
            label = "Empty Stack"
            dot_code += f'  stack [label="{label}", fillcolor="#f1f1f1", fontcolor="#888888"];\n'
        else:
           
            items = [f" {val} " + (" (TOP)" if i == 0 else "") 
                     for i, val in enumerate(reversed(st.session_state.stack))]
            label = "{ " + " | ".join(items) + " }"
            dot_code += f'  stack [label="{label}", fillcolor="#458588", fontcolor="white"];\n'
        
        dot_code += '}'
        return dot_code

    col_vis, col_code = st.columns([1.2, 1])

    with col_vis:
        st.subheader("Memory View")
        st.graphviz_chart(get_stack_diagram(), use_container_width=True)

    with col_code:
        st.subheader("Step-by-Step Execution")
        pseudocode = [
            "function PUSH(val):",
            "  if stack is full: return OVERFLOW",
            "  stack.append(val)",
            "function POP():",
            "  if stack is empty: return UNDERFLOW",
            "  return stack.pop()"
        ]
        
        for i, line in enumerate(pseudocode):
            if st.session_state.current_line == i:
                st.markdown(f'<div class="highlight-code">▶ {line}</div>', unsafe_allow_html=True)
            else:
                st.code(line)

    st.divider()
    input_val = st.text_input("Enter value:", placeholder="e.g. 10")
    c1, c2, c3 = st.columns(3)

    if c1.button("PUSH", use_container_width=True):
        if len(st.session_state.stack) < MAX_SIZE:
            if input_val:
                st.session_state.current_line = 1 
                time.sleep(0.4)
                st.session_state.current_line = 2 
                st.session_state.stack.append(input_val)
                st.rerun()
        else:
            st.error("Stack Overflow!")

    if c2.button("POP", use_container_width=True):
        if st.session_state.stack:
            st.session_state.current_line = 4 
            time.sleep(0.4)
            st.session_state.current_line = 5 
            st.session_state.stack.pop()
            st.rerun()
        else:
            st.error("Stack Underflow!")
            
    if c3.button("Reset", use_container_width=True):
        st.session_state.stack = []
        st.session_state.current_line = -1
        st.rerun()


elif page == " Quiz":
    st.title("Knowledge Check")
    
    with st.form("quiz_form"):
        q1 = st.radio("Which operation adds an element to the stack?", ["Pop", "Peek", "Push"])
        q2 = st.radio("What is the time complexity of Push/Pop in a stack?", ["O(n)", "O(log n)", "O(1)"])
        q3 = st.selectbox("Stack is a ____ data structure.", ["LIFO", "FIFO", "LILO"])
        q4 = st.radio("What is stack underflow?", ["When stack is full", "When stack is empty and pop is attempted", "When stack has one element left"])
        q5 = st.radio("What happens when you try to push an element onto a full stack?", ["Stack Overflow", "Stack Underflow", "Nothing happens"])
        submit = st.form_submit_button("Submit Results")
        
        if submit:
            score = 0
            if q1 == "Push": score += 1
            if q2 == "O(1)": score += 1
            if q3 == "LIFO": score += 1
            if q4 == "When stack is empty and pop is attempted": score += 1
            if q5 == "Stack Overflow": score += 1
            
            st.subheader(f"Your Score: {score}/5")
            if score == 5:
                st.balloons()
                st.success("Perfect Score!")
            else:
                st.warning("Review the theory and visualize the stack behavior and try again!")
