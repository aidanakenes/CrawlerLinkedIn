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
        'bcookie': 'v=2&46294f31-5790-4816-851e-93505dd3f569',
        'lissc': '1',
        'lidc': 'b=VGST06:s=V:r=V:g=1884:u=1:i=1597941717:t=1598007822:v=1:sig=AQFyZm-tHmid-FzehhgTt4mmWM1GNWI8',
        '_ga': 'GA1.2.2138477104.1597941657',
        '_gid': 'GA1.2.139093555.1597941657',
        'JSESSIONID': 'ajax:6637950272627955330',
        'bscookie': 'v=1&20200820164057c6c5d46b-63ea-4873-8d1b-9054e0f6dbb7AQF1QX3cpjKXLOoUvPk5nZn77znn28oW',
        'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-408604571%7CMCIDTS%7C18495%7CMCMID%7C64939351352439432300248894729552685567%7CMCAAMLH-1598546485%7C11%7CMCAAMB-1598546485%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1597948885s%7CNONE%7CvVersion%7C4.6.0%7CMCCIDH%7C1863148939',
        'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
        'aam_uuid': '65437925436202882450268930977811044916',
        'li_at': 'AQEDATISo7sABSubAAABdAy_A3sAAAF0MMuHe00AASAwa_X8LT_cFVnT19DemQjpTVsiqnRPwwNyiEe8NFGmP95q9pWheVn_uXNPUoyQS_cdb-O-7WNooIWrv796qcw5AdpsUDaGAU45R_xFDmnfnigR',
        'liap': 'true',
        'lang': 'v=2&lang=en-us',
        'UserMatchHistory': 'AQKChJYewzE4SAAAAXQMv4Y8UmbYIpKw2-BLTCWHOkcVq_AvY_7yiRYOyrzO2lbFUloMMnN2UmEOyofieZ7NcsvproXsck2IJTId0QqZ_2coxkHfe7hwfnqaMbpqso0Wp-4GBR_0NwpCbV4bj6tDMu-f3s9Nxf7yv4alU0xn5jmAW0RessFNmlUXftkyWR2alCHeXO6f8xU4RAWiVdQJVF_gSudOWsmWBteEvHYkemnf',
        'li_sugr': 'ec7056e5-b024-4a17-b0a4-26cd3e7ca891',
        '_guid': '2100f00e-523e-4a10-88fd-e2cca2ae7d64',
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
        'Accept-Language': 'en-US,en;q=0.5',
        'x-li-deco-include-micro-schema': 'true',
        'x-li-lang': 'en_US',
        'x-li-track': '{"clientVersion":"1.7.777","osName":"web","timezoneOffset":5,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":2880,"displayHeight":1800}',
        'x-li-page-instance': 'urn:li:page:d_flagship3_profile_view_base;d/DRJk4cSbqt32D++ff8JQ==',
        'csrf-token': 'ajax:6637950272627955330',
        'x-restli-protocol-version': '2.0.0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.linkedin.com/in/viktor-pavlov-156b0183/',
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
        'bcookie': 'v=2&46294f31-5790-4816-851e-93505dd3f569',
        'lissc': '1',
        'lidc': 'b=VGST06:s=V:r=V:g=1884:u=1:i=1597941896:t=1598007822:v=1:sig=AQGzCCWWel1SPASV2QgT5uM296Rwfz7a',
        '_ga': 'GA1.2.2138477104.1597941657',
        '_gid': 'GA1.2.139093555.1597941657',
        'JSESSIONID': 'ajax:6637950272627955330',
        'bscookie': 'v=1&20200820164057c6c5d46b-63ea-4873-8d1b-9054e0f6dbb7AQF1QX3cpjKXLOoUvPk5nZn77znn28oW',
        'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-408604571%7CMCIDTS%7C18495%7CMCMID%7C64939351352439432300248894729552685567%7CMCAAMLH-1598546485%7C11%7CMCAAMB-1598546485%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1597948885s%7CNONE%7CvVersion%7C4.6.0%7CMCCIDH%7C1863148939',
        'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
        'aam_uuid': '65437925436202882450268930977811044916',
        'li_at': 'AQEDATISo7sABSubAAABdAy_A3sAAAF0MMuHe00AASAwa_X8LT_cFVnT19DemQjpTVsiqnRPwwNyiEe8NFGmP95q9pWheVn_uXNPUoyQS_cdb-O-7WNooIWrv796qcw5AdpsUDaGAU45R_xFDmnfnigR',
        'liap': 'true',
        'lang': 'v=2&lang=en-us',
        'UserMatchHistory': 'AQIN6yEfp6CztgAAAXQMwka3HUmPyV3j9hCBE6A5PkuITYJf3svsQHNGyj776lvAW6wmTJef8pdHSGkrFQ_yu6nx5cKvF9qipbvtchCrh0oEYoJFq_0mMDSZ7qwVOHY8VtYZpJ5v7Gt5Owod1_IOEE8NXiqDUPpHgqO1srMrh1ggwrdP3Sak1fsLGSGAbml_tUd1-BLaJMSuWddKRXfIkWa8RDtiXDoy7Jd7Jo8qnq5Tpt7F-dq4F60nkz4Rrzv0tothWJ4',
        'li_sugr': 'ec7056e5-b024-4a17-b0a4-26cd3e7ca891',
        '_guid': '2100f00e-523e-4a10-88fd-e2cca2ae7d64',
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
        'Accept-Language': 'en-US,en;q=0.5',
        'x-li-lang': 'en_US',
        'x-li-track': '{"clientVersion":"1.7.777","osName":"web","timezoneOffset":5,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":2880,"displayHeight":1800}',
        'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_top;ltgTeydYQdOiepmjCCO+JQ==',
        'csrf-token': 'ajax:6637950272627955330',
        'x-restli-protocol-version': '2.0.0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.linkedin.com/search/results/all/?keywords=Viktor%20Pavlov&origin=GLOBAL_SEARCH_HEADER',
    }




