def learn_theta(data, colors):
    # single pass: track the largest blue and smallest red
    max_blue = None
    min_red = None

    for x, c in zip(data, colors):
        if c == 'blue':
            max_blue = x if max_blue is None else max(max_blue, x)
        elif c == 'red':
            min_red = x if min_red is None else min(min_red, x)
        else:
            raise ValueError(f"Unknown color: {c}")

    if max_blue is None or min_red is None:
        raise ValueError("Must have at least one blue and one red point.")

    # by assumption, max_blue < min_red; choose any θ in [max_blue, min_red)
    return (max_blue + min_red) / 2

def compute_ell(data, colors, theta):
    red_left = 0
    blue_right = 0
    for x, c in zip(data, colors):
        if c == 'red':
            if x <= theta:
                red_left += 1
        elif c == 'blue':
            if x > theta:
                blue_right += 1
        else:
            raise ValueError(f"Unknown color: {c}")
            
    return float(red_left + blue_right)

def minimize_ell(data, colors):
    if len(data) != len(colors):
        raise ValueError("data and colors must have the same length")
    if not data:
        raise ValueError("data must be non-empty")

    best_theta = None
    best_loss = float('inf')

    for theta in data:  # O(n) candidate thetas
        loss = compute_ell(data, colors, theta)  # O(n) per candidate
        if loss < best_loss or (loss == best_loss and (best_theta is None or theta < best_theta)):
            best_loss = loss
            best_theta = theta

    return float(best_theta)

def minimize_ell_sorted(data, colors):
    n = len(data)
    if n != len(colors):
        raise ValueError("data and colors must have the same length")
    if n == 0:
        raise ValueError("data must be non-empty")

    total_blue = sum(1 for c in colors if c == 'blue')
    red_le_theta = 0          # reds counted on/before current theta
    blue_gt_theta = total_blue  # invariant target: blues strictly after current theta

    best_theta = None
    best_loss = float('inf')

    # Iterate through sorted points; after processing data[i],
    # blue_gt_theta counts blues with value > data[i]
    for i, (x, c) in enumerate(zip(data, colors), start=1):
        if c == 'blue':
            blue_gt_theta -= 1  
        elif c == 'red':
            red_le_theta += 1 
        else:
            raise ValueError(f"Unknown color: {c}")

        loss = red_le_theta + blue_gt_theta
        if loss < best_loss or (loss == best_loss and (best_theta is None or x < best_theta)):
            best_loss = loss
            best_theta = x

        # Loop invariant: after the alpha=i iteration, blue_gt_theta is the number of blue points > data[i-1]

    return float(best_theta)