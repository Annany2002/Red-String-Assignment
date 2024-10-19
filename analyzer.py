import ast
import subprocess
import nltk 
import math


def parse_code(code):
    """Parses the given code and returns an AST."""
    try:
        tree = ast.parse(code)
        return tree
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        return None

def calculate_complexity(tree):
    """Calculates the cyclomatic complexity of an AST."""
    complexity = 1  # Start with 1
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
            complexity += 1
    return complexity

def detect_code_duplication(tree, threshold=5):
    """Detects code duplication based on a threshold of consecutive identical lines."""
    code_lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for body_node in node.body:
                if isinstance(body_node, ast.Expr) and isinstance(body_node.value, ast.Constant):
                    code_lines.append(body_node.value.value)
                elif isinstance(body_node, (ast.Assign, ast.Return, ast.If, ast.For, ast.While, ast.Try, ast.With)):
                    code_lines.append(ast.unparse(body_node))

    duplicates = []
    for i in range(len(code_lines) - threshold):
        for j in range(i + threshold, len(code_lines) - threshold):
            if code_lines[i:i + threshold] == code_lines[j:j + threshold]:
                duplicates.append((i, j, code_lines[i:i + threshold]))
    return duplicates


def run_flake8(filename):
    """Runs flake8 on the given file and returns the output."""
    result = subprocess.run(['flake8', filename], capture_output=True, text=True)
    return result.stdout

def analyze_code(filename):
    """Performs static analysis on the given Python file."""
    with open(filename, "r") as f:
        code = f.read()

    tree = parse_code(code)
    if tree:
        complexity = calculate_complexity(tree)
        print(f"Cyclomatic complexity: {complexity}")

        duplicates = detect_code_duplication(tree)
        if duplicates:
            print("Code duplication found:")
            for i, j, lines in duplicates:
                print(f"  Lines {i+1}-{i+len(lines)} duplicate lines {j+1}-{j+len(lines)}:")
                for line in lines:
                    print(f"    {line}")

        flake8_output = run_flake8(filename)
        if flake8_output:
            print("\nFlake8 output:")
            print(flake8_output)

def calculate_loc(code):
    """Calculates the lines of code, excluding blank lines and comments."""
    lines = code.splitlines()
    loc = 0
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            loc += 1
    return loc

def tokenize_code(code):
    """Tokenizes the code using nltk."""
    try:
        tokens = nltk.word_tokenize(code)
        return tokens
    except LookupError:
        nltk.download('punkt')  # Download required resource if not present
        tokens = nltk.word_tokenize(code)
        return tokens

def detect_code_duplication_tokens(tree, threshold=5):
    """Detects code duplication based on token similarity."""
    code_tokens = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for body_node in node.body:
                code_tokens.append(tokenize_code(ast.unparse(body_node)))

    duplicates = []
    for i in range(len(code_tokens) - threshold):
        for j in range(i + threshold, len(code_tokens) - threshold):
            if code_tokens[i:i + threshold] == code_tokens[j:j + threshold]:
                duplicates.append((i, j, code_tokens[i:i + threshold]))
    return duplicates

def detect_code_smells_with_llm(code_snippet, llm_model=None):
    """
    (Basic example) Uses an LLM (or a placeholder function for now) 
    to detect code smells in a code snippet.
    """
    # Placeholder for LLM integration (replace with actual LLM call later)
    if "long method" in code_snippet.lower():
        return ["Potential long method detected."]
    return []

def analyze_code(filename):
    """Performs static analysis on the given Python file."""
    with open(filename, "r") as f:
        code = f.read()

    tree = parse_code(code)
    if tree:
        complexity = calculate_complexity(tree)
        print(f"Cyclomatic complexity: {complexity}")

        duplicates = detect_code_duplication(tree)
        if duplicates:
            print("Code duplication found:")
            for i, j, lines in duplicates:
                print(f"  Lines {i+1}-{i+len(lines)} duplicate lines {j+1}-{j+len(lines)}:")
                for line in lines:
                    print(f"    {line}")

        flake8_output = run_flake8(filename)
        if flake8_output:
            print("\nFlake8 output:")
            print(flake8_output)

        loc = calculate_loc(code)
        print(f"Lines of Code (LOC): {loc}")

        duplicates = detect_code_duplication_tokens(tree)
        if duplicates:
            print("Code duplication (token-based) found:")
            # ... (print duplicate information)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                code_snippet = ast.unparse(node)
                smells = detect_code_smells_with_llm(code_snippet)
                if smells:
                    print(f"In function '{node.name}':")
                    for smell in smells:
                        print(f"  - {smell}")


