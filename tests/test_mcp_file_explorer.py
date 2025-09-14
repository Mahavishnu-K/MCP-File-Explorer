import pytest
from pathlib import Path
from src.mcp_file_explorer import MCPFileExplorer

@pytest.fixture
def explorer(tmp_path: Path) -> MCPFileExplorer:
    """Creates a temporary sandbox directory and an MCPFileExplorer instance for tests."""
    return MCPFileExplorer(str(tmp_path))

def test_write_and_read_file(explorer: MCPFileExplorer):
    """Test basic write and read functionality."""
    content = "Hello, World!"
    path = "test.txt"
    
    write_result = explorer.write_file(path, content)
    assert write_result['status'] == 'success'
    
    read_result = explorer.read_file(path)
    assert read_result['status'] == 'success'
    assert read_result['content'] == content

def test_list_files(explorer: MCPFileExplorer):
    """Test listing files and directories."""
    explorer.write_file("file1.txt", "a")
    (explorer.project_root / "subdir").mkdir()
    
    list_result = explorer.list_files(".")
    assert list_result['status'] == 'success'
    assert "file1.txt" in list_result['files']
    assert "subdir" in list_result['directories']

def test_security_path_traversal_is_blocked(explorer: MCPFileExplorer):
    """CRITICAL: Ensure the AI cannot escape the sandbox."""
    malicious_path = "../../test.txt"
    
    result = explorer.read_file(malicious_path)
    assert result['status'] == 'error'
    assert "Access denied" in result['message']

    result = explorer.write_file(malicious_path, "hacked")
    assert result['status'] == 'error'
    assert "Access denied" in result['message']

def test_delete_file(explorer: MCPFileExplorer):
    """Test deleting a file works and that the file is actually removed."""
    path = "delete_me.txt"
    content = "This file will be deleted."

    # First write a file
    write_result = explorer.write_file(path, content)
    assert write_result['status'] == 'success'

    # Confirm file exists
    assert (explorer.project_root / path).exists()

    # Delete the file
    delete_result = explorer.delete_file(path)
    assert delete_result['status'] == 'success'
    assert "deleted successfully" in delete_result['message']

    # Confirm it's gone
    assert not (explorer.project_root / path).exists()

def test_delete_nonexistent_file(explorer: MCPFileExplorer):
    """Deleting a non-existent file should return an error."""
    result = explorer.delete_file("i_do_not_exist.txt")
    assert result['status'] == 'error'
    assert "File not found" in result['message']