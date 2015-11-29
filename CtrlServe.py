import PSServe
import socket

if __name__ == "__main__":
    server = PSServe.Server(0x7079)
else:
    server = PSServe.EmptyServer()

current_vars = {"this": "{this}"}


def chunkify(msg):
    chunks = []
    not_sent_yet = msg.encode("UTF-8")
    while len(not_sent_yet) >= 8:
        current_chunk = not_sent_yet[:8]
        chunks.append(current_chunk)
        not_sent_yet = not_sent_yet[8:]
    chunks.append(not_sent_yet + b"\n" + b" "*(7-(len(not_sent_yet)+1)))
    return chunks


def send(msg, to=socket.gethostname()):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((to, 0x7079))
        for i in chunkify(msg):
            print(i)
            sock.send(i)
        return handle((to, 0x7079), sock, True)
    except Exception as e:
        return "ERR@SND " + str(e)


def execute(cmd):
    commands = {"say_hello": lambda args: "Hello! I like people liking the Pythonic State and Python."}
    if cmd.split(" ")[0] in commands.keys():
        try:
            return "SUCCESS "+commands[cmd.split(" ")[0]](cmd.split(" ")[1:])
        except Exception as e:
            return "ERR@CMD "+str(e)
    else:
        return "ERR@CMD Command not found"


@server.use
def handle(addr, sock, answer=False):
    times = 0
    print("Yay!")
    while (not answer) or times < 1:
        chunks = []
        chunk = sock.recv(8)
        chunks.append(chunk)
        if "\n" in chunk:
            times = 1
            msg = b"".join(chunks).decode("UTF-8").split("\n")[0]
            rmsg = msg.format(**current_vars)
            if answer:
                return rmsg
            else:
                if rmsg.startswith("{this}:"):
                    cmd = rmsg[len("{this}: "):]
                    sock.send(execute(cmd).encode("UTF-8"))
                elif rmsg.startswith(" "):
                    cmd = rmsg[len(" "):]
                    sock.send(execute(cmd).encode("UTF-8"))
                else:
                    sock.send(send(":".join(rmsg.split(":")[1:]), to=rmsg.split(":")[0]).encode("UTF-8"))