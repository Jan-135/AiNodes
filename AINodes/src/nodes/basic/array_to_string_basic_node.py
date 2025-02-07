from AINodes.src.core.basic_node import BasicNode
from AINodes.src.sockets.Input_socket import InputSocket
from AINodes.src.sockets.output_socket import OutputSocket


class ArrayToStringBasicNode(BasicNode):
    def __init__(self, node_id, separator=", "):
        """Wandelt ein Array in einen String um."""
        super().__init__(node_id)
        self.separator = separator

        # Input-Socket für das Array
        self.input_array = InputSocket(self, "array")
        self.inputs.append(self.input_array)

        # Output-Socket für den String
        self.output_string = OutputSocket(self, "string", "string_output")
        self.outputs.append(self.output_string)

    def execute(self):
        """Konvertiert das Array in einen String."""
        array_data = self.input_array.pass_data()

        if array_data is None:
            return None

        return {"string_output": self.separator.join(map(str, array_data))}