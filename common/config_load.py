import yaml

_config = {}
_pages = {}
_env = None
_options = {}


def init(env="k8s"):
    global _config
    global _env
    _config = yaml.load(open("../resources/config/env_config.yaml"), Loader=yaml.FullLoader)
    _env = _config.get(env)


def get_env():
    return _env


def get_page(page):
    global _pages
    if page not in _pages:
        try:
            _pages[page] = yaml.load(open("../resources/pages/" + page + ".yaml"), Loader=yaml.FullLoader)
        except Exception as e:
            print(e)
            return None
    return _pages[page]


def set_options(key, value):
    global _options
    _options[key] = value


def get_options():
    return _options
