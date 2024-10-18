# workspace-testbed
trying workspace features

## Presence Overview Feature

This repository includes a feature to display the presence of people in the office for the next two weeks based on a calendar URL specified in `credentials/calendars.py`.

### How to Use

1. Ensure you have the necessary credentials to access the calendar URL specified in `credentials/calendars.py`.
2. Create a `names.txt` file in the `credentials` directory and add the fixed vocabulary of people's names, one per line.
3. Run the `main.py` script.
4. The script will fetch items from the calendar URL, parse them for people names, and determine their presence in the office based on the event descriptions.
5. If the event description contains a name from the vocabulary, it is considered as a "not in the office" day. For all other days, they are considered as "present" days.
6. The presence information for the next two weeks will be displayed in an easy-to-understand way.

### Example Output

```
Presence overview for the next two weeks:
Monday, 01. May 2023: Alice, Bob
Tuesday, 02. May 2023: Alice, Bob
Wednesday, 03. May 2023: Alice, Bob
Thursday, 04. May 2023: Alice, Bob
Friday, 05. May 2023: Alice, Bob
Monday, 08. May 2023: Alice, Bob
Tuesday, 09. May 2023: Alice, Bob
Wednesday, 10. May 2023: Alice, Bob
Thursday, 11. May 2023: Alice, Bob
Friday, 12. May 2023: Alice, Bob
Monday, 15. May 2023: Alice, Bob
Tuesday, 16. May 2023: Alice, Bob
Wednesday, 17. May 2023: Alice, Bob
Thursday, 18. May 2023: Alice, Bob
Friday, 19. May 2023: Alice, Bob
```
