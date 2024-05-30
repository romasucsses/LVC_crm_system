def generate_code(pk: int) -> list:
    number_of_digits = 8
    results_list = []
    base_numbers = [11000, 1000]

    try:
        for base_number in base_numbers:
            number = base_number + pk
            zeros_need_before = (number_of_digits - len(str(number))) * '0'
            code = f'F{zeros_need_before}{number}'
            results_list.append(code)

        return results_list

    except Exception as e:
        print('Something Wrong, Generation of code is Failed', e)
