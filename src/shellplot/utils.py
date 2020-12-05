

def tolerance_round(x, tol=1e-3):
    error = 1.0
    decimals = 0

    while error > tol:
        if decimals == 0:
            x_rounded = round(x)
        else:
            x_rounded = round(x, decimals)
        error = abs(x - x_rounded) / (x+1e-7)
        decimals += 1

    return x_rounded
