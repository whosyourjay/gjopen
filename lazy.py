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

# Track when guess was made
time = 0
with open('gjo-' + question, 'r') as f:
    for line in f:
        name, *vals = line.split()
        last_guess[name] = tuple(map(int, vals))
        if name in pros:
            pro_guess[name] = [time] + list(map(int, vals))
        time += 1

f.close()

# Nice to look at these in order 
pros_by_time = [[pro, *pro_guess[pro]] for pro in pro_guess]
pros_by_time = sorted(pros_by_time, key=lambda x: x[1])
print("%s pros" % len(pro_guess))
for pro in pros_by_time:
    print(pro)

if len(pro_guess) < 1:
    print("too little data")
    exit(0)

answer_count = len(list(pro_guess.values())[0]) - 1

# Find the median in each bin for pros
all_vals = [[] for _ in range(answer_count)]
# Even pros have stale guesses
for _, _, *vals in pros_by_time[-5:]:
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
    scores.append(round(score, 3))
    #print("%s %s %.3f" % (name, ' '.join(map(str, last_guess[name])), score))

mid = len(scores)//2
print(sorted(scores)[mid-10:mid+1])
med_score = median(scores)
your_score = brier(your_vals, your_vals)/10**6

print("crowd score %.3f" % med_score)
print("your score %.3f" % your_score)
print("diff score %.3f" % (med_score - your_score))
