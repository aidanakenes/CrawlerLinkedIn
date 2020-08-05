import os


DB_PASS = os.environ.get('POSTGRE_PASS')
DB_NAME = os.environ.get('POSTGRE_DB')
ENGINE = f"postgresql://postgres:{DB_PASS}@localhost/{DB_NAME}"
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
REDIS_TTL = int(os.environ.get('REDIS_TTL'))

RedisConfig = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'decode_responses': True
}



USER_PARAMS = {
    'q': 'memberIdentity',
    'decorationId': 'com.linkedin.voyager.dash.deco.identity.profile.FullProfileWithEntities-53',
    'memberIdentity': ''
}

COMPANY_PARAMS = {
    'decorationId': 'com.linkedin.voyager.deco.organization.web.WebFullCompanyMain-28',
    'q': 'universalName',
    'universalName': ''
}

POST_PARAMS = {
    'count': '100',
    'q': 'companyRelevanceFeed',
    'companyIdOrUniversalName': ''
}
