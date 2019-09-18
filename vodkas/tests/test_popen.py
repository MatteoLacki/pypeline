x = Popen('powershell.exe ls', stdout=PIPE)
out, err = x.communicate()
out.decode("utf-8")
with open(Path(r'C:\SYMPHONY_VODKAS\temp\test_out.txt'), 'wb') as f:
    z = f.write(out)
