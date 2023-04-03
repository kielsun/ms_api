import re
from collections import Counter
import os


class Solution:

    def countOfAtoms(self, formula: str):
        i = 0
        stack = []
        formula_len = len(formula)

        def divide(pos):
            if pos >= formula_len:
                return None, formula_len, -1
            if formula[pos].isupper():
                char = formula[pos]
                pos += 1
                while pos < formula_len and formula[pos].islower():
                    char += formula[pos]
                    pos += 1
                return char, pos, 0
            elif formula[pos].isdigit():
                num = int(formula[pos])
                pos += 1
                while pos < formula_len and formula[pos].isdigit():
                    num = num * 10 + int(formula[pos])
                    pos += 1
                return str(num), pos, 1
            elif formula[pos] == '(':
                return '(', pos + 1, 2
            elif formula[pos] == ')':
                return ')', pos + 1, 3

        while i < formula_len:
            char, pos, flag = divide(i)
            i = pos
            if flag == 0 or flag == 1 or flag == 2:
                stack.append(char)
            elif flag == 3:
                tmp = Counter()
                char, pos, flag = divide(i)
                if flag == 1:
                    mul = int(char)
                    i = pos
                else:
                    mul = 1
                while stack:
                    char = stack.pop()
                    if char == '(':
                        break
                    elif char.isdigit():
                        num = int(char) * mul
                        char = stack.pop()
                        tmp[char] += num
                    else:
                        tmp[char] += mul
                for char in tmp:
                    stack.append(char)
                    stack.append(str(tmp[char]))
            else:
                stack.append(formula[i])
                i += 1
        tmp = Counter()
        while stack:
            char = stack.pop()
            if char.isdigit():
                tmp[stack.pop()] += int(char)
            else:
                tmp[char] += 1
        lis = []
        nu = []
        for char in tmp:
            lis.append(char)
        lis.sort()
        ans = ''
        for char in lis:
            ans += char
            if tmp[char] > 1:
                ans += str(tmp[char])
            nu.append(tmp[char])
        return [lis, nu]


def file_name(file) -> list:
    a = Solution()
    infos = []
    regex_1 = r"(.*)_(\d+)[\n\.\s*]"
    regex_2 = r"(.*)_on"
    regex_3 = r"(.*)\.outmol"
    try:
        d = re.findall(regex_1, file)[0]
        name = d[0]
        b = int(d[1])
    except Exception:
        try:
            d = re.findall(regex_2, file)[0]
            name = d
            b = 1
        except Exception:
            d = re.findall(regex_3, file)[0]
            name = d
            b = 1
    c = sum(a.countOfAtoms(name)[1])
    infos.append(name)  # 名称
    infos.append(c)  # 名称元素个数
    infos.append(b)  # 吸附分子个数
    infos.append(b * c)  # 总吸附原子个数
    return infos


def main():
    path = "./so2_outmol"
    files = os.listdir(path)
    for file in files:
        print(file)
        if not os.path.isdir(file):
            infos = file_name(file)
            print(infos)


if __name__ == "__main__":
    main()
