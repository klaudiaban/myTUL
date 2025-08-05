from collections import defaultdict, deque


class TrackStateManager:
    def __init__(self):
        self.position_history = defaultdict(lambda: deque(maxlen=15))
        self.track_states = defaultdict(lambda: {"counted": False, "last_side": None})
        self.entry_count = 0
        self.exit_count = 0
        self.positions = {}

    def get_trajectory(self, track_id):
        return (
            list(self.position_history[track_id])
            if track_id in self.position_history
            else []
        )

    def update_position(self, track_id, point):
        self.position_history[track_id].append(point)

    def get_history(self, track_id):
        return self.position_history.get(track_id, [])

    def has_been_counted(self, track_id):
        return self.track_states[track_id]["counted"]

    def set_counted(self, track_id, side):
        self.track_states[track_id]["counted"] = True
        self.track_states[track_id]["last_side"] = side

    def reset_counting_state(self, track_id):
        if track_id in self.track_states:
            self.track_states[track_id]["counted"] = False

    def reset_counters(self):
        self.entry_count = 0
        self.exit_count = 0
        self.track_states.clear()

    def cleanup_old_tracks(self, current_track_ids):
        current_set = set(current_track_ids)
        old_ids = set(self.position_history.keys()) - current_set
        for old_id in old_ids:
            del self.position_history[old_id]
            if old_id in self.track_states:
                del self.track_states[old_id]

    def print_summary(self):
        net = self.entry_count - self.exit_count
        print(
            f"Final Count - Entries: {self.entry_count}, Exits: {self.exit_count}, Net: {net}"
        )

    def get_all_positions(self):
        return {track_id: pos_list[-1] for track_id, pos_list in self.position_history.items() if pos_list}
