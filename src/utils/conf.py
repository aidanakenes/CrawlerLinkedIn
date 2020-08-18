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
        'bcookie': 'v=2&724672f2-5396-47a3-8119-87b5317e650b',
        'lissc': '1',
        'lidc': 'b=VGST06:s=V:r=V:g=1880:u=1:i=1597759611:t=1597845337:v=1:sig=AQEMG_hOCTi_zDXrvTzIudEUbLDBf3-F',
        '_ga': 'GA1.2.2142063084.1597759193',
        '_gid': 'GA1.2.1184598668.1597759193',
        'JSESSIONID': 'ajax:6180470792414447957',
        'bscookie': 'v=1&20200818135952741634bd-233e-4253-879a-ac98d62aa608AQFeME0L6x82QyAY7yAquWDZkEbK7tOA',
        'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-408604571%7CMCIDTS%7C18493%7CMCMID%7C27178785145023820071759532538875365890%7CMCAAMLH-1598364029%7C11%7CMCAAMB-1598364029%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1597766429s%7CNONE%7CvVersion%7C4.6.0%7CMCCIDH%7C-1689353346',
        'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
        'aam_uuid': '27001797250178259161775599924090157513',
        'li_at': 'AQEDATIONYQCAylQAAABdAHe68QAAAF0JetvxFYAERT7A8-3-rmNi8FFvTo6HOXXvk0qRvx09L4h1nQWuzLpoF7Q1XhhRyM0ZAqSlYCqGmAt7Dq0kVCwoAqY1HFhQ9amoTWztA9EFbndLdi-2JvfbyqP',
        'liap': 'true',
        'lang': 'v=2&lang=en-us',
        'UserMatchHistory': 'AQLnEUl60LZgWAAAAXQB5NjxqECScz9_zqi94iYDVSumRo2gL-fRWwzvcj5M7IVlYLmxLTkJ_KlvtPPB8mNTnmlh0EfzjFueRg1AxJBw5qAZ7w7RjTeE4TrSx868veaReFeLLDUIZadOMSSzCma6FP3YNTzpk4Haz1v37R4Eds6je38GE0WA70Qry4Od8H4tC0vsvECf3lMKqSk6OfTHnfusGy8PWdvMCGU9i6EHbuygqqn7jjXOjIR_QVnBu9bBkOQP5Js',
        'li_sugr': 'b7457aac-855e-4590-a852-9a0ecabbb0d9',
        '_guid': 'f17e7591-f36a-4b82-bc8c-83d05bdc0f86',
        'li_oatml': 'AQG2ri25jAiJ4AAAAXQB3xXxJTf_m7Q8pt9pZ-z3HXjMpbzJgDrttcOb-czDIwn-MUY8JnH8dYLDS-jDVueskV_tfuQVMGUU',
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
        'Accept-Language': 'en-US,en;q=0.5',
        'x-li-deco-include-micro-schema': 'true',
        'x-li-lang': 'en_US',
        'x-li-track': '{"clientVersion":"1.7.482","osName":"web","timezoneOffset":5,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":2880,"displayHeight":1800}',
        'x-li-page-instance': 'urn:li:page:d_flagship3_profile_view_base;fTwkzXuERiOQEt6xKRBwTg==',
        'csrf-token': 'ajax:6180470792414447957',
        'x-restli-protocol-version': '2.0.0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.linkedin.com/in/mary-james-7aa2b595/',
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
        'bcookie': 'v=2&724672f2-5396-47a3-8119-87b5317e650b',
        'lissc': '1',
        'lidc': 'b=VGST06:s=V:r=V:g=1880:u=1:i=1597759611:t=1597845337:v=1:sig=AQEMG_hOCTi_zDXrvTzIudEUbLDBf3-F',
        '_ga': 'GA1.2.2142063084.1597759193',
        '_gid': 'GA1.2.1184598668.1597759193',
        'JSESSIONID': 'ajax:6180470792414447957',
        'bscookie': 'v=1&20200818135952741634bd-233e-4253-879a-ac98d62aa608AQFeME0L6x82QyAY7yAquWDZkEbK7tOA',
        'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-408604571%7CMCIDTS%7C18493%7CMCMID%7C27178785145023820071759532538875365890%7CMCAAMLH-1598364029%7C11%7CMCAAMB-1598364029%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1597766429s%7CNONE%7CvVersion%7C4.6.0%7CMCCIDH%7C-1689353346',
        'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
        'aam_uuid': '27001797250178259161775599924090157513',
        'li_at': 'AQEDATIONYQCAylQAAABdAHe68QAAAF0JetvxFYAERT7A8-3-rmNi8FFvTo6HOXXvk0qRvx09L4h1nQWuzLpoF7Q1XhhRyM0ZAqSlYCqGmAt7Dq0kVCwoAqY1HFhQ9amoTWztA9EFbndLdi-2JvfbyqP',
        'liap': 'true',
        'lang': 'v=2&lang=en-us',
        'UserMatchHistory': 'AQLnEUl60LZgWAAAAXQB5NjxqECScz9_zqi94iYDVSumRo2gL-fRWwzvcj5M7IVlYLmxLTkJ_KlvtPPB8mNTnmlh0EfzjFueRg1AxJBw5qAZ7w7RjTeE4TrSx868veaReFeLLDUIZadOMSSzCma6FP3YNTzpk4Haz1v37R4Eds6je38GE0WA70Qry4Od8H4tC0vsvECf3lMKqSk6OfTHnfusGy8PWdvMCGU9i6EHbuygqqn7jjXOjIR_QVnBu9bBkOQP5Js',
        'li_sugr': 'b7457aac-855e-4590-a852-9a0ecabbb0d9',
        '_guid': 'f17e7591-f36a-4b82-bc8c-83d05bdc0f86',
        'li_oatml': 'AQG2ri25jAiJ4AAAAXQB3xXxJTf_m7Q8pt9pZ-z3HXjMpbzJgDrttcOb-czDIwn-MUY8JnH8dYLDS-jDVueskV_tfuQVMGUU',
        '_gat': '1',
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
        'Accept-Language': 'en-US,en;q=0.5',
        'x-li-lang': 'en_US',
        'x-li-track': '{"clientVersion":"1.7.482","osName":"web","timezoneOffset":5,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":2880,"displayHeight":1800}',
        'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_top;GGzRB1LdTq+5b3hqLfjRJg==',
        'csrf-token': 'ajax:6180470792414447957',
        'x-restli-protocol-version': '2.0.0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.linkedin.com/in/ivan-ivanov-8b02b21b5/',
        'TE': 'Trailers',
    }




