# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import scrapy
import datetime
from sofifa.items import SofifaItem
from lxml import html

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    # allowed_domains = ['example.com']

    start_urls = []

    def isLoan(self, team_name):
        # first case
        if self.current_team == '':
            self.current_team = team_name
            return False
        else:
            return self.current_team != team_name

    def __init__(self):
        self.current_team = ''
        self.team_id_list = [241]
        # self.start_urls = self.get_team_url(team_id_list)

    def start_requests(self):
        return [scrapy.FormRequest(self.team_url(team_id), meta={"team_id": team_id}) for team_id in self.team_id_list]


    def parse(self, response):

        if str(response.url).__contains__('team'):

            table = response.xpath('/html/body/div/div[1]/article/div[2]/table')[0]
            # table = table[1] if len(table) > 1 else table[0]
            figure = table.xpath('//figure[@class="avatar"]/img')
            for player_id in figure:
                p_id = int(player_id.attrib['id'])
                yield scrapy.Request('https://sofifa.com/player/{}{}'.format(p_id, '?units=mks'), meta={"team_id": response.meta["team_id"]})
        else:
            item = SofifaItem()
            # data = response.xpath('//div[contains(@class,"player")]')[0]
            # data2 = data.xpath('//div[@class="info"]')[0]
            # short_name = data2.xpath('//h1/text()').extract()[0].split('(')[0]
            content = html.fromstring(response.text)
            player = content.xpath('//div[contains(@class,"player")]')[0]
            info = player.xpath('//div[@class="info"]')[0]
            short_name = info.xpath('//h1')[0].text_content().split('(ID')[0]
            meta = info.xpath('//div[@class="meta"]')[0].text_content()
            full_name = meta.split('Age ')[0].split('  ')[0]
            position = meta.split('Age ')[0].split('  ')[1]
            position = position.replace(' ', ',')
            nationality = info.xpath('//div[@class="meta"]/a')[0].attrib['href']
            nationality_name = info.xpath('//div[@class="meta"]/a')[0].attrib['title']
            nationality = nationality.split('=')[1]

            # international team logo
            team_info = player.xpath('//div[contains(@class,"teams")]/div[1]/div')
            int_team_logo = ''
            if len(team_info) == 4:
                int_team_logo = player.xpath('//div[contains(@class,"teams")]/div[1]/div[4]//img')[0].attrib['data-src']

            # stats
            stats = player.xpath('//div[contains(@class,"stats")]//span/text()')
            overall_rating = stats[0]
            value = stats[2]
            wage = stats[3]

            # birthday, height, weight
            data = meta.split('Age ')[1]
            data = data.split(') ')
            birthday = data[0].split('(')[1]
            birthday = datetime.datetime.strptime(birthday, '%b %d, %Y')
            birthday = birthday.strftime('%m/%d/%Y')
            data = data[1].split(' ')
            height = data[0].replace("cm", "")
            weight = data[1].replace("kg", "")

            # foot
            card = player.xpath('.//div')[8]
            data = card.xpath('//ul[@class="pl"]/li')[0].text_content()
            foot = data.replace('Preferred Foot', '').strip()[:1]

            # remove loan players
            team_name = card.xpath('//ul[@class="pl"]/li//a')[0].text_content()
            loaned_from = ''
            item['name'] = short_name
            item['full_name'] = full_name
            item['team_id'] = response.meta["team_id"]

            yield item

    def get_team_url(self, team_id_list):
        return [self.team_url(team_id) for team_id in team_id_list]

    def team_url(self, team_id):
        return 'https://sofifa.com/team/{}'.format(team_id)
