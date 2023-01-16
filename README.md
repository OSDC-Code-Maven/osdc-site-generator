# OSDC Site generator

The code that generates all the web site by the OSDC course participants.

## Usage

See the https://github.com/osdc-Code-Maven/osdc-skeleton repositor as an example

In the GitHub Actionw workflow file add

```
    - name: Generate HTML Pages
      uses: osdc-code-maven/osdc-site-generator@v1
```

## Usage locally


* Clone the repository of the site generator:

```
git clone git@github.com:OSDC-Code-Maven/osdc-site-generator.git
```


* Clone your the repo of the OSDC course

```
git clone git@github.com:OSDC-Code-Maven/osdc-skeleton.git
```

So you will have two folders one next to the other:

```
osdc-site-generators
osdc-skeleton
```

```
cd osdc-skeleton
```

```
pip install -r ../osdc-site-generator/requirements.txt
../osdc-site-generator/generate.py
../osdc-site-generator/app.py
```

