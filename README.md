# Modpack server bootstrap

A bootstrapper for setting up new minecraft servers, making use of Packwiz for modpack download, nix for dependencies (java version) and some python scripts for convenience

Find Packwiz here (it's doing all the heavy lifting)

https://github.com/packwiz/packwiz-installer-bootstrap?tab=MIT-1-ov-file#readme
https://github.com/packwiz/packwiz


## Requirements:

Nix (can be installed on distros other than nixos)
Python 3 with tomllib package

## Setup

To use, modify the shell.nix and update the following values as needed

```nix
{
  memory_max = "5G";
  memory_min = "1G";

  modpack_name = "otherwhere";
  webserver_host = "change_me";

  pack_url = "${server_host}/modpacks/${modpack_name}/pack.toml";
}
```

The installer will download and install the modpack from the URL provided
(if needed, the whole pack URL can be replaced, this is the format I use)


## Usage

To setup the server:

```bash
nix-shell
install_server
```

To run:

```bash
nix-shell
run-loop # (or just run if you don't want auto restart)
```
