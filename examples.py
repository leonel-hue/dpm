#!/usr/bin/env python3
"""
Example usage of the Assembly Code Module

This script demonstrates various features of the asm_module.
"""

from asm_module import AssemblyCode, assemble, AssemblyParser


def example_basic_parsing():
    """Demonstrate basic parsing of assembly code."""
    print("="*60)
    print("Example 1: Basic Parsing")
    print("="*60)
    
    code = """
    mov rax, 10       ; Load 10 into rax
    mov rbx, 20       ; Load 20 into rbx
    add rax, rbx      ; Add rbx to rax (rax = 30)
    push rax          ; Push result onto stack
    pop rcx           ; Pop result into rcx
    ret               ; Return
    """
    
    asm = assemble(code)
    print(f"Parsed {asm.count_instructions()} instructions:\n")
    print(asm.to_string())
    print()


def example_programmatic_building():
    """Demonstrate building assembly code programmatically."""
    print("="*60)
    print("Example 2: Programmatic Code Building")
    print("="*60)
    
    asm = AssemblyCode()
    
    # Function prologue
    asm.add_instruction("push", ["rbp"], "Save base pointer")
    asm.add_instruction("mov", ["rbp", "rsp"], "Set up stack frame")
    
    # Function body - calculate factorial of 5
    asm.add_instruction("mov", ["rax", "1"], "Initialize result to 1")
    asm.add_instruction("mov", ["rcx", "5"], "Counter = 5")
    
    # Loop (conceptual - labels not implemented)
    asm.add_instruction("imul", ["rax", "rcx"], "result *= counter")
    asm.add_instruction("dec", ["rcx"], "counter--")
    asm.add_instruction("jnz", ["loop_start"], "Jump if not zero")
    
    # Function epilogue
    asm.add_instruction("pop", ["rbp"], "Restore base pointer")
    asm.add_instruction("ret", comment="Return")
    
    print("Generated function to calculate factorial:\n")
    print(asm.to_string())
    print()


def example_validation():
    """Demonstrate code validation."""
    print("="*60)
    print("Example 3: Code Validation")
    print("="*60)
    
    # Valid code
    valid_code = """
    mov rax, rbx
    add rax, 5
    ret
    """
    
    print("Validating valid code:")
    asm1 = AssemblyCode(valid_code)
    is_valid, errors = asm1.validate()
    print(f"Result: {'PASSED ✓' if is_valid else 'FAILED ✗'}")
    print()
    
    # Invalid code
    invalid_code = AssemblyCode()
    invalid_code.add_instruction("mov", ["rax", "rbx"])
    invalid_code.add_instruction("unknown_instruction", ["rax"])
    invalid_code.add_instruction("add", ["rax", "5"])
    
    print("Validating code with invalid instruction:")
    is_valid, errors = invalid_code.validate()
    print(f"Result: {'PASSED ✓' if is_valid else 'FAILED ✗'}")
    if errors:
        print("Errors found:")
        for error in errors:
            print(f"  • {error}")
    print()


def example_filtering():
    """Demonstrate filtering instructions."""
    print("="*60)
    print("Example 4: Filtering and Analysis")
    print("="*60)
    
    code = """
    mov rax, 0        ; Initialize rax
    mov rbx, 10       ; Initialize rbx
    mov rcx, 20       ; Initialize rcx
    add rax, rbx      ; Add rbx to rax
    add rax, rcx      ; Add rcx to rax
    push rax          ; Push result
    call print        ; Call print function
    pop rax           ; Pop result
    ret               ; Return
    """
    
    asm = assemble(code)
    
    print(f"Total instructions: {asm.count_instructions()}\n")
    
    # Count different instruction types
    instruction_types = {}
    for mnemonic in set(asm.get_mnemonics()):
        count = len(asm.filter_by_mnemonic(mnemonic))
        instruction_types[mnemonic] = count
    
    print("Instruction breakdown:")
    for mnemonic, count in sorted(instruction_types.items()):
        print(f"  {mnemonic.upper():8} : {count}")
    
    print("\nAll MOV instructions:")
    mov_instructions = asm.filter_by_mnemonic("mov")
    for inst in mov_instructions:
        print(f"  {inst}")
    print()


def example_complex_function():
    """Demonstrate parsing a more complex function."""
    print("="*60)
    print("Example 5: Complex Function")
    print("="*60)
    
    # A simple x64 function that adds two numbers
    code = """
    ; Function: add_numbers(a, b)
    ; Parameters: rdi (a), rsi (b)
    ; Returns: rax (sum)
    
    push rbp              ; Save base pointer
    mov rbp, rsp          ; Set up stack frame
    
    ; Function body
    mov rax, rdi          ; Move first parameter to rax
    add rax, rsi          ; Add second parameter
    
    ; Check for overflow (conceptual)
    jno no_overflow       ; Jump if no overflow
    mov rax, -1           ; Return -1 on overflow
    
    ; Cleanup and return
    pop rbp               ; Restore base pointer
    ret                   ; Return to caller
    """
    
    asm = assemble(code)
    
    print("Parsed complex function:\n")
    print(asm.to_string())
    print(f"\nTotal instructions: {asm.count_instructions()}")
    
    # Analyze control flow
    control_flow = asm.filter_by_mnemonic("jno")
    control_flow += asm.filter_by_mnemonic("ret")
    print(f"Control flow instructions: {len(control_flow)}")
    print()


def example_instruction_details():
    """Demonstrate accessing instruction details."""
    print("="*60)
    print("Example 6: Instruction Details")
    print("="*60)
    
    inst = AssemblyParser.parse_line("mov rax, [rbx + 8]  ; Load from memory")
    
    print("Parsed instruction details:")
    print(f"  Mnemonic : {inst.mnemonic}")
    print(f"  Operands : {inst.operands}")
    print(f"  Comment  : {inst.comment}")
    print(f"  String   : {inst}")
    print()


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print(" Assembly Code Module - Examples")
    print("="*60 + "\n")
    
    example_basic_parsing()
    example_programmatic_building()
    example_validation()
    example_filtering()
    example_complex_function()
    example_instruction_details()
    
    print("="*60)
    print(" All examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
