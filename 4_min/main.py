from amulet_env import CardGameEnv

def main():
    env = CardGameEnv()

    # Run an episode (assuming the game ends when there are no more cards in the deck)
    done = False
    while not done:
        env.render()
        current_player = env.state['current_player']
        action_keep = int(input(f"Player {current_player}, enter action (0: Discard, 1: Keep): "))
        if action_keep:
            action_index = int(input(f"Player {current_player}, enter index of the card to discard (0-4): "))
        else:
            action_index = 0
        _, reward, done, _ = env.step((action_keep, action_index))

    print("Game Over")

if __name__ == "__main__":
    main()
