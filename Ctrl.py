import CtrlServe

while True:
    cmd = input(">")
    answer = CtrlServe.send(cmd)
    if answer.startswith("ERR"):
        print(
            "</!\\ An exception occured while "+{"ERR@SND": "sending", "ERR@CMD": "executing"}[answer]+" your command."
        )
    else:
        print("< Command accepted and executed")
    print("<" + " ".join(answer.split(" ")[1:]).replace("\n", "\n<"))