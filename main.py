import intep as itp

name = input("Запускаемый файл: ")

with open(f"{name}", "r", encoding="utf-8") as file:
    content = file.read()

itp.run(content, False)
while True: pass
