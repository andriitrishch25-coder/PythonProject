def validate_brackets(text: str) -> str:
    stack = []
    matching = {')': '(', '}': '{', '>': '<'}
    opening = set(matching.values())
    errors = []

    for i, char in enumerate(text):
        if char in opening:
            stack.append((char, i))
        elif char in matching:
            if not stack:
                errors.append(i)
            else:
                top_char, top_i = stack.pop()
                if top_char != matching[char]:
                    errors.append(i)
                    # Якщо дужка не збігається, відкриваючу теж вважаємо хибною
                    errors.append(top_i)


    for char, i in stack:
        errors.append(i)

    if errors:
        errors = sorted(list(set(errors)))
        positions_str = ", ".join(map(str, errors))


        marker = [' '] * len(text)
        for p in errors:
            marker[p] = '^'
        visual = ''.join(marker)

        error_message = (
            f"Дужки незбалансовані на позиціях {positions_str}\n"
            f"{text}\n"
            f"{visual}"
        )
        raise ValueError(error_message)

    return "Строка валідна"


def main():
    text = input("Введіть строку: ")
    try:
        result = validate_brackets(text)
        print(result)
    except ValueError as e:
        print(e)
        raise


if __name__ == "__main__":
    main()