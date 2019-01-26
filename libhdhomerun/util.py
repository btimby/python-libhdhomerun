def ip_to_str(ip):
    return '%d.%d.%d.%d' % (
        (ip >> 24 & 0xff), (ip >> 16 & 0xff), (ip >> 8 & 0xff),
        (ip >> 0 & 0xff))
