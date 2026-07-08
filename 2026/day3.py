import sys, string, typing

def score_1(password : str):
    score = 0

    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    return score * len(password)

def score_2(password : str):
    score = 0

    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1

    if '7' in password and all(c == '7' or not c.isdigit() for c in password):
        score += 7

    best_run = 0
    last_run = 0
    last_char = None
    for c in password:
        if c == last_char:
            last_run += 1
        else:
            best_run = max(last_run, best_run)
            last_run = 1
            last_char = c
    best_run = max(last_run, best_run)
    if best_run >= 3:
        score += best_run ** 2
    
    if 'red' in password or 'green' in password or 'blue' in password:
        score *= 3
    
    score *= len(password)
    return score

def try_append(passwords : typing.Iterable[str], char : str):
    result = sum(score_2(password + char) for password in passwords)
    return result

def main():
    passwords = tuple(map(str.strip, sys.stdin))
    print("part1 =", max(passwords, key=score_1))
    print("part2 =", max(passwords, key=score_2))
    print("part3 =", max(try_append(passwords, c) for c in string.ascii_letters + string.digits))

if __name__ == "__main__":
    main()