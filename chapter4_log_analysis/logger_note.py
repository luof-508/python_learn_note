"""日志处理总结：
1、日志处理，首先实例化一个主对象Manger或者RootLogger。 ->传入name，则实例化Manger.getLogger(__name__)
2、其他处理方式（日志流处理、文件处理等）都通过addHandler添加进去
3、日志的处理方式handler主要有：
    StreamHandler：logging.StreamHandler；日志输出到流，可以是sys.stderr，sys.stdout或者文件
    FileHandler：logging.FileHandler；日志输出到文件
    BaseRotatingHandler：logging.handlers.BaseRotatingHandler；基本的日志回滚方式
    RotatingHandler：logging.handlers.RotatingHandler；日志回滚方式，支持日志文件最大数量和日志文件回滚
    TimeRotatingHandler：logging.handlers.TimeRotatingHandler；日志回滚方式，在一定时间区域内回滚日志文件
    SocketHandler：logging.handlers.SocketHandler；远程输出日志到TCP/IP sockets
    DatagramHandler：logging.handlers.DatagramHandler；远程输出日志到UDP sockets
    SMTPHandler：logging.handlers.SMTPHandler；远程输出日志到邮件地址
    SysLogHandler：logging.handlers.SysLogHandler；日志输出到syslog
    NTEventLogHandler：logging.handlers.NTEventLogHandler；远程输出日志到Windows NT/2000/XP的事件日志
    MemoryHandler：logging.handlers.MemoryHandler；日志输出到内存中的指定buffer

日志等级可以分为5个，从低到高分别是:
    1. DEBUG
    2. INFO
    3. WARNING
    4. ERROR
    5. CRITICAL
日志等级说明:
    DEBUG：程序调试bug时使用
    INFO：程序正常运行时使用
    WARNING：程序未按预期运行时使用，但并不是错误，如:用户登录密码错误
    ERROR：程序出错误时使用，如:IO操作失败
    CRITICAL：特别严重的问题，导致程序不能再继续运行时使用，如:磁盘空间为空，一般很少使 用
    默认的是WARNING等级，当在WARNING或WARNING之上等级的才记录日志信息。

日志还支持捕获traceback:
    两种方式：logger.exception(msg, *args)  <==> logger.error(msg, exc_info=True, *args)
"""
import logging

LOGGER_FORMAT = '[%(asctime)s][%(levelname)s][%(pathname)s][%(funcName)s][%(lineno)d] - %(message)s'
LOGGER_HANDLER_FORMAT = '[%(asctime)s][%(levelname)s][%(pathname)s][%(filename)s][%(funcName)s][%(lineno)d][%(threadName)s] - %(message)s'

# 将日志流steam打印到屏幕
# logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)

# 将日志流打印到屏幕二
console = logging.StreamHandler()
console.setLevel(logging.INFO)
con_format = logging.Formatter(LOGGER_FORMAT)
console.setFormatter(con_format)

# 将日志流保存到文件
handler = logging.FileHandler(filename='D:\\repository\\LeetCodeExercise\\plugins\\logger\\test.txt', mode='w')
_format = logging.Formatter(LOGGER_HANDLER_FORMAT)
handler.setFormatter(_format)
handler.setLevel(logging.INFO)

# 实例化日志主对象
logger = logging.getLogger(__name__)

# 添加日志处理方式
logger.addHandler(handler)
logger.addHandler(console)


# ------
logger.info('start print log')
logger.debug('do something')
logger.warning('something maybe fail')
logger.info('finish')

# 日志还支持捕获traceback
# 两种方式：logger.exception(msg, *args)  <==> logger.error(msg, exc_info=True, *args)
try:
    open('text.txt', 'rb')
except Exception:
    logger.exception('failed to open text.txt, Details:')
    logger.error('failed', exc_info=True)
