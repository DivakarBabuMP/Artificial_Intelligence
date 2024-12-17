INF = float('inf')

def alpha_beta_pruning(depth, node_index, is_maximizer, values, alpha, beta, max_depth):
    if depth == max_depth:
        return values[node_index]
    if is_maximizer:
        best = -INF
        for i in range(2):
            value = alpha_beta_pruning(depth + 1, node_index * 2 + i, False, values, alpha, beta, max_depth)
            best = max(best, value)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = INF
        for i in range(2):
            value = alpha_beta_pruning(depth + 1, node_index * 2 + i, True, values, alpha, beta, max_depth)
            best = min(best, value)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

if __name__ == "__main__":
    values = list(map(int, input("Enter leaf node values separated by spaces: ").split()))
    max_depth = int(input("Enter the maximum depth of the tree: "))
    alpha = -INF
    beta = INF
    result = alpha_beta_pruning(0, 0, True, values, alpha, beta, max_depth)
    print("The optimal value is:", result)

