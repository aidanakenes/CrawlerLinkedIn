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
        'bcookie': 'v=2&4c90c9fd-e235-4504-8794-ebaa453dc6f3',
        'lissc': '1',
        'lidc': 'b=VB63:s=V:r=V:g=2788:u=2:i=1597988712:t=1598067108:v=1:sig=AQERcG4Z4RKhbKu7Xx1V9lBx5ugvGawd',
        '_ga': 'GA1.2.1135684691.1597988630',
        '_gid': 'GA1.2.2058341034.1597988630',
        'JSESSIONID': 'ajax:4029450910969601173',
        'bscookie': 'v=1&202008210543495b189c4e-adbd-4158-8743-d8d8b8b8836cAQFAppH-Vs8YPaXc-JSpQVdIwJ-oENn5',
        'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-408604571%7CMCIDTS%7C18496%7CMCMID%7C68445526883368755491937724428170944461%7CMCAAMLH-1598593511%7C11%7CMCAAMB-1598593511%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1597995911s%7CNONE%7CvVersion%7C4.6.0%7CMCCIDH%7C1863148939',
        'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
        'li_rm': 'AQEGhBkI5m-MbAAAAXQPi3l_O1otPTom8KT7i6SluykzvV7nxBplFGssCviGToRmubqZfTGy9J6K7FWScbx4y55EiQcbXlW7KRVVY6j5ZuIskkr4XsIeeF5V',
        'aam_uuid': '67879310837406279261885602129176636422',
        'liap': 'true',
        'li_at': 'AQEDATISo7sDzrI9AAABdA-MkFwAAAF0M5kUXE0AzOYclPy1ZrxktsnpOAJ1ILAabQmfTQ1InfxXO-3z50mqu4Bfw7GGEAhRv0j6B0PsaN43VFg3-fwr33LL8oGIoyj2ab5Qj-14HFbTGoRykBpU730W',
        'lang': 'v=2&lang=en-us',
        'UserMatchHistory': 'AQKEY0hHSPlKYQAAAXQPjJ8KERdJkMQBenAiWyLvO7cXedH_l_OcYQP-8tnQqN_z9pBVsuoYLRfRsj9aaBQwN-SLoZdJMl6GT8RAKfGWfiZjEiQL6Wqb7R47nu_3ehUROAYzQnRoLqD9IG8CITNJAP11nOLP-NElsOSXshtky-jTDNxjpOJilsxtzcAdGqW6cV0yxKiW1gVILq2n5q1j6fWkkTzh746c7yMlv_MnEVQ3',
        'li_sugr': 'f811580d-1385-445f-8b96-e592f6819e39',
        '_guid': '77a2bc37-48c2-4884-95a9-c0fd830fb636',
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
        'Accept-Language': 'en-US,en;q=0.5',
        'x-li-lang': 'en_US',
        'x-li-track': '{"clientVersion":"1.7.785.4","osName":"web","timezoneOffset":5,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":2880,"displayHeight":1800}',
        'x-li-page-instance': 'urn:li:page:d_flagship3_profile_view_base;wGziQAd1S9aB2aFZGJEomw==',
        'csrf-token': 'ajax:4029450910969601173',
        'x-restli-protocol-version': '2.0.0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.linkedin.com/search/results/all/?keywords=Viktor%20Pavlov&origin=HISTORY',
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
        'bcookie': 'v=2&4c90c9fd-e235-4504-8794-ebaa453dc6f3',
        'lissc': '1',
        'lidc': 'b=VB63:s=V:r=V:g=2788:u=2:i=1597988712:t=1598067108:v=1:sig=AQERcG4Z4RKhbKu7Xx1V9lBx5ugvGawd',
        '_ga': 'GA1.2.1135684691.1597988630',
        '_gid': 'GA1.2.2058341034.1597988630',
        'JSESSIONID': 'ajax:4029450910969601173',
        'bscookie': 'v=1&202008210543495b189c4e-adbd-4158-8743-d8d8b8b8836cAQFAppH-Vs8YPaXc-JSpQVdIwJ-oENn5',
        'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-408604571%7CMCIDTS%7C18496%7CMCMID%7C68445526883368755491937724428170944461%7CMCAAMLH-1598593511%7C11%7CMCAAMB-1598593511%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1597995911s%7CNONE%7CvVersion%7C4.6.0%7CMCCIDH%7C1863148939',
        'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
        'li_rm': 'AQEGhBkI5m-MbAAAAXQPi3l_O1otPTom8KT7i6SluykzvV7nxBplFGssCviGToRmubqZfTGy9J6K7FWScbx4y55EiQcbXlW7KRVVY6j5ZuIskkr4XsIeeF5V',
        'aam_uuid': '67879310837406279261885602129176636422',
        'liap': 'true',
        'li_at': 'AQEDATISo7sDzrI9AAABdA-MkFwAAAF0M5kUXE0AzOYclPy1ZrxktsnpOAJ1ILAabQmfTQ1InfxXO-3z50mqu4Bfw7GGEAhRv0j6B0PsaN43VFg3-fwr33LL8oGIoyj2ab5Qj-14HFbTGoRykBpU730W',
        'lang': 'v=2&lang=en-us',
        'UserMatchHistory': 'AQKEY0hHSPlKYQAAAXQPjJ8KERdJkMQBenAiWyLvO7cXedH_l_OcYQP-8tnQqN_z9pBVsuoYLRfRsj9aaBQwN-SLoZdJMl6GT8RAKfGWfiZjEiQL6Wqb7R47nu_3ehUROAYzQnRoLqD9IG8CITNJAP11nOLP-NElsOSXshtky-jTDNxjpOJilsxtzcAdGqW6cV0yxKiW1gVILq2n5q1j6fWkkTzh746c7yMlv_MnEVQ3',
        'li_sugr': 'f811580d-1385-445f-8b96-e592f6819e39',
        '_guid': '77a2bc37-48c2-4884-95a9-c0fd830fb636',
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
        'Accept-Language': 'en-US,en;q=0.5',
        'x-li-lang': 'en_US',
        'x-li-track': '{"clientVersion":"1.7.785.4","osName":"web","timezoneOffset":5,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":2880,"displayHeight":1800}',
        'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_top;SSPtA5tHQC67L7YL7xe07w==',
        'csrf-token': 'ajax:4029450910969601173',
        'x-restli-protocol-version': '2.0.0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin',
    }




