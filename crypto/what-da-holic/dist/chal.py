from secret import FLAG


def main() -> None:
    flag = FLAG.encode() if isinstance(FLAG, str) else bytes(FLAG)

    if not flag.startswith(b"holic{") or not flag.endswith(b"}"):
        raise ValueError("Invalid flag format")

    m = int.from_bytes(flag, "big")
    bits = len(flag) * 8
    n = (1 << bits) - 1
    e = 65537
    c = n - m

    print(f"n = {n}")
    print(f"e = {e}")
    print(f"c = {c}")


if __name__ == "__main__":
    main()
