# ptop

An awesome task manager written in python. A more awesome top like thing in your terminal !


![ptop-image](https://github.com/darxtrix/ptop/blob/master/docs/ptop_demo.gif)


> Inspired by [vtop](https://github.com/MrRio/vtop)


## Some Screenshots

![ptop-1](https://github.com/darxtrix/ptop/blob/master/docs/ptop_01.png)

![ptop-2](https://github.com/darxtrix/ptop/blob/master/docs/ptop_02.png)


# Installation
`ptop` is compaible with both Python2.x and Python3.x and is tested on Linux and MaxOSx (should be invoked as root).

```bash
$ pip install ptop
```


## Usage

```bash
$ ptop

$ ptop -t <theme>   # custom theme

$ ptop -csrt 500    # custom refresh time for cpu stats 

$ ptop -h           # help
```

## Features
- Killing a process :heavy_check_mark:
- Showing system ports and files used by a process :heavy_check_mark:
- Network Monitor :heavy_check_mark:
- Process search :heavy_check_mark:
- Sorting on the basis of process lifetime and memory used :heavy_check_mark:
- Responsiveness with terminal :heavy_check_mark:
- Custom refresh times for different stats like memory info, process info etc :heavy_check_mark:
- Rolling version updates :heavy_check_mark:

For suggesting new features please add to this [issue](https://github.com/darxtrix/ptop/issues/29)


## Supported themes

- `colorful`     
- `elegant`    
- `simple`    
- `dark`   
- `light` 


## Developing ptop

```bash
$ git clone https://github.com/darxtrix/ptop
$ cd ptop   
$ pip install -r requirements.txt
$ python setup.py develop
```
**Note :** ptop will create a log file called `.ptop.log` in the home directory of the user.


## Main modules :
- `ptop.core` : Defines a basic `Plugin` class that other plugins in the `ptop.plugins` inherit.
- `ptop.interfaces` : The interface to the ptop built using npyscreen.
- `ptop.plugins` : This module contains all the plugin sensors supported i.e `Disk Sensor`,`Memory Sensor`,`Process Sensor`, etc. ( Any new plugin should be added here).
- `ptop.statistics` : Generate continuous statistics using background thread jobs by locating plugins in the plugins directory.
- `ptop.utils` : Custom thread classes.


## Main Dependencies
- [npyscreen](https://pypi.python.org/pypi/npyscreen)
- [psutil](https://pypi.python.org/pypi/psutil)
- [drawille](https://github.com/asciimoo/drawille)


## Contributions

- Pull requests are awesome and always welcome. Please use the [issue tracker](https://github.com/darxtrix/ptop/issues) to report any bugs or file feature requests.


## License 

MIT © [Ankush Sharma](http://github.com/darxtrix)