def hexto64(s):
    import base64, codecs
    return base64.b64encode(codecs.decode(s,"hex"))