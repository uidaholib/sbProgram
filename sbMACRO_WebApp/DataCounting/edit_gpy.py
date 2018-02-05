"""This module contains the method for editing the gl.py variables."""

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "DataCounting/"))
import gl  # pylint: disable=C0413



def clear_memory():
    """Reset all gl.py variables."""
    gl.ID[:] = []
    gl.URL[:] = []
    gl.object_type[:] = []
    gl.name[:] = []
    gl.fiscal_year[:] = []
    gl.project[:] = []
    gl.data_in_project[:] = []
    gl.data_per_file[:] = []
    gl.total_fy_data_list[:] = []
    gl.running_data_total[:] = []


    gl.project_items.clear()
    gl.project_files.clear()
    print("""
    Memory Cleared.""")
    return
