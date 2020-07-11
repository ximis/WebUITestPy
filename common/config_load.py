import yaml

_config = {}
_pages = {}
_env = None


def init(env="k8s"):
    global _config
    global _env
    _config = yaml.load(open("../resources/config/env_config.yaml"))
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
