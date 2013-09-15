'''
___README!___

THE ONLY METHOD YOU NEED TO CALL IS parseVotes(list input1, dict input2)

Specifications of parseVotes:
Inputs: (2 inputs)
    LIST of TUPLES with name and the bid for the current question
        example: [("bob", 50), ("joe", 40)]
    DICTIONARY, with the username as the key and a TUPLE of private
    and public scores as the entry
        example: {"bob":(0.6, 200), "joe":(0.75, 150)}
        
Output: A TUPLE
    -DICTIONARY with usernames and TUPLES of private/public scores UPDATED
    -An INT representing the true value of the answer to this question
'''


import math

def weightedAvg(votes, userscores):
    tot = 0
    wsum = 0
    for entry in votes:
        name = entry[0]
        tot += entry[1] * userscores[name][0]
        wsum += userscores[name][0]
    return tot/wsum

#input is list of tuples (name, vote)
def stdev(inputs):
    avg = 0
    for i in inputs:
        avg += i[1]
    avg /= len(inputs)
    dev = 0
    for i in inputs:
        diff = avg - i[1]
        dev += pow(diff, 2)
    dev /= len(inputs)
    return math.sqrt(dev)

#votes is list of tuples (name, vote)
def unweightavg(votes):
    sum = 0
    for e in votes:
        sum += e[1]
    return sum / len(votes)
    
#Returns the new Private score
#oldscore is the users hidden score (from 0-1)
#vote is the value the user bid
#trueval is the weighted average (hidden)
#avg is the nonweighted average
#stdev is stdev(list of all votes)
def newPrivateScore(oldscore, pval, vote, trueval, avg):
    perchange = (0.7 - pval) * 0.1
    if perchange < 0:
        perchange *= 0.5
        if perchange < - 0.8:
            perchange = - 0.8
        return oldscore * (1 + perchange)
    
    if abs(avg - vote) > abs(avg - trueval):
          perchange *= 1.25
    return oldscore + (1 - oldscore) * perchange

#Returns points received for answer 1 - 100
def newPublicScore(oldscore, pval):
    if pval < 0.1:
        pval = 0.1
    if pval > 10:
        pval = 10
    return oldscore + int(10/pval)

#Returns tuple (new private score, new public score)
def newScores(privatescore, publicscore, vote, avg, trueval, stdev):
    if (stdev = 0):
		pval = 0
	else:
		pval = abs((vote-trueval)/stdev)
    return (newPrivateScore(privatescore, pval, vote, trueval, avg),
            newPublicScore(publicscore, pval))

#votes is a list of tuples of (name, vote)
#userscores is a dictionary of {"name":(private, public)}
def parseVotes(votes, userscores):
    if len(votes) == 0:
        return userscores, None
    avg = unweightavg(votes)
    dev = stdev(votes)
    trueval = weightedAvg(votes, userscores)
    for entry in votes:
        name = entry[0]
        privatescore = userscores[name][0]
        publicscore = userscores[name][1]
        userscores[name] = newScores(privatescore, publicscore, entry[1],avg, trueval, dev)
    return userscores, trueval
