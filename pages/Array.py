import json
import streamlit as st
from streamlit_lottie import st_lottie
import time
import math
FRAMES = 15


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

st.set_page_config(
    layout="wide"
)


if "page" not in st.session_state:
    st.session_state["page"] = "basics"

col1, space1, col2, space2, col3= st.columns([1,0.5,2,0.5,1])

with col1:
    choose = st.selectbox("Choose",["Basics of Array","Interactive Array","Test your understanding"])
    if choose == "Basics of Array":
        if st.session_state["page"] == "interactive_array" or st.session_state["page"] == "basics":
            st.session_state["page"] = "basics"
        st.write(":green[Operations:]")
        if st.button("Array Traversal"):
            st.session_state["page"] = "array_traversal"
            st.rerun()
        if st.button("Array Insertion"):
            st.session_state["page"] = "insert_at_beginning"
            st.rerun()
        if st.button("Array Deletion"):
            st.session_state["page"] = "delete_first_element"
            st.rerun()
        progress = st.progress(0,"Progress")

    if choose == "Interactive Array":
        st.session_state["page"] = "interactive_array"

    if choose == "Test your understanding":
        st.session_state["page"] = "test"


if st.session_state["page"] == "basics":
    with col2:
        st.title(":blue[ARRAY]")
        st.header("BASICS:")
        st.write(''':green[Array is a container which can hold fix number of items and these items should be of same type. Most of the datastructure make use of array to implement their algorithms. Following are important terms to understand the concepts of Array.]''')
        st.write(''':orange[Element − Each item stored in an array is called an element.]''')
        st.write(''':orange[Index − Each location of an element in an array has a numerical index which is used to identify the element.]''')
        if st.button("NEXT"):
            progress.progress(0)
            st.sidebar.success("Chapter 1 completed")
            st.session_state["page"] = "operations"
            st.rerun()
    with col3:
        st.subheader("Array Representation")
        st.image("https://www.tutorialspoint.com/dsa_using_c/images/array.jpg",width=900)
        st.write('''As per above shown illustration, following are the important points to be considered.

Index starts with 0.

Array length is 8 which means it can store 8 elements.

Each element can be accessed via its index. For example, we can fetch element at index 6 as 9.''')

if st.session_state["page"] == "operations":
    progress.progress(50,"Progress")
    with col2:
        st.title(":blue[ARRAY]")
        st.header("Basic Operations:")
        st.write(''':green[Following are the basic operations supported by an array.]''')
        st.write(''':orange[Insertion − add an element at given index.]''')
        st.write(''':orange[Deletion − delete an element at given index.]''')
        st.write(''':orange[Search − search an element using given index or by value.]''')
        st.write(''':orange[Update − update an element at given index.]''')

        st.subheader("CODE:")
        st.markdown(":red[Declaration of Array:]")
        st.code('''
// This array will store integer type element
int arr[5];      

// This array will store char type element
char arr[10];   

// This array will store float type element
float arr[20];
        ''')

        st.markdown(":red[Initialization of Array:]")
        st.code('''
int arr[] = { 1, 2, 3, 4, 5 };
char arr[5] = { 'a', 'b', 'c', 'd', 'e' };
float arr[10] = { 1.4, 2.0, 24, 5.0, 0.0 };
        ''')
        x1, x2, x3 = st.columns([1,1,1])
        with x1:
            if st.button("Previous"):
                st.session_state["page"] = "basics"
                st.rerun()
        with x3:
            if st.button("Next"):
                st.session_state["page"] = "arr_del"
                st.rerun()
    with col3:
        st.image("pages/importance_of_array.png",width=400)

if st.session_state["page"] == "arr_del":
    progress.progress(100,"Progress")
    with col2:
        st.success("Congratulations, you completed the basics of array chapter")
        st.balloons()


