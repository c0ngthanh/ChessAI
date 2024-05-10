import math

# Constant K
K = 25
# Player elo 
player_rating = 1200
# Agent elo
agent_rating = 1000

# Expected score func
def expected_score(rating_a, rating_b):
    return 1 / (1 + math.pow(10, (rating_b - rating_a) / 400))

# Update elo rating func
def update_elo_rating(rating, expected_score, actual_score):
    return rating + K * (actual_score - expected_score)


# Math result for player (1: win, 0.5: draw, 0: lose)
result = 1

# Expected score of player
expected1 = expected_score(player_rating, agent_rating)

# Expected score of agent
expected2 = expected_score(agent_rating, player_rating)

# Update elo
player_rating = update_elo_rating(player_rating, expected1, result)
agent_rating = update_elo_rating(agent_rating, expected2, 1 - result)

# In kết quả
print("Elo rating player:", player_rating)
print("Elo rating agent:", agent_rating)