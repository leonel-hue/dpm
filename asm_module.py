"""
Assembly Code Module
====================

A Python module for working with assembly code.
Provides utilities for parsing, validating, and manipulating assembly instructions.
"""

import re
from typing import List, Dict, Optional, Tuple


class AssemblyInstruction:
    """Represents a single assembly instruction."""
    
    def __init__(self, mnemonic: str, operands: Optional[List[str]] = None, comment: Optional[str] = None):
        """
        Initialize an assembly instruction.
        
        Args:
            mnemonic: The instruction mnemonic (e.g., 'mov', 'add', 'push')
            operands: List of operands for the instruction
            comment: Optional comment associated with the instruction
        """
        self.mnemonic = mnemonic.lower()
        self.operands = operands or []
        self.comment = comment
    
    def __str__(self) -> str:
        """Return string representation of the instruction."""
        instruction = f"{self.mnemonic}"
        if self.operands:
            instruction += " " + ", ".join(self.operands)
        if self.comment:
            instruction += f"  ; {self.comment}"
        return instruction
    
    def __repr__(self) -> str:
        return f"AssemblyInstruction('{self.mnemonic}', {self.operands}, '{self.comment}')"


class AssemblyParser:
    """Parser for assembly code."""
    
    # Common x86/x64 instruction mnemonics
    VALID_MNEMONICS = {
        'mov', 'add', 'sub', 'mul', 'div', 'imul', 'idiv',
        'push', 'pop', 'call', 'ret', 'jmp', 'je', 'jne', 'jz', 'jnz',
        'jg', 'jge', 'jl', 'jle', 'ja', 'jae', 'jb', 'jbe',
        'cmp', 'test', 'and', 'or', 'xor', 'not', 'neg',
        'inc', 'dec', 'lea', 'nop', 'int', 'syscall',
        'shl', 'shr', 'sal', 'sar', 'rol', 'ror',
        'movzx', 'movsx', 'xchg', 'cbw', 'cwd', 'cdq'
    }
    
    # Common x86/x64 registers
    VALID_REGISTERS = {
        'rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'rbp', 'rsp',
        'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15',
        'eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp', 'esp',
        'ax', 'bx', 'cx', 'dx', 'si', 'di', 'bp', 'sp',
        'ah', 'al', 'bh', 'bl', 'ch', 'cl', 'dh', 'dl',
        'rip', 'eip', 'ip'
    }
    
    @staticmethod
    def parse_line(line: str) -> Optional[AssemblyInstruction]:
        """
        Parse a single line of assembly code.
        
        Args:
            line: A line of assembly code
            
        Returns:
            AssemblyInstruction object or None if the line is empty/comment only
        """
        # Remove leading/trailing whitespace
        line = line.strip()
        
        # Skip empty lines
        if not line:
            return None
        
        # Extract comment if present
        comment = None
        if ';' in line:
            parts = line.split(';', 1)
            line = parts[0].strip()
            comment = parts[1].strip()
        
        # Skip lines that are only comments
        if not line:
            return None
        
        # Skip labels (lines ending with :)
        if line.endswith(':'):
            return None
        
        # Parse instruction
        parts = line.split(None, 1)
        if not parts:
            return None
        
        mnemonic = parts[0]
        operands = []
        
        if len(parts) > 1:
            # Parse operands (split by comma)
            operand_str = parts[1]
            operands = [op.strip() for op in operand_str.split(',')]
        
        return AssemblyInstruction(mnemonic, operands, comment)
    
    @staticmethod
    def parse(code: str) -> List[AssemblyInstruction]:
        """
        Parse multiple lines of assembly code.
        
        Args:
            code: Multi-line assembly code string
            
        Returns:
            List of AssemblyInstruction objects
        """
        instructions = []
        for line in code.split('\n'):
            instruction = AssemblyParser.parse_line(line)
            if instruction:
                instructions.append(instruction)
        return instructions
    
    @staticmethod
    def validate_instruction(instruction: AssemblyInstruction) -> Tuple[bool, Optional[str]]:
        """
        Validate an assembly instruction.
        
        Args:
            instruction: AssemblyInstruction to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if mnemonic is valid
        if instruction.mnemonic not in AssemblyParser.VALID_MNEMONICS:
            return False, f"Unknown mnemonic: {instruction.mnemonic}"
        
        # Basic validation passed
        return True, None


class AssemblyCode:
    """High-level interface for working with assembly code."""
    
    def __init__(self, code: str = ""):
        """
        Initialize with assembly code.
        
        Args:
            code: Assembly code string
        """
        self.instructions = AssemblyParser.parse(code) if code else []
    
    def add_instruction(self, mnemonic: str, operands: Optional[List[str]] = None, comment: Optional[str] = None):
        """
        Add an instruction to the assembly code.
        
        Args:
            mnemonic: Instruction mnemonic
            operands: List of operands
            comment: Optional comment
        """
        instruction = AssemblyInstruction(mnemonic, operands, comment)
        self.instructions.append(instruction)
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate all instructions.
        
        Returns:
            Tuple of (all_valid, list_of_errors)
        """
        errors = []
        for i, instruction in enumerate(self.instructions):
            is_valid, error = AssemblyParser.validate_instruction(instruction)
            if not is_valid:
                errors.append(f"Line {i + 1}: {error}")
        return len(errors) == 0, errors
    
    def to_string(self) -> str:
        """
        Convert assembly code to string format.
        
        Returns:
            String representation of all instructions
        """
        return '\n'.join(str(instruction) for instruction in self.instructions)
    
    def get_mnemonics(self) -> List[str]:
        """
        Get list of all mnemonics used.
        
        Returns:
            List of mnemonics
        """
        return [instruction.mnemonic for instruction in self.instructions]
    
    def count_instructions(self) -> int:
        """
        Count the number of instructions.
        
        Returns:
            Number of instructions
        """
        return len(self.instructions)
    
    def filter_by_mnemonic(self, mnemonic: str) -> List[AssemblyInstruction]:
        """
        Filter instructions by mnemonic.
        
        Args:
            mnemonic: The mnemonic to filter by
            
        Returns:
            List of matching instructions
        """
        return [inst for inst in self.instructions if inst.mnemonic == mnemonic.lower()]


