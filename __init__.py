"""
DPM - Assembly Code Module

A Python module for working with assembly code.
Provides utilities for parsing, validating, and manipulating assembly instructions.
"""

from .asm_module import (
    AssemblyInstruction,
    AssemblyParser,
    AssemblyCode,
    assemble
)

__version__ = "1.0.0"
__author__ = "leonel-hue"
__all__ = [
    "AssemblyInstruction",
    "AssemblyParser", 
    "AssemblyCode",
    "assemble"
]
