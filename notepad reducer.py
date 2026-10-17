#!/usr/bin/env python3

import sys

current_rating = None
current_count = 0

for line in sys.stdin:

    line = line.strip()

    if not line:
        continue

    rating, count = line.split("\t")

    count = int(count)

    if current_rating == rating:
        current_count += count

    else:

        if current_rating is not None:
            print(f"{current_rating}\t{current_count}")

        current_rating = rating
        current_count = count

if current_rating is not None:
    print(f"{current_rating}\t{current_count}")