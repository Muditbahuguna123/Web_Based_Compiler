class X86Generator:
    def __init__(self):
        self.output = []
        self.variables = {}

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
        else:
            raise Exception(f"Unsupported expression: {node.type}")
