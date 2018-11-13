import lxml.html

class Parser:

    _parsing_rules = {"wired-network-card":6}

    async def _parse(self, part: str, raw_html: str):
        if part in self._parsing_rules:
            tags = await self._retrieve_data(raw_html)
            print('hi')

    async def _retrieve_data(self, raw_html: str):
        html = lxml.html.fromstring(raw_html)
        return html.xpath('.//*/text()')

    async def _chunk(self, iterable, chunk_size):
        for x in range(0, len(iterable), chunk_size):
            yield iterable[x:x + chunk_size]
