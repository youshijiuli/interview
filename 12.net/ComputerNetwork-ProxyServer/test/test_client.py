import requests


def main():
    """
    test proxy server
    """
    proxies = {
        "http": "127.0.0.1:8888"
    }
    r = requests.get("http://127.0.0.1/HelloWorld.html", proxies=proxies)
    print(r.text)

    """
    test web server

    r = requests.get("http://127.0.0.1/HelloWorld.html")
    print(r.text)
    """


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
