import streamlit as st

st.set_page_config(
    page_title="Home",
    layout="wide"
)



col1, col2, col3 = st.columns([1,2,1])

with col1:
    st.image("central_university_jammu_logo.png",width=200)

with col2:
    st.title(":orange[Central University of Jammu]",)

st.title(":orange[DESIGN AND DEVELOPMENT OF DATA STRUCTURE OPERATION VISUALIZER]")


st.write(":orange[Contributors:]")
st.write("Dr. Dinesh Kumar :blue-badge[Mentor]")
st.write("Sidharth Sharma")
st.write("Saksham Dubey")
st.write("Arun Kumar")
st.write("Antriksh Baskotra")

st.warning("Use side-bar to learn about data structures")
st.warning("Kindly use the icon on the top left side of this page")