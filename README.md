<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="Inz" />

  &#xa0;
</div>

<h1 align="center">Engineering Thesis</h1>

<h4 align="center"> 
	🚧  Inz 🚀 Under construction...  🚧
</h4> 

<hr>

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#computer-usage">Usage</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/SURZEDOWSKI" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

App created for my engineering thesis, detects player's cards in FIFA23 live from webcam, or from a given image. Allows you to pull up-to-date prices and display current values of detected players.

## :sparkles: Features ##

:heavy_check_mark: Scraper pulls up-to-date prices;\
:heavy_check_mark: Search players by name;\
:heavy_check_mark: Search players detected on an image;\
:heavy_check_mark: Search players detected on a live camera feed;

## :rocket: Technologies ##

Technologies used in project:

- [Python](https://www.python.org)
- [Conda](https://www.conda.io)
- [Jupyter](https://jupyter.org)
- [yolov5](https://github.com/ultralytics/yolov5)
- [PyTorch](https://pytorch.org)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [OpenCV](https://opencv.org)
- [label-studio](https://labelstud.io)
- [beautifulsoup](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://pypi.org/project/requests/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have [Git](https://git-scm.com),  [Python](https://www.python.org) and [Conda](https://www.conda.io) installed.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone --single-branch --branch main https://github.com/SURZEDOWSKI/inz 

# Access
$ cd inz

# Create Conda env
$ conda create -n card_detection python=3.9.15

# Activate Conda env
$ conda activate card_detection

# Install requirements from pip
$ pip install -r requirements.txt

# Install pytorch and cuda from conda
$ conda install pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 cudatoolkit=11.1 -c pytorch -c conda-forge

# Run the project
$ python run.py

# GUI will open after a few seconds
```

## :computer: Usage ##

1.  Pull prices by entering number of pages you want to pull; the bigger your database is, the bigger chanse for your player to be found, but takes more time to load. You can choose to either pull players with highest overall rating or highest price first. Click "GET PRICES" and wait. (tip: most of the time it takes 12 to 14 pages to get all playes above 1k if you pull by price)
2.  You can find players by typing their name in "Find Player" box, and clicking "FIND"
3.  You can find players on image by clicking "BROWSE" and choosing a photo/screenshot of your pack/card
4.  You can find players on live webcam feed by clicking "DETECT" and pointing your webcam at pack/card. Make sure the video is of good quality and you gave the app enough time to detect all players. You can see live detections in command line window that you started the program from.

## :memo: License ##

I do not agree for anyone to use this code without my permission.


Made with :heart: by <a href="https://github.com/SURZEDOWSKI" target="_blank">Szymon</a>

&#xa0;

<a href="#top">Back to top</a>
