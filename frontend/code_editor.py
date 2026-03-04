"""
Interactive Code Editor Component
Provides in-browser code editing with syntax highlighting and file tree navigation.
"""

import streamlit as st
import requests
from typing import Dict, Any, Optional, List
import json


API_BASE_URL = st.session_state.get("API_BASE_URL", "http://localhost:8000")


def render_code_editor(project_id: str, run_id: str):
    """
    Render the interactive code editor interface.
    
    Args:
        project_id: The project identifier
        run_id: The design run identifier
    """
    st.markdown("---")
    st.subheader("✏️ Interactive Code Editor")
    st.markdown("""
    Edit your generated code directly in the browser before downloading!
    
    **Features:**
    - 📁 File tree navigation
    - 🎨 Syntax highlighting
    - 💾 Save changes
    - 🔄 Reset to original
    - 📊 View changes diff
    """)
    
    # Initialize session state for editor
    if "editor_state" not in st.session_state:
        st.session_state.editor_state = {
            "project_id": None,
            "current_file": None,
            "file_content": {},
            "edited_files": set(),
            "file_tree": None
        }
    
    # Update project_id if changed
    if st.session_state.editor_state["project_id"] != project_id:
        st.session_state.editor_state["project_id"] = project_id
        st.session_state.editor_state["current_file"] = None
        st.session_state.editor_state["file_content"] = {}
        st.session_state.editor_state["edited_files"] = set()
        st.session_state.editor_state["file_tree"] = None
    
    # Fetch file tree
    if st.session_state.editor_state["file_tree"] is None:
        with st.spinner("Loading project files..."):
            file_tree = fetch_file_tree(project_id)
            if file_tree:
                st.session_state.editor_state["file_tree"] = file_tree
    
    if not st.session_state.editor_state["file_tree"]:
        st.error("Failed to load project files")
        return
    
    # Layout: File tree on left, editor on right
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### 📁 Files")
        render_file_tree(
            st.session_state.editor_state["file_tree"]["tree"],
            project_id
        )
        
        # Show edited files count
        edited_count = len(st.session_state.editor_state["edited_files"])
        if edited_count > 0:
            st.info(f"📝 {edited_count} file(s) edited")
    
    with col2:
        if st.session_state.editor_state["current_file"]:
            render_file_editor(project_id, st.session_state.editor_state["current_file"])
        else:
            st.info("👈 Select a file from the tree to start editing")
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💾 Save All Changes", type="primary", use_container_width=True):
            save_all_changes(project_id, run_id)
    
    with col2:
        if st.button("🔄 Reset All", use_container_width=True):
            reset_all_changes(project_id)
    
    with col3:
        if st.button("📊 View Diff", use_container_width=True):
            show_diff(project_id)
    
    with col4:
        if st.button("📥 Download", use_container_width=True):
            st.markdown(f"""
            <a href="{API_BASE_URL}/api/design/{run_id}/download/{project_id}" target="_blank">
                <button style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                    width: 100%;
                ">
                    Download ZIP
                </button>
            </a>
            """, unsafe_allow_html=True)


def render_file_tree(tree: List[Dict], project_id: str, indent: int = 0):
    """Render the file tree recursively."""
    for node in tree:
        if node["type"] == "directory":
            # Directory
            with st.expander(f"📁 {node['name']}", expanded=(indent == 0)):
                if node.get("children"):
                    render_file_tree(node["children"], project_id, indent + 1)
        else:
            # File
            file_path = node["path"]
            is_edited = file_path in st.session_state.editor_state["edited_files"]
            
            # File button with edit indicator
            label = f"{'📝' if is_edited else '📄'} {node['name']}"
            if st.button(label, key=f"file_{file_path}", use_container_width=True):
                st.session_state.editor_state["current_file"] = file_path
                st.rerun()


