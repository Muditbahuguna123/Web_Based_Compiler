from parser import parser
from ir_gen import IRGenerator
from vm import VM

code = """
int main() {
    int x = 5;
    return x + 3;
}
"""

ast = parser.parse(code)

irgen = IRGenerator()
ir = irgen.generate(ast)

print("Generated IR:")
for instr in ir:
    print(instr)

vm = VM()
result = vm.run(ir)

print("Program returned:", result)