if st.session_state["page"] == "delete_first_element":
    with col2:
        st.title(":blue[Array Deletion]")
        st.header(":red[Delete first element]")
        st.write("To delete an element from the beginning of an array in C, the algorithm requires shifting all remaining elements one position to the left to fill the gap, followed by decrementing the array size.  The process involves iterating from the first index (0) to the second-to-last element, assigning array[i] = array[i+1], and then reducing the logical size n by one.")
        st.subheader(":green[ALGORITM:]")
        st.code('''
1. Validate: Ensure the array is not empty (size > 0).

2. Shift: Use a loop starting from index i = 0 up to n - 2 (or i < n - 1) to move each element one step left: array[i] = array[i + 1]. 

3. Update: Decrease the element count n by 1.

4. Terminate: The element at the original beginning is effectively removed, and the new size reflects the reduced array. 
        ''',language=None,wrap_lines=True)
        st.write(":orange[The time complexity for this operation is O(n) because every element after the first one must be shifted.]")
        if st.button("Next"):
            st.session_state["page"] = "delete_last_element"
            st.rerun()

    with col3:
        if st.button("Delete first element"):
            delfirstele = load_lottiefile("pages/delete_first_element.json")
            st_lottie(
                delfirstele,
                width = 250,
                key = "delfirstele",
                loop = False
            )
            time.sleep(0.7)
            st.write("Shift: Use a loop starting from index i = 0 up to n - 2 (or i < n - 1) to move each element one step left: array[i] = array[i + 1].")
            time.sleep(4)
            st.write("Update: Decrease the element count n by 1.")
            time.sleep(0.5)
            st.write("Terminate: The element at the original beginning is effectively removed, and the new size reflects the reduced array. ")
            time.sleep(6)
            st.rerun()
        else:
            st.image("pages/delete_first_element.png",width=250)

if st.session_state["page"] == "delete_last_element":
    progress.progress(33,"progress")
    with col2:
        st.title(":blue[Array Deletion]")
        st.header(":red[Delete last element]")
        st.write("Deleting an element at the end of a C array involves logically reducing the array size by one, as C arrays have a fixed size and cannot physically remove elements from memory.  The process is efficient with a Time Complexity of O(1) because it requires no shifting of elements, only updating the size counter.")
        st.subheader(":green[ALGORITM:]")
        st.code('''
1. Identify the last element: The element to be deleted is located at index n-1, where n is the current number of elements.

2. Reduce the size: Decrement the size variable (n = n - 1) to exclude the last element from subsequent operations. 

3. Ignore the element: The value at the original last index remains in memory but is no longer accessed or printed as part of the array.
        ''',language=None,wrap_lines=True)
        x1, x2, x3 = st.columns([1,1,1])
        with x1:
            if st.button("Previous"):
                st.session_state["page"] = "delete_first_element"
                st.rerun()
        with x3:
            if st.button("Next"):
                st.session_state["page"] = "delete_middle_element"
                st.rerun()

    with col3:
        if st.button("Delete last element"):
            dellastele = load_lottiefile("pages/delete_last_element.json")
            st_lottie(
                dellastele,
                width = 250,
                key = "dellastele",
                speed=0.8,
                loop = False
            )
            time.sleep(0.7)
            st.write(":green[1. Identify the last element: The element to be deleted is located at index n-1, where n is the current number of elements.]")
            time.sleep(1.2)
            st.write(":green[2. Reduce the size: Decrement the size variable (n = n - 1) to exclude the last element from subsequent operations.]")
            time.sleep(2.8)
            st.write(":green[3. Ignore the element: The value at the original last index remains in memory but is no longer accessed or printed as part of the array.]")
            time.sleep(6)
            st.rerun()
        else:
            st.image("pages/delete_last_element.png",width=250)

