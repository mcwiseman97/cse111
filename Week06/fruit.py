def main():
  # Create and print a list named fruit.
  fruit_list = ["pear", "banana", "apple", "mango"]
  print(f"original: {fruit_list}")
  print(f"reversed: {fruit_list[::-1]}")

  fruit_list.append("orange")
  print(f"append orange: {fruit_list}")

  # Find where apple is in the list and insert cherry before apple.
  i = 0
  while fruit_list[i] != "apple":
    i += 1
  fruit_list.insert(i, "cherry")
  print(f"insert cherry: {fruit_list}")

  # Find banana and remove it
  fruit_list.remove("banana")
  print(f"remove banana:  {fruit_list}")

    # Find orange and remove it
  i = 0
  while fruit_list[i] != "orange":
    i += 1
  fruit_list.pop(i)
  print(f"pop orange: {fruit_list}")

  fruit_list.sort()
  print(f"sorted: {fruit_list}")

  fruit_list.clear()
  print(f"cleared: {fruit_list}")







if __name__ == "__main__":
    main()