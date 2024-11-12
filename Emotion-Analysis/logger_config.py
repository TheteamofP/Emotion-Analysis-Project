import logging
from logging.handlers import RotatingFileHandler

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
logfile = '%s.log' % __name__  # 将日志文件放在项目根目录下
# 使用RotatingFileHandler可以避免日志文件过大
fh = RotatingFileHandler(logfile, maxBytes=10000, backupCount=5, encoding='utf-8-sig')
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)

# 第四步，将logger添加到handler里面
logger.addHandler(fh)

# 日志测试
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')
