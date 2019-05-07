## THIS FILE MADE ONLY FOR TESTING PURPOSES

import random
import string

n = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))

f = open(n, "w")
f.close()