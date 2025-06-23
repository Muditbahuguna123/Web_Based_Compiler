class X86Generator:
    def __init__(self):
        self.output = []
        self.variables = {}
        self.label_counter = 0

    def generate(self, node):
        self.emit_section_headers()
        self.emit_main_start()
        self.handle_node(node)
        self.emit_main_end()
        return "\n".join(self.output)

    def emit(self, line):
        self.output.append(line)

    def emit_section_headers(self):
        self.emit("section .data")
        self.emit("section .text")
        self.emit("global _start")

    def emit_main_start(self):
        self.emit("_start:")

    def emit_main_end(self):
        self.emit("    mov rdi, rax")   # return value -> rdi
        self.emit("    mov rax, 60")    # syscall: exit
        self.emit("    syscall")        # call kernel

    def handle_node(self, node):
        method = getattr(self, f"gen_{node.type}", self.unsupported)
        return method(node)

    def unsupported(self, node):
        raise Exception(f"Unsupported AST node: {node.type}")

    def gen_main(self, node):
        for child in node.children:
            self.handle_node(child)

    def gen_decl(self, node):
        var_name = node.children[0].value
        value = self.eval_expr(node.children[1])
        self.variables[var_name] = value

    def gen_return(self, node):
        value = self.eval_expr(node.children[0])
        self.emit(f"    mov rax, {value}")  # return value in rax

    def gen_if(self, node):
        condition = node.children[0]
        then_body = node.children[1]
        
        # Generate unique labels
        false_label = f"label_{self.label_counter}"
        end_label = f"label_{self.label_counter + 1}"
        self.label_counter += 2
        
        # Generate condition code
        self.gen_condition(condition, false_label)
        
        # Generate then body
        for stmt in then_body:
            self.handle_node(stmt)
        
        # Jump to end
        self.emit(f"    jmp {end_label}")
        
        # False label
        self.emit(f"{false_label}:")
        
        # End label
        self.emit(f"{end_label}:")

    def gen_if_else(self, node):
        condition = node.children[0]
        then_body = node.children[1]
        else_body = node.children[2]
        
        # Generate unique labels
        false_label = f"label_{self.label_counter}"
        end_label = f"label_{self.label_counter + 1}"
        self.label_counter += 2
        
        # Generate condition code
        self.gen_condition(condition, false_label)
        
        # Generate then body
        for stmt in then_body:
            self.handle_node(stmt)
        
        # Jump to end
        self.emit(f"    jmp {end_label}")
        
        # False label (else body)
        self.emit(f"{false_label}:")
        for stmt in else_body:
            self.handle_node(stmt)
        
        # End label
        self.emit(f"{end_label}:")

    def gen_condition(self, condition, false_label):
        """Generate assembly for condition evaluation and conditional jump"""
        if condition.type in ["eq", "ne", "lt", "gt", "le", "ge"]:
            # Load left operand
            left_val = self.eval_expr(condition.children[0])
            self.emit(f"    mov rax, {left_val}")
            
            # Load right operand
            right_val = self.eval_expr(condition.children[1])
            self.emit(f"    mov rbx, {right_val}")
            
            # Compare
            self.emit("    cmp rax, rbx")
            
            # Jump based on condition
            if condition.type == "eq":
                self.emit(f"    jne {false_label}")
            elif condition.type == "ne":
                self.emit(f"    je {false_label}")
            elif condition.type == "lt":
                self.emit(f"    jge {false_label}")
            elif condition.type == "gt":
                self.emit(f"    jle {false_label}")
            elif condition.type == "le":
                self.emit(f"    jg {false_label}")
            elif condition.type == "ge":
                self.emit(f"    jl {false_label}")
        else:
            # For non-comparison expressions, treat as boolean
            value = self.eval_expr(condition)
            self.emit(f"    mov rax, {value}")
            self.emit("    cmp rax, 0")
            self.emit(f"    je {false_label}")

    def eval_expr(self, node):
        if node.type == "num":
            return node.value
        elif node.type == "id":
            return self.variables.get(node.value, 0)
        elif node.type == "add":
            left = self.eval_expr(node.children[0])
            right = self.eval_expr(node.children[1])
            return left + right
        elif node.type == "sub":
            left = self.eval_expr(node.children[0])
            right = self.eval_expr(node.children[1])
            return left - right
        elif node.type in ["eq", "ne", "lt", "gt", "le", "ge"]:
            # For constant folding, evaluate comparison
            left = self.eval_expr(node.children[0])
            right = self.eval_expr(node.children[1])
            if node.type == "eq":
                return 1 if left == right else 0
            elif node.type == "ne":
                return 1 if left != right else 0
            elif node.type == "lt":
                return 1 if left < right else 0
            elif node.type == "gt":
                return 1 if left > right else 0
            elif node.type == "le":
                return 1 if left <= right else 0
            elif node.type == "ge":
                return 1 if left >= right else 0
        else:
            raise Exception(f"Unsupported expression: {node.type}")
