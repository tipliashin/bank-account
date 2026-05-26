def read_non_empty_lines(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield line.strip()
    except FileNotFoundError:
        return
