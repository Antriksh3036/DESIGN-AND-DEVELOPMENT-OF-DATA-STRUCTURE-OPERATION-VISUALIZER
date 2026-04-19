import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import time

st.set_page_config(layout="wide")
st.title("🌐 Web Crawler Visualizer (BFS)")

# ---------------------------
# FETCH HTML
# ---------------------------
def get_html(url):
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except:
        return None

# ---------------------------
# EXTRACT LINKS (CONTROLLED)
# ---------------------------
def extract_links(url, max_links=2):
    html = get_html(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    links = []

    for tag in soup.find_all("a", href=True):
        href = tag["href"]

        if href.startswith("#") or "javascript" in href:
            continue

        full_url = urljoin(url, href)
        links.append(full_url)

    return links[:max_links]

# ---------------------------
# BFS CRAWLER WITH LEVELS
# ---------------------------
def bfs_crawl(start_url, max_nodes):
    queue = deque([(start_url, 0)])
    visited = set()
    graph = nx.Graph()
    steps = []
    levels = {start_url: 0}

    while queue and len(visited) < max_nodes:
        current, level = queue.popleft()

        if current in visited:
            continue

        visited.add(current)

        links = extract_links(current)

        for link in links:
            graph.add_edge(current, link)

            if link not in levels:
                levels[link] = level + 1

            queue.append((link, level + 1))

        steps.append((graph.copy(), current, levels.copy()))

    return steps

# ---------------------------
# HIERARCHY LAYOUT (TREE)
# ---------------------------
def hierarchy_layout(graph, levels):
    pos = {}

    level_nodes = {}
    for node, level in levels.items():
        level_nodes.setdefault(level, []).append(node)

    y_gap = 1.5
    x_gap = 2

    for level, nodes in level_nodes.items():
        for i, node in enumerate(nodes):
            pos[node] = (i * x_gap, -level * y_gap)

    return pos

# ---------------------------
# DRAW GRAPH
# ---------------------------
def draw_graph(graph, levels, current=None):
    fig, ax = plt.subplots(figsize=(6, 4))

    pos = hierarchy_layout(graph, levels)

    node_colors = []
    for node in graph.nodes():
        if node == current:
            node_colors.append("red")  # current node
        else:
            level = levels.get(node, 0)
            if level == 0:
                node_colors.append("gold")       # root
            elif level == 1:
                node_colors.append("skyblue")    # level 1
            else:
                node_colors.append("lightgreen") # deeper

    labels = {node: f"N{idx}" for idx, node in enumerate(graph.nodes())}

    nx.draw(graph, pos,
            labels=labels,
            node_size=500,
            node_color=node_colors,
            edge_color="gray",
            font_size=8,
            ax=ax)

    return fig

# ---------------------------
# UI INPUT
# ---------------------------
url = st.text_input("Enter URL", "https://example.com")
max_nodes = st.slider("Max Nodes", 3, 10, 6)

st.markdown("""
**Legend:**
- 🟡 Root Node  
- 🔵 Level 1 Nodes  
- 🟢 Level 2+ Nodes  
- 🔴 Current Node  
""")

# ---------------------------
# RUN BUTTON
# ---------------------------
if st.button("Start Crawling"):

    with st.spinner("Crawling websites..."):
        steps = bfs_crawl(url, max_nodes)

    st.success("Visualization Started")

    col1, col2, col3 = st.columns([1, 2, 1])

    placeholder = col2.empty()

    for graph, current, levels in steps:
        fig = draw_graph(graph, levels, current)

        placeholder.pyplot(fig)
        time.sleep(1.5)

        plt.close(fig)

    st.success("Crawling Complete!")