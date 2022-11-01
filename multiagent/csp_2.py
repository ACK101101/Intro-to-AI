from operator import le
from re import T


def small_add(la, lb):
    cx = 0
    f = la + lb
    if f >= 10:     cx = 1
    return f, cx

def big_add(letters):
    f0, c0 = small_add(letters['D'], letters['D'])
    f1, c1 = small_add(letters['L'], letters['L'])
    f2, c2 = small_add(letters['A'], letters['A'])
    f3, c3 = small_add(letters['N'], letters['R'])
    f4, c4 = small_add(letters['O'], letters['E'])
    f5, c5 = small_add(letters['D'], letters['G'])
    f = [f0, f1, f2, f3, f4, f5]
    c = [c0, c1, c2, c3, c4, c5]
    final = 0
    for i in range(len(f)):
        final += f[i] * 10**i
    return final

def check_assign(letters):
    for l in letters.keys():
        if letters[l] == -1:
            return False
    
    d_plus_g = big_add(letters)
    final = 0
    f = ['T', 'R', 'E', 'B', 'O', 'R']
    for i in range(len(f)):
        final += letters[f[i]] * 10**i
    if final == d_plus_g:
        return True
    return False

def choose_x(letters):
    choose_from = []
    for k, v in letters.items():
        if v == -1:     choose_from.append(k)

    priority = ['D', 'R', 'A', 'E', 'L', 'O', 'B', 'G', 'N', 'T']
    for p in priority:
        if str(p) in choose_from:
            #print("YAY")
            return p

def forward_check(letters):
    c0, c1, c2, c3, c4 = 0, 0, 0, 0, 0
    c0_f, c1_f, c2_f, c3_f, c4_f = False, False, False, False, False

    if letters['D'] != -1 and letters['T'] != -1:
        s, c = small_add(letters['D'], letters['D'])
        c0_f = True
        if c == 1:
            c0 = 1                  
            s = s - 10
        if s != letters['T']: return False
    if letters['L'] != -1 and letters['R'] != -1 and c0_f:
        s, c = small_add(letters['L'], letters['L'])
        c1_f = True
        if c == 1:
            c1 = 1                  
            s = s - 10
        if s + c0 != letters['R']:       
            return False
    if letters['A'] != -1 and letters['E'] != -1 and c1_f:
        s, c = small_add(letters['A'], letters['A'])
        c2_f = True
        if c == 1:                  
            s = s - 10
            c2 = 1
        if s + c1 != letters['E']:       
            return False
    if letters['N'] != -1 and letters['R'] != -1 and letters['B'] != -1 and c2_f:
        s, c = small_add(letters['N'], letters['R'])
        c3_f = True
        if c == 1: 
            c3 = 1                 
            s = s - 10
        if s + c2 != letters['B']:       return False
    if letters['O'] != -1 and letters['E'] != -1 and c3_f:
        s, c = small_add(letters['O'], letters['E'])
        c4_f = True
        if c == 1:                  
            c4 = c
            s = s - 10
        if s + c3 != letters['O']:       return False
    if letters['D'] != -1 and letters['G'] != -1 and letters['R'] != -1 and c4_f:
        s, c = small_add(letters['D'], letters['G'])
        if c == 1:                  
            s = s - 10
        if s + c4 != letters['R']:       return False
    return True

def empty(num_domain):
    if len(num_domain) == 0:
        return True
    return False

def csp(letters, num_domain):
    #print("letters: ", letters)
    if check_assign(letters):
        return letters
    
    if empty(num_domain):
        return False
    chosen_l = choose_x(letters)
    #print("chosen l: ", chosen_l)
    
    for v in num_domain:
        #print("chosen l: {l}, chosen v: {va}".format(l=chosen_l, va=v))
        new_letters = letters.copy()
        new_letters[chosen_l] = v
        #print("new letters: ", new_letters)
        n_num_domain = num_domain.copy()
        n_num_domain.remove(v)
        #print("new domain: ", n_num_domain)
        #print("forward_check: ", forward_check(new_letters))
        if forward_check(new_letters):
            #print("empty? ", n_num_domain)
            if empty(n_num_domain) == False:
                print("chosen l: {l}, chosen v: {va}".format(l=chosen_l, va=v))
                result = csp(new_letters, n_num_domain)
                if result != False:
                    return result
    return False

#letters = {'D': 5, 'O': -1, 'N': -1, 'A': -1, 'L': -1, 'G': -1, 'E': -1, 'R': -1, 'B': -1, 'T': -1}
letters = {'D': 5, 'O': -1, 'N': -1, 'A': 4, 'L': -1, 'G': -1, 'E': 9, 'R': -1, 'B': -1, 'T': 0}
num_domain = [0, 1, 2, 3, 4, 6, 7, 8, 9]

r = csp(letters, num_domain)
print(r)
