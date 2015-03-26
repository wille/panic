# panic

Inspired by and text from [panic_bcast](https://github.com/qnrq/panic_bcast) by [qnrq](http://qnrq.se)

Written in Python 3 with the intention to support Windows, OS X and Linux.

panic is a network protocol panic button operating decentralized through UDP broadcasts and HTTP. It's intended to act a panic button in a sensitive network making it harder to perform cold boot attacks. A serious freedom fighter will run something like this on all nodes in the computerized network.

To trigger the panic signal over HTTP simply request http://...:8080/<key> from a machine that is running panic. Which ever will do.

## How it works

1. An activist has uninvited guests at the door
2. The activist sends the panic signal, a UDP broadcast, with panic
3. Other machines in the network pick up the panic signal
4. Once it has picked the panic signal it ejects all mounted TrueCrypt drives and powers off the machine.

## Authentication

You will need to set a password/key using --key to prevent unauthorized machines to shut down computers running panic

For script help execute with the --help parameter.

## Synopsis

```
'python(3) panic.py' [-b | --bport <button-port>] [-s | --sport <udp-port>] [-h | --help] [-k | --key <key>]
```
