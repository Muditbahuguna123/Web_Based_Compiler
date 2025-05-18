from parser import parser
from code_gen import generate_code

code = """
int main() {
    int x = 5 + 3;
    return x;
}
"""

ast = parser.parse(code)

if ast is None:
    print("❌ Parsing failed.")
else:
    print("✅ Code generation result:")
    print(generate_code(ast))
