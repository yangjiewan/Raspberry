import json, os

_content = ''
with open('control_page.html') as fp:
    _content = fp.read()
_car_action = None


def home(request_, response_, route_args_):
    if 'car_action' in route_args_ and _car_action is not None:
        _car_action(route_args_['car_action'])
    return response_.write_response_OK_(content_type_='text/html', content_=_content, charset_='UTF-8')


rpc_registry = {}


def ajax_(request_, response_, route_args_):
    global rpc_registry
    params_ = request_.params_
    assert 'data' in params_, '服务请求参数中缺少 data'
    data = json.loads(params_['data'])
    assert 'func_name' in data
    assert 'argv' in data
    func_name = data['func_name']
    argv = data['argv']
    assert func_name in rpc_registry, f'服务中没有登记函数 {func_name}, 所有函数: {", ".join(rpc_registry.keys())}'
    res = rpc_registry[func_name](*argv)
    json_ = json.dumps(res)
    return response_.write_response_JSON_OK_(json_)


def start_server_(port_, max_threads_, esp32_html_=None, car_action=None):
    from .lib.http_ import Http_
    http_ = Http_(ip_='0.0.0.0', port_=port_, web_path_='web', max_threads_=max_threads_)
    if car_action is not None:
        global _car_action
        _car_action = car_action
    if esp32_html_ is not None:
        http_.add_route_('/', esp32_html_, client_addr_='192.168.4.')
    http_.add_route_('/ajax', ajax_, 'GET')
    http_.add_route_('/ajax', ajax_, 'POST')
    http_.add_route_('/', home, 'GET')
    http_.add_route_('/home/{car_action}', home, 'GET')
    http_.start_()


if __name__ == '__main__':
    start_server_(80, 100)