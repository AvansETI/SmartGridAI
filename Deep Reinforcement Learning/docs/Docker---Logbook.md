## Docker

**Why this choice**
With docker we can easily deploy containers to develop in, it'd be easy to setup our production development as well for the Jetson Nano boards we are going to use and the server as well.

**Findings - Jetson Nano**
Trying to deploy a docker image for the Jetson Nano did prove difficult, unfortunatly deploying an image on a Arm based processor (such as the Jetson Nano) is very new and hasn't been implemented into a stable version of docker yet. We found that it's only possible to build such images with the newest realeases. For the Nano's we needed a bunch of packages including but not limited to `OpenAIGym, Tensorflow, numpy` all of these also requires the target to compile the package, making for extra deployment time.

We found that there were various issues with trying to get this setup running, and building an image would take around an hour if not more, because of this and the time pressure we decided to go with a simple python script that can currently be found in the `NanoSetup` branch under the `nanoInstall` folder.

Unfortunatly we didn't add the old docker version to our current github branch, so we can't provide an example with this. It looks a lot like the current install file.

**Current implementation - Jetson Nano**
As explained before, we didn't implement docker after some research and work was done on it.

**Conclusion**
For the Jetson Nano a docker container is unfortunatly not the correct tool.

****Sources used****
[Docker.com](https://www.docker.com/resources/what-container)