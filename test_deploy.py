import urllib.request, urllib.error
try:
    print(urllib.request.urlopen("https://alumni-portal-two-pi.vercel.app/api/health").read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("ERROR TRACEBACK:", e.read().decode())
