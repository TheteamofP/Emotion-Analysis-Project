import re
from datetime import datetime

from visualization.mappings import weibo_type_mapping, contain_type_mapping

def update_settings(setting_name, new_value, file_path="settings.py"):
    """在 settings.py 中更新指定的配置项"""
    # 使用正则表达式找到配置项并替换为新的值
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 将新的值转换为字符串格式
    if isinstance(new_value, (dict, list)):
        new_value = repr(new_value)  # 将字典或列表转换为字符串表示

    # 使用 re.sub 替换内容，并将结果赋值回 content
    content = re.sub(
        rf"^{setting_name} = .*",
        f"{setting_name} = {new_value}",
        content,
        flags=re.MULTILINE
    )

    # 写入更新后的内容
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    # 提示用户输入关键词列表和 Cookie等基础信息
    cookie = input("请输入 Cookie: ")
    keywords = input("请输入关键词列表，用逗号分隔: ")
    start_date = input("请输入搜索的起始日期（格式 yyyy-mm-dd）：")
    end_date = input("请输入搜索的终止日期（格式 yyyy-mm-dd）：")
    regions = input("请输入想要筛选的微博发布的地区，用逗号分隔：")
    weibo_type_input = input("请输入微博类型（全部微博，全部原创微博，热门微博，关注人微博，认证用户微博，媒体微博，观点微博）: ")
    contain_type_input = input("请输入筛选类型（不筛选，包含图片，包含视频，包含音乐，包含短链接）: ")

    # 检查日期格式是否符合要求
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("日期格式错误，请使用 yyyy-mm-dd 格式")
        return


    # 将关键词转换为 Python 列表格式
    keyword_list = [kw.strip() for kw in keywords.split(",")]

    if regions.strip() == "":
        region_list = []
    else:
        region_list = [region.strip() for region in regions.split(",")]

    # 更新 DEFAULT_REQUEST_HEADERS 中的 'cookie' 字段
    default_request_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "cookie": cookie
    }
    update_settings("DEFAULT_REQUEST_HEADERS", default_request_headers)

    # 更新 settings.py 中的 KEYWORD_LIST 和 REGION
    update_settings("KEYWORD_LIST", keyword_list)
    update_settings("REGION", region_list)

    # 更新 settings.py 中的 START_DATE 和 END_DATE
    update_settings("START_DATE", f"'{start_date}'")
    update_settings("END_DATE", f"'{end_date}'")


    # 根据用户输入获取对应的数值
    weibo_type = weibo_type_mapping.get(weibo_type_input, 0)
    contain_type = contain_type_mapping.get(contain_type_input, 0)

    # 更新 settings.py 中的 WEIBO_TYPE 和 CONTAIN_TYPE
    update_settings("WEIBO_TYPE", weibo_type)
    update_settings("CONTAIN_TYPE", contain_type)

    print("settings.py 已成功更新！")


if __name__ == "__main__":
    main()
