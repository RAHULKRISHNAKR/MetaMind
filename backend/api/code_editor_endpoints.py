"""
Code Editor API Endpoints
Provides endpoints for interactive code editing in the browser.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
import json

router = APIRouter(prefix="/api/code-editor", tags=["Code Editor"])


class FileContentRequest(BaseModel):
    """Request model for updating file content."""
    content: str = Field(..., description="New file content")


class FileContentResponse(BaseModel):
    """Response model for file content."""
    path: str
    content: str
    language: str
    size: int


class FileTreeNode(BaseModel):
    """Model for file tree node."""
    name: str
    path: str
    type: str  # "file" or "directory"
    children: Optional[List['FileTreeNode']] = None
    size: Optional[int] = None


class FileTreeResponse(BaseModel):
    """Response model for file tree."""
    tree: List[FileTreeNode]
    total_files: int
    total_size: int


class SaveProjectRequest(BaseModel):
    """Request model for saving edited project."""
    files: Dict[str, str] = Field(..., description="Map of file paths to content")


class SaveProjectResponse(BaseModel):
    """Response model for save operation."""
    status: str
    files_saved: int
    message: str
    download_url: Optional[str] = None


# In-memory storage for edited projects (in production, use Redis or database)
edited_projects: Dict[str, Dict[str, Any]] = {}


@router.get("/{project_id}/tree", response_model=FileTreeResponse)
async def get_file_tree(project_id: str):
    """
    Get the file tree structure for a project.
    
    Returns a hierarchical tree of all files and directories.
    """
    try:
        # Get project path from generated_projects
        from ..api.main import generated_projects
        
        if project_id not in generated_projects:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project_info = generated_projects[project_id]
        project_path = Path(project_info["project_path"])
        
        if not project_path.exists():
            raise HTTPException(status_code=404, detail="Project directory not found")
        
        # Build file tree
        def build_tree(path: Path, base_path: Path) -> FileTreeNode:
            relative_path = path.relative_to(base_path)
            
            if path.is_file():
                return FileTreeNode(
                    name=path.name,
                    path=str(relative_path),
                    type="file",
                    size=path.stat().st_size
                )
            else:
                children = []
                for child in sorted(path.iterdir()):
                    children.append(build_tree(child, base_path))
                
                return FileTreeNode(
                    name=path.name,
                    path=str(relative_path),
                    type="directory",
                    children=children
                )
        
        # Get all files for stats
        all_files = list(project_path.rglob('*'))
        file_count = sum(1 for f in all_files if f.is_file())
        total_size = sum(f.stat().st_size for f in all_files if f.is_file())
        
        # Build tree starting from project root
        tree = [build_tree(child, project_path) for child in sorted(project_path.iterdir())]
        
        return FileTreeResponse(
            tree=tree,
            total_files=file_count,
            total_size=total_size
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file tree: {str(e)}")


@router.get("/{project_id}/file", response_model=FileContentResponse)
async def get_file_content(project_id: str, file_path: str):
    """
    Get the content of a specific file.
    
    Args:
        project_id: The project identifier
        file_path: Relative path to the file within the project
    """
    try:
        from ..api.main import generated_projects
        
        if project_id not in generated_projects:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project_info = generated_projects[project_id]
        project_path = Path(project_info["project_path"])
        full_path = project_path / file_path
        
        # Security check: ensure file is within project directory
        if not str(full_path.resolve()).startswith(str(project_path.resolve())):
            raise HTTPException(status_code=403, detail="Access denied")
        
        if not full_path.exists() or not full_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Read file content
        content = full_path.read_text()
        
        # Determine language from extension
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.json': 'json',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.md': 'markdown',
            '.txt': 'text',
            '.env': 'shell',
            '.sh': 'shell',
            '.dockerfile': 'dockerfile',
        }
        
        suffix = full_path.suffix.lower()
        if full_path.name.lower() == 'dockerfile':
            language = 'dockerfile'
        else:
            language = language_map.get(suffix, 'text')
        
        return FileContentResponse(
            path=file_path,
            content=content,
            language=language,
            size=len(content)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")


@router.put("/{project_id}/file")
async def update_file_content(project_id: str, file_path: str, request: FileContentRequest):
    """
    Update the content of a specific file.
    
    Changes are stored in memory until the project is saved.
    """
    try:
        from ..api.main import generated_projects
        
        if project_id not in generated_projects:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Store edited content in memory
        if project_id not in edited_projects:
            edited_projects[project_id] = {"files": {}}
        
        edited_projects[project_id]["files"][file_path] = request.content
        
        return {
            "status": "success",
            "message": f"File {file_path} updated in memory",
            "file_path": file_path,
            "size": len(request.content)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update file: {str(e)}")


@router.post("/{project_id}/save", response_model=SaveProjectResponse)
async def save_project(project_id: str, request: SaveProjectRequest):
    """
    Save all edited files to disk and create a new ZIP archive.
    
    This commits all in-memory changes to the file system.
    """
    try:
        from ..api.main import generated_projects
        from ..agents.code_generator_agent import CodeGeneratorAgent
        
        if project_id not in generated_projects:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project_info = generated_projects[project_id]
        project_path = Path(project_info["project_path"])
        
        # Write all edited files
        files_saved = 0
        for file_path, content in request.files.items():
            full_path = project_path / file_path
            
            # Security check
            if not str(full_path.resolve()).startswith(str(project_path.resolve())):
                continue
            
            # Create parent directories if needed
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            full_path.write_text(content)
            files_saved += 1
        
        # Create new ZIP archive
        generator = CodeGeneratorAgent()
        zip_path = generator.create_zip_archive(project_path)
        
        # Update project info
        project_info["zip_path"] = str(zip_path)
        
        # Clear edited files from memory
        if project_id in edited_projects:
            del edited_projects[project_id]
        
        return SaveProjectResponse(
            status="success",
            files_saved=files_saved,
            message=f"Saved {files_saved} files and created new ZIP archive",
            download_url=f"/api/design/{project_info['run_id']}/download/{project_id}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save project: {str(e)}")


@router.post("/{project_id}/reset")
async def reset_project(project_id: str):
    """
    Reset all in-memory edits for a project.
    
    This discards all unsaved changes.
    """
    try:
        if project_id in edited_projects:
            del edited_projects[project_id]
        
        return {
            "status": "success",
            "message": "All unsaved changes discarded"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset project: {str(e)}")


@router.get("/{project_id}/diff")
async def get_project_diff(project_id: str):
    """
    Get a diff of all edited files vs original files.
    
    Returns a list of changed files with their modifications.
    """
    try:
        from ..api.main import generated_projects
        
        if project_id not in generated_projects:
            raise HTTPException(status_code=404, detail="Project not found")
        
        if project_id not in edited_projects:
            return {
                "status": "no_changes",
                "changed_files": [],
                "message": "No unsaved changes"
            }
        
        project_info = generated_projects[project_id]
        project_path = Path(project_info["project_path"])
        
        changed_files = []
        for file_path, new_content in edited_projects[project_id]["files"].items():
            full_path = project_path / file_path
            
            if full_path.exists():
                original_content = full_path.read_text()
                
                # Simple line-based diff
                original_lines = original_content.splitlines()
                new_lines = new_content.splitlines()
                
                changed_files.append({
                    "path": file_path,
                    "original_lines": len(original_lines),
                    "new_lines": len(new_lines),
                    "lines_added": len(new_lines) - len(original_lines),
                    "changed": original_content != new_content
                })
        
        return {
            "status": "success",
            "changed_files": changed_files,
            "total_changes": len(changed_files)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get diff: {str(e)}")