# ... (previous functions: parse_code, calculate_complexity, run_flake8, 
#      calculate_loc, tokenize_code, detect_code_duplication_tokens,
#      detect_code_smells_with_llm)

def calculate_comment_density(code):
    """Calculates the comment density of the code."""
    lines = code.splitlines()
    code_lines = 0
    comment_lines = 0
    for line in lines:
        line = line.strip()
        if line:
            if line.startswith("#"):
                comment_lines += 1
            else:
                code_lines += 1
    if code_lines == 0:
        return 0  # Avoid division by zero
    return comment_lines / code_lines

def count_functions_classes(tree):
    """Counts the number of functions and classes in the AST."""
    function_count = 0
    class_count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_count += 1
        elif isinstance(node, ast.ClassDef):
            class_count += 1
    return function_count, class_count

def calculate_halstead_metrics(tree):
    """Calculates Halstead metrics (basic implementation)."""
    # This is a simplified example. More accurate calculation 
    # would involve a deeper analysis of operators and operands.
    operators = 0
    operands = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.Add, ast.Sub, ast.Mult, ast.Div, 
                             ast.Eq, ast.NotEq, ast.Lt, ast.Gt)):
            operators += 1
        elif isinstance(node, (ast.Name, ast.Constant)):
            operands += 1

    # Calculate Halstead metrics (example)
    program_length = operators + operands
    vocabulary = len(set(ast.walk(tree)))  # Approximation
    volume = program_length * math.log2(vocabulary) if vocabulary > 0 else 0
    difficulty = (operators / 2) * (operands / vocabulary) if vocabulary > 0 else 0
    effort = difficulty * volume

    return {
        "program_length": program_length,
        "vocabulary": vocabulary,
        "volume": volume,
        "difficulty": difficulty,
        "effort": effort
    }

def detect_basic_security_issues(code):
    """Detects basic security issues like use of eval()."""
    issues = []
    if "eval(" in code:
        issues.append("Potential security risk: Use of eval() detected.")
    # Add more checks for hardcoded passwords, SQL injection, etc.
    return issues

def analyze_code(filename):
    """Performs static analysis on the given Python file."""
    with open(filename, "r") as f:
        code = f.read()

    tree = parse_code(code)
    if tree:
        complexity = calculate_complexity(tree)
        print(f"Cyclomatic complexity: {complexity}")

        duplicates = detect_code_duplication(tree)
        if duplicates:
            print("Code duplication found:")
            for i, j, lines in duplicates:
                print(f"  Lines {i+1}-{i+len(lines)} duplicate lines {j+1}-{j+len(lines)}:")
                for line in lines:
                    print(f"    {line}")

        flake8_output = run_flake8(filename)
        if flake8_output:
            print("\nFlake8 output:")
            print(flake8_output)

        loc = calculate_loc(code)
        print(f"Lines of Code (LOC): {loc} \n")

        duplicates = detect_code_duplication_tokens(tree)
        if duplicates:
            print("Code duplication (token-based) found:")
            # ... (print duplicate information)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                code_snippet = ast.unparse(node)
                smells = detect_code_smells_with_llm(code_snippet)
                if smells:
                    print(f"In function '{node.name}':")
                    for smell in smells:
                        print(f"  - {smell}")

        comment_density = calculate_comment_density(code)
        print(f"Comment Density: {comment_density:.2f}")

        function_count, class_count = count_functions_classes(tree)
        print(f"Number of Functions: {function_count}")
        print(f"Number of Classes: {class_count}")

        halstead = calculate_halstead_metrics(tree)
        print("Halstead Metrics:")
        for metric, value in halstead.items():
            print(f"  {metric}: {value:.2f}")

        security_issues = detect_basic_security_issues(code)
        if security_issues:
            print("\nSecurity Issues:")
            for issue in security_issues:
                print(f"  - {issue}")

        # ... (rest of the analysis: code duplication, LLM)

if __name__ == "__main__":
    filename = "my_code.py"
    analyze_code(filename)