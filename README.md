# clinix

The clinix application performs simple introspection to display its
own package details, geolocation information for the invoking host,
the local time and the path used to launch the program.
Every second it checks to see if its own invocation path has changed,
and if so it will then re-exec itself using the updated version.

## Floxify

```
flox init
```
* select "Application" type
* select `buildPythonApplication()` builder

## Build

```
flox build
```

## Register

```
flox register
```

## Publish

```
flox publish
```

## Deploy

```
flox install
flox pull
```
