from parser import parser
from x86_generator import X86Generator

code = """
int main() {
    int x = 5;
    return x + 3;
}
"""

ast = parser.parse(code)
gen = X86Generator()
assembly = gen.generate(ast)

with open("output.asm", "w") as f:
    f.write(assembly)

print("Assembly code written to output.asm")
