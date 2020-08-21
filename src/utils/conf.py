import os


class Redis:
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = int(os.environ.get('REDIS_PORT'))
    REDIS_TTL = int(os.environ.get('REDIS_TTL'))
    RedisConfig = {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'decode_responses': True
    }


class Postgres:
    DB_USER = os.environ.get('POSTGRES_USER')
    DB_PASS = os.environ.get('POSTGRES_PASSWORD')
    DB_NAME = os.environ.get('POSTGRES_DB')
    DB_HOST = os.environ.get('POSTGRES_HOST')
    ENGINE = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


class RabbitMQ:
    RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
    RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT')
    RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
    RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS')
    RABBITMQ_CRAWLER_QUEUE = 'crawler_tasks'
    RABBITMQ_SAVER_QUEUE = 'saver_tasks'
    RABBIT_CONF = {
        'host': RABBITMQ_HOST,
        'port': RABBITMQ_PORT,
    }
    RABBIT_AUTH = {
        'username': RABBITMQ_USER,
        'password': RABBITMQ_PASS
    }


class UserRequest:
    URL = 'https://www.linkedin.com/voyager/api/identity/dash/profiles'
    PARAMS = {
        'q': 'memberIdentity',
        'decorationId': 'com.linkedin.voyager.dash.deco.identity.profile.FullProfileWithEntities-57',
        'memberIdentity': ''
    }

    COOKIES = {
        'JSESSIONID': 'ajax:3334360243601494753',
        'bcookie': 'v=2&76c1b172-4fb6-4636-840c-7b64186be361',
        'bscookie': 'v=1&20200821140025afe592ca-f298-4cce-85cb-ec4183df47beAQFtGjU4eRyMwJ7veB3ad_6uPONY-NWX',
        'lissc': '1',
        'lidc': 'b=TB87:s=T:r=T:g=2379:u=1:i=1598018602:t=1598104708:v=1:sig=AQEz5vFm6_HZvEpTbn1wxcpdSFrRIMHO',
        'G_ENABLED_IDPS': 'google',
        '_ga': 'GA1.2.1311922123.1598018428',
        '_gid': 'GA1.2.1253358727.1598018428',
        'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-408604571%7CMCIDTS%7C18496%7CMCMID%7C35948363064849090828773144381992676666%7CMCOPTOUT-1598025799s%7CNONE%7CvVersion%7C4.6.0',
        'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
        'li_rm': 'AQHleuBhqmGzYAAAAXQRVDCrifSd5PedIe6xs-yj7eaHvbKJj8zEZvylK6YHSs6iGS6GQcExUm2FaHylmGFocsKo7HobdlqtYtZLqgYeh029GJnA1EX7Mkde',
        'liap': 'true',
        'li_at': 'AQEDATGag98B679wAAABdBFUfQwAAAF0NWEBDE4AxsMQMa0kb5CtE8DXYgPDi4CrniigxcayHs8kekCR81RZf1qVKuljoHcTx_BrUKlWPneaniKq6mY-qlDRXXsjN4-HZA6F-q59QUjt1OmD3a6ZMO_Z',
        'lang': 'v=2&lang=en-us',
        'UserMatchHistory': 'AQIB4bE8x_KztAAAAXQRVK4kfn4v56rK-t1WNtKCZj1RHQ-YHLe6dYxfUT7m1hrx32mDFX6MYxdZV_HZRnYfYYAaA26JAEi2t2hgPfObwgT5VmCZ89L9TIgOse3OsTl73w1-x0Eo0OQF9J4jtNdLObH4YjedvEtpIcGWG9jSdIdlgZdd9JcyhP5sUUziWez51z29WPUl06XfAJ1ge7YEiqS-u2cObLUI25Rv0JyzxTV7',
        'li_sugr': '3acdd729-cd6e-4c63-a8b1-241c20436e5f',
        '_guid': '818d8041-9b6f-4a37-bc0a-17ba7a6a7c7b',
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
        'Accept-Language': 'en-US,en;q=0.5',
        'x-li-lang': 'en_US',
        'x-li-track': '{"clientVersion":"1.7.785.4","osName":"web","timezoneOffset":6,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1.2,"displayWidth":1365.6,"displayHeight":768}',
        'x-li-page-instance': 'urn:li:page:d_flagship3_profile_view_base;VVZM2xwzSO62kTvkgzuCbA==',
        'csrf-token': 'ajax:3334360243601494753',
        'x-restli-protocol-version': '2.0.0',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.linkedin.com/search/results/all/?keywords=viktor%20pav&origin=GLOBAL_SEARCH_HEADER',
        'TE': 'Trailers',
    }


