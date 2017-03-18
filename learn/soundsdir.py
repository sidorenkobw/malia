import urllib, datetime

userForId = {
    '13EubbAsOYgy3eZX4LAHsB5Hzq72': 'donna',
    '8WO9WnJj80SP6WRdbIZh4IxgPP82': 'drewpca',
    '4WGnHLHt9CbiOdaqOVAJGzbW2QP2': 'andrew',
    '4GGUPEPZYNahAwZpQSG6n4QIR913': 'dave',
    'd8Lo6MJMqZOGXeGDbnHkpXzeovY2': 'd8?',
}

def soundFields(p):
    segments = p.split('/')
    try:
        d = {}
        if segments[0] == 'sounds':
            segments.pop(0)
        if segments[0] == 'incoming':
            segments.pop(0)

        if len(segments) > 0:
            d['user'] = userForId.get(segments[0], segments[0])
        if len(segments) > 1:
            d['word'] = urllib.unquote(segments[1])
            if segments[1].endswith('.webm'):
                # old format
                d['word'], m = segments[1].split('_', 1)
                d['milli'] = int(m.split('.')[0])
            elif len(segments) > 2:
                d['milli'] = int(segments[2].replace('.webm', ''))
        if 'milli' in d:
            d['iso'] = datetime.datetime.fromtimestamp(d['milli'] / 1000).isoformat('T').split('.')[0]
        return d

    except Exception:
        print 'segments = %r' % segments
        raise
