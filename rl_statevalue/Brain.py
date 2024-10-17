import numpy as np
from Agent import Agent
from Direction import Direction
from Grid import Grid

class Brain():
    def __init__(self, agent: Agent, grid: Grid, discount_factor: float = 0.7) :
        self.Agent = agent 
        self.Grid = grid 
        self.Gamma = discount_factor
        self.update_count = 0
        

    def updateStateValues(self) -> None:
        """Update state values using Bellman's Equation"""
        new_state_values = np.copy(self.Grid.states)
        ## print(f"I Range: {range(self.Grid.DIMENSION)}")
        ## print(f"J Range: {range(self.Grid.DIMENSION)}")
        for i in range(self.Grid.DIMENSION):
            for j in range(self.Grid.DIMENSION):
                current_position = (i,j)
                print(f"[*LOG*] Calculating value for state {current_position}")
                total_state_value = []

                for action in Direction:
                    # Get next state (N) and probability (P)
                    N = self.getNextState(current_position, action)
                    ## print(f"N: {N}")
                    R = self.getReward((N[0],N[1]))
                    P = self.getPolicy(current_position, action)

                    # Agent will remain in the same state if it 'bounces'
                    if N[0] >= self.Grid.DIMENSION:
                        N=(self.Grid.DIMENSION-1, N[1])
                    if N[0] < 0:
                        N=(0,N[1])
                    if N[1] >= self.Grid.DIMENSION:
                        N=(N[0], self.Grid.DIMENSION-1)
                    if N[1] < 0:
                        N=(N[0], 0)

                    state_action_value = P*(R+(self.Gamma*self.Grid.states[N[0], N[1]]))
                    total_state_value.append(state_action_value)
                new_state_values[i,j]=sum(total_state_value)
                print(f"[LOG] State Value for {current_position} = {total_state_value} = {sum(total_state_value)}")
        self.Grid.states = new_state_values
        # State value for the goal should always be 0.
        # self.Grid.states[self.Grid.Goal[0], self.Grid.Goal[1]] = 0
            

    def getNextState(self, position: tuple[int,int], action: Direction) -> tuple[int, int]:
        """Returns the next state (as a tuple coordinate) based on current position and action."""
        delta = action.value
        new_position = (position[0]+delta[0], position[1]+delta[1])
        print(f"[LOG] Next State at Position: {new_position}")
        
        return new_position

    def getReward(self, position: tuple[int,int]):
        """Returns the reward for a given coordinate"""
        if not self.Grid.rewards_set:
            raise ValueError("Rewards have not been specified. Please initialize using '[grid_variable].setRewards([numpy array])'")

        # Check if the agent will "bounce"
        if (position[0] < 0 or position[0] >= self.Grid.rewards.shape[0] or position[1] < 0 or position[1] >= self.Grid.rewards.shape[1]):
            return -1
        
        return self.Grid.rewards[position[0],position[1]]

    def getPolicy(self, current_position:tuple[int, int], action:Direction):
        i,j = current_position
        return self.Grid.policy[i][j][action.name]


    ### Need to fix this. i,j should be to self.Grid.DIMENSION, not DIMENSION-1.
    ### This means I need to update the code inside, to handle coordinates outside the respective grids.
    def updatePolicy(self) -> None:
        """Update the policy for each state."""
        for i in range(self.Grid.DIMENSION-1):
            for j in range(self.Grid.DIMENSION-1):
                current_position = (i,j)
                best_action = None
                max_value = float('-inf')

                for action in Direction:
                    next_state = self.getNextState(current_position, action)
                    reward = self.getReward(next_state)
                    # state_value = self.Grid.states[i,j]
                    state_value = reward + self.Gamma * self.Grid.states[next_state[0], next_state[1]]
                    self.Grid.policy[i][j][action.name] = state_value

                    if state_value > max_value:
                        max_value = state_value
                        best_action = action


if __name__ == "__main__":
    test_grid = Grid(3)
    test_agent = Agent(test_grid)
    # test_grid.setRewards((0,1), 5, 0)
    test_grid.setRewards((1,1), 5)

    # test_grid.setRewardsManual(np.array([[0,5],[0,0]]))
    # test_grid.setRewardsManual(np.array([[0,0,0],[0,5,0],[0,0,0]]))

    test_brain = Brain(test_agent, test_grid)
    index = 0
    # How many times do you want to update your state/policy values?
    while index < 1:
        test_brain.updateStateValues()
        test_brain.updatePolicy()
        index=index+1
    test_grid.print()
    # test_brain.updateStateValues()
    # test_brain.updatePolicy()
    # test_grid.print()
