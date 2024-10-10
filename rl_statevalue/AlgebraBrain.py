import numpy as np
from Agent import Agent
from Direction import Direction
from Grid import Grid

class Brain():
    def __init__(self, agent:Agent, grid:Grid, discount_factor):
        self.Agent = agent
        self.Grid = grid
        self.Gamma = discount_factor

    def build_transition_matrix(self) -> np.ndarray:
        grid_size = self.Grid.DIMENSION
        num_states = grid_size * grid_size
        P = np.zeros((num_states, num_states))

        for i in range(grid_size):
            for j in range(grid_size):
                current_state = i*grid_size + j
                neighbors = []
                #Add valid neighbors
                if i > 0: # North
                    neighbors.append((i-1) * grid_size + j)
                if i < grid_size-1: # South
                    neighbors.append((i+1)*grid_size+j)
                if j > 0: # West
                    neighbors.append(i*grid_size + (j-1))
                if j < grid_size - 1: # East
                    neighbors.append(i*grid_size + (j+1))

                # Assign equal probability to all valid moves
                prob = 1/len(neighbors) if neighbors else 0
                for neighbor in neighbors:
                    P[current_state, neighbor] = prob

        print("[LOG] Transition Matrix P built")
        return P

    def get_rewards_vector(self) -> np.ndarray:
        """Flatten rewards grid into a vector."""
        rewards_vector = self.Grid.rewards.flatten()
        print("[LOG] Rewards vector created: ", rewards_vector)
        return rewards_vector

    def solve_bellman_equation(self, P: np.ndarray, R: np.ndarray) -> np.ndarray:
        I = np.eye(len(P))
        try:
            V = np.linalg.inv(I-self.Gamma * P).dot(R) # (I-gamma*P)^-1 * R
            print("[LOG] State values solved using matrix.")
        except np.linalg.LinAlgError:
            raise ValueError("[ERROR] Could not invert the matrix. Check the transition probabilities.")
        return V

    def update_state_values(self)->None:
        P = self.build_transition_matrix()

        R = self.get_rewards_vector()

        new_state_values = self.solve_bellman_equation(P,R)
        self.Grid.states = new_state_values.reshape(self.Grid.DIMENSION, self.Grid.DIMENSION)
        print("[LOG] State values updated in grid.")

if __name__ == "__main__":
    test_grid = Grid(3)
    test_agent = Agent(test_grid)
    import numpy as np
from rl_statevalue.Agent import Agent, Direction
from rl_statevalue.Grid import Grid

class Brain():
    def __init__(self, agent: Agent, grid: Grid, discount_factor: float = 0.7) :
        self.Agent = agent 
        self.Grid = grid 
        self.Gamma = discount_factor
        

    def updateStateValues(self) -> None:
        """Update state values using Bellman's Equation"""
        new_state_values = np.copy(self.Grid.states)
        for i in range(self.Grid.DIMENSION-1):
            for j in range(self.Grid.DIMENSION-1):
                current_position = (i,j)
                print(f"[*LOG*] Calculating value for state {current_position}")
                total_state_value = 0

                for action in Direction:
                    # Get next state (N) and probability (P)
                    N = self.getNextState(current_position, action)
                    R = self.getReward((N[0],N[1]))
                    P = self.getPolicy()
                    state_action_value = P*(R+(self.Gamma*self.Grid.states[N[0], N[1]]))
                    total_state_value += state_action_value
                new_state_values[i,j]=total_state_value
                print(f"[LOG] State Value for {current_position} = {total_state_value}")
        self.Grid.states = new_state_values
            

    def getNextState(self, position: tuple[int,int], action: Direction) -> tuple[int, int]:
        """Returns the next state (as a tuple coordinate) based on current position and action."""
        delta = action.value
        new_position = (position[0]+delta[0], position[1]+delta[1])
        print(f"[LOG] Next State at Position: {new_position}")
        if (new_position[0] >= 3 or new_position[1] >= 3):
            raise ValueError(f"[ERROR] State {new_position} is out of bounds")
        return (position[0]+delta[0], position[1]+delta[1])

    def getReward(self, position: tuple[int,int]):
        """Returns the reward for a given coordinate"""
        if not self.Grid.rewards_set:
            raise ValueError("Rewards have not been specified. Please initialize using '[grid_variable].setRewards([numpy array])'")

        # Check if the agent will "bounce"
        if (position[0] < 0 or position[0] >= self.Grid.rewards.shape[0] or position[1] < 0 or position[1] >= self.Grid.rewards.shape[1]):
            return -1
        
        return self.Grid.rewards[position[0],position[1]]

    def getPolicy(self) -> float:
        return 0.25

    def updatePolicy(self) -> None:
        ... 


if __name__ == "__main__":
    test_grid = Grid(3)
    test_agent = Agent(test_grid)

    # test_grid.setRewards(np.array([[0,5],[0,0]]))
    test_grid.setRewards(np.array([[0,0,0],[0,5,0],[0,0,0]]))
    test_brain = Brain(test_agent, test_grid)

    test_brain.updateStateValues()
    test_grid.print()

            
