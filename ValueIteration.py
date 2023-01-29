'''
adjusting the variables: gamma and noise in line 191 and 195
then run the code
the last output shows the best V-value for every field
'''



#Gridworld
height = 5
width = 5

class Vvalue:
    def __init__(self, x, y, v_value, action):
        self.x = x
        self.y = y
        self.v_value = v_value
        self.action = action

    def print_value(self):
        print("state x:%s y:%s V:%s" % (self.x, self.y, self.v_value))

class State:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.orientation = orientation

    def print_state(self):
        print("state x:%s y:%s orientation:%s " % (self.x, self.y, self.orientation))

    def action_1_forward(self):
        new_x = self.x
        new_y = self.y
        if not is_collision(self):
            if self.orientation == 'N':
                new_y = self.y + 1
            elif self.orientation == "E":
                new_x = self.x + 1
            elif self.orientation == "S":
                new_y = self.y - 1
            else:
                new_x = self.x - 1
            return -1.5, State(new_x, new_y, self.orientation)
        else:
            return False, False

    def action_2_forward(self):
        new_x = self.x
        new_y = self.y
        if not is_collision_2_forward(self):
            if self.orientation == 'N':
                new_y = self.y + 2
                if self.y + 1 == 4 and self.x == 4:
                    r = -1002
            elif self.orientation == "E":
                new_x = self.x + 2
                if self.x + 1 == 4 and self.y == 4:
                    r = -1002
            elif self.orientation == "S":
                new_y = self.y - 2
                if self.y - 1 == 4 and self.x == 4:
                    r = -1002
            else:
                new_x = self.x - 2
                if self.x - 1 == 4 and self.y == 4:
                    r = -1002
            return -2, State(new_x, new_y, self.orientation)
        else:
            return False, False

    def turn_right(self):
        return -0.5, State(self.x, self.y, self.orientation)

    def turn_left(self):
        return -0.5, State(self.x, self.y, self.orientation)


def search_state(searched_state, v_list):
    for val in v_list:
        if val.x == searched_state.x and val.y == searched_state.y:
            return v_list.index(val)
    return False


def is_collision(state):
    if state.orientation == 'N' and state.y + 1 > height:
        return True
    elif state.orientation == 'E' and state.x + 1 > width:
        return True
    elif state.orientation == "S" and state.y - 1 == 0:
        return True
    elif state.orientation == "W" and state.x - 1 == 0:
        return True
    elif state.x == 5 and state.y == 3 and state.orientation == "N":
        return True
    elif state.x == 5 and state.y == 4 and state.orientation == "S":
        return True
    elif state.x == 3 and state.y == 5 and state.orientation == "W":
        return True
    elif state.x == 2 and state.y == 5 and state.orientation == "E":
        return True

    for blocked_cell in blocked_cells:
        if state.orientation == 'N' and state.y + 1 >= blocked_cell.y > state.y and state.x == blocked_cell.x:
            return True
        elif state.orientation == 'E' and state.x + 1 >= blocked_cell.x > state.x and state.y == blocked_cell.y:
            return True
        elif state.orientation == "S" and state.y - 1 <= blocked_cell.x < state.y and state.x == blocked_cell.x:
            return True
        elif state.orientation == "W" and state.x - 1 <= blocked_cell.x < state.x and state.y == blocked_cell.y:
            return True
        else:
            return False


def is_collision_2_forward(state):
    if state.orientation == 'N' and state.y + 2 > height:
        return True
    elif state.orientation == 'E' and state.x + 2 > width:
        return True
    elif state.orientation == "S" and state.y - 2 < 1:
        return True
    elif state.orientation == "W" and state.x - 2 < 1:
        return True
    elif state.orientation == "N" and state.x == 5 and (state.y == 2 or state.y == 3):
        return True
    elif state.orientation == "S" and state.x == 5 and state.y == 4:
        return True
    elif state.orientation == "E" and (state.x == 1 or state.x == 2) and state.y == 5:
        return True
    elif state.orientation == "W" and (state.x == 3 or state.x == 4) and state.y == 5:
        return True

    for blocked_cell in blocked_cells:
        if state.orientation == 'N' and state.y + 2 >= blocked_cell.y > state.y and state.x == blocked_cell.x:
            return True
        elif state.orientation == 'E' and state.x + 2 >= blocked_cell.x > state.x and state.y == blocked_cell.y :
            return True
        elif state.orientation == "S" and state.y - 2 <= blocked_cell.x < state.y and state.x == blocked_cell.x:
            return True
        elif state.orientation == "W" and state.x - 2 <= blocked_cell.x < state.x and state.y == blocked_cell.y:
            return True
        else:
            return False

