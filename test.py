import sys

print("Сколько модулей в sys.modules при старте:", len(sys.modules))
print()

print("Примеры модулей в кэше при запуске:")
for name in sys.modules.keys():
    print("-", name)