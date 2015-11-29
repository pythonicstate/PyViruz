import PSServe
import socket

server = PSServe.Server(0x7079)
current_vars = {"this": "{this}"}


def chunkify(msg):
    chunks = []
    not_sent_yet = msg
    while len(not_sent_yet) >= 64:
        current_chunk = not_sent_yet[:64]
        chunks.append(current_chunk)
        not_sent_yet = not_sent_yet[64:]
    chunks.append(not_sent_yet + "\n" + " "*(64-(len(not_sent_yet)+1)))
    return chunks


def send(msg, to):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((to, 0x7079))
        for i in chunkify(msg):
            sock.send(i)
        return handle((to, 0x7079), sock, True)
    except:
        return "ERR@SND"


def execute(cmd):
    commands = {}
    if cmd.split(" ")[0] in commands.keys():
        return "SUCCESS "+commands[cmd.split(" ")[0]](cmd.split(" ")[1:])
    else:
        return "ERR@CMD"


@server.use
def handle(addr, sock, answer=False):
    times = 0
    while (not answer) or times < 1:
        times = 1
        chunks = []
        chunk = sock.recv(64)
        chunks.append(chunk)
        if "\n" in chunk:
            msg = "".join(chunks).split("\n")[0]
            rmsg = msg.format(**current_vars)
            if answer:
                return rmsg
            else:
                if rmsg.startswith("{this}:"):
                    cmd = rmsg[len("{this}:"):]
                    sock.send(execute(cmd))
                elif rmsg.startswith(" "):
                    cmd = rmsg[len(" "):]
                    sock.send(execute(cmd))
                else:
                    sock.send(send(":".join(rmsg.split(":")[1:]), to=rmsg.split(":")[0]))