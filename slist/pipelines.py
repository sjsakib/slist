import requests


class SlistPipeline(object):

    def open_spider(self, spider):
        self.data = {}

    def process_item(self, item, spider):
        user = item['id']
        if user not in self.data:
            self.data[user] = {'failed': [], 'judges': {}}
        if item['status'] == 'FAILED':
            self.data[user]['failed'].append(item['judge'])
        else:
            self.data[user]['judges'][item['judge']] = item['lst']

        return item

    def close_spider(self, spider):
        requests.post(spider.settings.get('POST_URL'), json=self.data)
