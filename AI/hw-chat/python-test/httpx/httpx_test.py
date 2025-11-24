import httpx
from fake_useragent import UserAgent
#
# headers = {
#     'user-agent': UserAgent().random,
# }
# params = {
#     'wd': 'python'
# }
# response = httpx.get('https://www.baidu.com/s', params=params, headers=headers)
# response.encoding = response.charset_encoding
# print(response.text)
#
#

# data = {'key1': 'value1', 'key2': 'value2'}
# r = httpx.post("https://httpbin.org/post", data=data)
# print(r.text)
#
# with httpx.Client() as client:
#     pass
#
# client = httpx.Client()
# try:
#     pass
# finally:
#     client.close()


# # 共用请求头
# url = 'http://httpbin.org/headers'
# headers = {'user-agent': 'my-app/0.0.1'}
# with httpx.Client(headers=headers) as client:
#     r = client.get(url)
#
# print(r.json()['headers']['User-Agent'])

# 公共 + 私有
# headers = {'X-Auth': "from-client"}
# params = {'client_id': "client1"}
# with httpx.Client(headers=headers, params=params) as client:
#     headers_ = {'X-Custom': 'from-request'}
#     params_ = {'request_id': 'request1'}
#     r = client.get('https://example.com', headers=headers_, params=params_)
# print(r.request.url)
# print(r.request.headers['X-Auth'])
# print(r.request.headers['X-Custom'])

