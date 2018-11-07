import lxml.html

class Parser:

    async def _parse(self, part: str, raw_html: str):
        tags = await self._tr_tags(raw_html)
        print('hi')

    async def _tr_tags(self, raw_html: str):
        html = lxml.html.fromstring(raw_html)
        return html.xpath('.//*/text()')