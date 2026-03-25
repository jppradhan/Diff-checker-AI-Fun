"""Tools for the agent to use."""
from langchain.tools import tool
from difflib import unified_diff


@tool
def diff_checker(first_string: str, second_string: str) -> str:
    """Check the differences between two strings using unified diff format.
    
    Uses Python's difflib.unified_diff for standard unified diff output.
    
    Args:
        first_string: Original text to compare
        second_string: Modified text to compare
        
    Returns: Unified diff format as string with context lines and markers (-, +, etc.)
    """
    try:
        lines1 = first_string.splitlines(keepends=True)
        lines2 = second_string.splitlines(keepends=True)
        
        # Generate unified diff
        diff_lines = list(unified_diff(
            lines1,
            lines2,
            fromfile='original',
            tofile='modified',
            lineterm=''
        ))
        
        # Return diff as string
        diff_output = '\n'.join(diff_lines)
        return diff_output if diff_output else "No differences found"
    except Exception as e:
        return f"Error: {str(e)}"

ALL_TOOLS = [diff_checker]