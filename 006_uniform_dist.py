p=[0.2, 0.2, 0.2, 0.2, 0.2]

world=['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'red']
motions = [1, 1]
pMiss = 0.2
pHit = 0.6
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def sense(p, Z):
    q = []
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1 - hit) * pMiss))

    s = sum(q)
    for i in range(len(p)):
        q[i] = q[i] / s
    return q

def move(p, U):
    # current_value = p[0]
    # array_length = len(p)
    # for i in range(array_length):
    #     tmp = p[(i + U) % array_length]
    #     p[(i + U) % array_length] = current_value
    #     current_value = tmp
    q = []
    array_length = len(p)
    for i in range(array_length):
        s = pExact * p[(i - U) % array_length]
        s = s + pOvershoot * p[(i - U - 1) % array_length]
        s = s + pUndershoot * p[(i - U + 1) % array_length]
        q.append(s)
    return q

# for k in range(len(measurements)):
#     p = sense(p, measurements[k])

for k in range(len(measurements)):
    p = sense(p, measurements[k])
    p = move(p, motions[k])

print(p)
