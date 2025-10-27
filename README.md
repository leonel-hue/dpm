# DPM - Assembly Code Module

A Python module for working with assembly code. Provides utilities for parsing, validating, and manipulating x86/x64 assembly instructions.

## Features

- **Parse Assembly Code**: Parse assembly language instructions from strings
- **Instruction Validation**: Validate assembly instructions against known x86/x64 mnemonics
- **Programmatic Code Generation**: Build assembly code programmatically
- **Code Analysis**: Filter, count, and analyze assembly instructions
- **Comment Support**: Handle inline comments in assembly code

## Installation

Simply copy `asm_module.py` to your project directory and import it:

```python
from asm_module import AssemblyCode, assemble
```

## Usage

### Basic Parsing

```python
from asm_module import assemble

# Parse assembly code from a string
code = """
    mov rax, rbx      ; Move rbx to rax
    add rax, 5        ; Add 5 to rax
    push rax          ; Push rax onto stack
    ret               ; Return
"""

asm = assemble(code)
print(f"Total instructions: {asm.count_instructions()}")
print(asm.to_string())
```

### Programmatic Code Building

```python
from asm_module import AssemblyCode

# Build assembly code programmatically
asm = AssemblyCode()
asm.add_instruction("mov", ["eax", "0"], "Initialize eax")
asm.add_instruction("add", ["eax", "10"], "Add 10")
asm.add_instruction("ret", comment="Return")

print(asm.to_string())
```

### Validation

```python
from asm_module import AssemblyCode

code = """
    mov rax, rbx
    add rax, 5
    invalid_instruction rax
"""

asm = AssemblyCode(code)
is_valid, errors = asm.validate()

if is_valid:
    print("Code is valid!")
else:
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")
```

### Filtering and Analysis

```python
from asm_module import assemble

code = """
    mov rax, rbx
    add rax, 5
    mov rcx, rdx
    push rax
"""

asm = assemble(code)

# Get all mnemonics
mnemonics = asm.get_mnemonics()
print(f"Mnemonics: {mnemonics}")

# Filter by specific mnemonic
mov_instructions = asm.filter_by_mnemonic("mov")
print(f"Found {len(mov_instructions)} MOV instructions")
```

## API Reference

### Classes

#### `AssemblyInstruction`
Represents a single assembly instruction.

**Constructor:**
- `AssemblyInstruction(mnemonic, operands=None, comment=None)`
  - `mnemonic`: Instruction mnemonic (e.g., 'mov', 'add')
  - `operands`: List of operands
  - `comment`: Optional comment

#### `AssemblyParser`
Static parser for assembly code.

**Methods:**
- `parse_line(line)`: Parse a single line of assembly code
- `parse(code)`: Parse multiple lines of assembly code
- `validate_instruction(instruction)`: Validate an instruction

#### `AssemblyCode`
High-level interface for working with assembly code.

**Constructor:**
- `AssemblyCode(code="")`: Initialize with optional assembly code string

**Methods:**
- `add_instruction(mnemonic, operands=None, comment=None)`: Add instruction
- `validate()`: Validate all instructions, returns `(is_valid, errors)`
- `to_string()`: Convert to string representation
- `get_mnemonics()`: Get list of all mnemonics
- `count_instructions()`: Count number of instructions
- `filter_by_mnemonic(mnemonic)`: Filter instructions by mnemonic

### Functions

#### `assemble(code)`
Convenience function to create an AssemblyCode object from a string.

## Supported Instructions

The module supports common x86/x64 instruction mnemonics including:

- Data movement: `mov`, `push`, `pop`, `lea`, `xchg`
- Arithmetic: `add`, `sub`, `mul`, `div`, `imul`, `idiv`, `inc`, `dec`
- Logical: `and`, `or`, `xor`, `not`, `neg`, `test`, `cmp`
- Control flow: `jmp`, `je`, `jne`, `jz`, `jnz`, `jg`, `jge`, `jl`, `jle`, `ja`, `jae`, `jb`, `jbe`, `call`, `ret`
- Bit manipulation: `shl`, `shr`, `sal`, `sar`, `rol`, `ror`
- Other: `nop`, `int`, `syscall`, `movzx`, `movsx`, `cbw`, `cwd`, `cdq`

## Running Tests

Run the included unit tests:

```bash
python3 -m unittest test_asm_module.py -v
```

## Examples

See `asm_module.py` for more examples in the `if __name__ == "__main__"` section.

## License

MIT License - See LICENSE file for details.