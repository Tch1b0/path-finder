from utility.utility import Coordinates, GameField

class LevelInterpreter():
    """
    An interpreter used for generating GameFields from a
    configuration file
    """

    def __init__(self, file_path) -> None:
        with open(file_path, "r") as f:
            self.level_code: list[list[str]] = [x.split(" ", 1) for x in f.readlines() if x not in [" ", "\n", ""]]

    def build_game_field(self) -> GameField:
        """
        Build a new GameField from the loaded file
        """

        game_field: GameField
        try:
            raw_size = list(filter(lambda x: x[0] == "siz", self.level_code))[0][1]
            x, y = [int(x) for x in raw_size.split(",")]
            game_field = GameField((x, y))
        except:
            raise Exception("LevelInterpreter: missing 'siz' command in lvl file")

        for command in self.level_code:
            match command[0]:
                case "plr":
                    coords = Coordinates(*[int(x) for x in command[1].split(",")])
                    game_field.spawn_player(coords)
                case "trg":
                    coords = Coordinates(*[int(x) for x in command[1].split(",")])
                    game_field.spawn_target(coords)
                case "wal":
                    coords = command[1].split(" ")
                    from_coord = Coordinates(*[int(x) for x in coords[0].split(",")])
                    to_coord = Coordinates(*[int(x) for x in coords[1].split(",")])
                    game_field.spawn_wall(from_coord, to_coord)

        return game_field
