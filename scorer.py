import sys

question = sys.argv[1]
your_vals = list(map(int, sys.argv[2:]))
answer_count = len(your_vals)

last_guess = {}
with open('gjo-' + question, 'r') as f:
    for line in f:
        user, *vals = line.split()
        last_guess[user] = tuple(map(int, vals))

f.close()

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

scores = []
all_vals = [[] for _ in range(len(your_vals))]
for name in last_guess:
    score = brier(last_guess[name], your_vals)/10**6
    scores.append(score)
    print("%s %s %.3f" % (name, ' '.join(map(str, last_guess[name])), score))

med_score = median(scores)
your_score = brier(your_vals, your_vals)/10**6

print("crowd score %.3f" % med_score)
print("your score %.3f" % your_score)
print("diff score %.3f" % (med_score - your_score))

