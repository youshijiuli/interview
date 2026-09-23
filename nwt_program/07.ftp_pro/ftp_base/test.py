import sys


def upload():
    pass

opt_dic = {
    'operate':'upload'
}

if __name__ == '__main__':
    print(sys.modules)
    print(__name__)
    print(sys.modules[__name__])
    print(hasattr(sys.modules[__name__], opt_dic['operate']))