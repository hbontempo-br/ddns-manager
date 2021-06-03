# dynamic-ip-updater-google-domains
Easily keep your Google Domains Synthetic Record up to date with your Dynamic IP.


**dynamic-ip-updater-google-domains** is a small and easy project made with python3 that intents to help you keep
your Google Domains Synthetic Record pointing to your machine when you have a dynamic IP from your ISP.

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
You can hire a service for this like [no-ip](https://www.noip.com) and they do a grate job, but if you want advance 
control or even some simple things like using your custom domain are paid and sometimes even require you to transfer 
your domain their platform.

[TODO] Put reference to inspiration article.

## Objective

This project have a direct purpose: with just a domain in Google Domains keep a subdomain pointing to your home without 
worrying with static IP or ane other paid service. Just a small script running on your computer.

It's meant to do a simple and very specific function: monitor changes on it's current external IP and, if a change is 
noticed, update the domain on Google Domains Synthetic Records.

## Getting Started

### Before you start

You must have a domain in Google Domain (if you don't have one you can 
[buy one](https://support.google.com/domains/answer/4491208?hl=en) or 
[transfer your domain](https://support.google.com/domains/answer/9003139?hl=en)) and must set up a Dynamic DNS 
synthetic record a get it's credentials (detailed steps: https://support.google.com/domains/answer/6147083?hl=en).

### Clone

Cloning this project requires [git][git], instructions provided below.

#### Option 1: HTTPS

Check [clone with https][git_clone_https] for further information.

```bash
    $ git clone https://github.com/hbontempo-br/dynamic-ip-updater-google-domains.git
```

#### Option 2: SSH

Check [clone with ssh][git_clone_ssh] for further information.

```bash
    $ git clone git@github.com:hbontempo-br/dynamic-ip-updater-google-domains.git
```


### Run script

Install dependencies (setting up a virtual environment is recommended):

With pip:
```bash
    $ pip3 install requirements.txt
```

Make sure you have the following environment variables set:
- USERNAME=<your_domains_username>
- PASSWORD=<your_domains_password>
- HOSTNAME=<your_domain>
- UPDATE_DELAY=<[optional]seconds_between_verifications>

Then just run the [app.py](app.py):

```bash
    $ python3 app.py
```

### Test [TODO]

:construction: :construction: :construction: :construction: :construction:
Testing this project requires **...**, instructions provided below.

```bash
    $ echo 'instructions'
```

## Running on Docker

### Build

The latest image of this project can be found on in 
[DockerHub](https://cloud.docker.com/u/hbontempo/repository/docker/hbontempo/dynamic-ip-updater-google-domains), 
but you can build it yourself:
```bash
    $ docker build -t dynamic-ip-updater-google-domains -f Dockerfile .
```

### Run

**It the recommended way**, just use the environment variables described above:

```bash
    $ docker run \
        -e USERNAME=<your_domains_username> \
        -e PASSWORD=<your_domains_password> \
        -e HOSTNAME=<your_domain> \
        -e UPDATE_DELAY=<[optional]seconds_between_verifications> \
        --restart=always \
        -d hbontempo/dynamic-ip-updater-google-domains
```

It's a good practice to run your this container with a `--restart=always` as showed above so your container 
starts running again even if a problem happens.

## Pack [TODO]

:construction: :construction: :construction: :construction: :construction:
Packing this project requires **...**, instructions provided below.

```bash
    $ echo 'instructions'
```

## Contributors

This project is originally designed by **[Henrique Bontempo][author]**.
Check the [contributors][contributors] list for further information.

## Contributing

This project has some rules, a code of conduct, and a process for submitting
code and pull requests. Check the [contributing](CONTRIBUTING.md) file for
further information.

## Versioning

This project follows [semantic versioning][semantic_versioning] and
[keep a changelog][keep_a_changelog] practices. Changelog files should be
provided in a per release basis using these practices.

## License

This project is licensed under the **MIT** license. Check the [license](LICENSE)
file for further information.



[author]: https://github.com/hbontempo-br/
[git]: https://git-scm.com
[git_clone_https]: https://help.github.com/articles/which-remote-url-should-i-use/#cloning-with-https-urls-recommended
[git_clone_ssh]: https://help.github.com/articles/which-remote-url-should-i-use/#cloning-with-ssh-urls
[contributors]: https://github.com/hbontempo-br/dynamic-ip-updater-google-domains/contributors
[semantic_versioning]: http://semver.org/spec/v2.0.0.html
[keep_a_changelog]: http://keepachangelog.com/en/1.0.0/