if st.session_state["page"] == "delete_middle_element":
    progress.progress(66,"progress")
    with col2:
        st.title(":blue[Array Deletion]")
        st.header(":red[Delete middle element]")
        st.write("To delete an element from the middle of an array in C, the algorithm requires shifting all subsequent elements one position to the left to fill the gap created by the deletion.  This process involves finding the element's position, overwriting it with the next element, and decrementing the array size counter")
        st.subheader(":green[ALGORITM:]")
        st.code('''
1. Store the deleted item: Assign the element at the target position K to a temporary variable ITEM to preserve the value before it is overwritten.

2. Shift elements: Iterate from index K to N-1 (where N is the current number of elements), assigning A[I] = A[I+1] to move every subsequent element one step left.

3. Update size: Decrement the total count N by 1 to reflect the removal.
        ''',language=None, wrap_lines=True)
        st.write(":orange[Time Complexity: The operation has a time complexity of O(n) because finding the element (if not already known) and shifting the remaining elements both require linear time relative to the array size.  Space Complexity is O(1) as the operation is performed in-place without requiring extra memory proportional to the input size.]")
        x1, x2, x3 = st.columns([1,1,1])
        with x1:
            if st.button("Previous"):
                st.session_state["page"] = "delete_last_element"
                st.rerun()
        with x2:
            if st.button("Next"):
                st.session_state["page"] = "delete_done"
                st.rerun()
        with col3:
            if st.button("Delete middle element"):
                time.sleep(0.8)
                delmidele = load_lottiefile("pages/delete_middle_element.json")
                st_lottie(
                    delmidele,
                    width = 250,
                    key = "delmidele",
                    speed=0.6,
                    loop = False
                )
                time.sleep(0.7)
                st.write(":green[Store the deleted item: Assign the element at the target position K to a temporary variable ITEM to preserve the value before it is overwritten.]")
                time.sleep(0.4)
                st.write(":green[Shift elements: Iterate from index K to N-1 (where N is the current number of elements), assigning A[I] = A[I+1] to move every subsequent element one step left.]")
                time.sleep(1.5)
                st.write(":green[Update size: Decrement the total count N by 1 to reflect the removal.]")
                time.sleep(4.5)
                st.rerun()
            else:
                st.image("pages/delete_middle_element.png",width=250)

if st.session_state["page"] == "delete_done":
    progress.progress(100,"progress")
    with col2:
        st.success("Congratulations, you have learnt array deletion")
        st.balloons()

if st.session_state["page"] == "array_traversal":
    with col2:
        st.title(":blue[Array Traversal]")
        st.write("Array traversal in C is the process of accessing each element of an array exactly once, typically to read data, search for values, or verify insertion/deletion operations.  This is most commonly achieved using loops (for or while) that iterate through the array indices, though recursion and pointers are also valid techniques.")
        st.subheader(":green[ALGORITM:]")
        st.code('''
1. Initialize a counter variable (e.g., i = 0) to the lower bound of the array. 

2. Process the current element (e.g., print or modify arr[i]). 
Increment the counter (i = i + 1).

3. Check Condition: If i <= n (where n is the size), repeat steps 2 and 3; otherwise, stop.
        ''',language=None,wrap_lines=True)
        st.subheader(":green[Code:]")
        st.code('''
#include <stdio.h>

void traverse(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]); // Process element
    }
    printf("\n");
}

int main() {
    int arr[] = {1, 2, 3, 4, 5};
    int n = sizeof(arr) / sizeof(arr);
    traverse(arr, n);
    return 0;
}   
        ''',language="c")
        if st.button("Next"):
            st.session_state["page"] = "traversal_done"
            st.rerun()

    with col3:
        if st.button("Traverse all elements"):
            traverse = load_lottiefile("pages/array_traversal.json")
            st_lottie(
                traverse,
                width = 250,
                key = "traverse",
                loop = False
            )
            time.sleep(4.5)
            st.rerun()
        else:
            st.image("pages/array_traversal.png",width=250)

if st.session_state["page"] == "traversal_done":
    progress.progress(100,"progress")
    with col2:
        st.success("Congratulations, you have completed array traversal")
        st.balloons()


