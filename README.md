# workspace-testbed
trying workspace features

## Presence Overview Feature

This repository includes a feature to display the presence of people in the office for the next two weeks based on the zfdm calendar.

### How to Use

1. Ensure you have the necessary credentials to access the zfdm calendar.
2. Create a `names.txt` file in the same directory as `main.py` and add the fixed vocabulary of people's names, one per line.
3. Run the `main.py` script.
4. The script will fetch items from the zfdm calendar, parse them for people names, and determine their presence in the office based on the event descriptions.
5. If the event description starts with a name from the vocabulary, it is considered as a "not in the office" day. For all other days, they are considered as "present" days.
6. The presence information for the next two weeks will be displayed in an easy-to-understand way.

### Example Output

```
Presence overview for the next two weeks:
2023-04-01: (nobody)
2023-04-02: (nobody)
2023-04-03: Alice
2023-04-04: Alice
2023-04-05: Bob
2023-04-06: (nobody)
2023-04-07: (nobody)
2023-04-08: (nobody)
2023-04-09: (nobody)
2023-04-10: (nobody)
2023-04-11: (nobody)
2023-04-12: (nobody)
2023-04-13: (nobody)
2023-04-14: (nobody)
2023-04-15: (nobody)
```
