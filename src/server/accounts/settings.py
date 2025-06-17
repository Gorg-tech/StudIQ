INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'account',
]

AUTH_USER_MODEL = 'account.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
