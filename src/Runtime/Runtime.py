import json

from src.FrameModel.Object import Object


class Runtime:
    @staticmethod
    def objects_are_the_same(a: Object, b: Object) -> bool:
        a_kind = a.get_object_kind()
        b_kind = b.get_object_kind()

        a_colour, a_relative_positions_string = a_kind.split(":")
        b_colour, b_relative_positions_string = b_kind.split(":")

        if a_colour != b_colour:
            return False

        a_relative_positions = list(map(
            lambda position: (position[0], position[1]),
            json.loads(a_relative_positions_string)
        ))
        b_relative_positions = list(map(
            lambda position: (position[0], position[1]),
            json.loads(b_relative_positions_string)
        ))
        if a_relative_positions != b_relative_positions:  # todo: won't recognise objects as the same if one is rotated
            return False

        return True

