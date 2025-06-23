from parser import parser
from x86_generator import X86Generator

def compile_code(code: str) -> str:
    ast = parser.parse(code)
    gen = X86Generator()
    assembly = gen.generate(ast)
    return assembly

if __name__ == "__main__":
    code = """
int main() {
    int x = 5;
    return x + 5;
}
"""
    assembly = compile_code(code)
    with open("output.asm", "w") as f:
        f.write(assembly)
    print("Assembly code written to output.asm")
