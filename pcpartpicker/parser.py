import lxml.html
from .parts import *
import re
import time

class Parser:

    _parsing_rules = {"wired-network-card":6}
    _part_mappings = {"wired-network-card":EthernetCard}

    async def _parse(self, part: str, raw_html: str):

        part_list = []
        if part in self._parsing_rules:
            start = time.perf_counter()
            for chunk in self._chunk(await self._retrieve_data(raw_html), self._parsing_rules[part]):
                func = self._get_func(part)
                part_list.append(await func(chunk))
            print(time.perf_counter() - start)
        return part_list

    async def _retrieve_data(self, raw_html: str):
        html = lxml.html.fromstring(raw_html)
        return html.xpath('.//*/text()')

    def _chunk(self, iterable, chunk_size):
        start_index = 0
        end_index = -1
        for x in range(0, len(iterable), chunk_size):
            it = iterable[start_index + x:x + chunk_size + end_index]
            if it[-1] == "Add":
                it[-1] = "00.00"
                start_index -= 1
                end_index -= 1
            yield it

    def _get_func(self, part: str):
        return getattr(Parser, "_{}".format(part.replace("-", "_")))

    @staticmethod
    def _float_string():
        return r"(?<![a-zA-Z:])[-+]?\d*\.?\d+"

    @staticmethod
    async def _wired_network_card(chunk):
        if "x" in chunk[2]:
            connection_data = re.findall(Parser._float_string(), chunk[2])
            num_ports = int(connection_data[1])
        else:
            num_ports = 1
        price = re.findall(Parser._float_string(), chunk[4])[0]
        price = Decimal(price)
        return EthernetCard(chunk[0], price, chunk[1], chunk[2], num_ports)


