'''🧠 Analogy
Think of the input C code as a human language sentence,
the AST as the meaning/structure,
and the code generation as translating that meaning into a new form (maybe even a new language).

✅ TL;DR
You're generating code not to repeat the input, but to:

Confirm your compiler "understood" the structure

Enable transformation to other forms (Python, IR, assembly, etc.)

Set up for optimization or low-level generation

Let me know if you want to:

Start generating intermediate code

Translate into Python instead of C

Jump into code execution (interpreter) or real compilation

We can take any path from here depending on your goal.
'''

def generate_code(node, indent=0):
    space = '    ' * indent

    if node.type == "main":
        return "int main() {\n" + "\n".join(generate_code(child, indent + 1) for child in node.children) + "\n}"

    elif node.type == "decl":
        var_name = node.children[0].value
        expr_code = generate_code(node.children[1])
        return space + f"int {var_name} = {expr_code};"

    elif node.type == "return":
        return space + f"return {generate_code(node.children[0])};"

    elif node.type == "add":
        return f"({generate_code(node.children[0])} + {generate_code(node.children[1])})"

    elif node.type == "sub":
        return f"({generate_code(node.children[0])} - {generate_code(node.children[1])})"

    elif node.type == "num":
        return str(node.value)

    elif node.type == "id":
        return node.value

    else:
        raise Exception(f"Unknown node type: {node.type}")










