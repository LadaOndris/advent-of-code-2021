import operator
from abc import ABC, abstractmethod
from enum import IntEnum
from functools import reduce
from typing import List

from days.base import Day


class Packet(ABC):

    def __init__(self, version, type):
        self.version = version
        self.type = type
        self.length = 6

    @abstractmethod
    def evaluate(self):
        pass

    @staticmethod
    def decode(bin_repr):
        version = int(bin_repr[0:3], 2)
        type = int(bin_repr[3:6], 2)
        if type == 4:
            return LiteralPacket(version, type, bin_repr[6:])
        else:
            return OperatorPacket(version, type, bin_repr[6:])


class LiteralPacket(Packet):

    def __init__(self, version, type, bin_repr):
        super().__init__(version, type)
        self.value = self._decode_from_bin_repr(bin_repr)

    def _decode_from_bin_repr(self, bin_repr):
        value_bits = ''
        for i in range(0, len(bin_repr), 5):
            value_bits += bin_repr[i + 1: i + 5]
            leading_bit = bin_repr[i]
            if leading_bit == '0':
                self.length += (i + 5)
                break
        return int(value_bits, 2)

    def evaluate(self):
        return self.value


class Operation(IntEnum):
    Sum = 0,
    Product = 1,
    Minimum = 2,
    Maximum = 3,
    Greater = 5,
    Less = 6,
    Equal = 7


class OperatorPacket(Packet):

    def __init__(self, version, type, bin_repr):
        super().__init__(version, type)
        self.packets = []
        self._decode_from_bin_repr(bin_repr)

    def _decode_from_bin_repr(self, bin_repr):
        length_type = bin_repr[0]
        self.length += 1
        if length_type == '0':
            value_length = int(bin_repr[1:16], 2)
            new_packet_repr = bin_repr[16:16 + value_length]
            self.length += 15
            while len(new_packet_repr) > 0:
                new_packet_repr = self._decode_sub_packet(new_packet_repr)
        else:
            num_packets = int(bin_repr[1:12], 2)
            new_packet_repr = bin_repr[12:]
            self.length += 11
            for packet_num in range(num_packets):
                new_packet_repr = self._decode_sub_packet(new_packet_repr)

    def _decode_sub_packet(self, bin_repr) -> str:
        packet: Packet = Packet.decode(bin_repr)
        packet_length = packet.length
        self.length += packet_length
        self.packets.append(packet)
        new_packet_repr = bin_repr[packet_length:]
        return new_packet_repr

    def evaluate(self):
        packet_type = Operation(self.type)
        sub_packet_values = [packet.evaluate() for packet in self.packets]
        if packet_type == Operation.Sum:
            return sum(sub_packet_values)
        elif packet_type == Operation.Product:
            return reduce(operator.mul, sub_packet_values, 1)
        elif packet_type == Operation.Minimum:
            return min(sub_packet_values)
        elif packet_type == Operation.Maximum:
            return max(sub_packet_values)
        elif packet_type == Operation.Greater:
            return sub_packet_values[0] > sub_packet_values[1]
        elif packet_type == Operation.Less:
            return sub_packet_values[0] < sub_packet_values[1]
        elif packet_type == Operation.Equal:
            return sub_packet_values[0] == sub_packet_values[1]
        raise RuntimeError('Invalid packet type: ', self.type)


class Day16(Day):

    def __init__(self):
        super().__init__('days/day_16/input.txt')
        input_number_dec = int(self.input_content, 16)
        bin_chars = len(self.input_content) * 4
        self.input_number_bin = bin(input_number_dec)[2:].zfill(bin_chars)

    def part_one(self):
        root: Packet = Packet.decode(self.input_number_bin)
        versions: List[int] = self._traverse_hierarchy_for_versions(root)
        return sum(versions)

    def _traverse_hierarchy_for_versions(self, packet: Packet) -> List[int]:
        if isinstance(packet, LiteralPacket):
            return [packet.version]
        elif isinstance(packet, OperatorPacket):
            versions = [packet.version]
            for sub_packet in packet.packets:
                versions.extend(self._traverse_hierarchy_for_versions(sub_packet))
            return versions
        return []

    def part_two(self):
        root: Packet = Packet.decode(self.input_number_bin)
        return root.evaluate()


if __name__ == '__main__':
    day = Day16()
    print(day.part_one())
    print(day.part_two())
