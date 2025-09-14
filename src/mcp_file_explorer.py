import os
from pathlib import Path

class MCPFileExplorer:

    def __init__(self, project_root: str):
        self.project_root = Path(project_root).resolve()
        if not self.project_root:
            self.project_root.mkdir(parents=True, exist_ok=True)
        print(f"MCPFileExplorer initialized. Sandboxed to: {self.project_root}")
    
    def _get_secure_path(self, relative_path: str) -> Path:
        
        resolved_path = (self.project_root / relative_path).resolve()

        if self.project_root not in resolved_path.parents and resolved_path != self.project_root:
            raise PermissionError("Access denied: Path is outside the sandboxed project root.")
        
        return resolved_path

    def list_files(self, path: str = '.') -> dict:
        """Lists files and directories at a given relative path."""
        try:
            secure_path = self._get_secure_path(path)
            if not secure_path.is_dir():
                return {'error': f"Path '{path}' is not a directory."}
            
            directories = [d.name for d in secure_path.iterdir() if d.is_dir()]
            files = [f.name for f in secure_path.iterdir() if f.is_file()]
            
            return {'status': 'success', 'path': path, 'directories': directories, 'files': files}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def read_file(self, path: str) -> dict:
        """Reads the content of a file at a given relative path."""
        try:
            secure_path = self._get_secure_path(path)
            if not secure_path.is_file():
                return {'error': f"File not found at '{path}'."}
            
            content = secure_path.read_text(encoding='utf-8')
            return {'status': 'success', 'path': path, 'content': content}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def write_file(self, path: str, content: str) -> dict:
        """Writes (or overwrites) content to a file."""
        try:
            secure_path = self._get_secure_path(path)
            secure_path.parent.mkdir(parents=True, exist_ok=True)
            secure_path.write_text(content, encoding='utf-8')
            return {'status': 'success', 'message': f"File '{path}' written successfully."}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def delete_file(self, path: str) -> dict:
        """Deletes a file at a given relative path."""
        try:
            secure_path = self._get_secure_path(path)
            if not secure_path.is_file():
                return {'status': 'error', 'message': f"File not found at '{path}'."}
            
            secure_path.unlink()
            return {'status': 'success', 'message': f"File '{path}' deleted successfully."}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
