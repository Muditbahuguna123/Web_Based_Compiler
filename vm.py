class VM:
    def __init__(self):
        self.env = {}  # Variable storage

    def run(self, instructions):
        result = None
        for instr in instructions:
            op = instr[0]

            if op == "assign":
                _, var_name, value = instr
                self.env[var_name] = value

            elif op == "add":
                _, target, op1, op2 = instr
                val1 = self.env.get(op1, op1) if isinstance(op1, str) else op1
                val2 = self.env.get(op2, op2) if isinstance(op2, str) else op2
                self.env[target] = val1 + val2

            elif op == "sub":
                _, target, op1, op2 = instr
                val1 = self.env.get(op1, op1) if isinstance(op1, str) else op1
                val2 = self.env.get(op2, op2) if isinstance(op2, str) else op2
                self.env[target] = val1 - val2

            elif op == "return":
                _, value = instr
                result = self.env.get(value, value) if isinstance(value, str) else value
                break  # Stop execution on return

            else:
                raise Exception(f"Unknown instruction: {instr}")

        return result
