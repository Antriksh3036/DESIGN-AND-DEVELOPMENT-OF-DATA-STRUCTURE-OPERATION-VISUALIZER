import json
import streamlit as st
from streamlit_lottie import st_lottie
import time

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
        st.image("importance_of_array.png",width=400)

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
            delfirstele = load_lottiefile("delete_first_element.json")
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
            st.image("delete_first_element.png",width=250)

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
            dellastele = load_lottiefile("delete_last_element.json")
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
            st.image("delete_last_element.png",width=250)

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
                delmidele = load_lottiefile("delete_middle_element.json")
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
                st.image("delete_middle_element.png",width=250)

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
            traverse = load_lottiefile("array_traversal.json")
            st_lottie(
                traverse,
                width = 250,
                key = "traverse",
                loop = False
            )
            time.sleep(4.5)
            st.rerun()
        else:
            st.image("array_traversal.png",width=250)

if st.session_state["page"] == "traversal_done":
    progress.progress(100,"progress")
    with col2:
        st.success("Congratulations, you have completed array traversal")
        st.balloons()



if st.session_state["page"] == "interactive_array":
    with col2:
        if "nodes" not in st.session_state:
            st.session_state["nodes"] = [10, 20, 30]

        st.title("🔷 Interactive Array Visualizer")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Add in the end")
            var1 = st.number_input("Enter the input", value=0)
            if st.button("Add"):
                if var1 != 0:
                    st.session_state["nodes"].append(var1)
                st.rerun()
        with col2:
            st.write("Remove last")
            if st.button("Remove"):
                st.session_state["nodes"].pop()
                st.rerun()
        st.graphviz_chart(f'''
            digraph{{
                node [shape = square]
                {" ".join(str(x) for x in st.session_state["nodes"])}
            }}
        ''')