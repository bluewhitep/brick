# Description

This is to use the pixel change of the brick to get the moving distance

This CLI version.

## Install

`pipenv install -r requirements.txt  ` 

## Depend

| Depend | Version  |
| :----: | :------: |
| python |  3.7.9   |
| numpy  |  1.19.1  |
| pandas |  1.2.0   |
| opencv | 4.4.0.44 |

## Option

|        Option        |                    Description                    |
| :------------------: | :-----------------------------------------------: |
|    -v, --version     |                      Version                      |
|  -n, --nooverwrite   |  Disable Overwrite at current Image to old Image  |
|    -o, --oldImage    |                  old Image Path                   |
|  -c, --currentImage  |                current Image Path                 |
| -p, --pixel2distance | Pixel to distance coefficient [cm](default: 1.58) |

## Example

Place 2 images into the `img` directory and name them `oldImage.png` and `currentImage.png`

* `python brick.py`

    Will be overwrite at `currentImage.png` to `oldImage.png` and rename to `oldImage.png`

Disable Overwrite

* `python brick.py -n` 

    Keep `oldImage.png` and `currentImage.png`

## Result

Return `[x_distance, y_distance]`
> x_distance: Positive values is distance moved forward  
> y_distance: Positive values is distance moved left  

Unit is **centimeter**



## 处理过程



## 视频

