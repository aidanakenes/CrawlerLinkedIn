import os


DB_PASS = os.environ.get('POSTGRE_PASS')
DB_NAME = os.environ.get('POSTGRE_DB')
DB_HOST = os.environ.get('POSTGRE_HOST')
ENGINE = f"postgresql://postgres:{DB_PASS}@{DB_HOST}/{DB_NAME}"
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

USER_REQUEST_URL = 'https://www.linkedin.com/voyager/api/identity/dash/profiles'
USER_REQUEST_PARAMS = {
    'q': 'memberIdentity',
    'decorationId': 'com.linkedin.voyager.dash.deco.identity.profile.FullProfileWithEntities-53',
    'memberIdentity': ''
}

SEARCH_REQUEST_URL = 'https://www.linkedin.com/voyager/api/search/blended'
SEARCH_REQUEST_PARAMS = {
    'start': '0',
    'count': '10',
    'filters': 'List(resultType->PEOPLE,firstName->{first_name},lastName->{last_name})',
    'keywords': '',
    'origin': 'FACETED_SEARCH',
    'q': 'all',
    'queryContext': 'List(spellCorrectionEnabled->true,relatedSearchesEnabled->true)'
}