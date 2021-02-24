# Expand here. The value from evalHand is added to the win%

def evalHand(Hand, street):
    extra_prob = 0
    if street == "preflop":
        return 0
    # Suited
    if Hand[0].suit == Hand[1].suit:
        extra_prob += 0.01

    # Connectors
    if abs(Hand[0].value - Hand[1].value) == 1:
        extra_prob += 0.01

    return extra_prob
