import json
from functools import wraps
from urllib.request import urlopen

from flask import request
from jose import jwt

AUTH0_DOMAIN = 'udacity-coffeeshop.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://localhost:5000/'

# AuthError Exception

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
"""
A function to get the token from request 'Authorization' header

:param None

Checks 'Authorization' header if it exists and set default value to None

Splits the header into two parts

Checks that the first part of the header contains the right 'Auth Scheme' which is 'Bearer'

Checks the length of the parts, that's not bigger than 2 or equal to 1

:raises 'Auth Error' (401)

:returns token of type String

"""


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)

    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]

    return token


"""
A function to check for permissions in the payload provided

:param payload (token payload after decoded)
:param permission (permission (str) from the decorator specified on various endpoints

Checks if the 'permissions' claim is in the payload
Checks if the provided 'param permission' is 'permissions' claim

:raises 'Auth Error' (400)
:raises 'Auth Error' (403)

:returns true

"""


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in the token!'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permissions not found!'
        }, 403)

    return True


"""
A function that decodes the provided token (JWT)

:param token (str) which is a JWT

Gets the Json Web Key from the url ('https://{udacity-coffeeshop.auth0.com}/.well-known/jwks.json')
Gets the 'unverified_header'

Checks if 'kid' is not in the 'unverified header'

Gets RSA Key by checking all the keys in the jwks['key']

Decodes the jwt using the toke, RSA key, algorithm, audience, issuer

:raises 'Auth Error' (401) 
:raises 'Auth Error' (400) 

:returns payload

"""


def verify_decode_jwt(token):
    jsonurl = urlopen('https://{}/.well-known/jwks.json'.format(AUTH0_DOMAIN))

    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:

        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


"""
A decorator to request authentication to secure endpoints

:param permission (str) 

:returns @requires_auth_decorator  
"""


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
