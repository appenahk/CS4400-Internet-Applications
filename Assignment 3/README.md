# Distributed File System

## Distributed Transparent File Access

This is the core of any distributed file system and consists of a server which provides access to files on the machine on which it is executed and a client side file service proxy that provides a language specific interface to the file system.
## Directory Service

The directory service is responsible for mapping human readable, global file names into file identifiers used by the file system itself. 
## Caching

Caching is a vital element of any file system design that is required to give good performance and scale. Put simply, the purpose of caching is to make files quicker to access. 
## Lock Service

The lock service is an important user tool. Certain classes of user applications will modify (deliberately) the same files in a distributed file system. Such tools will need exclusive access to the files they modify.
## Security Service

All interactions between the various servers of a distributed file system should be protected so that third parties cannot spy on the content of messaging crossing the net work, or worse still, damage or corrupt this data.

It works but is rather faulty and prone to errors, security service just outputs an encrypted token, this was meant to be used later but other bugs prevented me from moving much further.