if st.session_state["page"] == "interactive_array":
    
    # ---------------- STATE ----------------
    if "arr" not in st.session_state:
        st.session_state.arr = []

    if "vars" not in st.session_state:
        st.session_state.vars = {"i": None, "n": 0, "pos": None, "target": None}

    if "history" not in st.session_state:
        st.session_state.history = []

    # ---------------- CONTROLS ----------------
    st.sidebar.markdown("### ⏱️ Animation Speed")
    speed = st.sidebar.slider("Delay (seconds)", 0.3, 2.0, 0.6)

    st.title("📊 Animated Array Visualizer")

    colA, colB = st.columns(2)

    with colA:
        if st.button("Load Sample Array", key="load_sample"):
            st.session_state.arr = [10, 20, 30, 40, 50]
            st.session_state.vars["n"] = len(st.session_state.arr)
            st.rerun()

    with colB:
        if st.button("Reset Array", key="reset_arr"):
            st.session_state.arr = []
            st.session_state.history = []
            st.rerun()

    placeholder = st.empty()
    step_info = st.empty()

    # ---------------- RENDER ----------------
    def render_array(arr, highlight=None, found=None, source=None, direction=None, progress=0):
        cols = st.columns(len(arr) if arr else 1)

        for i in range(len(arr)):
            color = "rgba(255,255,255,0.05)"
            opacity = 1

            if source == i:
                color = "rgba(0, 123, 255, 0.8)"
                opacity = 1 - progress * 0.7

            if highlight == i:
                color = "rgba(255, 193, 7, 0.9)"
                opacity = 0.5 + progress * 0.5

            if found == i:
                color = "rgba(0, 255, 127, 0.9)"

            shift_x = 0
            if highlight == i:
                if direction == "right":
                    shift_x = progress * 80
                elif direction == "left":
                    shift_x = -progress * 80

            scale = 1.1 if highlight == i else 1

            with cols[i]:
                st.markdown(f"""
                <div style="
                    background:{color};
                    opacity:{opacity};
                    padding:15px;
                    border-radius:10px;
                    text-align:center;
                    border:1px solid rgba(255,255,255,0.2);
                    transition: all 0.1s linear;
                    transform: translate({shift_x}px, -5px) scale({scale});
                ">
                    <div style="font-size:12px;color:#aaa;">Index: {i}</div>
                    <div style="font-size:20px;font-weight:600;">
                        {arr[i] if arr[i] != "" else "_"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ---------------- ARRAY ----------------
    st.markdown("### 📦 Array")
    render_array(st.session_state.arr)

    tab1, tab2, tab3, tab4 = st.tabs(["➕ Insert", "❌ Delete", "🔍 Search", "📜 Traverse"])

    # ---------------- INSERT ----------------
    with tab1:
        val = st.number_input("Value", key="ins_val")
        pos = st.number_input("Position", min_value=0, step=1, key="ins_pos")

        if st.button("Insert", key="insert_btn"):
            arr = st.session_state.arr.copy()

            if pos > len(arr):
                pos = len(arr)

            arr.append(0)

            for i in range(len(arr)-1, pos, -1):
                st.session_state.vars["i"] = i
                step_info.info(f"arr[{i}] = arr[{i-1}]")

                # 🔥 Smooth animation with easing
                for step in range(FRAMES):
                    t = step / (FRAMES - 1)
                    progress = 0.5 * (1 - math.cos(math.pi * t))  # ease-in-out

                    with placeholder.container():
                        render_array(arr,
                                    highlight=i,
                                    source=i-1,
                                    direction="right",
                                    progress=progress)

                    time.sleep(speed / FRAMES)

                # ✅ update AFTER animation
                arr[i] = arr[i-1]

            arr[pos] = val
            st.session_state.arr = arr
            st.session_state.vars["n"] = len(arr)

            st.session_state.history.append(f"Insert {val} at {pos}")

            time.sleep(0.2)
            st.rerun()

    # ---------------- DELETE ----------------
    with tab2:
        pos = st.number_input("Index", min_value=0, step=1, key="del_pos")

        if st.button("Delete", key="delete_btn"):
            arr = st.session_state.arr.copy()

            if 0 <= pos < len(arr):
                original_len = len(arr)

                for i in range(pos, original_len - 1):
                    st.session_state.vars["i"] = i
                    step_info.info(f"arr[{i}] = arr[{i+1}]")

                    temp_arr = arr.copy()
                    temp_arr[original_len - 1] = ""

                    # 🔥 Smooth animation with easing
                    for step in range(FRAMES):
                        t = step / (FRAMES - 1)
                        progress = 0.5 * (1 - math.cos(math.pi * t))

                        with placeholder.container():
                            render_array(temp_arr,
                                        highlight=i,
                                        source=i+1,
                                        direction="left",
                                        progress=progress)

                        time.sleep(speed / FRAMES)

                    # ✅ update AFTER animation
                    arr[i] = arr[i+1]

                arr.pop()
                st.session_state.arr = arr
                st.session_state.vars["n"] = len(arr)

                st.session_state.history.append(f"Delete at {pos}")

                time.sleep(0.2)
                st.rerun()

        else:
            st.warning("Invalid index")

    # ---------------- SEARCH ----------------
    with tab3:
        target = st.number_input("Value", key="search_val")

        if st.button("Search", key="search_btn"):
            arr = st.session_state.arr

            for i in range(len(arr)):
                st.session_state.vars["i"] = i
                step_info.info(f"arr[{i}] == {target} ?")

                with placeholder.container():
                    render_array(arr, highlight=i)

                time.sleep(speed)

                if arr[i] == target:
                    step_info.success(f"Found at {i}")
                    st.session_state.history.append(f"Search {target} → {i}")
                    time.sleep(0.3)
                    st.rerun()

            step_info.error("Not Found")
            st.session_state.history.append(f"Search {target} → Not Found")
            time.sleep(0.3)
            st.rerun()

    # ---------------- TRAVERSE ----------------
    with tab4:
        if st.button("Traverse", key="traverse_btn"):
            arr = st.session_state.arr

            for i in range(len(arr)):
                st.session_state.vars["i"] = i
                step_info.info(f"Visiting arr[{i}]")

                with placeholder.container():
                    render_array(arr, highlight=i)

                time.sleep(speed)

            time.sleep(0.3)
            st.rerun()

    # ---------------- VARIABLES ----------------
    st.markdown("### 🧠 Variables")
    st.json(st.session_state.vars)

    # ---------------- HISTORY ----------------
    st.markdown("### 📜 History")
    for h in st.session_state.history[::-1]:
        st.write("•", h)

    if not st.session_state.arr:
        st.info("Array is empty")


if st.session_state["page"] == "insert_at_beginning":
    with col2:
        st.title(":blue[Array Insertion]")
        st.header(":red[Insert at beginning]")
        st.write("To insert an element at the beginning of an array, all existing elements must be shifted one position to the right to make space for the new value at index 0.  This operation is necessary because arrays store elements in continuous memory locations, leaving no gap at the start for direct insertion.")
        st.subheader(":green[Algorithm:]")
        st.code('''
Initialize: Define the array, current size, maximum capacity, and the new element. 

Check Space: Verify if current_size < max_capacity.

Shift Elements: Iterate from the last element down to the insertion index (0), moving each element to the next position (array[i+1] = array[i]). 

Insert: Assign the new value to the first position (array[0] = new_element). 

Update Size: Increment the size counter (size = size + 1)
        ''',language=None,wrap_lines=True)
        st.subheader(":green[Code:]")
        st.code('''
#include <stdio.h>

int main() {
    int arr[] = {10, 20, 30, 40, 0}; // Array with extra space for insertion
    int n = 4; // Current number of elements
    int element = 50; // Element to insert

    printf("Array before insertion:\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }

    // Shift elements to the right
    for (int i = n - 1; i >= 0; i--) {
        arr[i + 1] = arr[i];
    }

    // Insert the new element at the beginning
    arr[0] = element;

    printf("\nArray after insertion:\n");
    for (int i = 0; i <= n; i++) {
        printf("%d ", arr[i]);
    }

    return 0;
}   
        ''',language="c")
        st.warning('''Time Complexity: The operation runs in O(n) time because every existing element must be moved. ''')
        st.warning('''Space Requirement: The array must be declared with a size one greater than the current number of elements to accommodate the new item without overflow.''')

    with col3:

        if st.button("Insert at beginning"):
            insert_at_beginning = load_lottiefile("pages/insert_at_beginning.json")
            st_lottie(
                insert_at_beginning,
                width = 250,
                loop=False,
                key = "insatbeg",
            )
            st.write(":green[Initialize: Define the array, current size, maximum capacity, and the new element. ]")
            st.write(":green[Check Space: Verify if current_size < max_capacity.]")
            time.sleep(2.2)
            st.write(":green[Shift Elements: Iterate from the last element down to the insertion index (0), moving each element to the next position (array[i+1] = array[i]).]")
            time.sleep(1)
            st.write(":green[Insert: Assign the new value to the first position (array[0] = new_element).]")
            time.sleep(1.5)
            st.write(":green[Update Size: Increment the size counter (size = size + 1)]")

            time.sleep(4.5)
            st.rerun()
        else:
            st.image("pages/insert_at_beginning.png",width=250)

if st.session_state["page"] == "test":
    col1,col2,col3 = st.columns([1,4,0.7])
    with col2:
        st.title("🧠 Test Your Understanding: Arrays")

        # ---------------- QUESTIONS ----------------
        questions = [
            {
                "q": "What is the index of the first element in an array?",
                "options": ["0", "1", "-1", "Depends on language"],
                "answer": "0"
            },
            {
                "q": "What is the time complexity of accessing an element by index?",
                "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"],
                "answer": "O(1)"
            },
            {
                "q": "Which operation requires shifting elements?",
                "options": ["Traversal", "Insertion at beginning", "Access", "Search"],
                "answer": "Insertion at beginning"
            },
            {
                "q": "What is the time complexity of deleting the last element?",
                "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
                "answer": "O(1)"
            },
            {
                "q": "Which data structure uses contiguous memory?",
                "options": ["Array", "Linked List", "Tree", "Graph"],
                "answer": "Array"
            },
            {
                "q": "What happens if you insert in a full array?",
                "options": ["Overflow", "Nothing", "Array expands automatically", "Crash always"],
                "answer": "Overflow"
            },
            {
                "q": "What is the time complexity of searching in an unsorted array?",
                "options": ["O(n)", "O(log n)", "O(1)", "O(n log n)"],
                "answer": "O(n)"
            },
            {
                "q": "Which operation is fastest in arrays?",
                "options": ["Access by index", "Insertion at beginning", "Deletion in middle", "Traversal"],
                "answer": "Access by index"
            }
        ]

        # ---------------- STATE ----------------
        if "score" not in st.session_state:
            st.session_state.score = 0

        if "submitted" not in st.session_state:
            st.session_state.submitted = False

        user_answers = []

        # ---------------- QUIZ UI ----------------
        for i, q in enumerate(questions):
            st.subheader(f"Q{i+1}. {q['q']}")
            ans = st.radio(
                "Choose your answer:",
                q["options"],
                key=f"q{i}"
            )
            user_answers.append(ans)

        # ---------------- SUBMIT ----------------
        if st.button("Submit Quiz"):
            score = 0

            for i, q in enumerate(questions):
                if user_answers[i] == q["answer"]:
                    score += 1

            st.session_state.score = score
            st.session_state.submitted = True

        # ---------------- RESULT ----------------
        if st.session_state.submitted:
            score = st.session_state.score
            st.success(f"Your Score: {score} / {len(questions)}")

            # Feedback logic
            if score == len(questions):
                st.balloons()
                st.success("🔥 Perfect! You’ve mastered arrays.")
            elif score >= 5:
                st.info("👍 Good understanding, just revise a bit.")
            else:
                st.warning("⚠️ You need more practice. Go back to basics.")

            # ---------------- REVIEW ----------------
            st.markdown("### 📘 Review Answers")
            for i, q in enumerate(questions):
                if user_answers[i] == q["answer"]:
                    st.write(f"✅ Q{i+1}: Correct")
                else:
                    st.write(f"❌ Q{i+1}: Correct answer → {q['answer']}")

        # ---------------- RESET ----------------
        if st.button("Reset Quiz"):
            for i in range(len(questions)):
                st.session_state.pop(f"q{i}", None)

            st.session_state.score = 0
            st.session_state.submitted = False
            st.rerun()