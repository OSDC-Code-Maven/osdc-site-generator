# OSDC Site generator

The code that generates all the web site by the OSDC course participants.

## Usage

See the https://github.com/osdc-Code-Maven/osdc-skeleton repositor as an example

In the GitHub Action workflow file add

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
osdc-site-generator
osdc-skeleton
```

```
cd osdc-site-generator
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt -c constraints.txt
```

* Generate GITHUB token
    * See the [documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

    * Visit [GitHub](https://github.com/) (and log in)
    * Go to [Settings](https://github.com/settings/profile)
    * Go to [Developer Settings](https://github.com/settings/apps)
    * Personal Access tokens / Tokens
    * Generate New token
    * Enable following: notifications, read:org, read:project, read:user, user:email

Then create the environment variable with the value:

```
export MY_GITHUB_TOKEN=.....
```



```
cd ../osdc-skeleton
../osdc-site-generator/generate.py
../osdc-site-generator/app.py
```

## Tools

There is a tool to verify that the CI processes are the same in all the courses as in the skeleton

Another tool allows us to run generate.py on all the courses.
