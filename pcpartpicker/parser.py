from lxml import etree


class Parser:

    _lxml = etree.HTMLParser()

    async def _parse(self, part: str, raw_html: str):
        part = "_{}".format(part)
        func = getattr(self, part)
        return func(raw_html)

    async def _tr_tags(self, raw_html: str):
        html = etree.parse(raw_html, self._lxml)
        return html.xpath('//tr')

    async def _cpu(self, raw_html: str):
        tags = await self._tr_tags(raw_html)
        print('hi')
