# Using reinforcement learning to train an autonomous vehicle to follow someone

This project has for purpose to make a robot learn how to follow an object based on sensors and the detection of the person. It uses reinforcement learning with Q_learning to learn how to avoid obstacles while trying to follow a person.
This is a simulation that can be implemented on a real vehicle.


## Installing

These instructions are for a fresh Ubuntu 16.04 box. Most of the same should apply to OS X. If you have issues installing, feel free to open an issue with your error and I'll do my best to help.

### Basics

Recent Ubuntu releases come with python3 installed. I use pip3 for installing dependencies so install that with `sudo apt install python3-pip`. Install git if you don't already have it with `sudo apt install git`.

Then clone this repo with `git clone https://github.com/harvitronix/reinforcement-learning-car.git`. It has some pretty big weights files saved in past commits, so to just get the latest the fastest, do `git clone https://github.com/harvitronix/reinforcement-learning-car.git --depth 1`.

### Python dependencies

`pip3 install numpy keras h5py`

That should install a slew of other libraries you need as well.

### Install Pygame

Install Pygame's dependencies with:

`sudo apt install mercurial libfreetype6-dev libsdl-dev libsdl-image1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev libavformat-dev libsdl-mixer1.2-dev libswscale-dev libjpeg-dev`

Then install Pygame itself:

`pip3 install hg+http://bitbucket.org/pygame/pygame`

### Install Pymunk

This is the physics engine used by the simulation. It just went through a pretty significant rewrite (v5) so you need to grab the older v4 version. v4 is written for Python 2 so there are a couple extra steps.

Go back to your home or downloads and get Pymunk 4:

`wget https://github.com/viblo/pymunk/archive/pymunk-4.0.0.tar.gz`

Unpack it:

`tar zxvf pymunk-4.0.0.tar.gz`

Update from Python 2 to 3:

`cd pymunk-pymukn-4.0.0/pymunk`

`2to3 -w *.py`

Install it:

`cd ..`
`python3 setup.py install`

Now go back to where you cloned `reinforcement-learning-car` and make sure everything worked with a quick `python3 learning.py`. If you see a screen come up with a little dot flying around the screen, you're ready to go!

## Training

First, you need to train a model. This will save weights to the `saved-models` folder. *You may need to create this folder before running*. You can train the model by running:

`python3 learning.py`

It can take anywhere from an hour to 36 hours to train a model, depending on the complexity of the network and the size of your sample. However, it will spit out weights every 25,000 frames, so you can move on to the next step in much less time.

## Playing

Edit the `nn.py` file to change the path name for the model you want to load. Sorry about this, I know it should be a command line argument.

Then, watch the car drive itself around the obstacles!

`python3 playing.py`

That's all there is to it.

## Plotting

Once you have a bunch of CSV files created via the learning, you can convert those into graphs by running:

`python3 plotting.py`

This will also spit out a bunch of loss and distance averages at the different parameters.

## Credits

- great tutorials on reinforcement learning that a lot of my project is based on: http://outlace.com/Reinforcement-Learning-Part-3/
- https://medium.com/@harvitronix/using-reinforcement-learning-in-python-to-teach-a-virtual-car-to-avoid-obstacles-6e782cc7d4c6#.67rk1cfl4
