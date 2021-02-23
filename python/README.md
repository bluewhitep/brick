# Description

This is to use the pixel change of the brick to get the moving distance

This CLI version.

## Install

`pip install -r requirements.txt  ` 

## Depend

|       Depend       |          Version        |
| :----------------: | :---------------------: |
|       python       |          3.7.9          |
|       numpy        |          1.19.1         |
|       pandas       |          1.2.0          |
|       opencv       |          4.4.0          |

## Option

|       Option       |                   Description                   |
| :----------------: | :---------------------------------------------: |
|   -v, --version    |                     Version                     |
| -n, --nooverwrite  | Disable Overwrite at current Image to old Image |
|   -o, --oldImage   |                 old Image Path                  |
| -c, --currentImage |               current Image Path                |

## Example

Place 2 images into the `img` directory and name them `oldImage.png` and `currentImage.png`

* `python brick.py`

    Will be overwrite at `currentImage.png` to `oldImage.png` and rename to `oldImage.png`

Disable Overwrite

* `python brick.py -n` 

    Keep `oldImage.png` and `currentImage.png`
