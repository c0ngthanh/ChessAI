import math

# Constant K
K = 25

result = [1,1,1,1,1,1,1,1,1,1]

# Expected score func
def expected_score(rating_a, rating_b):
    return 1 / (1 + math.pow(10, (rating_b - rating_a) / 400))

# Update elo rating func
def update_elo_rating(rating, expected_score, actual_score):
    return rating + K * (actual_score - expected_score)

def elo(agent1_rating, agent2_rating):
    for i in range(10):
        # Expected score of player
        expected1 = expected_score(agent1_rating, agent2_rating)

        # Expected score of agent
        expected2 = expected_score(agent2_rating, agent1_rating)

        # Update elo
        agent1_rating = update_elo_rating(agent1_rating, expected1, result[i])
        agent2_rating = update_elo_rating(agent2_rating, expected2, 1 - result[i])

    # In kết quả
    print("Elo rating agent white:", agent1_rating)
    print("Elo rating agent black:", agent2_rating)

    return agent1_rating, agent2_rating