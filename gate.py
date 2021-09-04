from collections import deque


ENTER = 0
EXIT = 1


class Vehicle:
    def __init__(self, arrival, direction, arrival_order):
        self.arrival = int(arrival)
        self.direction = int(direction)
        self.arrival_order = int(arrival_order)

    @property
    def entering(self):
        return self.direction == ENTER
    
    @property
    def exiting(self):
        return self.direction == EXIT
    
    def at_gate(self, time):
        return self.arrival <= time


def get_gate_order(times, directions):
    """ Get the order vehicles will move based on the direction they're headed and arrival times

    Parameters:
        times       (list)  time value for nth vehicle's arrival at gate
        directions  (list)  direction nth vehicle is headed
    
    Returns:
        (list)  the order in which the vehicles pass through the gate
    
    """
    gate_order = deque(maxlen=len(times))
    entering_vehicles = deque()
    exiting_vehicles = deque()
    gate_state = EXIT
    previous_time = -1

    # Establish arrival order and distinguish directional queues
    for arrival_order, time in enumerate(times):
        vehicle = Vehicle(time, directions[arrival_order], arrival_order)
        if vehicle.entering:
            entering_vehicles.append(vehicle)
        elif vehicle.exiting:
            exiting_vehicles.append(vehicle)

    # Iterate over time values as opposed to counting. Creates additional logic
    # but bypasses the need to count seconds
    for time in times:
        # Time management
        time = int(time)

        if time < previous_time:
            time = previous_time + 1
        elif time == previous_time:
            time += 1
        elif time > previous_time + 1:
            # reset gate if enough time has passed
            gate_state = EXIT

        previous_time = time

        # Vehicles At Gate
        vehicle_to_enter = entering_vehicles[0].at_gate(time) if entering_vehicles else None
        vehicle_to_exit = exiting_vehicles[0].at_gate(time) if exiting_vehicles else None

        # Vehicle Departure Order Logic
        if (vehicle_to_exit and not vehicle_to_enter) or (vehicle_to_enter and vehicle_to_exit and gate_state == EXIT):
            vehicle = exiting_vehicles.popleft()
            gate_state = EXIT
        elif (vehicle_to_enter and not vehicle_to_exit) or (vehicle_to_enter and vehicle_to_exit and gate_state == ENTER):
            vehicle = entering_vehicles.popleft()
            gate_state = ENTER

        # Vehicle Departure Order Output
        gate_order.insert(vehicle.arrival_order, time)

    # Converting to list per stated output
    return list(gate_order)
