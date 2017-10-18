import scrapy
import json
import random
import re


class ListmakerSpider(scrapy.Spider):
    name = 'listmaker'
    # allowed_domains = ['lightoj.com']
    # start_urls = ['http://lightoj.com/']

    def __init__(self, lst='[{"id":"sjsakib","loj":"16179","timus":"201180","uva":"512628","cf":"sjsakib"}]', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lst = json.loads(lst)

    def start_requests(self):
        for user in self.lst:
            if 'loj' in user:
                url = self.settings.get('LOJ')
                url += user['loj']
                url += '&q=' + str(random.random())
                reqloj = scrapy.Request(url, self.parse_loj)
                reqloj.meta['id'] = user['id']
                yield reqloj

            if 'timus' in user:
                url = self.settings.get('TIMUS')
                url += user['timus']
                reqtimus = scrapy.Request(url, self.parse_timus)
                reqtimus.meta['id'] = user['id']
                yield reqtimus

            if 'uva' in user:
                url = self.settings.get('UVA')
                url += user['uva']
                requva = scrapy.Request(url, self.parse_uva)
                requva.meta['id'] = user['id']
                yield requva

            if 'cf' in user:
                url = self.settings.get('CF')
                url += user['cf']
                reqcf = scrapy.Request(url, self.parse_cf)
                reqcf.meta['id'] = user['id']
                yield reqcf

    def parse_loj(self, response):
        data = {}
        data['id'] = response.meta['id']
        data['judge'] = 'LOJ'
        if response.status == 200:
            matches = re.findall(r'(\d{4})(,)', response.text)
            lst = [m[0] for m in matches]
            data['lst'] = lst
            data['status'] = 'OK'
        else:
            data['lst'] = []
            data['status'] = 'FAILED'
        yield data

    def parse_timus(self, response):
        data = {}
        data['id'] = response.meta['id']
        data['judge'] = 'TIMUS'
        if response.status == 200:
            lst = response.css('td.accepted a::text').extract()
            data['lst'] = lst
            data['status'] = 'OK'
        else:
            data['lst'] = []
            data['status'] = 'FAILED'
        yield data

    def parse_uva(self, response):
        data = {}
        data['id'] = response.meta['id']
        data['judge'] = 'UVA'
        if response.status == 200:
            lst = []
            resp = json.loads(response.text)
            for j, x in enumerate(resp[0]['solved']):
                for i in range(32):
                    if (x & (1 << i)):
                        lst.append(str((j*32)+i))
            data['lst'] = lst
            data['status'] = 'OK'
        else:
            data['lst'] = []
            data['status'] = 'FAILED'
        yield data

    def parse_cf(self, response):
        data = {}
        data['id'] = response.meta['id']
        data['judge'] = 'CF'
        if response.status == 200:
            lst = set()
            resp = json.loads(response.text)
            for sub in resp['result']:
                pid = str(sub['problem']['contestId'])+sub['problem']['index']
                if sub['verdict'] == 'OK' and pid not in lst:
                    lst.add(pid)
            data['lst'] = list(lst)
            data['status'] = 'OK'
        else:
            data['lst'] = []
            data['status'] = 'FAILED'
        yield data
