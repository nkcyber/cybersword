
This challenge prompts the user to learn how to get
data from a `sqlite_schema`.

If you google for it, you might find something like this:

```
SELECT sql FROM sqlite_schema
```

We have to update the sql injection to be aware of the application.

This is pretty common; if an application expects data to be in a certain
format, the injection needs to match that format.

Here's the solution, just padding to the column width:

```
'; SELECT sql, 1, 1 FROM sqlite_schema --
```

You could also get something that returns three useful tables:

```
'; SELECT name, sql, type FROM sqlite_schema --
```