def assemble(code: str) -> AssemblyCode:
    """
    Convenience function to create an AssemblyCode object from a string.
    
    Args:
        code: Assembly code string
        
    Returns:
        AssemblyCode object
    """
    return AssemblyCode(code)


# Example usage and demonstration
if __name__ == "__main__":
    # Example 1: Parse assembly code
    sample_code = """
    mov rax, rbx      ; Move rbx to rax
    add rax, 5        ; Add 5 to rax
    push rax          ; Push rax onto stack
    call my_function  ; Call function
    pop rbx           ; Pop from stack to rbx
    ret               ; Return
    """
    
    asm = assemble(sample_code)
    print("Parsed Instructions:")
    print(asm.to_string())
    print(f"\nTotal instructions: {asm.count_instructions()}")
    
    # Example 2: Validate code
    is_valid, errors = asm.validate()
    print(f"\nValidation: {'PASSED' if is_valid else 'FAILED'}")
    if errors:
        for error in errors:
            print(f"  - {error}")
    
    # Example 3: Build assembly code programmatically
    print("\n" + "="*50)
    print("Building assembly code programmatically:")
    asm2 = AssemblyCode()
    asm2.add_instruction("mov", ["eax", "0"], "Initialize eax")
    asm2.add_instruction("add", ["eax", "10"], "Add 10")
    asm2.add_instruction("ret", comment="Return")
    print(asm2.to_string())
    
    # Example 4: Filter instructions
    print("\n" + "="*50)
    print("Filtering 'mov' instructions:")
    mov_instructions = asm.filter_by_mnemonic("mov")
    for inst in mov_instructions:
        print(f"  {inst}")
