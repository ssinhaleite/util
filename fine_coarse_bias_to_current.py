def print_current(index_coarse, fine, w_file):

    global maximum_current

    unit = coarse[index_coarse]

    max_current = float(unit.split(unit[-1])[0])

    current = fine * max_current / 256

    current_str = str(round(current, 4)) + unit[-1]

    if unit[-1] == "u":

        multiplier = 10e-6

    if unit[-1] == "p":

        multiplier = 10e-12

    if unit[-1] == "n":

        multiplier = 10e-9

    current_final = current * multiplier

    if current_final > maximum_current:
        w_file.write(
            str(index_coarse)
            + " - "
            + str(fine)
            + " - "
            + current_str
            + " = "
            + str(current_final)
            + " = "
            + str(current_final * 10e12)
            + "\n"
        )
        maximum_current = current_final


if __name__ == "__main__":

    w_file = open("/home/vleite/Desktop/fine_coarse_current3.txt", "w")

    coarse = ["15p", "105p", "820p", "6.5n", "50n", "0.4u", "3.2u", "24u"]

    fine = range(0, 256)

    maximum_current = -1

    for i in range(len(coarse)):
        for j in fine:
            print_current(i, j, w_file)
