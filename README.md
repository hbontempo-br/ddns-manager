# ddns-manager
[![ci](https://circleci.com/gh/hbontempo-br/ddns-manager.svg?style=shield)](https://circleci.com/gh/hbontempo-br/ddns-manager) 
[![codecov](https://codecov.io/gh/hbontempo-br/ddns-manager/branch/master/graph/badge.svg)](https://codecov.io/gh/hbontempo-br/ddns-manager)

Easily keep your DNS records up to date with your Dynamic IP.

**ddns-manager** is a small and easy project made with python3 that intents to help you keep
your DNS records pointing to your machine when you have a dynamic IP from your ISP.

Originally designed by **[Henrique Bontempo][author]**.

## The problem

If you want to access you home network through a VPN, host your own website, host a game server, have remote access to 
our security cameras or any other task that you have to access your home network from the internet you must have to 
locate it .

The most direct way is through your public IP , and it's easy if you have a static IP, but they are expensive and for 
many regions almost exclusive to business. If your ISP won't provide static IP on your location or you don't want to 
pay for it than you are stuck with a dynamic IP. You still can reach your home through your external IP, but there are 
no guarantees that this address won't change without a notice.

To circumvent this problem the most common idea is to use a url address that is constantly updated your external IP. 

## Objective

This project have a direct purpose: a simple and easy way of managing your DDNS.

## Getting Started

### Clone

Cloning this project requires [git][git], instructions provided below.

#### Option 1: HTTPS

Check [clone with https][git_clone_https] for further information.

```bash
    $ git clone https://github.com/hbontempo-br/ddns-manager.git
```

#### Option 2: SSH

Check [clone with ssh][git_clone_ssh] for further information.

```bash
    $ git clone git@github.com:hbontempo-br/ddns-manager.git
```


### Run script

Install dependencies (setting up a virtual environment is recommended):

With pip:
```bash
    $ pip3 install requirements.txt
```

Then just run:

```bash
    $ python3 -m ddns_manager
```

### Test

No secret here:

```bash
    $ python3 -m unittest discover
```

## Running on Docker

You can run the update loop inside a docker container.
~~The image can be found in Docker-hub.~~

### Build

```bash
    $ docker build -t ddns-manager -f Dockerfile .
```

### Run

**It the recommended way**, just use the environment variables described above:

```bash
    $ docker run \
        -v PATH_CONFIG:/config/config.yml
        -d hbontempo/ddns-manager
```

It's a good practice to run your this container with a `--restart=always` as showed above so your container 
starts running again even if a problem happens.

## Contributors

This project is originally designed by **[Henrique Bontempo][author]**.
Check the [contributors][contributors] list for further information.

## Contributing

This project has some rules, a code of conduct, and a process for submitting
code and pull requests. Check the [contributing](CONTRIBUTING.md) file for
further information.

## ~~Versioning~~

~~This project follows [semantic versioning][semantic_versioning] and
[keep a changelog][keep_a_changelog] practices. Changelog files should be
provided in a per release basis using these practices.~~

## License

This project is licensed under the **MIT** license. Check the [license](LICENSE)
file for further information.



[author]: https://github.com/hbontempo-br/
[git]: https://git-scm.com
[git_clone_https]: https://help.github.com/articles/which-remote-url-should-i-use/#cloning-with-https-urls-recommended
[git_clone_ssh]: https://help.github.com/articles/which-remote-url-should-i-use/#cloning-with-ssh-urls
[contributors]: https://github.com/hbontempo-br/ddns-manager/contributors
[semantic_versioning]: http://semver.org/spec/v2.0.0.html
[keep_a_changelog]: http://keepachangelog.com/en/1.0.0/
