import PSServe

server = PSServe.Server(0x7079)
current_vars = {"this": "{this}"}


def send(msg, to):
    pass


def execute(cmd):
    pass


@server.use
def handle(addr, sock):
    while True:
        chunks = []
        chunk = sock.recv(64)
        chunks.append(chunk)
        if "\n" in chunk:
            msg = "".join(chunks).split("\n")[0]
            rmsg = msg.format(**current_vars)
            if rmsg.startswith("{this}:"):
                cmd = rmsg[len("{this}:"):]
                execute(cmd)
            else:
                send(":".join(rmsg.split(":")[1:]), to=rmsg.split(":")[0])