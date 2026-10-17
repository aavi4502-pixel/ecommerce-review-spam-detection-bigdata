#!/usr/bin/env python3

import sys
import json

for line in sys.stdin:
    try:
        review = json.loads(line)

        rating = review.get("overall")

        if rating is not None:
            print(f"{rating}\t1")

    except json.JSONDecodeError:
        continue