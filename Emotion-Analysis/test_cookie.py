import requests


def check_cookie_validity(cookies):
    # 目标网站的URL
    url = 'https://s.weibo.com/'

    # 使用Session对象，它可以自动处理Cookie
    session = requests.Session()

    # 向目标网站发送请求
    response = session.get(url, cookies=cookies)

    # 检查响应状态码
    if response.status_code != 200:
        print("Cookie可能无效，无法访问页面，状态码：", response.status_code)
        return False

    print("Cookie可能有效，可以正常访问搜索页面。")

    # 检查页面中是否存在某个只有未登录用户才能看到的元素
    login_button = ('<div class="woo-box-flex">'
                    '<a class="LoginBtn_btn_10QRY LoginBtn_btna_1hH9H">登录</a>'
                    '<a class="LoginBtn_btn_10QRY LoginBtn_btnb_bArTC">注册</a>'
                    '</div>')
    if login_button in response.text:
        print("Cookie无效，搜索页面包含登录/注册按钮。")
        return False
    else:
        print("Cookie有效，搜索页面不包含登录/注册按钮。")
        return True


if __name__ == "__main__":
    cookies = input("请输入 Cookie: ")
    check_cookie_validity(cookies)
