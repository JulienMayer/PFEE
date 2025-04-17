from main import run_circuits

def test_oracle1_easy():
    csss =   [
                [
                    [0, 1], # a*b+b = 1
                    [1, 1]
                ],
                [
                    [1, 1], # a+a*b+b = 1
                    [1, 0]
                ]
            ]
    solution = run_circuits(csss, 1)
    for s in solution:
        assert check_solution(csss, s)
        print()

def test_oracle2_easy():
    csss =   [
                [
                    [0, 1], # a*b+b = 1
                    [1, 1]
                ],
                [
                    [1, 1], # a+a*b+b = 1
                    [1, 0]
                ]
            ]
    solution = run_circuits(csss, 2)
    for s in solution:
        assert check_solution(csss, s)
        print()
        
def test_oracle1_medium():
    csss =   [
                [
                    [0, 1, 1, 0, 1],
                    [1, 0, 1, 1, 0],
                    [1, 1, 0, 0, 0],
                    [0, 1, 0, 0, 0],
                    [1, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1],
                    [0, 1, 0, 0, 1],
                    [0, 1, 0, 0, 0],
                    [0, 1, 1, 0, 1]
                ],
                [
                    [1, 1, 0, 1, 0],
                    [1, 0, 1, 1, 0],
                    [0, 1, 0, 1, 1],
                    [1, 1, 1, 0, 1],
                    [0, 0, 1, 1, 1]
                ],
                [
                    [0, 0, 1, 0, 1],
                    [0, 1, 0, 1, 1],
                    [1, 0, 1, 1, 0],
                    [0, 1, 1, 0, 0],
                    [1, 1, 0, 0, 0]
                ]
            ]
    
    solution = run_circuits(csss, 1)
    for s in solution:
        assert check_solution(csss, s)
        print()

def test_oracle2_medium():
    csss =   [
                [
                    [0, 1, 1, 0, 1],
                    [1, 0, 1, 1, 0],
                    [1, 1, 0, 0, 0],
                    [0, 1, 0, 0, 0],
                    [1, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1],
                    [0, 1, 0, 0, 1],
                    [0, 1, 0, 0, 0],
                    [0, 1, 1, 0, 1]
                ],
                [
                    [1, 1, 0, 1, 0],
                    [1, 0, 1, 1, 0],
                    [0, 1, 0, 1, 1],
                    [1, 1, 1, 0, 1],
                    [0, 0, 1, 1, 1]
                ],
                [
                    [0, 0, 1, 0, 1],
                    [0, 1, 0, 1, 1],
                    [1, 0, 1, 1, 0],
                    [0, 1, 1, 0, 0],
                    [1, 1, 0, 0, 0]
                ]
            ]
    
    solution = run_circuits(csss, 2)
    for s in solution:
        assert check_solution(csss, s)
        print()

def check_solution(csss, solution):
    for i in range(len(solution)):
        print(chr(65 + i), '=', solution[i], end=' ')
    print()
    for equation in csss:
        if not check_equation(equation, solution):
            return False
    return True

def check_equation(equation, solution):
    result = 0
    eq = ""
    for i in range(len(equation)):
        for j in range(i, len(equation[i])):
            if equation[i][j] == 1:
                if eq != "":
                    eq += "+"
                eq += chr(65 + i)
                if i != j:
                    eq += '*' + chr(65 + j)
                result += int(solution[i]) * int(solution[j])
            else:
                continue
    print(eq, '=', result % 2)  
    return result % 2 == 1