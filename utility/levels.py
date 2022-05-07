from utility.utility import Coordinates, FieldType, GameField


class Instruction:
    command: str
    args: list

    def __init__(self, command: str, args: list):
        self.command = command
        self.args = []
        for arg in args:
            if Coordinates.is_coordinate(arg):
                self.args.append(Coordinates.from_string(arg))
            else:
                self.args.append(arg)

    @classmethod
    def from_string(cls, string: str):
        command, *args = string.split(" ")
        return cls(command, args)


class LevelInterpreter():
    """
    An interpreter used for generating GameFields from a
    configuration file
    """

    file_content: str
    instructions: list[Instruction]
    is_map: bool

    def __init__(self, file_path) -> None:
        with open(file_path, "r") as f:
            self.file_content = f.read()

        self.is_map = not "siz" in self.file_content

        if not self.is_map:
            self.instructions: list[Instruction] = []
            for line in self.file_content.split("\n"):
                if len(line) <= 2 or line.startswith("#"):
                    continue
                self.instructions.append(Instruction.from_string(line))

    def build_game_field(self) -> GameField:
        return self.build_game_field_from_map() if self.is_map else self.build_game_field_from_instructions()

    def build_game_field_from_instructions(self) -> GameField:
        """
        Build a new GameField from the loaded file
        """

        if any(x.command == "siz" for x in self.instructions):
            size = [x for x in self.instructions if x.command == "siz"][0].args[0]
            game_field = GameField((size.x, size.y))
        else:
            raise Exception(
                "LevelInterpreter: missing 'siz' command in lvl file")

        for instruction in self.instructions:
            match instruction.command:
                case "plr":
                    coords = instruction.args[0]
                    game_field.spawn_player(coords)
                case "trg":
                    coords = instruction.args[0]
                    game_field.spawn_target(coords)
                case "wal":
                    from_coord = instruction.args[0]
                    to_coord = instruction.args[1]
                    game_field.spawn_wall(from_coord, to_coord)

        return game_field

    def build_game_field_from_map(self) -> GameField:
        """
        Build a new GameField from a map
        """

        rows: list[list[FieldType]] = []

        for line in self.file_content.split("\n"):
            row: list[FieldType] = []

            for char in line:
                match char:
                    case "P":
                        row.append(FieldType.START)
                    case "T":
                        row.append(FieldType.TARGET)
                    case "#":
                        row.append(FieldType.WALL)
                    case " ":
                        row.append(FieldType.EMPTY)
                    case _:
                        raise Exception(
                            f"LevelInterpreter: unknown character '{char}'")

            rows.append(row)

        game_field = GameField((len(rows[0]), len(rows)))
        for y, row in enumerate(rows):
            for x, col in enumerate(row):
                if col == FieldType.START:
                    game_field.spawn_player(Coordinates(x, y))
                else:
                    game_field.field[y][x] = col

        return game_field
