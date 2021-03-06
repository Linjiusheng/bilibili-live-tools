from bilibili import bilibili
import time
import datetime
import asyncio
import printer
import login


def CurrentTime():
    currenttime = int(time.mktime(datetime.datetime.now().timetuple()))
    return currenttime


async def heartbeat():
    json_response = await bilibili.apppost_heartbeat()
    json_response = await bilibili.pcpost_heartbeat()
    json_response = await bilibili.heart_gift()
    # print('pcpost_heartbeat', json_response)


# 因为休眠时间差不多,所以放到这里,此为实验性功能
async def draw_lottery():
    blacklist = ['test', 'TEST', '测试', '加密']
    max = 10000
    min = 50
    while max > min:
        # print(min, max)
        middle = int((min + max + 1) / 2)
        code_middle = (await bilibili.get_lotterylist(middle))['code']
        if code_middle:
            code_middle1 = (await bilibili.get_lotterylist(middle + 1))['code']
            code_middle2 = (await bilibili.get_lotterylist(middle + 2))['code']
            if code_middle1 and code_middle2:
                max = middle - 1
            else:
                min = middle + 1
        else:
            min = middle
    print('最新实物抽奖id为', min, max)
    for i in range(max - 30, max + 1):
        json_response = await bilibili.get_lotterylist(i)
        print('id对应code数值为', json_response['code'], i)
        # -400 不存在
        if not json_response['code']:
            temp = json_response['data']['title']
            if any(word in temp for word in blacklist):
                print("检测到疑似钓鱼类测试抽奖，默认不参与，请自行判断抽奖可参与性")
                # print(temp)
            else:
                check = json_response['data']['typeB']
                for g, value in enumerate(check):
                    join_end_time = value['join_end_time']
                    join_start_time = value['join_start_time']
                    ts = CurrentTime()
                    if int(join_end_time) > int(ts) > int(join_start_time):
                        json_response1 = await bilibili.get_gift_of_lottery(i, g)
                        print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                        print("参与实物抽奖回显：", json_response1)
                    else:
                        pass
        
        
async def run():
    while 1:
        printer.info(["心跳"], True)
        login.HandleExpire()
        await heartbeat()
        await draw_lottery()
        await asyncio.sleep(300)