# calculate the number of possible actions
def possibilities(s, a):
    p = 0
    for act in actions:
        if act == 1:
            r, new_s = s.action_1_forward()
        elif act == 2:
            r, new_s = s.action_2_forward()
        elif act == 3:
            r, new_s = s.turn_left()
        elif act == 4:
            r, new_s = s.turn_right()
        if r:
            p = p + 1

    return p-1

#calculae the value for the wrong actions, so not the expected action
def options(current_state, current_action, v_copy):
    poss = possibilities(current_state, current_action)

    prob = 0
    if poss == 0 or noise == 0:
        return 0
    else:
        prob = noise / poss

    sum_values = 0
    for a in actions:
        if a == current_action:
            break
        elif action == 1:
            r, new_s = current_state.action_1_forward()
        elif action == 2:
            r, new_s = current_state.action_2_forward()
        elif action == 3:
            r, new_s = current_state.turn_left()
        elif action == 4:
            r, new_s = current_state.turn_right()

        if r:
            idx = search_state(new_s, v_copy)
            sum_values = sum_values + (prob * (r + gamma * v_copy[idx].v_value))
    return sum_values


gamma =
reward = 0
new_state = 0

noise = 0
probability = 1 - noise
'''
1: move 1 cell forward cost=1.5
2: move 2 cell forward cost=2
3: turn left cost=0.5
4: turn right cost=0.5
'''
orientations = ["N", "E", "S", "W"]
actions = [1, 2, 3, 4]
states = []
V = []
blocked_cells = [State(2, 2, 0), State(2, 3, 0), State(3, 2, 0)]

# initialize initial V values -> all 0, except terminate states
for i in range(1, height+1):
    for j in range(1, width+1):
        flag = True
        for s in blocked_cells:
            if s.x == i and s.y == j:
                flag = False

        if i == 5 and j == 5:
            V.append(Vvalue(i, j, 100, 0))
        elif i == 4 and j == 4:
            V.append(Vvalue(i, j, -1000, 0))
        elif flag:
            V.append(Vvalue(i, j, 0, 0))


# initialize all possible states
for i in range(1, height+1):
    for j in range(1, width+1):
        for ori in orientations:
            flag = True
            for s in blocked_cells:
                if s.x == i and s.y == j:
                    flag = False
            if (i == 4 and j == 4) or (i == 5 and j == 5):
                flag = False
            if flag:
                states.append(State(i, j, ori))


for k in range(0, 10):
    print("iteration %i" % k)
    V_copy = V.copy()

    for state in states:
        Q = {}
        for action in actions:
            if action == 1:
                reward, new_state = state.action_1_forward()
            elif action == 2:
                reward, new_state = state.action_2_forward()
            elif action == 3:
                reward, new_state = state.turn_left()
            elif action == 4:
                reward, new_state = state.turn_right()

            if reward:
                idx = search_state(new_state, V_copy)
                noise_options = options(state, action, V_copy)
                Q[action] = (probability * (reward + gamma * V_copy[idx].v_value)) + noise_options

        idx = search_state(state, V)
        best_action = 0

        if Q:
            max_q = max(Q.values())
            # list out keys and values separately
            key_list = list(Q.keys())
            val_list = list(Q.values())

            position = val_list.index(max_q)
            best_action = (key_list[position])

            actual_value = V[idx].v_value
            if actual_value < max_q:
                V[idx].v_value = max_q
                V[idx].action = best_action


        print("State x:%s y:%s orientation:%s v:%s best action:%s" % (state.x, state.y, state.orientation, max_q, best_action))

for v in V:
    v.print_value()


