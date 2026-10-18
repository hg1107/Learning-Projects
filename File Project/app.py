import streamlit as st
from pathlib import Path

st.set_page_config(page_title="File Manager", page_icon="📁", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    .block-container { padding-top: 2.5rem; max-width: 720px; }
    h1 { font-size: 1.9rem !important; }
    div[data-testid="stVerticalBlock"] > div:has(> .stButton) { margin-top: 0.2rem; }
    .result-box {
        padding: 0.9rem 1.1rem;
        border-radius: 10px;
        margin-top: 0.8rem;
        font-size: 0.95rem;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .success-box { background-color: rgba(46, 160, 67, 0.15); border-color: rgba(46,160,67,0.4); }
    .error-box { background-color: rgba(220, 53, 69, 0.15); border-color: rgba(220,53,69,0.4); }
    .content-box {
        background-color: #161b22;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1rem;
        white-space: pre-wrap;
        font-family: 'SFMono-Regular', Consolas, monospace;
        font-size: 0.9rem;
        margin-top: 0.6rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📁 File Manager")
st.caption("Create, read, update, and delete files — all from one place.")

tab_create, tab_read, tab_update, tab_delete = st.tabs(
    ["🆕 Create", "📖 Read", "✏️ Update", "🗑️ Delete"]
)

# ---------- CREATE ----------
with tab_create:
    st.subheader("Create a new file")
    name = st.text_input("File name", key="create_name", placeholder="example.txt")
    data = st.text_area("File content", key="create_data", height=150)

    if st.button("Create File", type="primary", key="create_btn"):
        if not name:
            st.markdown('<div class="result-box error-box">⚠️ Please enter a file name.</div>', unsafe_allow_html=True)
        else:
            try:
                path = Path(name)
                if path.exists():
                    st.markdown('<div class="result-box error-box">❌ A file with that name already exists.</div>', unsafe_allow_html=True)
                else:
                    with open(path, "w") as fs:
                        fs.write(data)
                    st.markdown('<div class="result-box success-box">✅ File created successfully.</div>', unsafe_allow_html=True)
            except Exception as er:
                st.markdown(f'<div class="result-box error-box">❌ Error occurred: {er}</div>', unsafe_allow_html=True)

# ---------- READ ----------
with tab_read:
    st.subheader("Read a file")
    name = st.text_input("File name", key="read_name", placeholder="example.txt")

    if st.button("Read File", type="primary", key="read_btn"):
        if not name:
            st.markdown('<div class="result-box error-box">⚠️ Please enter a file name.</div>', unsafe_allow_html=True)
        else:
            try:
                path = Path(name)
                if path.exists():
                    with open(path, "r") as fs:
                        content = fs.read()
                    st.markdown('<div class="result-box success-box">✅ File loaded.</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="content-box">{content if content else "(empty file)"}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="result-box error-box">❌ No such file exists.</div>', unsafe_allow_html=True)
            except Exception as er:
                st.markdown(f'<div class="result-box error-box">❌ Error occurred: {er}</div>', unsafe_allow_html=True)

# ---------- UPDATE ----------
with tab_update:
    st.subheader("Update a file")
    name = st.text_input("File name", key="update_name", placeholder="example.txt")
    operation = st.radio(
        "Choose an operation",
        ["Rename", "Append content", "Overwrite content"],
        key="update_op",
        horizontal=True,
    )

    if operation == "Rename":
        new_name = st.text_input("New file name", key="rename_new")
        if st.button("Rename", type="primary", key="rename_btn"):
            if not name or not new_name:
                st.markdown('<div class="result-box error-box">⚠️ Please enter both file names.</div>', unsafe_allow_html=True)
            else:
                try:
                    path = Path(name)
                    new_path = Path(new_name)
                    if not path.exists():
                        st.markdown('<div class="result-box error-box">❌ Source file does not exist.</div>', unsafe_allow_html=True)
                    elif new_path.exists():
                        st.markdown('<div class="result-box error-box">❌ A file with the new name already exists.</div>', unsafe_allow_html=True)
                    else:
                        path.rename(new_path)
                        st.markdown('<div class="result-box success-box">✅ Renamed successfully.</div>', unsafe_allow_html=True)
                except Exception as er:
                    st.markdown(f'<div class="result-box error-box">❌ Error occurred: {er}</div>', unsafe_allow_html=True)

    elif operation == "Append content":
        append_data = st.text_area("Content to append", key="append_data", height=120)
        if st.button("Append", type="primary", key="append_btn"):
            if not name:
                st.markdown('<div class="result-box error-box">⚠️ Please enter a file name.</div>', unsafe_allow_html=True)
            else:
                try:
                    path = Path(name)
                    if not path.exists():
                        st.markdown('<div class="result-box error-box">❌ No such file exists.</div>', unsafe_allow_html=True)
                    else:
                        with open(path, "a") as fs:
                            fs.write("\n" + append_data)
                        st.markdown('<div class="result-box success-box">✅ Appended successfully.</div>', unsafe_allow_html=True)
                except Exception as er:
                    st.markdown(f'<div class="result-box error-box">❌ Error occurred: {er}</div>', unsafe_allow_html=True)

    else:  # Overwrite
        overwrite_data = st.text_area("New content (replaces existing content)", key="overwrite_data", height=120)
        if st.button("Overwrite", type="primary", key="overwrite_btn"):
            if not name:
                st.markdown('<div class="result-box error-box">⚠️ Please enter a file name.</div>', unsafe_allow_html=True)
            else:
                try:
                    path = Path(name)
                    if not path.exists():
                        st.markdown('<div class="result-box error-box">❌ No such file exists.</div>', unsafe_allow_html=True)
                    else:
                        with open(path, "w") as fs:
                            fs.write(overwrite_data)
                        st.markdown('<div class="result-box success-box">✅ Overwritten successfully.</div>', unsafe_allow_html=True)
                except Exception as er:
                    st.markdown(f'<div class="result-box error-box">❌ Error occurred: {er}</div>', unsafe_allow_html=True)

# ---------- DELETE ----------
with tab_delete:
    st.subheader("Delete a file")
    name = st.text_input("File name", key="delete_name", placeholder="example.txt")
    confirm = st.checkbox("I confirm I want to permanently delete this file", key="delete_confirm")

    if st.button("Delete File", type="primary", key="delete_btn"):
        if not name:
            st.markdown('<div class="result-box error-box">⚠️ Please enter a file name.</div>', unsafe_allow_html=True)
        elif not confirm:
            st.markdown('<div class="result-box error-box">⚠️ Please confirm deletion first.</div>', unsafe_allow_html=True)
        else:
            try:
                path = Path(name)
                if path.exists():
                    path.unlink()
                    st.markdown('<div class="result-box success-box">✅ File deleted successfully.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="result-box error-box">❌ No such file exists.</div>', unsafe_allow_html=True)
            except Exception as er:
                st.markdown(f'<div class="result-box error-box">❌ Error occurred: {er}</div>', unsafe_allow_html=True)