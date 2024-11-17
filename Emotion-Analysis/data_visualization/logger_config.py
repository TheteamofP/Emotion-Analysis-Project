import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta

# 确保日志文件存放的目录存在
log_directory = '../logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建一个handler，用于写入日志文件
logfile = os.path.join(log_directory, '%s.log' % __name__)
# 使用RotatingFileHandler可以避免日志文件过大
fh = RotatingFileHandler(logfile, maxBytes=10000, backupCount=5,
                         encoding='utf-8-sig')
fh.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] "
                              "- %(levelname)s: %(message)s")
fh.setFormatter(formatter)

# 将logger添加到handler里面
logger.addHandler(fh)


# 定义一个函数来检查并删除过旧的日志文件
def delete_old_logs(log_directory, days=1):
    current_time = datetime.now()
    for filename in os.listdir(log_directory):
        file_path = os.path.join(log_directory, filename)
        if os.path.isfile(file_path):
            file_age = current_time - datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_age > timedelta(days=days):
                os.remove(file_path)
                logger.info(f"Deleted old log file: {filename}")


# 调用函数，例如每天删除一次过旧的日志
delete_old_logs(log_directory)

# # 日志测试
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')
