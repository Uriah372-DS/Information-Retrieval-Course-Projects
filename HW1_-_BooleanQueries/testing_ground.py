
def evaluate(expression,inv):
    stack = []
    for ele in expression:
        if ele not in ["and", "or", "not"]:
            stack.append(ele)
        else:
            right = stack.pop()
            if isinstance(right,str):
                right=inv.get(right,[]).copy()
            left = stack.pop()
            if isinstance(left,str):
                left=inv.get(left,[]).copy()
            a=1
            if ele == "and":
                res=[]
                index_l =0
                for val in right:
                    while index_l < len(left) and left[index_l]<val:
                        index_l+=1
                    if index_l < len(left) and val == left[index_l]:
                        res.append(val)
                        index_l+=1
                stack.append(res)
            elif ele == 'or':
                # finds value in left that are not in right, and inserts them in place
                index_r = 0
                for val in left:
                    while index_r < len(right) and right[index_r] < val:
                        index_r += 1
                    if index_r < len(right) and right[index_r] != val:
                        right.insert(index_r, val)
                        index_r += 1
                    if index_r >= len(right):
                        right.append(val)
                stack.append(right)
            elif ele == 'not':
                index_l = 0
                for val in right:
                    while index_l < len(left) and left[index_l] < val:
                        index_l += 1
                    if index_l < len(left) and val == left[index_l]:
                        left.pop(index_l)
                stack.append(left)

    # return final answer.
    return stack.pop()