import multiprocessing
import time
import base64
import jieba
import gevent
from concurrent.futures import ThreadPoolExecutor


def func(msg):
    print("msg:", msg)
    time.sleep(3)
    print("end")
    return "123" + msg

def test(num,input):
    # global num
    # print('num:',num)
    print('num:',num,'input:',input)
    print('res:',res)
    res[num] = input + '123'
    # output = input + '123'
    # return num,output
    return res

    # process = multiprocessing.cpu_count()
    # print('cpu num:',process)
    # pool = multiprocessing.Pool(process)
    # result = []
    # msg = '一个快捷键对应一个命令或功能，如果使用本命令多次定义同一快捷键，则最新配置生效。如果多次使用本命令将多个快捷键和同一命令、功能绑定，则这些绑定的快捷键均生效。'
    # msg = msg.strip().split('。')
    # # print(msg)
    # for i in range(len(msg)):
    #     ms = msg[i]
    #     result.append(pool.apply_async(func, (ms, )))
    # pool.close()
    # pool.join()
    # data = '.'.join(res.get() for res in result)
    # print(data)
    # for res in result:
    #     print(":::", res.get())
    # print("Sub-process(es) done.")
    # zh = '''
    #   用户按下快捷键后，设备会立即执行对应的命令行或者功能。
    #   用户按下快捷键后，设备会立即执行对应的命令行或者功能。用户按下快捷键后，设备会立即执行对应的命令行或者功能。
    #   '''
    # msg = zh.strip().split('。')
    #
    # to_trans = []
    # for zh in msg:
    #     if not zh == '':
    #         input = " ".join(jieba.cut(zh.strip()))
    #         to_trans.append(input)
    # print(to_trans)
def foo():
    s = '为方便用户快捷操作设备，设备支持23个快捷键。用户按下快捷键后，设备会立即执行对应的命令行或者功能。如果这些快捷键和用户登录终端定义的快捷键冲突，或者不符合用户的使用习惯，用户可使用该命令重新定义快捷键，甚至取消快捷键的绑定关系。'
    msg = s.strip().split('。')
    to_trans = []
    for zh in msg:
        if not zh == '':
            input = " ".join(jieba.cut(zh.strip()))
            to_trans.append(input)
    global res
    res = [None] * len(to_trans)
    # var_list = (len(to_trans),to_trans)
    # for index,value in enumerate(to_trans):
    #     print(ine)
    print('to_trans:',to_trans)
    jobs = [gevent.spawn(test,num,input) for num,input in enumerate(to_trans)]
    # res[num] = job.value
    gevent.joinall(jobs)
    print([job.value for job in jobs])
    print(res)
    print('\n'.join(res))

    # res = ['','','']
    # res[0] = 'ab'
    # print(res)

def get_thread_time(times):
    # time.sleep(times)
    return times
if __name__ == "__main__":





    start = time.time()
    executor = ThreadPoolExecutor(max_workers=4)
    to_trans = ['aa','bb','cc']
    i = 1
    results = executor.map(get_thread_time, [input for input in to_trans])
    # for result in executor.map(get_thread_time, [input for input in to_trans]):
    #     print("task{}:{}".format(i, result))
    #     i += 1
    print(' '.join(results))



