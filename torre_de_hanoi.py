import heapq

class HanoiState:
    def __init__(self, pegs):
        self.pegs = pegs

    def __str__(self):
        return str(self.pegs)

    def is_goal(self, num_disks):
        return len(self.pegs['destino']) == num_disks

    def __lt__(self, other):
        return True

class HanoiProblem:
    def __init__(self, num_disks):
        self.num_disks = num_disks
        initial_pegs = {
            'origem': list(range(num_disks, 0, -1)),
            'trabalho': [],
            'destino': []
        }
        self.initial_state = HanoiState(initial_pegs)

    def actions(self, state):
        valid_moves = []
        for source in ['origem', 'trabalho', 'destino']:
            for target in ['origem', 'trabalho', 'destino']:
                if source != target and state.pegs[source]:
                    if not state.pegs[target] or state.pegs[source][-1] < state.pegs[target][-1]:
                        valid_moves.append((source, target))
        return valid_moves

    def result(self, state, action):
        new_pegs = {k: v[:] for k, v in state.pegs.items()}
        source, target = action
        disk = new_pegs[source].pop()
        new_pegs[target].append(disk)
        return HanoiState(new_pegs), disk

    def heuristic(self, state):
        peg_weights = {'origem': 4, 'trabalho': 2, 'destino': 0}
        total_cost = 0
        for peg, disks in state.pegs.items():
            for disk in disks:
                disk_weight = disk + 1
                total_cost += disk_weight * peg_weights[peg]
        return total_cost

    def a_star_search(self):
        frontier = []
        heapq.heappush(frontier, (self.heuristic(self.initial_state), 0, self.initial_state, []))
        explored = set()

        while frontier:
            _, path_cost, current_state, path = heapq.heappop(frontier)

            if current_state.is_goal(self.num_disks):
                return path

            explored.add(str(current_state))

            for action in self.actions(current_state):
                child_state, moved_disk = self.result(current_state, action)
                new_path_cost = path_cost + 1
                total_cost = new_path_cost + self.heuristic(child_state)
                if str(child_state) not in explored:
                    heapq.heappush(frontier, (total_cost, new_path_cost, child_state, path + [(action, moved_disk)]))

        return None

if __name__ == "__main__":
    problem = HanoiProblem(3)
    solution = problem.a_star_search()
    if solution:
        print(f"Solução para {problem.num_disks} discos:")
        for (source, target), disk in solution:
            print(f"Mover disco {disk} de {source} para {target}")
    else:
        print("Nenhuma solução encontrada.")