# intermediate representation
class IRGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, node):
        method = getattr(self, f"gen_{node.type}", self.generic_gen)
        return method(node)

    def generic_gen(self, node):
        raise Exception(f"No generator for node type: {node.type}")

    def gen_main(self, node):
        for child in node.children:
            self.generate(child)
        return self.instructions

    def gen_decl(self, node):
        var_name = node.children[0].value
        expr_result = self.generate(node.children[1])
        self.instructions.append(("assign", var_name, expr_result))

    def gen_return(self, node):
        value = self.generate(node.children[0])
        self.instructions.append(("return", value))

    def gen_add(self, node):
        left = self.generate(node.children[0])
        right = self.generate(node.children[1])
        temp = self.new_temp()
        self.instructions.append(("add", temp, left, right))
        return temp

    def gen_sub(self, node):
        left = self.generate(node.children[0])
        right = self.generate(node.children[1])
        temp = self.new_temp()
        self.instructions.append(("sub", temp, left, right))
        return temp

    def gen_num(self, node):
        return node.value

    def gen_id(self, node):
        return node.value
