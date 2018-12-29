import requests
from bs4 import BeautifulSoup
import json
import datetime
import time
import csv
import os

class Mackolik:
    """
        Params:
            file_name -- name of file which the matches will be written.
            start_date -- start date of the to be retrieved matches.
            end_date -- end date of the to be retrieved matches.
                - if end_date not given, the program works on only start_date.
                - if end_date given, the program works on between start_date and end_date.

        Example use:
            - m = Mackolik('mackolik', '01/01/2018')
            - m.main()

            OR

            - m = Mackolik('mackolik', '01/01/2018', '01/12/2018')
            - m.main()
    """
    def __init__(self, file_name, start_date, end_date = None):
        self.file_name = file_name
        self.start_date = start_date
        self.end_date = end_date
        self.matches = []
        self.dates = []
        self.match_data_url = 'http://goapi.mackolik.com/livedata?date={}' # data url of matches which played on a given date
        self.match_odds_url = 'http://arsiv.mackolik.com/Match/Default.aspx?id={}' # the url that contains betting odds of a match given as id
        # session
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'})


    def calculate_date_range(self):
        """
            Calculates dates between 'self.start_date' and 'self.end_date' and returns.
            If 'self.end_date' is None, only returns 'self.start_date'

            Example:
                ['30/04/2017']
                    OR
                ['30/04/2017', '01/05/2017',....]
        """
        dates = []
        if self.end_date == None or self.end_date == '':
            self.dates.append(self.start_date)
        else:
            format = '%d/%m/%Y' # eg. 04/01/2018
            start = datetime.datetime.strptime(self.start_date, format)
            end = datetime.datetime.strptime(self.end_date, format)
            step = datetime.timedelta(days=1)
            while start <= end:
                date = start.date().strftime(format)
                self.dates.append(date)
                start += step


    def get_matches(self, date):
        """
            Requests to for getting matches which played on date given as parameter.
            Returns details and IDs of matches

            Example return:
                details --
                    [['01/01/2013', '2012/2013', '14:45', 502, 'İNP', 'West Bromwich', 'Fulham', '0-1', '1-2'],
                     ['01/01/2013', '2012/2013', '17:00', 509, 'İNP', 'Manchester City', 'Stoke City', '1-0', '3-0'],....]
                ids --
                    [972904, 972896,....]

        """
        url = self.match_data_url.format(date) # eg. http://goapi.mackolik.com/livedata?date=23/12/2018
        req = self.session.get(url)
        if req.status_code == 200:
            matches = req.json()['m']
            details = []
            ids = []
            for row in matches:
                if row[23] == 1 and row[14] != 0:
                    # this check is for retrieving only football matches that has bet odds.
                    # if row[23] is equal to 1, it is football match.
                    # if row[14] is equal to 1, it has bet odds.
                    match_id = row[0]
                    match_code = row[14]
                    match_time = row[16]
                    home_team = row[2]
                    away_team = row[4]
                    halftime_score = row[7]
                    fulltime_score = row[29] + '-' + row[30]
                    match_date = row[35]
                    league = row[36][9]
                    season = row[36][5]
                    ids.append(match_id)
                    details.append([match_date,
                                    season,
                                    match_time,
                                    match_code,
                                    league,
                                    home_team,
                                    away_team,
                                    halftime_score,
                                    fulltime_score])
            return details, ids
        else:
            time.sleep(15) # sleep to prevent the 503 error
            return self.get_matches(data)


    def get_odds_data(self, id):
        """
            Requests to for getting odds data of match.

            Params:
                id -- id of match

            Example return:
                [[['Maç Sonucu', 'Handikap'], ['3.60', '3.30', '1.60', '+1h', '1.75', '3.30', '2.50', '']],
                [['IY 1,5 Gol', 'AÜ 1,5 Gol', 'AÜ 2,5 Gol', 'AÜ 3,5 Gol'], ['1.45', '1.80', '-', '-', '2.15', '1.35', '1.55', '1.65']],
                [['Karşılıklı Gol', 'İlk Yarı Sonucu'], ['1.25', '2.20', '3.60', '2.10', '2.00']],
                [['Çifte Şans', 'Toplam Gol'], ['1.72', '1.11', '1.08', '4.50', '2.00', '1.95', '9.00']],
                [['İlk Yarı / Maç Sonucu'], ['7.00', '10.00', '18.00'], ['7.75', '5.50', '4.25'], ['22.00', '11.00', '2.35']],
                [['Maç Skoru'], ['12.50', '15.00', '10.00', '24.00', '17.00', '22.00', '55', '55'],
                                ['50', '55', '60', '60', '60', '80', '150', ''],
                                ['11.00', '6.50', '8.50', '28.00', '55', '60', '', ''],
                                ['10.00', '9.50', '7.50', '9.50', '8.00', '13.00', '16.00', '15.00'],
                                ['24.00', '45.00', '17.00', '16.00', '28.00', '60', '80', '']]]

        """
        url = self.match_odds_url.format(id) # eg. http://arsiv.mackolik.com/Match/Default.aspx?id=1158481
        req = self.session.get(url)
        if req.status_code == 200:
            soup = BeautifulSoup(req.content, 'html.parser')
            tables = soup.find_all('table', attrs={'class':'iddaa-ms-h'})
            odds_data = []
            counter = 0
            for table in tables:
                odds_data.append([])
                rows = table.find_all('tr', class_=lambda x: x != 'iddaa-tab-alt')
                for row in rows:
                    cols = row.find_all('td')
                    cols = [col.text.strip() for col in cols]
                    odds_data[counter].append(cols)
                counter += 1
            return odds_data
        else:
            time.sleep(15)# sleep to prevent the 503 error
            return self.get_odds_data(id)


    def parse_odds_data(self, data):
        """
            Parsing process of odds

            Params:
                data -- specific list which contains odds and types of odds.

            Example 'data' parameter:
                [[['Maç Sonucu', 'Handikap'], ['3.60', '3.30', '1.60', '+1h', '1.75', '3.30', '2.50', '']],
                [['IY 1,5 Gol', 'AÜ 1,5 Gol', 'AÜ 2,5 Gol', 'AÜ 3,5 Gol'], ['1.45', '1.80', '-', '-', '2.15', '1.35', '1.55', '1.65']],
                [['Karşılıklı Gol', 'İlk Yarı Sonucu'], ['1.25', '2.20', '3.60', '2.10', '2.00']],
                [['Çifte Şans', 'Toplam Gol'], ['1.72', '1.11', '1.08', '4.50', '2.00', '1.95', '9.00']],
                [['İlk Yarı / Maç Sonucu'], ['7.00', '10.00', '18.00'], ['7.75', '5.50', '4.25'], ['22.00', '11.00', '2.35']],
                [['Maç Skoru'], ['12.50', '15.00', '10.00', '24.00', '17.00', '22.00', '55', '55'],
                                ['50', '55', '60', '60', '60', '80', '150', ''],
                                ['11.00', '6.50', '8.50', '28.00', '55', '60', '', ''],
                                ['10.00', '9.50', '7.50', '9.50', '8.00', '13.00', '16.00', '15.00'],
                                ['24.00', '45.00', '17.00', '16.00', '28.00', '60', '80', '']]]

            Example return:
                ['3.60', '3.30', '1.60', '+1h', '1.75', '3.30', '2.50', '', '1.45',
                '1.80', '', '', '2.15', '1.35', '1.55', '1.65', '1.25', '2.20', '3.60',
                '2.10', '2.00', '1.72', '1.11', '1.08', '4.50', '2.00', '1.95', '9.00',
                '7.00', '10.00', '18.00', '7.75', '5.50', '4.25', '22.00', '11.00', '2.35']

        """
        # Eg. 'Maç Sonucu' odds type has 3 different odds.(MS1, MSX, MS2)
            # data[0][1][0:3] => 'Maç Sonucu' odds
        # Eg. 'Handikap' odds type has 5 different odds.(h, H1, HX, H2, h)
            # data[0][1][3:8] => 'Handikap' odds
        # Eg. 'IY 1,5 Gol' odds type has 2 different odds.(1.5A, 1.5Ü)
            # data[1][1][0:2] => 'IY1,5' odds
        #
        #  -- Scheme --
        # 'odds type':['how many different odds', 'list index for append']
        scheme = {'Maç Sonucu':[3,0],
                  'Handikap':[5,3],
                  'IY 1,5 Gol':[2,8],
                  'AÜ 1,5 Gol':[2,10],
                  'AÜ 2,5 Gol':[2,12],
                  'AÜ 3,5 Gol':[2,14],
                  'Karşılıklı Gol':[2,16],
                  'İlk Yarı Sonucu':[3,18],
                  'Çifte Şans':[3,21],
                  'Toplam Gol':[4,24]}
        processed_odds = ['' for _ in range(0,37)]
        for i in range(0, len(data)):
            index = 0
            if len(data[i][0]) != 1:
                for k in range(0, len(data[i][0])):
                    counter = 0
                    key = scheme[data[i][0][k]]
                    odds = data[i][1]
                    for odd in odds[index:index+key[0]]:
                        if odd == '-':
                            odd = ''
                        processed_odds[key[1]+counter] = odd
                        index += 1
                        counter += 1
            # ilk yarı/maç sonucu
            elif data[i][0][0] == 'İlk Yarı / Maç Sonucu':
                counter = 28 # index
                for k in range(1, len(data[i])):
                    for l in range(0, len(data[i][k])):
                        processed_odds[counter] = data[i][k][l]
                        counter += 1
            elif data[i][0][0] == 'Maç Sonucu':
                continue
        return processed_odds


    def write(self):
        """
            Writes matches to csv file

            Format -- > [Date, Season, Time, Code, League, Home, Away, HT, FT, MS1, MSX, MS2,
                         H, H1, HX, H2, H, IY1.5A, IY1.5U, 1.5A, 1.5U, 2.5A, 2.5U, 3.5A, 3.5U,
                         KGV, KGY, IY1, IY0, IY2, 1X, 12, X2, TG01, TG23, TG46, TG7,
                         1/1, 1/X, 1/2, X/1, X/X, X/2, 2/1, 2/X, 2/2]
        """
        path = os.path.dirname(os.path.abspath(__file__))
        extension = '.csv'
        with open(path + '/' + self.file_name + extension, 'a') as file:
            writer = csv.writer(file, delimiter = ',')
            for match in self.matches:
                writer.writerow(match)


    def main(self):
        self.calculate_date_range()
        for date in self.dates:
            print("==> {}".format(date))
            details = self.get_matches(date)
            self.matches.extend(details[0])
            for idx, id in enumerate(details[1]):
                odds_data = self.get_odds_data(id)
                odds = self.parse_odds_data(odds_data)
                self.matches[idx].extend(odds)
                time.sleep(0.5) # wait
            self.write()
            self.matches.clear()
            print("Matches which played on {} has written".format(date))