def render_file_editor(project_id: str, file_path: str):
    """Render the code editor for a specific file."""
    st.markdown(f"### 📄 {file_path}")
    
    # Fetch file content if not in cache
    if file_path not in st.session_state.editor_state["file_content"]:
        with st.spinner(f"Loading {file_path}..."):
            content = fetch_file_content(project_id, file_path)
            if content:
                st.session_state.editor_state["file_content"][file_path] = content
    
    if file_path not in st.session_state.editor_state["file_content"]:
        st.error("Failed to load file content")
        return
    
    file_data = st.session_state.editor_state["file_content"][file_path]
    
    # Show file info
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"**Language:** {file_data['language']}")
    with col2:
        st.caption(f"**Size:** {file_data['size']} bytes")
    
    # Code editor
    edited_content = st.text_area(
        "Edit code:",
        value=file_data["content"],
        height=500,
        key=f"editor_{file_path}",
        label_visibility="collapsed"
    )
    
    # Check if content changed
    if edited_content != file_data["content"]:
        st.session_state.editor_state["edited_files"].add(file_path)
        st.session_state.editor_state["file_content"][file_path]["content"] = edited_content
        
        # Save button for individual file
        if st.button("💾 Save File", key=f"save_{file_path}"):
            save_file(project_id, file_path, edited_content)
    
    # Syntax highlighting info
    st.caption(f"💡 Tip: Use your IDE's syntax highlighting by copying the code")


def fetch_file_tree(project_id: str) -> Optional[Dict]:
    """Fetch the file tree from the API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/code-editor/{project_id}/tree")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch file tree: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching file tree: {str(e)}")
        return None


def fetch_file_content(project_id: str, file_path: str) -> Optional[Dict]:
    """Fetch file content from the API."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/code-editor/{project_id}/file",
            params={"file_path": file_path}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch file: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching file: {str(e)}")
        return None


def save_file(project_id: str, file_path: str, content: str):
    """Save a single file to the server."""
    try:
        response = requests.put(
            f"{API_BASE_URL}/api/code-editor/{project_id}/file",
            params={"file_path": file_path},
            json={"content": content}
        )
        if response.status_code == 200:
            st.success(f"✅ Saved {file_path}")
        else:
            st.error(f"Failed to save file: {response.status_code}")
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")


def save_all_changes(project_id: str, run_id: str):
    """Save all edited files to the server."""
    try:
        # Collect all edited files
        files_to_save = {}
        for file_path in st.session_state.editor_state["edited_files"]:
            if file_path in st.session_state.editor_state["file_content"]:
                files_to_save[file_path] = st.session_state.editor_state["file_content"][file_path]["content"]
        
        if not files_to_save:
            st.warning("No changes to save")
            return
        
        # Save to server
        with st.spinner(f"Saving {len(files_to_save)} file(s)..."):
            response = requests.post(
                f"{API_BASE_URL}/api/code-editor/{project_id}/save",
                json={"files": files_to_save}
            )
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ {result['message']}")
            
            # Clear edited files
            st.session_state.editor_state["edited_files"] = set()
            
            # Show download link
            if result.get("download_url"):
                st.info("📥 New ZIP archive created! Use the Download button to get it.")
        else:
            st.error(f"Failed to save changes: {response.status_code}")
    
    except Exception as e:
        st.error(f"Error saving changes: {str(e)}")


def reset_all_changes(project_id: str):
    """Reset all unsaved changes."""
    try:
        response = requests.post(f"{API_BASE_URL}/api/code-editor/{project_id}/reset")
        
        if response.status_code == 200:
            st.success("✅ All changes reset")
            
            # Clear local state
            st.session_state.editor_state["file_content"] = {}
            st.session_state.editor_state["edited_files"] = set()
            st.session_state.editor_state["current_file"] = None
            
            st.rerun()
        else:
            st.error(f"Failed to reset: {response.status_code}")
    
    except Exception as e:
        st.error(f"Error resetting changes: {str(e)}")


def show_diff(project_id: str):
    """Show diff of all changes."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/code-editor/{project_id}/diff")
        
        if response.status_code == 200:
            result = response.json()
            
            if result["status"] == "no_changes":
                st.info("No unsaved changes")
            else:
                st.subheader("📊 Changes Summary")
                
                for file_change in result["changed_files"]:
                    with st.expander(f"📝 {file_change['path']}"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Original Lines", file_change["original_lines"])
                        with col2:
                            st.metric("New Lines", file_change["new_lines"])
                        with col3:
                            delta = file_change["lines_added"]
                            st.metric("Lines Changed", delta, delta=delta)
        else:
            st.error(f"Failed to get diff: {response.status_code}")
    
    except Exception as e:
        st.error(f"Error getting diff: {str(e)}")

# Made with Bob
