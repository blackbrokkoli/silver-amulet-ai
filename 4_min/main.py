from amulet_env import CardGameEnv
import random

def random_agent_action():
    keep = random.choice([0, 1])
    discard_index = random.choice(range(5)) if keep else 0
    return keep, discard_index

def main():
    env = CardGameEnv()

    # Run an episode (assuming the game ends when there are no more cards in the deck)
    done = False
    while not done:
        env.render()
        current_player = env.state['current_player']

        if current_player == 0:
            action_keep = int(input(f"Player {current_player}, enter action (0: Discard, 1: Keep): "))
            if action_keep:
                action_index = int(input(f"Player {current_player}, enter index of the card to discard (0-4): "))
            else:
                action_index = 0
        else:
            action_keep, action_index = random_agent_action()
            print(f"Player {current_player} random agent action: {(action_keep, action_index)}")

        _, reward, done, _ = env.step((action_keep, action_index))

    print("Game Over. Reward: ", reward)

if __name__ == "__main__":
    main()
