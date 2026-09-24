def processBar(num, total):
    rate = num / total
    rate_num = int(rate*100)
    if rate_num == 100:
        r = '\r%s>%d%%\n' % ('=' * rate_num, rate_num,)
    else:
        r = '\r%s>%d%%' % ('=' * rate_num, rate_num,)
    print(r, flush=True)


processBar(2048, 10240)
