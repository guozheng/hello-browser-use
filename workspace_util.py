import os
import tempfile
from browser_use_sdk.v3 import AsyncBrowserUse

async def upload_string_to_workspace(
    client: AsyncBrowserUse, 
    workspace_name: str, 
    content: str, 
    filename: str, 
    extension: str = ""
) -> str:
    """
    Uploads a string as a file to a browser-use workspace.
    
    Args:
        client: The AsyncBrowserUse client
        workspace_name: The name of the workspace to upload to
        content: The string content to upload
        filename: The desired filename (without extension if extension is provided)
        extension: Optional extension (e.g., '.md', 'txt')
        
    Returns:
        The workspace ID
    """
    if extension:
        if not extension.startswith('.'):
            extension = '.' + extension
        if not filename.endswith(extension):
            full_filename = filename + extension
        else:
            full_filename = filename
    else:
        full_filename = filename
        
    # 1. Find or create the workspace
    workspace_id = None
    response = await client.workspaces.list()
    for w in response.items:
        if w.name == workspace_name:
            workspace_id = w.id
            break
            
    if not workspace_id:
        workspace = await client.workspaces.create(name=workspace_name)
        workspace_id = workspace.id

    # 2. Save content to a temporary file locally
    # It must be saved in the CWD or a temp dir. If we use temp dir, the upload API
    # might keep the remote filename as the literal filepath basename, which works.
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, full_filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    # 3. Upload the file to the workspace
    await client.workspaces.upload(workspace_id, filepath)
    
    # 4. Clean up the local temp file
    try:
        os.remove(filepath)
    except OSError:
        pass
        
    return workspace_id
