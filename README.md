# Huawei Image challenge

## General use
To debur an image you just have to:

```shell
$ python main.py --data input.jpg --output output.jpg
```

### Input data

The maximum width is 245 pixels, the maximum height is 78 pixels.

### Data Struture

```
.
├── README.md
├── data                 //Where data is going to be
└── src                  //Where code and pre-processing is going to be
    └── mnist_convnet.py
```

### Git

We use `git` to control the version and we have following conventions to keep our repository clean and tidy.

#### Branches Management

Each developer should work in their own branch. Except the `master`, all branches' name will be prefixed with `dev-` and concatenated with developers' name or functionalities.

Each developer should only have a master branch and your owning branches in local system.

Each developer should only `add` and `commit` to your own branches. If you need to merge it to `master`, please create a pull request on GitHub.

### Virtual Environments

To use the virtual environment, you first have to create it in the repo after you clone it. To do this, use venv to create it, then activate it and finally install all the requirements in the [requirements.txt](/requirements.txt).

``` shell
$ python -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

When you are done with the virtual environment and with editing the project, you can deactivate it like this.

``` shell
$ deactivate
```

## Resources

### Papers

- [Motion deblurring](http://www.cse.cuhk.edu.hk/leojia/projects/motion_deblurring/deblur_siggraph08.pdf)
- [Blurred image restoration](http://yuzhikov.com/articles/BlurredImagesRestoration1.htm)
- [Image restoration](https://en.wikipedia.org/wiki/Image_restoration)

#### Wiener Deconvolution

- [Matlab Wiener deconvolution](https://uk.mathworks.com/help/images/examples/deblurring-images-using-a-wiener-filter.html)
- [Wiener deconvolution Wikipedia](https://en.wikipedia.org/wiki/Wiener_deconvolution)
