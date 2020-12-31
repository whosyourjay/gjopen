import sys

def median(arr):
    n = len(arr)
    if n % 2 == 1:
        return sorted(arr)[n//2]
    return (sorted(arr)[n//2 - 1] + sorted(arr)[n//2])/2

def brier(vals, truth):
    total = 0
    for pos in range(answer_count):
        total += vals[pos]**2 * (100 - truth[pos]) \
            + (100 - vals[pos])**2 * truth[pos]
    return total

# 1 arg
question = sys.argv[1]

pros = set()
with open('pros', 'r') as f:
    for line in f:
        pros.add(line.strip())

# Load guesses and filter pros
# Todo keep order
last_guess = {}
pro_guess = {}
with open('gjo-' + question, 'r') as f:
    for line in f:
        name, *vals = line.split()
        last_guess[name] = tuple(map(int, vals))
        if name in pros:
            pro_guess[name] = tuple(map(int, vals))

f.close()

answer_count = len(list(pro_guess.values())[0])

if len(pro_guess) < 3:
    print("too little data")
    exit(0)

print("%s pros" % len(pro_guess))
for name in pro_guess:
    print("%s %s" % (name, pro_guess[name]))

# Find the median in each bin for pros
all_vals = [[] for _ in range(answer_count)]
for vals in list(pro_guess.values()):
    for pos in range(answer_count):
        all_vals[pos].append(vals[pos])
med_vals = [median(vals) for vals in all_vals]

# Normalize
denom = sum(med_vals)
your_vals = [round(val*100/denom, 1) for val in med_vals]
print(your_vals)

scores = []
for name in last_guess:
    score = brier(last_guess[name], your_vals)/10**6
    if score > 2:
        continue
    scores.append(score)
    #print("%s %s %.3f" % (name, ' '.join(map(str, last_guess[name])), score))

print(sorted(scores))
med_score = median(scores)
your_score = brier(your_vals, your_vals)/10**6

print("crowd score %.3f" % med_score)
print("your score %.3f" % your_score)
print("diff score %.3f" % (med_score - your_score))
