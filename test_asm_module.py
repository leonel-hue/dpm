"""
Unit tests for the Assembly Code Module
"""

import unittest
from asm_module import (
    AssemblyInstruction,
    AssemblyParser,
    AssemblyCode,
    assemble
)


class TestAssemblyInstruction(unittest.TestCase):
    """Test cases for AssemblyInstruction class."""
    
    def test_instruction_creation(self):
        """Test creating an instruction."""
        inst = AssemblyInstruction("mov", ["rax", "rbx"])
        self.assertEqual(inst.mnemonic, "mov")
        self.assertEqual(inst.operands, ["rax", "rbx"])
        self.assertIsNone(inst.comment)
    
    def test_instruction_with_comment(self):
        """Test creating an instruction with a comment."""
        inst = AssemblyInstruction("add", ["rax", "5"], "Add 5 to rax")
        self.assertEqual(inst.mnemonic, "add")
        self.assertEqual(inst.operands, ["rax", "5"])
        self.assertEqual(inst.comment, "Add 5 to rax")
    
    def test_instruction_str_representation(self):
        """Test string representation of instruction."""
        inst = AssemblyInstruction("push", ["rax"], "Save rax")
        expected = "push rax  ; Save rax"
        self.assertEqual(str(inst), expected)
    
    def test_instruction_without_operands(self):
        """Test instruction with no operands."""
        inst = AssemblyInstruction("ret")
        self.assertEqual(str(inst), "ret")
    
    def test_mnemonic_case_insensitive(self):
        """Test that mnemonics are converted to lowercase."""
        inst = AssemblyInstruction("MOV", ["RAX", "RBX"])
        self.assertEqual(inst.mnemonic, "mov")


class TestAssemblyParser(unittest.TestCase):
    """Test cases for AssemblyParser class."""
    
    def test_parse_simple_instruction(self):
        """Test parsing a simple instruction."""
        inst = AssemblyParser.parse_line("mov rax, rbx")
        self.assertIsNotNone(inst)
        self.assertEqual(inst.mnemonic, "mov")
        self.assertEqual(inst.operands, ["rax", "rbx"])
    
    def test_parse_instruction_with_comment(self):
        """Test parsing instruction with comment."""
        inst = AssemblyParser.parse_line("add rax, 5  ; Add 5")
        self.assertIsNotNone(inst)
        self.assertEqual(inst.mnemonic, "add")
        self.assertEqual(inst.operands, ["rax", "5"])
        self.assertEqual(inst.comment, "Add 5")
    
    def test_parse_empty_line(self):
        """Test parsing empty line."""
        inst = AssemblyParser.parse_line("")
        self.assertIsNone(inst)
    
    def test_parse_comment_only_line(self):
        """Test parsing comment-only line."""
        inst = AssemblyParser.parse_line("; This is a comment")
        self.assertIsNone(inst)
    
    def test_parse_label(self):
        """Test parsing label (should return None)."""
        inst = AssemblyParser.parse_line("my_label:")
        self.assertIsNone(inst)
    
    def test_parse_instruction_no_operands(self):
        """Test parsing instruction without operands."""
        inst = AssemblyParser.parse_line("ret")
        self.assertIsNotNone(inst)
        self.assertEqual(inst.mnemonic, "ret")
        self.assertEqual(inst.operands, [])
    
    def test_parse_multiline_code(self):
        """Test parsing multiple lines of code."""
        code = """
        mov rax, rbx
        add rax, 5
        ret
        """
        instructions = AssemblyParser.parse(code)
        self.assertEqual(len(instructions), 3)
        self.assertEqual(instructions[0].mnemonic, "mov")
        self.assertEqual(instructions[1].mnemonic, "add")
        self.assertEqual(instructions[2].mnemonic, "ret")
    
    def test_parse_with_whitespace(self):
        """Test parsing with various whitespace."""
        inst = AssemblyParser.parse_line("  mov   rax,  rbx  ")
        self.assertIsNotNone(inst)
        self.assertEqual(inst.mnemonic, "mov")
        self.assertEqual(len(inst.operands), 2)
    
    def test_validate_valid_instruction(self):
        """Test validating a valid instruction."""
        inst = AssemblyInstruction("mov", ["rax", "rbx"])
        is_valid, error = AssemblyParser.validate_instruction(inst)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_invalid_mnemonic(self):
        """Test validating an invalid mnemonic."""
        inst = AssemblyInstruction("invalid_op", ["rax", "rbx"])
        is_valid, error = AssemblyParser.validate_instruction(inst)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        self.assertIn("Unknown mnemonic", error)


