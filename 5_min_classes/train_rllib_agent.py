import ray
from ray import tune

def main():
    ray.init()
    
    tune.run(
        "PPO",
        stop={"training_iteration": 20},
        config={
            "env": "CardGame-v0",
            "num_gpus": 0,
            "num_workers": 1,
            "framework": "torch",
        },
    )

if __name__ == "__main__":
    main()
