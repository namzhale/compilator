# test_cases.py

from main import run

def run_test_case(code, expected_result):
    print("=== Новый тест ===")
    print("Код:")
    print(code)
    print("\nОжидаемый результат:", expected_result)
    result = run(code)  # Do not enable debug mode here
    print("Результат:", result)
    print("Тест успешен!" if result == expected_result else "Тест провален!")
    print("\n" + "="*20 + "\n")

# Тесты

# Тест 1: Возведение в степень с циклом while
run_test_case("""
integ = 3;
power = 4;
result = 1;
while (power > 0) {
    result = result * integ;
    power = power - 1;
}
result;
""", 81)  # 3^4 = 81

# Тест 2: Факториал числа 5 с помощью цикла while
run_test_case("""
n = 5;
result = 1;
while (n > 1) {
    result = result * n;
    n = n - 1;
}
result;
""", 120)  # 5! = 120

# Тест 3: Использование вложенного цикла while для вычисления суммы первых 5 квадратов
run_test_case("""
i = 1;
sum = 0;
while (i <= 5) {
    j = 1;
    square = 0;
    while (j <= i) {
        square = square + i;
        j = j + 1;
    }
    sum = sum + square;
    i = i + 1;
}
sum;
""", 55)  # 1^2 + 2^2 + 3^2 + 4^2 + 5^2 = 55

# Тест 4: Логические условия и несколько переменных
run_test_case("""
a = 10;
b = 5;
result = 0;
if (a > b) {
    result = result + 1;
}
if (a == 10 && b < 6) {
    result = result + 2;
}
result;
""", 3)  # result = 1 + 2 = 3

# Тест 5: Проверка циклов и условий
run_test_case("""
x = 0;
y = 0;
while (x < 3) {
    if (y == 0) {
        y = y + 1;
    } else {
        y = y + 2;
    }
    x = x + 1;
}
y;
""", 5)  # y = 1 + 2 + 2 = 5 after three iterations

# Тест 6: Проверка выражений с операциями умножения и сложения
run_test_case("""
a = 2;
b = 4;
c = 5;
d = (a * b) + c;  # 2 * 4 + 5 = 8 + 5 = 13
d;
""", 13)

# Тест 7: Проверка деления и остатка
run_test_case("""
a = 10;
b = 3;
div = a / b;  # Integer division (10 / 3 = 3)
mod = a - (b * div);  # Calculating 10 % 3
mod;
""", 1)  # 10 % 3 = 1

# Тест 8: Простое создание и доступ к массиву
run_test_case("""
arr = [1, 2, 3];
arr[0];
""", 1)

# Тест 9: Присваивание значения элементу массива
run_test_case("""
arr = [10, 20, 30];
arr[1] = 99;
arr[1];
""", 99)

# Тест 10: Использование массива в цикле
run_test_case("""
arr = [0, 0, 0];
i = 0;
while (i < 3) {
    arr[i] = i * 2;
    i = i + 1;
}
arr[2];
""", 4)

# Тест 11: Суммирование элементов массива
run_test_case("""
arr = [1, 2, 3, 4, 5];
sum = 0;
i = 0;
while (i < 5) {
    sum = sum + arr[i];
    i = i + 1;
}
sum;
""", 15)

