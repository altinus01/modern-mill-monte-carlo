from mtg_mill_simulation.code.game import game
import mtg_mill_simulation.code.game_params as game_params
import pandas as pd
import os

def sim(sim_number:int=1, removal_prio:float=0)->list[dict]:
    """Simulates sim_number times the game function.

    Parameters:
        sim_number: int, default=1
        removal_prio: float, default=0

    Returns:
    list[dict]:[{
        "game_number": int,
        "start": "str",
        "kill_turn": float|None,
        "actions": list
        },{...}]
    """
    results=[]
    for i in range(1, sim_number + 1):
        result = game(removal_prio)
        if result is not None:
            result["game_number"] = i
            results.append(result)#inserts game number
    return results

script_dir = os.path.dirname(os.path.abspath(__file__))
print("Start simulation without removal")
simulation=sim(100000,removal_prio=0)
print("Finished simulation without removal")
print("Exporting to no_rem.csv file")
df = pd.DataFrame(simulation)
output_path = os.path.join(script_dir, "..", "data", "no_rem.csv")
df.to_csv(output_path, sep=";", index=False)
print("Exporting done")

print("Start simulation at half removal.")
simulation=sim(100000,removal_prio=0.5)
print("Finished simulation at half removal.")
print("Exporting to half_rem.csv file")
df = pd.DataFrame(simulation)
output_path = os.path.join(script_dir, "..", "data", "half_rem.csv")
df.to_csv(output_path, sep=";", index=False)
print("Exporting done")

print("Start simulation at full removal.")
simulation=sim(100000,removal_prio=1)
print("Finished simulation at full removal.")
print("Exporting to full_rem.csv file")
df = pd.DataFrame(simulation)
output_path = os.path.join(script_dir, "..", "data", "full_rem.csv")
df.to_csv(output_path, sep=";", index=False)
print("Exporting done")

print("Simulations finished!")
