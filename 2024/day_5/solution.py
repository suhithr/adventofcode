import collections
import shared.constants

def solve():
    total = 0
    with open('day_5/input', 'r') as f:
        lines = f.readlines()
    
    rules = lines[:lines.index('\n')]
    updates = lines[lines.index('\n')+1:]

    # load rules
    anti_connection: dict[int, set[int]] = collections.defaultdict(set)
    for rule in rules:
        prev, nxt = list(map(int, rule.split('|')))
        anti_connection[nxt].add(prev)
    
    for upd in updates:
        upd = list(map(int, upd.split(',')))
        valid = True
        for i in range(len(upd)):
            for j in range(i, len(upd)):
                if upd[j] in anti_connection[upd[i]]:
                    valid = False
                    break
            if valid == False:
                break
        
        if valid:
            total += upd[len(upd)//2]
    
    print(total)

def solve_2():
    total = 0
    inc_updates: list[list[int]] = []
    with open('day_5/input', 'r') as f:
        lines = f.readlines()
    
    rules = lines[:lines.index('\n')]
    updates = lines[lines.index('\n')+1:]

    # load rules
    anti_connection: dict[int, set[int]] = collections.defaultdict(set)
    for rule in rules:
        prev, nxt = list(map(int, rule.split('|')))
        anti_connection[nxt].add(prev)
    
    for upd in updates:
        upd = list(map(int, upd.split(',')))
        valid = True
        for i in range(len(upd)):
            for j in range(i, len(upd)):
                if upd[j] in anti_connection[upd[i]]:
                    inc_updates.append(upd[::])
                    valid = False
                    break
            if valid == False:
                break
    
    # separating concerns

    # for incorrect updates we check
    # but now we swap pairs then restart checks
    # corrected with CLAUDE. RIP. Need to restart bubble sort completely
    for inc in inc_updates:
        changed = True
        while changed:
            changed = False
            for i in range(len(inc)):
                for j in range(i + 1, len(inc)):  # Start from i+1, not i
                    if inc[j] in anti_connection[inc[i]]:  # Fixed: inc[i] not upd[i]
                        inc[i], inc[j] = inc[j], inc[i]    # Fixed: swap inc[i] and inc[j]
                        changed = True
                        break
                if changed:
                    break

        total += inc[len(inc)//2]
    
    print(total)


    

    

if __name__ == '__main__':
    solve_2()
        
        

    