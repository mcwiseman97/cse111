
def main():
    
    province_list = read_provinces("CSE111/W05/provinces.txt")
    print(province_list)


def read_provinces(file_location):
    province_list = []
    with open(file_location, mode="rt") as provinces_file:
        for line in provinces_file:
            clean_line = line.strip()
            province_list.append(clean_line)
    return province_list


if __name__ == "__main__":
    main()