class TestAssemblyCode(unittest.TestCase):
    """Test cases for AssemblyCode class."""
    
    def test_create_empty_assembly(self):
        """Test creating empty assembly code."""
        asm = AssemblyCode()
        self.assertEqual(asm.count_instructions(), 0)
    
    def test_create_from_string(self):
        """Test creating assembly code from string."""
        code = "mov rax, rbx\nadd rax, 5"
        asm = AssemblyCode(code)
        self.assertEqual(asm.count_instructions(), 2)
    
    def test_add_instruction(self):
        """Test adding instruction to assembly code."""
        asm = AssemblyCode()
        asm.add_instruction("mov", ["rax", "rbx"])
        self.assertEqual(asm.count_instructions(), 1)
        self.assertEqual(asm.instructions[0].mnemonic, "mov")
    
    def test_add_instruction_with_comment(self):
        """Test adding instruction with comment."""
        asm = AssemblyCode()
        asm.add_instruction("push", ["rax"], "Save rax")
        inst = asm.instructions[0]
        self.assertEqual(inst.comment, "Save rax")
    
    def test_to_string(self):
        """Test converting assembly code to string."""
        asm = AssemblyCode()
        asm.add_instruction("mov", ["rax", "rbx"])
        asm.add_instruction("ret")
        result = asm.to_string()
        self.assertIn("mov rax, rbx", result)
        self.assertIn("ret", result)
    
    def test_get_mnemonics(self):
        """Test getting list of mnemonics."""
        code = "mov rax, rbx\nadd rax, 5\nmov rcx, rdx"
        asm = AssemblyCode(code)
        mnemonics = asm.get_mnemonics()
        self.assertEqual(mnemonics, ["mov", "add", "mov"])
    
    def test_filter_by_mnemonic(self):
        """Test filtering instructions by mnemonic."""
        code = "mov rax, rbx\nadd rax, 5\nmov rcx, rdx\npush rax"
        asm = AssemblyCode(code)
        mov_instructions = asm.filter_by_mnemonic("mov")
        self.assertEqual(len(mov_instructions), 2)
        for inst in mov_instructions:
            self.assertEqual(inst.mnemonic, "mov")
    
    def test_validate_valid_code(self):
        """Test validating valid assembly code."""
        code = "mov rax, rbx\nadd rax, 5\nret"
        asm = AssemblyCode(code)
        is_valid, errors = asm.validate()
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_invalid_code(self):
        """Test validating invalid assembly code."""
        asm = AssemblyCode()
        asm.add_instruction("invalid_op", ["rax"])
        is_valid, errors = asm.validate()
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions."""
    
    def test_assemble_function(self):
        """Test the assemble convenience function."""
        code = "mov rax, rbx\nadd rax, 5"
        asm = assemble(code)
        self.assertIsInstance(asm, AssemblyCode)
        self.assertEqual(asm.count_instructions(), 2)


class TestComplexScenarios(unittest.TestCase):
    """Test cases for complex scenarios."""
    
    def test_parse_realistic_function(self):
        """Test parsing a realistic assembly function."""
        code = """
        ; Function prologue
        push rbp
        mov rbp, rsp
        
        ; Function body
        mov eax, 0
        add eax, 10
        
        ; Function epilogue
        pop rbp
        ret
        """
        asm = AssemblyCode(code)
        self.assertEqual(asm.count_instructions(), 6)
        
        # Verify specific instructions
        mnemonics = asm.get_mnemonics()
        self.assertIn("push", mnemonics)
        self.assertIn("mov", mnemonics)
        self.assertIn("add", mnemonics)
        self.assertIn("pop", mnemonics)
        self.assertIn("ret", mnemonics)
    
    def test_instruction_statistics(self):
        """Test gathering statistics about instructions."""
        code = """
        mov rax, rbx
        mov rcx, rdx
        add rax, 5
        add rcx, 10
        push rax
        push rcx
        call my_func
        pop rcx
        pop rax
        ret
        """
        asm = AssemblyCode(code)
        
        # Count different instruction types
        mov_count = len(asm.filter_by_mnemonic("mov"))
        add_count = len(asm.filter_by_mnemonic("add"))
        push_count = len(asm.filter_by_mnemonic("push"))
        pop_count = len(asm.filter_by_mnemonic("pop"))
        
        self.assertEqual(mov_count, 2)
        self.assertEqual(add_count, 2)
        self.assertEqual(push_count, 2)
        self.assertEqual(pop_count, 2)


if __name__ == '__main__':
    unittest.main()
