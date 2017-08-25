# rezrxt

**rezrxt** is a simple baked resolve management layer for rez. It provides an interface and example implementation of a database which tracks rxt files for a given context and package over time. 

Currently, there is a file based implementation, with a planned Postgres + RESTful api coming once the database schema proves stable.

# File Backed DB

The first implementation is backed by a directory structure, which looks something like this:

```
/root
    /context
	/<context>
            /name
		/<name>
            	    /timestamp
 			/<epoc>
                	    /<context>-<name>-<epoc>.rxt
```

An example entry example looks like this:

```
/rezrxt_root/context/fx/name/houdini/timestamp/4311234/fx-houdini-4311234.rxt
```

It is an extreme stretch to refer to this as a database. However, I can play with the api interface without too much trouble. In the future, I plan on using Postgres, and storing the data as bson blobs. This should make for a fun hybrid approach (sql/document), as well as open up queries on metadata.

# Using rezrxt

0. release rezrxt as a rez package.
1. set up your environment, including the path to the database, via env var (REZRXT__DB_ROOT)
2. resolve your environment via ```rez env rezrxt```.
 
