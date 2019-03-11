inpu = ['e', 'o', 'i', 'c', 'n', 'm']
# inpu = ['l', 'o', 'v', 'e', 's']
sara = ['a', 'e', 'i', 'o', 'u', 'y']
rep = []

state = 0

def dimen3():
    for i in range(len(inpu)):
        # 1 alphabet
        for j in range(len(inpu)):
            # 2 alphabet
            for k in range(len(inpu)):
                # 3 alphabet
                if i != j and i != k and k != j:
                    out = inpu[i] + inpu[j] + inpu[k]
                    for a in sara:
                        if a in out:
                            if out not in rep:
                                rep.append(out)
                                print(out)


def dimen4():
    for i in range(len(inpu)):
        # 1 alphabet
        for j in range(len(inpu)):
            # 2 alphabet
            for k in range(len(inpu)):
                # 3 alphabet
                for l in range(len(inpu)):
                    # 4 alphabet
                    if i != j and i != k and i != l:
                        if j != k and j!= l and k != l:
                            out = inpu[i] + inpu[j] + inpu[k] + inpu[l]
                            for a in sara:
                                if a in out:
                                    if out not in rep:
                                        rep.append(out)
                                        print(out)


def dimen5():
    for i in range(len(inpu)):
        # 1 alphabet
        for j in range(len(inpu)):
            # 2 alphabet
            for k in range(len(inpu)):
                # 3 alphabet
                for l in range(len(inpu)):
                    # 4 alphabet
                    for m in range(len(inpu)):
                        # 5 alphabet
                        if i != j and i != k and i != l and i != m:
                            if j != k and j!= l and j != m:
                                if k != l and k != m and l != m:
                                    out = inpu[i] + inpu[j] + inpu[k] + inpu[l] + inpu[m]
                                    for a in sara:
                                        if a in out:
                                            if out not in rep:
                                                rep.append(out)
                                                print(out)
                #         for n in range(len(inpu)):
                #             # 6 alphabet
                #             for o in range(len(inpu)):
                #                 # 7 alphabet
                #                 for p in range(len(inpu)):
                #                     pass

def dimen6():
    for i in range(len(inpu)):
        # 1 alphabet
        for j in range(len(inpu)):
            # 2 alphabet
            for k in range(len(inpu)):
                # 3 alphabet
                for l in range(len(inpu)):
                    # 4 alphabet
                    for m in range(len(inpu)):
                        # 5 alphabet
                        for n in range(len(inpu)):
                            # 6 alphabet
                            if i != j and i != k and i != l and i != m and i != n:
                                if j != k and j!= l and j != m and j != n:
                                    if k != l and k != m and k != n:
                                        if l != m and l != n and m != n:
                                            out = inpu[i] + inpu[j] + inpu[k] + inpu[l] + inpu[m] + inpu[n]
                                            for a in sara:
                                                if a in out:
                                                    if out not in rep:
                                                        rep.append(out)
                                                        print(out)


def dimen7():
    for i in range(len(inpu)):
        # 1 alphabet
        for j in range(len(inpu)):
            # 2 alphabet
            for k in range(len(inpu)):
                # 3 alphabet
                for l in range(len(inpu)):
                    # 4 alphabet
                    for m in range(len(inpu)):
                        # 5 alphabet
                        for n in range(len(inpu)):
                            # 6 alphabet
                            for o in range(len(inpu)):
                                # 7 alphabet
                                if i != j and i != k and i != l and i != m and i != n and i != o:
                                    if j != k and j!= l and j != m and j != n and j != o:
                                        if k != l and k != m and k != n and k != o:
                                            if l != m and l != n and l != o:
                                                if m != n and m != o and n != o:
                                                    out = inpu[i] + inpu[j] + inpu[k] + inpu[l] + inpu[m] + inpu[n] + inpu[o]
                                                    for a in sara:
                                                        if a in out:
                                                            if out not in rep:
                                                                rep.append(out)
                                                                print(out)


if __name__ == "__main__":
    dimen6()
