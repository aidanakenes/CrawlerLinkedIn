import os


class Postgres:
    DB_PASS = os.environ.get('POSTGRE_PASS')
    DB_NAME = os.environ.get('POSTGRE_DB')
    DB_HOST = os.environ.get('POSTGRE_HOST')
    ENGINE = f"postgresql://postgres:{DB_PASS}@{DB_HOST}/{DB_NAME}"


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
        'decorationId': 'com.linkedin.voyager.dash.deco.identity.profile.FullProfileWithEntities-53',
        'memberIdentity': ''
    }
    COOKIES = {
        'bcookie': 'v=2&b26ab65b-5306-42e2-8029-bab44c66528f',
        'bscookie': 'v=1&20191210151429d54bb621-b2d8-4aaa-829c-2ccd4c5a38f6AQHWMr_3NZXH_esEZbmuczzoqeEouMW9',
        'visit': 'v=1&M',
        'lissc': '1',
        'lidc': 'b=OB76:s=O:r=O:g=2085:u=1:i=1597648269:t=1597662710:v=1:sig=AQFSH77dURxUrTPxzourSe5sIcifzUJ_',
        'G_ENABLED_IDPS': 'google',
        'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-408604571%7CMCIDTS%7C18492%7CMCMID%7C87899833160021010473793650099046185123%7CMCOPTOUT-1597655472s%7CNONE%7CvVersion%7C4.6.0',
        'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
        'g_state': '{"i_p":1597654934810,"i_l":1}',
        'UserMatchHistory': 'AQKFoj9zlSFoxAAAAXP7QedO2S1lRewR9_B7gMVXBM-YwFZ36IwzVkp3tMdDfOYqq5T32kAMKvYSm4jF7MBAdstNpYqH2YEvqixS7yuF1xvi_HWBlV6sCDOwdrz-_Se4N2he92wi4_pnTALU2tHdieeVKi3XKAV0QC-34ec1rKIy5Xwo-xd1VvJCdo4oUrMlE6DdVczWC_2MLeN971kzX09wVGVmjIqXPWA03j6CA6nu',
        'li_sugr': '08f176c3-c1d0-43c5-b823-6cc591d51026',
        '_guid': '92bd9b3d-3e4d-4522-94df-7be63de562ca',
        'JSESSIONID': 'ajax:0666574109541261707',
        'li_rm': 'AQG4Rj397uOWywAAAXP7QQyprMwyxE-WqLNvVcNulK3XVR3s3_EYYdT6HshjTevFCpKJBUeYWX2zEnCXCZ3LO2CetlQ287PaX2H-_39c8XKrtxvMtfXrh8j9',
        'liap': 'true',
        'li_at': 'AQEDATFx_NQC3IqFAAABc_tBnI0AAAF0H04gjU0ARune19MWJpJ9yhdqxJURG2-0JbsDuI0uIGABicM5HX_1qsvyX74iBfZw0idZPFc_Z9G5ZRrMHDnqdrZpz_67eFYrOg7SR9-BNKlYhVAxHSpVPHmU',
        'lang': 'v=2&lang=en-us',
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'x-li-deco-include-micro-schema': 'true',
        'x-li-lang': 'en_US',
        'x-li-track': '{"clientVersion":"1.7.373","osName":"web","timezoneOffset":6,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1.25,"displayWidth":1920,"displayHeight":1080}',
        'x-li-page-instance': 'urn:li:page:d_flagship3_profile_view_base;1XN6vKMyTRKdqHhcjrspWQ==',
        'csrf-token': 'ajax:0666574109541261707',
        'x-restli-protocol-version': '2.0.0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.linkedin.com/in/mary-james-7aa2b595/',
        'Cache-Control': 'max-age=0',
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
        'JSESSIONID': 'ajax:0666574109541261707',
        'li_at': 'AQEDATFx_NQC3IqFAAABc_tBnI0AAAF0H04gjU0ARune19MWJpJ9yhdqxJURG2-0JbsDuI0uIGABicM5HX_1qsvyX74iBfZw0idZPFc_Z9G5ZRrMHDnqdrZpz_67eFYrOg7SR9-BNKlYhVAxHSpVPHmU'
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'x-li-deco-include-micro-schema': 'true',
        'x-li-lang': 'en_US',
        'x-li-track': '{"clientVersion":"1.7.373","osName":"web","timezoneOffset":6,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1.25,"displayWidth":1920,"displayHeight":1080}',
        'x-li-page-instance': 'urn:li:page:d_flagship3_profile_view_base;1XN6vKMyTRKdqHhcjrspWQ==',
        'csrf-token': 'ajax:0666574109541261707',
        'x-restli-protocol-version': '2.0.0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.linkedin.com/in/mary-james-7aa2b595/',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers',
    }



