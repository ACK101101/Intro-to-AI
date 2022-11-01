def check_satisfied(assignments, words):                        # check if problem is satisfied; [1]=1 means not all assigned, 0 means all assigned
    # turn each word into a number
    numbers = []
    for word in words:
        number = ''
        w = word.split(' ')
        for c in w:
            digit = assignments[c]
            if digit == -1:                     return False, 1      # not all assignments made
            number = number+str(digit)
        numbers.append(int(number))
    #print("numbers: ", numbers)
    if numbers[0] + numbers[1] == numbers[2]:   return True, 0    
    return False, 0

def assign_time(assignments, domains):                             # pick a variable to assign a value to
    chosen_0 = []
    for letter in assignments.keys():               # get letters that need assignments
        if assignments[letter] == -1:
            chosen_0.append(letter)
    #print("chosen_0: ", chosen_0)
    if len(chosen_0) == 1:          return chosen_0[0]

    d_size = 10000
    chosen_1 = []
    for letter in chosen_0:                         # most-constrained (smallest remaining domain)
        if len(domains[letter]) <= d_size:
            chosen_1.append(letter)
            d_size = len(domains[letter])
    #print("chosen_1: ", chosen_1)
    if len(chosen_1) == 1:          return chosen_1[0]

    '''largest_count = 0
    chosen_2 = []
    for letter in chosen_1:                         # most-constraining (appears most in remaining domains)
        count = 0
        for c in chosen_0:
            if letter in domains[c]:
                count += 1
        if count >= largest_count:
            chosen_2.append(letter)
            largest_count == count
    #print("chosen_2: ", chosen_2)
    if len(chosen_2) == 1:          return chosen_2[0]'''

    smallest = chosen_1[0]
    for letter in chosen_1:                         # choose alphabetically
        if letter < smallest:
            smallest = letter

    return smallest

def emptyCheck(domains):                           # checks if all domains are empty
    all_e = True
    for d in domains.keys():
        if len(domains[d]) > 1:
            all_e = False
            break
    return all_e

def forwardCheck(assignments, domains, words):             # update domains
    new_domains = domains.copy()

    nums = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}     
    for a in assignments.keys():                    # nums is dict of nums not used
        if assignments[a] in nums.keys():
            del nums[assignments[a]]

    for b in assignments.keys():
        if assignments[b] == -1:
            new_domains[b] = list(nums.keys())
        else:
            new_domains[b] = [assignments[b]]
    print('new domains: ', new_domains)

    '''new_domains = domains.copy()
    for d in new_domains.keys():
        legal_d = nums.copy()
        if assignments[d] != -1:
            legal_d[assignments[d]] = 0
        legal = list(legal_d.keys())
        legal.sort()
        new_domains[d] = legal''' 
    
    return new_domains


def csp(assignments, domains, words):
    satisfied, assi = check_satisfied(assignments, words)
    if satisfied == True:                   return assignments

    select_letter = assign_time(assignments, domains)
    letter_domain = domains[select_letter]

    for v in letter_domain:
        new_assign = assignments.copy()
        new_assign[select_letter] = v

        f_check_domains = forwardCheck(new_assign, domains, words)
        #print("f_check_domains: ", f_check_domains)
        check_empty = emptyCheck(f_check_domains)
        #print("check empty: ", check_empty)
        check_add, check_ass = check_satisfied(new_assign, words)
        go = ((check_add == True) and (check_ass == 0)) or ((check_add == False) and (check_ass == 1))

        if (check_empty == False):
            #print("Var {l} assigned value {va}".format(l=select_letter, va=v)) 
            #print("Domains: {d}".format(d=f_check_domains))
            result = csp(new_assign, f_check_domains, words)
            if result != False:
                return result
    
    return False


X = ['D', 'O', 'N', 'A', 'L', 'G', 'E', 'R', 'B', 'T']
D = {'D': [5], 
    'O': [0, 1, 2, 3, 4, 6, 7, 8, 9], 
    'N': [0, 1, 2, 3, 4, 6, 7, 8, 9], 
    'A': [0, 1, 2, 3, 4, 6, 7, 8, 9], 
    'L': [0, 1, 2, 3, 4, 6, 7, 8, 9], 
    'G': [1, 2, 3, 4, 6, 7, 8, 9], 
    'E': [0, 1, 2, 3, 4, 6, 7, 8, 9], 
    'R': [1, 2, 3, 4, 6, 7, 8, 9], 
    'B': [0, 1, 2, 3, 4, 6, 7, 8, 9], 
    'T': [0, 1, 2, 3, 4, 6, 7, 8, 9]}
assigned = {'D': 5, 'O': -1, 'N': -1, 'A': -1, 'L': -1, 'G': -1, 'E': -1, 'R': -1, 'B': -1, 'T': -1}
names = ['D O N A L D', 'G E R A L D', 'R O B E R T']
#prev_ass = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}     # 0 if not assigned, 1 if assigned
######


ans = csp(assigned, D, names)
print(ans)
#print(526485 + 197485 == 723970)