class SearchRequest:
    URL = 'https://www.linkedin.com/voyager/api/search/blended'
    PARAMS = {
        'start': '0',
        'count': '10',
        'filters': 'List(resultType->PEOPLE,firstName->{first_name},lastName->{last_name})',
        'keywords': '',
        'origin': 'FACETED_SEARCH',
        'q': 'all',
        'queryContext': 'List(spellCorrectionEnabled->true,relatedSearchesEnabled->true)'
    }

    COOKIES = {
        'JSESSIONID': 'ajax:3334360243601494753',
        'bcookie': 'v=2&76c1b172-4fb6-4636-840c-7b64186be361',
        'bscookie': 'v=1&20200821140025afe592ca-f298-4cce-85cb-ec4183df47beAQFtGjU4eRyMwJ7veB3ad_6uPONY-NWX',
        'lissc': '1',
        'lidc': 'b=TB87:s=T:r=T:g=2379:u=1:i=1598018602:t=1598104708:v=1:sig=AQEz5vFm6_HZvEpTbn1wxcpdSFrRIMHO',
        'G_ENABLED_IDPS': 'google',
        '_ga': 'GA1.2.1311922123.1598018428',
        '_gid': 'GA1.2.1253358727.1598018428',
        'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-408604571%7CMCIDTS%7C18496%7CMCMID%7C35948363064849090828773144381992676666%7CMCOPTOUT-1598025799s%7CNONE%7CvVersion%7C4.6.0',
        'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
        'li_rm': 'AQHleuBhqmGzYAAAAXQRVDCrifSd5PedIe6xs-yj7eaHvbKJj8zEZvylK6YHSs6iGS6GQcExUm2FaHylmGFocsKo7HobdlqtYtZLqgYeh029GJnA1EX7Mkde',
        'liap': 'true',
        'li_at': 'AQEDATGag98B679wAAABdBFUfQwAAAF0NWEBDE4AxsMQMa0kb5CtE8DXYgPDi4CrniigxcayHs8kekCR81RZf1qVKuljoHcTx_BrUKlWPneaniKq6mY-qlDRXXsjN4-HZA6F-q59QUjt1OmD3a6ZMO_Z',
        'lang': 'v=2&lang=en-us',
        'UserMatchHistory': 'AQIB4bE8x_KztAAAAXQRVK4kfn4v56rK-t1WNtKCZj1RHQ-YHLe6dYxfUT7m1hrx32mDFX6MYxdZV_HZRnYfYYAaA26JAEi2t2hgPfObwgT5VmCZ89L9TIgOse3OsTl73w1-x0Eo0OQF9J4jtNdLObH4YjedvEtpIcGWG9jSdIdlgZdd9JcyhP5sUUziWez51z29WPUl06XfAJ1ge7YEiqS-u2cObLUI25Rv0JyzxTV7',
        'li_sugr': '3acdd729-cd6e-4c63-a8b1-241c20436e5f',
        '_guid': '818d8041-9b6f-4a37-bc0a-17ba7a6a7c7b',
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
        'Accept-Language': 'en-US,en;q=0.5',
        'x-li-lang': 'en_US',
        'x-li-track': '{"clientVersion":"1.7.785.4","osName":"web","timezoneOffset":6,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1.2,"displayWidth":1365.6,"displayHeight":768}',
        'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_top;zBbJZ9WhQBGuSuDTivjorA==',
        'csrf-token': 'ajax:3334360243601494753',
        'x-restli-protocol-version': '2.0.0',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.linkedin.com/search/results/all/?keywords=vorkp%20pav&origin=GLOBAL_SEARCH_HEADER',
    }





