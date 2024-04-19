def chunk(s, chunkSize=256, overlap=64):
    words = s.split(" ")
    return [" ".join(words[i:i+chunkSize]) for i in range(0, len(words), chunkSize - overlap)]

if __name__ == "__main__":
    cases = [
        (
            "",
            [""],
        ),
        (
            "hi",
            ["hi"],
        ),
        (
            "this is a test",
            ["this is a test"],
        ),
        (
            "this is a long test with more than ten words so that we can test overlap",
            [
                "this is a long test with more than ten words",
                "ten words so that we can test overlap",
            ],
        ),
    ]


    print("Testing chunk function.")
    for case in cases:
        input = case[0]
        expected = case[1]
        actual = chunk(input, 10, 2)
        print("\nInput: %s \nExpected: %s\nActual:   %s" % (str(input), str(expected), str(actual)))
        assert actual == expected, "%s != %s" % (actual, expected)

    print('\nAll tests passed.')

