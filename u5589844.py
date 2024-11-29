import random

class Bot(object):
    def __init__(self):
        self.name = "5589844"  
        self.history = []

    def get_bid(
        self,
        current_round,
        bots,
        winner_pays,
        artists_and_values,
        round_limit,
        starting_budget,
        painting_order,
        target_collection,
        my_bot_details,
        current_painting,
        winner_ids,
        amounts_paid,
    ):
        """Strategy for collection type games.

        Parameters:
        current_round(int): 			The current round of the auction game
        bots(dict): 					A dictionary holding the details of all of the bots in the auction
                                                                        For each bot, you are given these details:
                                                                        bot_name(str):		The bot's name
                                                                        bot_unique_id(str):	A unique id for this bot
                                                                        paintings(dict):	A dict of the paintings won so far by this bot
                                                                        budget(int):		How much budget this bot has left
                                                                        score(int):			Current value of paintings (for value game)
        winner_pays(int):				Rank of bid that winner plays. 1 is 1st price auction. 2 is 2nd price auction.
        artists_and_values(dict):		A dictionary of the artist names and the painting value to the score (for value games)
        round_limit(int):				Total number of rounds in the game - will always be 200
        starting_budget(int):			How much budget each bot started with - will always be 1001
        painting_order(list str):		A list of the full painting order
        target_collection(list int):	A list of the type of collection required to win, for collection games - will always be [3,2,1]
                                                                        [5] means that you need 5 of any one type of painting
                                                                        [4,2] means you need 4 of one type of painting and 2 of another
                                                                        [3,2,1] means you need 3 of one type of painting, 2 of another, and 1 of another
        my_bot_details(dict):			Your bot details. Same as in the bots dict, but just your bot.
                                                                        Includes your current paintings, current score and current budget
        current_painting(str):			The artist of the current painting that is being bid on
        winner_ids(list str):			A list of the ids of the winners of each round so far
        amounts_paid(list int):			List of amounts paid for paintings in the rounds played so far

        Returns:
        int:Your bid. Return your bid for this round.
        """
        # Initialization and strategy definition
        my_budget = my_bot_details["budget"]
        essential_paintings = self.identify_essential_paintings(my_bot_details["paintings"], target_collection)
        late_game = current_round > round_limit * 0.75  # Define late game phase

        # Analyze opponents' bidding behavior and adjust bid
        adjusted_bid = self.analyze_and_adjust_bid(bots, my_budget, essential_paintings, late_game, current_painting)

        # Adjust bid based on the auction type
        if winner_pays == 2:  # Adjust for second-price auction
            adjusted_bid *= 1.1

        # Ensure the bid does not exceed the available budget
        return min(int(adjusted_bid), my_budget)

    def identify_essential_paintings(self, my_paintings, target_collection):
        """
        Identifies paintings that are essential to winning the collection game.
        """
        # Check if the bot has completed the winning collection
        if self.check_winning_collection(my_paintings):
            return []

        essentials = []
        for artist, amount in my_paintings.items():
            if amount < max(target_collection):
                essentials.append(artist)
        return essentials

    def check_winning_collection(self, my_paintings):
        """
        Check if the bot has completed the winning collection.
        """
        # Define the winning combination
        winning_combination = [3, 3, 1, 1]

        # Count the number of paintings for each artist
        artist_counts = list(my_paintings.values())

        # Check if the bot has the winning combination
        return artist_counts == winning_combination

    def analyze_and_adjust_bid(self, bots, my_budget, essential_paintings, late_game, current_painting):
        """
        Analyze opponents' behavior and adjust bid to maximize chances of winning.
        """
        # Placeholder logic for analyzing opponents and adjusting bid
        avg_opponent_bid = self.calculate_average_opponent_bid(bots)
        opponent_budgets = [bot["budget"] for bot in bots if bot["bot_unique_id"] != self.name]
        avg_opponent_budget = sum(opponent_budgets) / len(opponent_budgets) if opponent_budgets else my_budget

        # Adjust bid based on opponent's bidding patterns and budget levels
        adjusted_bid = my_budget * 0.1  # Default conservative bid
        if avg_opponent_bid > adjusted_bid:
            adjusted_bid = avg_opponent_bid + 1  # Outbid opponents if their average bid is higher
        if avg_opponent_budget > my_budget:
            adjusted_bid *= 1.1  # Increase bid if opponents have higher budgets

        # Adjust bid based on the importance of the current painting and game phase
        if current_painting in essential_paintings:
            adjusted_bid = max(adjusted_bid, my_budget * 0.2)  # More aggressive bid for essential paintings
        if late_game:
            adjusted_bid *= 1.2  # Increase bid in the late game

        return adjusted_bid

    def calculate_average_opponent_bid(self, bots):
        """
        Calculate the average bid of opponents.
        """
        opponent_bids = [bot["last_bid"] for bot in bots if bot.get("name") != self.name and "last_bid" in bot]
        if opponent_bids:
            return sum(opponent_bids) / len(opponent_bids)
        else:
            return 0