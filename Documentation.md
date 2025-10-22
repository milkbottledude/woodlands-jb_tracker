![image](progress_pics/project_banner.jpg) 

Once again, feel free to skip ⏭️ to any chapters or versions that interest you 😊.

## Table of Content 📖
Chapter 1: Collecting raw data 
- 1.1: [Web Scraping](#11-web-scraping) 
- 1.2: [Automating Web Scraping with GCloud](#12-automating-web-scraping-with-gcloud) 
- 1.3: [Creating a Dockerized Container](#13-creating-a-dockerized-container) 
- 1.4: [Setting up GCloud Bucket and Scheduler](#14-setting-up-gcloud-bucket-and-scheduler)


Chapter 2: Object Detection
- 2.1: [OpenCV and YOLOv4](#21-opencv-and-yolov4)
- 2.2: [Annotating with CVAT](#22-annotating-with-cvat)
- 2.3: [YOLOv8 and pain](#23-yolov8-and-pain)

Chapter 3: Processing and Visualizing Data
- 3.1: [Data Preprocessing](#31-data-preprocessing)
- 3.2: [Exploratory Data Analysis (EDA)](#32-exploratory-data-analysis-eda)

Chapter 4: Machine Learning
- 4.1: [One-hot encoding, sin-cos encoding, and Linear Regression model](#41-one-hot-encoding-sin-cos-encoding-and-linear-regression-model)
- 4.2: [Random Forest + Decision Tree Regression](#42-random-forest-and-decision-tree-regression)
- 4.3: [Feature Engineering](#43-feature-engineering)
- 4.4: [Feature Selection Testing (in progress)](#44-feature-selection-testing-in-progress) (delete when done)
- 4.5: [Hyperparameter Tuning (tbc!)](#45-hyperparameter-tuning-tbc) (delete when done)

Chapter 5: Deploying Code to Website
- 5.1: [Making HTML & CSS for Frontend (in progress)](#51-making-html-and-css-for-frontend) (delete when done)
- 5.2: [Creating Backend with Flask, main.py, and then app.yaml](#52-creating-backend-with-flask-mainpy-and-then-appyaml)
- 5.3: [.joblib file & Project Folder structure](#53-joblib-file-and-project-folder-structure)
- 5.4: [Creating main.py v2 & app.yaml](#54-creating-mainpy-v2-and-appyaml)

Chapter 6: ResNet Neural Network for Labelling Traffic Images
- 6.1: [Prepping Input Data (in progress)](#61-prepping-input-data) (delete when done)
- 6.2: [Experimenting with Different Hyperparameters (in progress)](#62-experimenting-with-different-hyperparameters) (delete when done)
- 6.3:


[Conclusion](#conclusion)



## 📚 Documentation





## Chapter 1 - Collecting raw data


### 1.1: Web Scraping


Time to collect the most important ingredient in any data analysis or machine learning project: **Data**. Firstly, I import all the necessary libraries to use Selenium to scrape live data from a website:

>We need the **datetime** class, as it helps us to organize the data neatly by date and time. It also allows us to manage the date and time values which can be used during machine learning and graphing in Chapter 3 and 4.
```
from datetime import datetime
```
>We need the **Requests** library for interacting with websites and scraping them too.
```
import requests
```
>**Webdriver** works together with chromedriver.exe to create a 'robot' Google Chrome window, which you saw for a split second in the GIF above (Fig smth).
```
from selenium import webdriver
```
**Service** provides the path to the local chromedriver.exe file to Selenium
```
from selenium.webdriver.chrome.service import Service
```
**By** helps me to find the object I want to scrape by letting me key in attributes of the object so that Selenium knows what object i want to scrape.
```
from selenium.webdriver.common.by import By
```
**Options** allows us to modify the web scraping process. For example, we can run chrome in 'headless mode' by doing this `chrome_options.add_argument("--headless")`.

This allows us to carry out the web scraping task but without the chrome window popping up like you saw in the earlier GIF.
```
from selenium.webdriver.chrome.options import Options
```
- Now moving on to the actual code, starting with the function `getjpg(url)`, where the 'url' inside the brackets is the only argument of the function and is where we will pass the LTA website's url.

    ![Fig 1.1](progress_pics/Fig-1.1-first_part_of_getjpg_function.jpg)

    Fig 1.1: Web scraping portion of `getjpg` function

    Let's go through each line of code one by one:

    For Line 16, we are launching the Chrome window with our custom chrome options. Line 17 then gives the url for the Chrome window to go to, followed by Line 18 which waits 2 seconds for all html elements to load.

    Line 19 gets the snapshot element from the website using the attribute 'alt' which is unique to the snapshot object. Then in Line 20 we get the actual image url through the 'src' attribute, as you can see in Fig 1.2 below.

    ![Fig 1.2](progress_pics/Fig-1.2-LTA-website-inspect-ss.jpg)

    Fig 1.2: Attributes and tags of snapshot element can be seen by right clicking and pressing 'Inspect'/ 


    Line 21 captures the actual image and downloads it into the current directory, the project's repository folder.

- The second part of the function focuses on the format of the image file name after downloading it, as that will be important in the later chapters for organizing and visualising of data.

    ![Fig 1.3](progress_pics/Fig-1.3-naming_part_of_getjpg.jpg)

    Fig 1.3: Constructing image file name

    Line 22 gets the day, date and time at the moment the code is run, all in a single datetime object. Lines 23, 24 and 25 split the datetime up into its day, date and time components after it is converted to a string using strftime.

    Line 26 forms the filename by using an f-string to structure the day, date, time and jpeg file extension into a neat filename. Line 27 and 28 adds the file to my laptop, and Line 29 ends the Chrome window session.


The result is what you see in Figure V, I also wrote a print() statement which displays the name of the file saved, as you can see at the bottom of the screen where my mouse is circling. This is just to confirm the naming format is correct.

The 'yay' is a another print statement i put at the end of the web scraping `getjpeg` function so I know that the code ran smoothly. 

These print statements may not look important now, but in the next subchapter where I move this code to Google Cloud Run Functions, there will be many hiccups and errors. 

I need to know at which point did the code stop working, so its important to set up logging statements here and there, which allows us to pinpoint where the code stopped based on which statements are output.

I know this is in the README already, but I like GIFs so ill put it down here again👍.

![Fig V](progress_pics/Fig-V-selenium_screenrecord.gif)

The web scraping script works and all, but I want to be able to automate it and not have to open my laptop every hour to run the code. In the next subchapter, I prepare my code to run in a dockerized container from Google Cloud.

### 1.2: Automating Web Scraping with GCloud

---

After trying out various cloud services like PythonAnywhere and Amazon Web Services (AWS), I eventually settled on Google Cloud

One reason is because PythonAnywhere could not run Selenium chromedriver (which I only found out after paying for it 🥲). Plus I already had a Google account with billing set up prior to this project 💸, but not for Amazon. Also I don't like Jeff Bezos, but thats a story for another day.

Anyway, let's adapt this code to Google Cloud Run Functions. Google Cloud is Linux-based, so we will have to change the way the chromedriver is installed and run 🔧.

The adapted code is in [gcloudscrape.py](python_scripts/gcloudscrape.py). Very similar, but with more imported libraries and functions. Let's start with the new libraries.

```
from google.cloud import storage 
```
This library is for storing the image files to Google Storage Bucket 🪣
```
from io import StringIO
```
StringIO allows for reading of file data from a Storage Bucket without needing to download it, which requires additional code and runs the risk of having duplicate files in the Bucket afterwards 📂. 

```
import chromedriver_binary
```
As dockerized containers are Linux-based, the process of running a Chrome window using chromedriver here requires directing the chromedriver path to the directory using this method instead.

Moving on to the code:

- For the function `adddatetime(bucketname, data)`, its primary use was to write down the date and time for every web scrape session into a csv file for tracking purposes 📝. But ever since I managed to code the datetime info into the filenames, the function is not of much use anymore.

    ![Fig 1.4](progress_pics/Fig-1.4-adddatetime_function.jpg)

    Fig 1.4: `adddatetime()` function 

- The meat of the script is actually the function `scrapeaddpic()`, which not only scrapes the LTA website for the images like in Chapter 1.1, but also saves the images to the Google Storage Bucket. 

    I also added code to scrape the part of the crossing before the Singapore Woodlands Customs, as you can see in Line 53.

    ![Fig 1.5](progress_pics/Fig-1.5-scrapeaddpic_function.jpg)

    Fig 1.5: `scrapeaddpic()` function, such an eyesore...

    You can also see I've sprinkled some print statements here and there ✨ (Lines 47, 54, 57, 60, 62, 73, & 76). 
    
    I can look back at the logs after running the code and see which statements were printed and which were not, allowing me to pinpoint where the code went wrong 🎯.

    To not bore ourselves with the nitty gritty, let's skip the parts already covered in Chapter 1.1 and go through this quickly 🧐:

    Lines 61-64 obtain the Bucket which we will be storing our image files in 🪣, and Lines 71 to 76 write the files to the bucket as 'blobs', which is Google Cloud's way of handling data for standardization purposes.

That's the main python script for Google Cloud, but theres more to automating code than just the code itself. Next we will be creating the GCloud dockerized container for the code to run in 📦.

> If you have any questions just telegram me, my @ is linked at the top. Like fr i need someone to discuss my projects with 🗿.

### 1.3: Creating a Dockerized Container

---

As the web scraping code will be running from the cloud without a platform like VS Code or PyCharm to execute it, we need to create whats called a "container" for the code instead with our very own [Dockerfile](GCloud/Dockerfile).

![Fig 1.6](progress_pics/Fig-1.6-Dockerfile_screenshot_from_gcloudrun.jpg)

Fig 1.6: Dockerfile code screenshot from Cloud Run Functions

Line 8 gets the latest version of Google Chrome and Line 9 installs it 📥. Line 4 ensures that all the packages installed is the most updated version there is 🔄, while Line 5 installs all the packages are needed for chrome to run in the docker environment, but not part of google chrome and so are not installed by the code in Line 9.

Take note that due to Line 4, the container's google chrome version will always stay updated, but the chromedriver version won't. Be sure to monitor the logs of the GCloud function 👀 and update the chromedriver binary version in requirements.txt when necessary.

Lines 12 and 13 moves our python file 🚚➡️ into the /app directory in the container 📦, and makes sure that subsequent commands like COPY in Line 14 and RUN in Line 17 will execute relative to /app. 

Line 14 copies all files that are created in the Run Function, but for some reason it was not working, so i ran the command again in Line 16 for requirements.txt. Then I installed the requirements into the container in Line 17. Finally, Line 19 runs main.py ▶️, our web scraping python file.

**Quick Reflection:** The code itself is really little, but don't let that fool you. This was the hardest part of the project 💪, and it really killed me because I had never used Google Cloud to run code or used Linux before, let alone know what a dockerized container was 📦. 

I had to borrow many 'Google Cloud for beginners' books 📖 and watch numerous tutorials 👨‍💻💢, just to get the knowledge i needed to make this little shi-

It was pretty discouraging, because the more I learnt, the more I realised how much *I didn't know*. Furthermore, some of the books and tutorials were outdated and did not work like it was supposed to, which I only realized after spending weeks trying to learn it 😩. That's probably my bad though I should have picked the more recent ones from the start.

But after 2 arduous weeks, I finally managed to get a container, with chrome and chromedriver properly installed, up and running without any problems. That was a good day, felt super accomplished.

### 1.4: Setting up GCloud Bucket and Scheduler

---

First I created the bucket 🪣 in GCloud storage called 'frickubucket' (don't ask me about the name I made it at 2am on a Sunday morning 😵‍💫), then added 2 folders 📁. One for pictures of the crossover before Singapore Woodlands Checkpoint called towardsbkesnapshot/, and the other for pictures of the crossover after the SG checkpoint and leading up to the JB customs. This folder was simply called snapshots/.

![](progress_pics/Fig-1.7-buckets.jpg)

Fig 1.7: Bucket and folders in GCloud storage

Below are all the pictures that have accumulated in snapshots/ since I started the cloud scheduler in November 2024 📸.

As you can see all the filenames are formatted nicely as date_time_day.

![](progress_pics/Fig-1.8-snapshotsfiles.jpg)

Fig 1.8: jpeg files inside the snapshot/ folder

Of course, all the work prior would be useless if not for the GCloud Scheduler job running everything periodically 🔁. Here is it's configuration:

![](progress_pics/Fig-1.9-scheduler_config.jpg)

Fig 1.9: Scheduler job's configuration

At the bottom, you can see the execution target type is set to `HTTP`. This is to tell the job that our code is a webscraping code that targets `HTTP`/`HTTPS` websites 🌐 (all standard Google website links start with either one or the other).

At the top, you can see the job frequency, which controls the dates and times at which your code runs.

Scraping the LTA website at a high frequency 📶 (eg: every 2, 5 or 10 minutes) may help pinpoint times of congestion more accurately, but it will also:

 1) take up more space in the Bucket folder, and 
 2) mean that the code has to run more often in a short span of time. 

These make the process more computationally expensive and would lead to additional costs for me 💸😭. However, having too much time between web scrapes makes it hard to capture congestion trends.

Finally I settled on what I think is a balanced time interval of 1 hour between scrapes, thats why the timestamps of the images in Fig 1.7 are all an hour from each other.

This translates to a frequency configuration of `0 * * * *`, which is quite confusing if you are not familiar with the time-field formatting which GCloud Scheduler uses (like me at the start of this project).

Here is a snippet from Google's Cloud scheduler guide 📝 to help you.

![](progress_pics/Fig-1.10-Scheduler_time_format.jpg)

Fig 1.10: Cloud Scheduler time-field formatting information

In order to collect the data from the bucket, you need a python script and link your google credentials to said script. You can find mine [here](python_scripts/frombucket.py), the filename is frombucket.py. You won't find my credentials though cuz that stuff is private. If you want, you can get your own under your gmail account, its free.

That wraps up Chapter 1, let's move on to object detection in Chapter 2.


## Chapter 2 - Object Detection
### 2.1: OpenCV and YOLOv4

I found OpenCV and YOLO from a nice chap who goes by the name of [Pysource](https://www.youtube.com/@pysource-com) on YouTube, it was from his videos that I got introduced to computer vision and its many uses. 

In this particular [video](https://www.youtube.com/watch?v=O3b8lVF93jU&t=46s&ab_channel=Pysource), he shares the weights of a yoloV4 object detection model that was already pre-trained 🏋️‍♀️ on tens of thousands of cars, which saves us the hassle of manually drawing the car objects' bounding boxes ✍️ and feeding the training images to the model. 

The object detection model consists of 2 files. One is [vehicle_detector.py](python_scripts/vehicle_detector.py), which defines the object classes and retrieves the pre-trained weights ⚖️ using OpenCV.

The other is [yoloimage.py](python_scripts/yoloimage.py), where you define the image you want to carry out object detection on and feed it to the model. The results are quite accurate, as you can see in the figure below 🎯.

![](progress_pics/Fig-2.1-Pysource-video-YOLOv4.jpg)

Fig 2.1: Pysource's YOLOv4 model performance (a screenshot from his video)

However, the difference in resolution between pictures taken from afar by LTA traffic cameras (installed more than 2 decades ago) and modern webcams much closer to the highway 🛣️ (like in Fig 2.1) is large 👀. Below is a picture of the causeway after annotations by the pre-trained YOLOv4 model.

![](progress_pics/Fig-2.2-annotated_pre-trained_YOLOv4.jpg)

Fig 2.2: Pre-trained YOLOv4 model's annotations on a picture of the causeway

While some vehicles were detected 🔍, the majority of the cars were not. It also detected a bus which is not our intention.

This model may work if the camera pictures were of higher quality, but the data quality cannot be changed. Instead, we have no choice but to improve the model. Easier said than done though🥴...

### 2.2: Annotating with CVAT

---

#### How object detection works
To train an object detection model, you need to tell it what kind of object you want it to detect 🔍. This means force-feeding it pictures of said object highlighted in a bounding box, until it learns what the object 'looks like' 🚗. 

A bounding box is the box that surrounds the object in the image, you can see a couple in [Figure IV](progress_pics/Fig-IV-yolo_beachscreenshot.jpg) above in the Overview🔎. 

Each bounding box has a centre coordinate value, a width and length value, and a class value, which tells the YOLO model what object class it is (ill explain more on classes later). The centre coordinate value will come in handy later on in [Chapter 3.1](#31-data-preprocessing).

Of course, the number of pictures you need to sufficiently train a model depends on:

1) the quality and resolution of your picture 🖼️. a model can pick up patterns in the image pixels better if there are more pixels.

2) how complex your object looks. Learning the characteristics of something simple, like for eg: a sunflower 🌻, which do not vary in shape or design, is relatively simple. 

Cars on the other hand are more difficult, with varying numbers of doors, colours, designs, etc 🚗 🚙 🚕 🚓.

The model needs to generalise its object detection pattern and not overfit on irrelevant attributes unique only to certain cars.
    
This means learning general characteristics of cars, such as '4 wheels', and not fixating on things like '2 doors' or 'spherical headlights', as not all cars have those features.

Unfortunately, our data ticks neither box. The image quality isn't the worst, but having the cars so far away means that the image pixels making up the cars are fewer. It also does not help that the image quality becomes even grainier on rainy days 🌧️.

![insert rainy day pic here LINKKKKKKKKKK](GCloud/snaps_3/11-17_13-00_Sun.jpg)

Fig 2.3: Picture of the bridge on a rainy day, looks like it was taken in 12 b.c

Furthermore, the headlights of cars at night make it difficult to see the outline of the car bodies (Fig 2.4)

![insert nightime pic here OIIIIIIIIIIIII](GCloud/snaps_2/11-29_07-00_Fri.jpg)

Fig 2.4: Picture of the bridge at night, the headlights are very glaring.

With all these problems, its a 50/50 whether or not the YOLO model will ever be able to detect the cars if I annotate enough training images. However, YOLO has been able to detect objects of only about 16x16 pixels in an image. Also, to detect such small and grainy objects like in our case, we probably need around one to two thousand training images minimum.

Right now the success of the YOLO model is still uncertain 🤔, but I won't quit until I at least hit 2000 manually annotated training images. If the performance still does not improve at a satisfactory rate, then I may have to admit defeat. 

However, at that point we would have a large enough training dataset of 2000 hours of data for decent data analysis with Tensorflow or SKlearn machine learning, enough for the insights gathered to be more reliable and accurate👌.

#### CVAT

CVAT is a website that allows you to manually draw bounding boxes ☐ around objects of interest 🚘 in your training images. If you have an object that is unique or niche that nobody else has trained an object detection model for, this website can help you. 

However, if the object you are trying to detect is quite well known (eg: dogs, people, etc), you are better off looking for a pre-trained model that already had someone else do the dirty work, rather than spending time drawing bounding boxes yourself 🐶.

I annotated about 14 images worth of cars to start ✏️ and trained my first ever YOLO model with them. I set the number of epochs to 40, which is the number of times the object detection model goes over the training data, kind of like how you revise your textbooks repeatedly to better solidify the knowledge into your brain 🔄. 

However, unlike us humans, going over the training data too many times 🌀 can result in the model learning unnecessary details and characteristics, causing it to overfit to the training data, hence I set the epoch number at low 40 to test the waters.

At this time, I had just started my object detection journey after seeing people train successful models with just 50 to 100 high resolution training images, so poor me had no idea that low resolution images meant I had to annotate **a lot** more ✏️

![0](progress_pics/Fig-2.5-first_time_annotating_with_cvat.jpg)

Fig 2.5: First time using CVAT

Obviously, the model did not do well, detecting no cars whatsoever. I also received some metrics of the object detection process.

![0](progress_pics/Fig-2.6-first_attempt_axis_aligned_results.jpg)

Fig 2.6: Metrics of object detection model's first training attempt

I'm not super knowledgable on the math and nitty gritty of object detection ML/DL, but I do know that loss = errors = 👎. And as you can see at the bottom left, the validation loss is actually **increasing** as the number of epochs increases. 

By right, the more times a machine learning model goes over the training data, the more it should be refining its weights and improving its performance 🔧. So obviously, this training session was a failure.

I tried to find loopholes around the picture quality to train the YOLO model, such as detecting traffic congestion areas as a whole:

![0](progress_pics/Fig-2.7-hexagon_bounding_box.jpg)

Fig 2.7: Hexagon bounding box

However, this did not work. This is because they need the centre of the box to be clearly defined to accurately identify the centre of mass of the object and generalise characteristics, and YOLO is not able to do so for odd shapes 🛑.

YOLO breaks up the box into a grid of pixels to detect patterns and calculate loss. This process is programmed in a way that it only supports 4-sided, axis-aligned 📐 bounding boxes. I'm not educated enough on the subject to know the exact details behind the way the YOLO model is set up 📚, so I cannot explain specifics. For that I apologise.

In the end, I settled for identifying **areas** of congestion on the causeway 🛣️. It somewhat solved the low-pixel problem by making the bounding box area bigger, while at the same time still keeping the majority of the bounding box around an area of cars. It was also feasible with 4-sided-boxes aligned to the axes.

![0](progress_pics/Fig-2.8-axis_aligned_cvat.jpg)

Fig 2.8: Bounding boxes now surround areas of congestion rather than individual cars

### 2.3: YOLOv8 and pain

---

After a few weeks of monotonous manual annotating, I managed to get 184 training images. I trained the model again and kept the epoch parameter the same as before.

![0](progress_pics/Fig-2.9-results_184train.jpg)

Fig 2.9: metrics from training with 184 training images

The numbers are still far from ideal, but at least the loss is decreasing now 📉 instead of increasing with epoch number.

Afterwards, there was just a bunch more annotation ✏️. I split the total images I had at the time (about 1000) into 7 batches in the GCloud folder 📦. I hit 334 training images after annotating the 2nd batch and trained the model again:

![0](progress_pics/Fig-2.10-results_334train.jpg)

Fig 2.10: metrics from training with 334 training images

The results did show improvement 📈 in model performance, but not much. The training loss and validation loss only improved very slightly from when i trained the model with 184 images, almost half the number of images. Same for the recall and precision, only marginally better, and they were not smooth curves meaning the model is not performing very consistently. Not good news.

A few late nights later, I hit 514 images after completing the 3rd batch 📦 of image annotations:

![0](progress_pics/Fig-2.11-results_514train.jpg)

Fig 2.11: metrics from training with 514 images

Slight improvement, the metrics mAP50 and 50-95 which, to my limited understanding, basically sees if there is a certain amount of overlap between the actual bounding box and that placed by the model, have increased from when the model was trained with 334 images, from around 0.3 to 0.4. 

The mAP50-95 (basically the same thing except the amount of overlap varies) also increased ⬆️ from around 0.100 to slighly below 0.15. It also looks like validation dfl loss decreased slightly ⬇️ (rough explanation: measures loss for the corners of the bounding box placed by the model). However, it looks like the box loss gradient may be stagnating 〰️ which does not look good.

Here are the metrics of the 2 model metrics side by side so its easier to compare:

![0](progress_pics/Fig-2.12-side_by_side_334_&_514.jpg)

Fig 2.12: Fig 2.11 on the right, Fig 2.10 on the left

On a brighter note, when I used the weights of the model after this training session ⚖️ on a random image of the bridge taken at night 🌙, it managed to detect a small fraction of the congestion in the picture. 

Granted, it doesn't look very impressive, but it was my first visible progress after a long period of work and no results, so I was quite thrilled.

![0](progress_pics/Fig-2.13-first_annotation_by_model.jpg)

Fig 2.13: First annotation by model

As I annotate more images, I will continue to update you guys on the results for future models. We have about 1300 currently, and so far only about 500 have been annotated (batch 3 out of 7 📦), so I feel there is still potential for the YOLO model. Or maybe im just being delusional. Either way, I'm not stopping until I reach 2000.

Now that we have a decent amount of raw data on the causeway congestion, we can preprocess the data and use tables/graphs 📊 to contextualize it for better readability and understanding.

## Chapter 3 - Processing and Visualizing Data
### 3.1: Data Preprocessing

The source code for this subchapter can be found in [splittingroad_&_preprocessing.py](python_scripts/splittingroad_&_preprocessing.py)

#### Differentiating the roads

Its all well and good if we can identify areas of congestion on the causeway, but the causeway goes both ways 🛣️. While theres a jam on the road towards Woodlands, the road to Johor could be empty.

Us humans can tell which road goes to which country 🇸🇬/🇲🇾, but the object detection model only cares about detecting areas of congestion on both roads, not which road is congested. We need a way to tell our code which road is congested to conduct any meaningful data analysis 📊.

This problem puzzled me for quite a while and I researched some possible ways to get around this, such as incorporating image cropping into the code such that it separated the 2 lanes ✂️ into separate pictures, or using shapes to define the regions of the road. None of those really appealed to me though, and eventually I settled on using the centre coordinates 📍 of the bounding boxes to determine which lane the congestion belonged to.

First, I gathered the centre coordinates of all bounding boxes in every single image of the causeway I annotated, then I plotted them all into a graph using Matplotlib.

![0](progress_pics/Fig-3.1-distinct_coord_grps.jpg)

Fig 3.1: Plotted coordinates of all bounding box centres

Notice something? There is a clear separation ✂️ between what appears to be 2 groups of coordinates, obviously the 2 groups are the lanes of the coordinates.

The plan now is to plot a line that perfectly separated the 2 groups, so that in the future, the code knows how to differentiate coordinates and their lanes by simply looking at which side of the separating line they lie on.

At first, I tried to separate them with a normal straight line. I did some trial and error and came up with was a formula of: y = -0.94x + 1.18

![0](progress_pics/Fig-3.2-orange_line.jpg)

Fig 3.2: Straight line graph plotted together with bounding box coordinates

Its not bad, but you look carefully at the top left of the graph, there's a tiny problem. Some coordinates belonging to the top group managed to sneak below the line. Incorrect data leads to incorrect predictions and flawed data analysis, which is unacceptable.

After tinkering with Matplotlib and Desmos, the online math graphing app, for a bit, I managed to get a curve that perfectly separated the coordinates.

![0](progress_pics/Fig-3.3-sigmoid_reflected_in_y-axis.jpg)

Fig 3.3: Curved line separates all the coordinates, including the ones at the top left which the straight line could not

This curve actually originated from a sigmoid. I was looking at different types of curve lines and their formulas, and the sigmoid caught my eye. Thanks to Graphs and Transformations from JC maths, I managed to invert the sigmoid about the y-axis and adjust its y-intercept, as well as its gradient (x coefficient), finally getting the formula of the perfect line: y = 1/1+e^^4(x-0.73)

Using this formula, I coded splittingroad.py, which goes through every single bounding box's centre coordinate 📍 and subs it's x-coordinate into the formula 🧪. If the y value from the formula > the actual y-coordinate, that means the coordinate is below the line and belongs to the lane below the curve. 

I separated the coordinates into 2 different lists, then coloured the coordinates differently in Matplotlib (Fig 3.5, which is further down below).

Thats the TLDR of the first part of code in splittingroad.py, now I will explain how the whole thing works in detail part by part 🔍

```
import os
import matplotlib.pyplot as plt
import numpy as np
```
First I imported the required packages: 
- **os** for extracting and working with local files 🗂️
- **matplotlib** to plot the coordinates in a graph 📊
- **numpy** for its math functions 🔢 which we use to plot our sigmoid curve

```
1   folder_path_template = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\coords_"

2   x_coords = []
3   y_coords = []
4   for i in range(1, 4):
5        folder_path = folder_path_template + str(i)
6        for file_name in os.listdir(folder_path):
7           file_path = os.path.join(folder_path, file_name)
```
Lets start simple with Lines 2 and 3. As you can probably tell from their names, they are just lists to store the x and y coordinate values of the bounding box centres. 

In Line 1, I define 'folder_path_template'. If you look carefully at my coord files 🗂️ (which contain the bounding box details and coordinates) in the [GCloud](GCloud) folder, you will see that they have names like 'coords_1', 'coords_2', etc. But the path ends in just 'coords_', hence its called a "template".

This leads us to lines 4 and 5. Line 4 iterates through the numbers 1 to 3, and Line 5 attaches the string number to the end of the template to form the actual 'folder path'🗂️. 

I went through the trouble of making a template so that in the future, when we have many 'coord' files, we don't have to keep adding file paths, we can just edit the latter number argument in range(). 

Was pretty chuffed with myself for coming up with this 😤

Lastly, Lines 6 and 7 attach the names of the actual files 🗂️ in the coord folder ➰ to the end of the 'folder path' to form the 'file path'. Here, I utilize the 'listdir' and 'path.join' capabilities of **os**.

Moving on with the rest of the 'for' loop:
```
8          with open(file_path, 'r') as file:
9              for line in file:
10                 numbers = line.split()
11                 x_coords.append(float(numbers[1][:4]))
12                 y_coords.append(float(numbers[2][:4]))
```
After opening the file in read mode (Line 8), I iterate through each line in the file. For the next lines, its important to understand how the files' contents are formatted. 

Here is how the contents of a typical bounding box file looks like.

![0](progress_pics/Fig-3.4-typical_box_file.jpg)

Fig 3.4: contents of one of the thousand bounding box files

This particular [file](GCloud/coords_2/11-15_13-00_Fri.txt) has 4 bounding boxes, hence there are 4 lines of data.

The first value is the object class, underlined in white ⚪. As we only have 1 object class 'traffic jam', hence they are all the same number '0'.

The second value is the x-coordinate of the bounding box centre, underlined in red 🔴. The third value underlined in green is the y-coordinate 🟢, and the value underlined in yellow is the width of the bounding box 🟡. The last value, the one underlined in blue, is the height of the bounding box 🔵. 

> This strict YOLO file formatting also shows how bounding boxes not aligned to the axes or of varying number of sides will not work 🚫, as stated in Chapter 2.2.

In Line 9, I go through the lines of data one by one. In each line of data, I split the 5 numbers (Line 10), then add the 2nd number (x-coord underlined in red🔴) and 3rd number (y-coord underlined in green🟢) to the x-coord and y-coord lists respectively in Lines 11 and 12.

I converted the string values to float (using float()) for math calculations later on, and also only added the numbers up to 2dp (using string slicing - [:4]) for simplicity.

Now that we have acquired all the coordinate values neatly into x and y lists, its time to classify them into their respective roads on the causeway 🛣️, which is what the code in the 2nd part of splittingroad_&_preprocessing.py is about.

#### Segmenting the centre coordinates

```
1   x_coords_johor = []
2   y_coords_johor = []
3   x_coords_wdlands = []
4   y_coords_wdlands = []
```
We will be splitting the x and y coordinate values further, then they will be appended to their respective lists depending on which side of the causeway they are on.

```
5   for i in range(len(x_coords)):
6      x = x_coords[i]
7      actual_y = y_coords[i]
8      y = 1 / (1 + np.exp(4 * (x - 0.73)))
9      if actual_y < y:
10         x_coords_johor.append(x)
11         y_coords_johor.append(actual_y)
12     else:
13         x_coords_wdlands.append(x)
14         y_coords_wdlands.append(actual_y)
```


In line 1, I iterate through 🔁 the indexes in the 'x-coords' list, since it has the same number of values in the list 'y-coords'. Then I get the pair of centre coordinates in Lines 2 and 3.

Line 4 defines the inverted sigmoid formula we came up with earlier. The **numpy** package comes in handy here to get Euler's number, '*e*'.

The x-coordinate value is subbed into the formula, and Line 5 checks if the actual y-coordinate value is greater or smaller than the y value from the formula.

If the actual centre coordinate lies below the curve ⬇️, that means it belongs to the road going to Johor, otherwise it belongs to the road headed to Woodlands. Lines 6 to 10 append the coordinates to the correct lists mentioned above in Lines 1 to 4.

To make sure all the points were classified properly, I made a simple coloured scatterplot using Matplotlib 🔴🔵📈

```
1   plt.xlim(0, 1)
2   plt.ylim(0, 1)
3   plt.grid()
4   x = np.linspace(0, 1, 100)
5   y = 1 / (1 + np.exp(4 * (x - 0.73)))
6   plt.plot(x, y)
```
Lines 1 and 2 set the limits of the axes so neither axis has a tick of value greater than 1.

Line 3 enables gridlines ⊞ on the plot, while Lines 4 and 5 create the coordinates of the sigmoid curve, which is then plotted by the code in Line 6. 

```
7   plt.scatter(x_coords_johor, y_coords_johor, c='blue')
8   plt.scatter(x_coords_wdlands, y_coords_wdlands, c='red')
9   plt.xlabel('x value')
10  plt.ylabel('y value')
11  plt.show()
```
Line 7 plots the box coordinates 📌 that lie on the road to Johor and colours them blue 🔵, while Line 8 does the same for the road to Woodlands, except the coordinates are coloured red instead 🔴. Lines 9 and 10 label the axes, and Line 11 showcases the graph 📈

![0](progress_pics/Fig-3.5-coloured_coords_with_curve.jpg)

Fig 3.5: Plotted the sigmoid curve and coloured coordinates

If you are wondering why there seems to be even more points than in Fig VII, thats because I've annotated a few more batches since then, so theres more coordinates now.

With all the coordinates properly preprocessed and classified according to their road, we can now do some data analysis 📊

### 3.2: Exploratory Data Analysis (EDA)

The code in this chapter can all be found in [data_analysis.py](python_scripts/data_analysis.py)

First, I imported the packages I would need:

```
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```
The packages are the same as in chapter 3.1 except for pandas 🐼, as I will need the Dataframes𝄜that come with the pandas library to showcase the data in a neat table.

Then I defined a list of all the days in a week 🗓️, and a list of all the times of a day 🕒. This is needed for later when organising the congestion values in a pd dataframe according to day and time 🗃️

```
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
times = ['00-00', '01-00', '02-00', '03-00', '04-00', '05-00', '06-00', '07-00', '08-00', '09-00', '10-00', '11-00', '12-00', '13-00', '14-00', '15-00', '16-00', '17-00', '18-00', '19-00', '20-00', '21-00', '22-00', '23-00']
```

Theres probably a more automated way around doing this, but its not worth the brain power compared to just listing them out like this compared to the file paths scenario.

```
1   area_dict = {}
2   for day in days:
3       area_dict[day] = {}
4       for time in times:
5           area_dict[day][time] = [0, 0]

6   table = pd.DataFrame(columns=days, index=times)
```
I then created a dictionary (day, Line 3) within another dictionary (area_dict, Line 1) to store 2 values (Line 5): 
1) the total area of bounding boxes for each day and time 📐
2) the number of instances of that particular day and time 🔢

This is so that I can calculate the average amount of congestion that occurs at that time and day by dividing total area (1st value) by total number of instances (2nd value).

In Line 6 I create a pd Dataframe defined as 'table' to store the average congestion area values at every time and day.

This next part of the code is quite complicated, so ill break it up into smaller chunks 😉

```
1   for num in range(1, 4):
2       path = coords_path_template + str(num)
3       for file_name in os.listdir(path):
4           parts = file_name.split('_')
5           date = parts[0]
6           time = parts[1]
7           day = parts[2][:3]
8           area_dict[day][time][1] += 1
9           file_path = os.path.join(path, file_name)
```
First I iterate over the numbers 1 to 3 🔄 (last number, 4, is not inclusive when using range()) to go over all coords folders 🗂️. I then extract each file from each folder (Line 3) and split their filenames into parts (Line 4-7).

This is the reason why I named the jpeg files like so in my GCloud web scraping code. Since the bounding box files returned by CVAT will also be of the same name as the jpeg files 📂, I could simply sort the files into dictionaries by using parts of the filename as dictionary keys 🔑(Line 8). I then construct the file path in Line 9.


```
1        with open(file_path, 'r') as file:
2            total_box_area = 0
3            for line in file:
4                numbers = line.split()
5                x = float(numbers[1])
6                actual_y = float(numbers[2])
7                y = 1 / (1 + np.exp(4 * (x - 0.73)))
8                if actual_y < y:
9                    box_area = float(numbers[3]) * float(numbers[4])
10                   total_box_area += box_area
```

I do the same thing as in Chapter 3.1, checking whether the centre coordinates lie below ⬇️ or above ⬆ the curve (Lines 1-7). However, unlike in [splittingroad_&_preprocessing.py](python_scripts/splittingroad_&_preprocessing.py), I don't classify the coordinates on the road to Woodlands. 

Thats because I'm only analysing data of congestion going into Johor as of now. So in this case, if the coordinate lies above the curve, I ignore it 🙈. You can see this in Line 8, where I only process the data if actual_y < y.

In Line 9, I calculate the area of the bounding box by multiplying the width ↔️ of the box(numbers[3]) by its height ↕️ (numbers[4]). Then I add the area to the total_box_area variable. This will represent how much congestion is present in that image. Greater area = Greater congestion.

```
11           area_dict[day][time][0] += total_box_area
12           total_area = area_dict[day][time][0]
13           instance_no = area_dict[day][time][1]
14           table.loc[time, day] = total_area/instance_no
```
With the file still open and in 'read' mode, I add the total_box_area to the 1st value of the list in the nested dictionary (Line 11). 

Then I define the sum of areas and sum of instances, before calculating the average congestion area and adding it to the table 📝(Line 14). Here is how the table looks.

![0](progress_pics/Fig-3.6-first_look_at_table.jpg)

Fig 3.6: First look at table of congestion values

Not pretty. The values are oddly scaled, nobody would really understand what they mean, and they have more decimal places than I care to count 😵‍💫

Let's try to fix this, can't have my dataframe looking like ASCII art of a fish or something ( ◡̀_◡́)ᕤ

```
1   max_value = table.max().max()
2   table = table.astype(float)
3   table = table/max_value * 5
5   table = table.apply(lambda x: x.round(2))
6   print(table)
7   table.to_csv('sorted_data.csv', index=False)
```

My plan is to make the congestion area values scale from 1 to 5, with 1 being no/little congestion 😌, and 5 being very congested 😖. But before that I min-max scaled the values by getting the max value (Line 1) and multiplying all the values in the table by 5/max_value (Line 3). 

Line 2 is just to ensure all the values are floats so that we can round them off to 2dp (Line 5). Line 7 saves the table as a csv file, which you can see [here](python_scripts/sorted_data.csv), and Line 6 prints out the table.

![0](progress_pics/Fig-3.7-scaled_&_2dp.jpg)

Fig 3.7: Same table, now scaled and rounded to 2dp

An improvement for sure, but still not much insight can be gained from a glance (👁ˋ _ ˊ 👁). Also its a bit too bland for my liking. But not to worry, we will be exploring other ways of data visualization in this chapter, starting off with a simple line graph 📈

```
1   d = 0
2   color = ['red', 'blue', 'green', 'yellow', 'black', 'purple', 'pink']
3   for col in table.columns:
4       y = list(table[col])
5       plt.plot(times, y, label=days[d], color=color[d])
6       d += 1
7   plt.legend()
8   plt.show()
```
First I created a list of 7 colors (Line 2), one for each day of the week 🗓️. The columns in the table are the days of the week, so I iterate over them using a 'for' loop 🔁 (Line 3).

Line 1 and 6 work together to select a different line colour for different days, with Line 6 increasing 'd' by 1 after every column value (day) is iterated over.

In Line 5, the average congestion area (y axis) is plotted against the 24 hour times of a day (x-axis). The label and line color is changed accordingly with days[d] and color[d] as 'd' increments. 

Finally, Line 7 adds a legend to tell the line graphs apart 📈📉 as you can see in the top right of the figure above, and Line 8 outputs the final product.

![0](progress_pics/Fig-3.8-colorful_line_graph.jpg)

Fig 3.8: Coloured line graphs of congestion area against time of day

Pretty messy, but it gives a general idea of how congestion varies against time 🕒 for the different days.

The graph aligns with some common knowledge of the causeway, such as:

- presence of jam from 1900 to 2300 for only Fridays, as that is the period after work when people want to spend the weekend in Johor 🥳
- large spike in jam 📈 on Saturday mornings for people that are not willing to go to Johor immediately after work on Friday, but still want to spend some weekend time in Johor
  (Update: Afterwards, I found out that some muslims practice a Fri-Sat weekend instead of the traditional Sat-Sun, which could also explain the large influx of people going into Johor on Sat - probably Malaysian citizens who spent their weekend in SG returning home)

However, its interesting to note that there is not much jam on Sundays. My assumption was that both days of the week would have the roads to Johor jammed up, but I guess people aren't as willing to go to Johor on Sunday compared to Saturday. 

On the contrary, the road to Woodlands may be congested due to people coming back to SG after going to Johor on Saturday/Friday 🚗💨

Let's try bar graphs next. The plot containing line graphs for every day of the week is a little too cramped for my liking, so for the bar graphs I'll be plotting on separate axes.



```
1   fig, axes = plt.subplots(2, 4)
2   axesrows = [0, 0, 0, 0, 1, 1, 1]
3   axescols = [0, 1, 2, 3, 0, 1, 2]
4   for col in table.columns:
5       y = list(table[col])
6       axes[axesrows[d], axescols[d]].bar(range(24), y)
7       axes[axesrows[d], axescols[d]].set_xticks(range(24))
8       axes[axesrows[d], axescols[d]].set_xticklabels(times, rotation=66, fontsize=7)
9       axes[axesrows[d], axescols[d]].set_title(days[d])
10      axes[axesrows[d], axescols[d]].set_ylim(0, 5)
11      d += 1
12  axes[1, 3].axis('off')
13  plt.show()
```
Line 1 plots 8 subplots (2 rows by 4 columns), and Lines 2 and 3 represent the subplot coordinates. For example, [0, 1] is the 1st row 2nd col subplot, which represents Tuesday in Fig 3.10 below. 

Line 6 and 7 sets 24 bars 📊 across the x-axis in each subplot, with 'y' being the value for the bar height. Line 8 rotates the x-axis time labels 🔄 and sets the fontsize to a smaller 7 to prevent them from overlapping 🙂⃤

Line 9 sets the title according to days[d] which gives the correct day 📆 as 'd' increases (Line 11), and Line 10 sets the max bar height at 5 units. Line 12 removes the bottom right subplot, since theres space for 8 subplots but we only need 7, and finally Line 13 outputs all bar graphs.

> Or are they histograms? Cuz even though they aren't connected, they represent continuous values over time, not categorical... I don't know man I'm rambling >ᴗ<

Hope you haven't fallen asleep while reading. I've done that a couple times already while writing this 💤

![](progress_pics/Fig-3.9-to_jb_separate_histos.jpg)

Fig 3.9: Separate bar graphs of congestion against time of day, 1 for each day of the week

This is slightly easier to understand than Fig 3.9, which may have been too colorful and messy 🌈𖡎. We can see that the day with the lowest congestion levels overall is actually Tuesday, followed by Monday.

If you could not already tell from the line graph, the subplot bar graphs make it very clear that if you go to Johor on Friday or Saturday, you would most likely be met with an unpleasant jam 🚗🚙😫🚌

Let's do this for the congestion values going into Woodlands as well. Not much change in code needed, just gotta swap the '<' in `if actual_y < y:` to '>'.

![](progress_pics/Fig-3.10-to_wdlnads_separate_histos.jpg)

Fig 3.10: Separate bar graphs (or histograms?🤔) for congestion coming into Woodlands

As expected, there's a large influx of fellas coming into Singapore on Monday mornings from 00-00 to 01-00 for work etc 💼💻, and some from 06-00 to 09-00 for what I assume is school 📚🎒. There is also plenty of congestion on Fridays for most of the day, from people who want to spend their weekend in Singapore perhaps?

One strange thing I noticed was the unusually high congestion rate on Thurday afternoons 🚙🚗💨, not sure why there so many people coming in on a workday in the middle of the week. 

Edit: Afterwards I found out that some states of Malaysia starts their weekends on Fridays, so our 'Thursday' is like their 'Friday'. 

> This means their 2 day weekend consists of Friday and Saturday. Apparently it is a common practice for some muslim-predominant states such as Afghanistan 🇦🇫, Saudi Arabia 🇸🇦, and Dubai 🇦🇪, although Dubai phased out this practice in 2022. That's cool, I learnt something new today. 

As for other days such as Tuesday and Wednesday occasionally having periods of high congestion coming into SG, I'm not quite sure what is the reasoning behind it. My best guess is transport of company and business goods, but I could be wrong 🚚🚛📦.

These graphs may not present ground-breaking discoveries, but they do show some trends and patterns that we did not know before, and they definitely gave us some food for thought going into the next Chapter of the project: Machine Learning

🥗🍗😋🍽️ --> 🧠 ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧

## Chapter 4: Machine Learning
### 4.1: One-hot encoding, sin-cos encoding, and Linear Regression model

The code in this chapter can all be found in [Predicting_with_LinReg.py](python_scripts/Predicting_with_LinReg.py)

We don't have many variables at the moment, just day and time, but its enough for a neural network model to work with after one-hot encoding all the values. 

One-hot encoding is basically splitting up a categorical column like 'day' into other columns 📆, each column representing a particular value of 'day'. Since there are 7 days, there would be 7 'day' columns (Mon, Tues, etc).

However, I will be getting rid of 1 column to make it 6 'day' columns. This is to prevent multicollinearity, something we want to steer clear of in ML 🙅‍♂️.

I'm not an expert, but I'll try my best to explain it in simple terms. If you do want an expert's article on it, you can go [here](https://www.analyticsvidhya.com/blog/2020/03/what-is-multicollinearity/), it explains it pretty well ✍️.

Taking the 'day' variable as an example. If a particular row's day was Tuesday, the 'Tues' column would be 'True' while the rest would be 
'False'.

However, what if I told you that for another row, the binary value for the columns 'Mon, Tues, Thurs, Fri, Sat, Sun' were False ❌. By elimination, you would know that the value for 'Wed', the only column not mentioned, was 'True' ✅ without me telling you. This essentially means you can predict the state/value of an independent variable (x value in a 'y against many x' relationship) through other independent variables.

This is bad for machine learning models including NN's because, in simple terms, it makes it more difficult to detect the relationships between each individual independent variable (x) and the dependent variable (y).

Another example which I learned from a book on Linear Regression models uses a regular corporate job as an analogy. A hardworking person 👨‍💻 is likely to work longer hours than average ⏳, and hardworking people also tend to produce higher quality work 🌟. In the end, the hardworking person would probably get a pay raise 💰💰. But is the pay raise a result of A) working longer hours? or B) higher quality work? 

As for the time values, I don't have to one-hot encode them since they are numerical. However, they are **cyclical** in nature 🔄. For instance, 11pm is closer to 1am than 5am, even though 5 as a number is closer to 1 than 11. Basically the values loop around. There is a way to manage cyclical values, by using cos and sin on the values to preserve their cyclic nature, but it did not go well the last time I used it.

I tried this method of encoding in my previous Machine Learning project, a Kaggle competition, where I was trying to predict Insurance Premiums. One of the variables was 'Policy Start Date', the date the insurance was bought 🗓️. I applied sin-cos encoding on the month values (since December loops back to January), but the model accuracy decreased for some reason when tested against the test data, I'm not sure why. 

So to start, I'll train the model with no encoding for the time variable, then afterwards I'll encode it and see how it performs.

First I had to create a pd dataframe, such that each row represented an instance, so slightly different than the previous dfs we made.

```
import os
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
```
I'm sure by now you are already familiar with the first 3 packages. The 4th and last library, sklearn, has different subpackages 📦 such as 'tree' and 'ensemble', which provide us with different machine learning models to try out and test against each other 🤖.

```
1   column_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Time of Day', 'congestion_area']

2   coords_path_template = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\coords_"

3   df = pd.DataFrame(columns=column_names)

4   for num in range(1, 4):
5       path = coords_path_template + str(num)
6       for file_name in os.listdir(path):
7           parts = file_name.split('_')
8           date = parts[0]
9           time = parts[1]
10          day = parts[2][:3]
11          index = None
12          for i in range(len(column_names)):
13              if day == column_names[i]:
14                    index = i
15                    break
```
In Line 1 I define a list of column names, omitting one of the seven days ('Sun') to prevent multicollinearity. Also included in the list are 'time of day' 🕒, another independent variable, and lastly the dependent variable 'congestion_area'.

You have already seen Line 2 and Line 4-10, where I extract the bounding box text files 📄 and split the file names into parts.

Before that, I make a DataFrame using the list of columns (Line 3). After extracting the information from the file name, I check what is the index 🔢 of the day in the 'column_names' list (Line 12-13). I then assign the value to 'index' (Line 14) and 'break' to save time. If the day from the file name is 'Sun' and is not present in column_names, 'index' will remain as 'None'.

```
16          total_box_area = 0
17          file_path = os.path.join(path, file_name)
18          with open(file_path, 'r') as file:
19              for line in file:
20                  numbers = line.split()
21                  x = float(numbers[1])
22                  actual_y = float(numbers[2])
23                  y = 1 / (1 + np.exp(4 * (x - 0.73)))
24                  if actual_y < y:
25                        box_area = float(numbers[3]) * float(numbers[4])
26                        total_box_area += box_area
27          new_row = [0, 0, 0, 0, 0, 0, int(time[:2]), total_box_area]
28            if index:
29                new_row[index] = 1
30          df.loc[len(df)] = new_row

31  max_value = df['congestion_area'].max().max()
32  df['congestion_area'] = df['congestion_area']/max_value * 5 # scaled values range from 0 to 5; 0 = no jam, 5 = very congested, then rounding to 2dp for readability
33  df['congestion_area'] = df['congestion_area'].apply(lambda value: round(value, 2))
34  print(df)
35  df.to_csv('df', index=False)
```

The code from Line 16-26 is the same as in [data_analysis.py](python_scripts/data_analysis.py), determining which side of the causeway the bounding box is on, then calculating the box area sum for that image and defining it as total_box_area.

Line 27 creates the new row of data to be added to the df. Lines 28 and 29 check if 'index' has a valid number 🔢 then replaces the correct day column value with '1' to indicate 'True' ✅, otherwise leaving everything as '0' ❌ if the day was 'Sun'. Line 30 adds the new row to the last index of the df to finish.

Line 31-33 applies min-max scaling to the congestion_area column's values. The code is basically copied from data_analysis.py, where I also applied min-max scaling except to an entire Dataframe not just a single column. Lastly, Line 35 converts the Dataframe into a csv file 📜, so I don't have to keep making the table again and again.

Here are the first 4 rows of the dataframe.
```
     Mon  Tue  Wed  Thu  Fri  Sat  Time of Day  congestion_area
0    0.0  0.0  0.0  0.0  0.0  1.0          0.0             0.00
1    0.0  0.0  0.0  0.0  0.0  1.0         18.0             2.22
2    0.0  0.0  0.0  0.0  0.0  1.0         23.0             0.00
3    0.0  0.0  0.0  0.0  0.0  0.0          0.0             0.00
4    0.0  0.0  0.0  0.0  0.0  0.0          6.0             0.00
```
The '1's under the 'Sat' column indicate that the first 3 days are Saturdays, while the absence of '1' in any of the day columns indicate that the last 2 rows are Sundays. The hour of the day can be found in the 'Time of day' column 🕒, and the relative congestion value (scaled from 1 to 5), can be found under the last column 🚙🚗💨

One thing I'm uncomfortable with though, is the lack of rows with congestion_area values > 0. After printing `len(df)` and `len(df[df['congestion_area'] > 0]), which output the total number of rows and the number of rows with a congestion value thats not '0', I got 143 and 517 respectively. The days with congestion are severly underrepresented, with the distribution of y values are imbalanced and skewed towards 0.

This can lead to the ML model leaning towards the skew as congestion values of '0' are much more frequent in the training data. To get around this, I'll be removing some of the rows with congestion value '0' 🗑️ at random so that the rows with congestion_area > 0 are not so outnumbered. We all know getting rid of data is a waste, especially when we have so little of it here, but in this case I feel its gotta be done 😕.

```
31  df.sort_values(by='congestion_area', ascending=False, inplace=True)
32  df = df.iloc[:293]
```
First I sort the rows by the 'congestion_area' column in ascending order, so all the rows with congestion values > 0 gather at the top of the df (Line 31).
Since there are only 143 rows with a positive congestion value, I want the number of rows of 0 to be about the same, so I decided to keep 150 '0' rows. So total number of rows is now reduced ⬇️ from 517 rows to (143+150) = 293 rows.

Now we can train our first machine learning model, starting off small with a simple linear regression model 📈
 ```
33  y_column = df.pop('congestion_area')
34  model = LinearRegression()
35  model.fit(df, y_column)
```
In Line 33, I removed the y_variable column from the df and defined it as y_column. Next I defined the machine learning model we would be using (Line 34), then trained the model with the x and y variables 🏋 by calling model.fit() (Line 35).

Making a default linear regression model is actually super simple, its the tuning of hyperparameters that requires expertise 🔧. For now I'll leave the hyperparameters as default.

Since I don't have enough training data to further split it into train and test data, I'll be using a mix of pictures 🖼️ (21 images) I scrounged from the other unannotated snaps folders to form the [test_snaps](GCloud/test_snaps) folder. I hand picked the photos to ensure we had a good variety of pictures with varying degrees of congestion, now we gotta convert them into a test dataframe.

```
36  test_df = pd.DataFrame(columns=column_names[:-1])
37  test_snaps_path = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\test_snaps"
38  for file_name in os.listdir(test_snaps_path):
39        parts = file_name.split('_')
40        date = parts[0]
41        time = parts[1]
42        day = parts[2][:3]
43        index = None
44        for i in range(len(column_names)):
45            if day == column_names[i]:
46                index = i
47                break
48        new_test_row = [0, 0, 0, 0, 0, 0, int(time[:2])]
49        if index:
50            new_test_row[index] = 1
51        test_df.loc[len(test_df)] = new_test_row
52  test_df.to_csv('test_df', index=False)

53  predictions = model.predict(test_df)
54  test_df['congestion_prediction'] = pd.Series(predictions)
55  print(test_df)
```

In Line 36, I created the test Dataframe, which is similar to the train data except I don't add the 'congestion_area' column, which is what the model will be predicting for us 😎

Line 37-47 were copied from the above code (getting pics from the coords folders), except this time the folder path (Line 37) is different. I define the row to add to the df 📝 in Line 48, with only 7 values instead of 8 in the training df. Line 49-51 is the same as above, except I add the row to the test_df, not df. 

Finally, we generate the predictions on the test data (Line 52) and append it to the end of test Dataframe as the final column (Line 53). Let's print out the results 📋 (Line 54) and compare them with the images 🔎🖼️

Here are the first 5 rows of test_df:

```
    Mon  Tue  Wed  Thu  Fri  Sat  Time of Day  congestion_prediction
0     0    0    1    0    0    0            6               0.768147
1     0    0    1    0    0    0            7               0.836279
2     0    0    1    0    0    0            8               0.904411
3     0    0    1    0    0    0            9               0.972543
4     0    0    1    0    0    0           10               1.040674
```

If you look at the first 5 pictures in [test_snaps](GCloud/test_snaps), you will see they all have very little 🤏 or no jam at all on the road to Johor. The linear regression model somewhat predicts this with congestion values ranging between 0 to 1, albeit a bit higher than I'd like since the correct value is 0.

Now lets take a look at some other rows with different days and times.

```
    Mon  Tue  Wed  Thu  Fri  Sat  Time of Day  congestion_prediction 
7     0    0    0    1    0    0            8               0.327395
8     0    0    0    1    0    0            9               0.395527
9     0    0    0    1    0    0           10               0.463658
10    0    0    0    1    0    0           11               0.531790
16    0    0    0    0    0    1            6               2.113028
17    0    0    0    0    0    1            7               2.181160
18    0    0    0    0    0    1            8               2.249292
```
For rows 7 and 8, you can see low congestion prediction 🔻, which is correct. Their corresponding [picture files](GCloud/test_snaps/11-21_08-00_Thu.jpg) do not show any jam to Johor. However, rows 9 and 10, which the LinReg model also thinks has low congestion, are wrongly predicted. 

If you refer to their [picture files](GCloud/test_snaps/11-21_10-00_Thu.jpg), you will see that the road to Johor is actually as congested as it can be, so the congestion_prediction value should actually be somewhere between 4 and 5.

Furthermore, although rows 16-18 do indicate moderate congestion with values between 2 and 3, only row 17 is somewhat correct. That's because if you refer to their corresponding files, the [image for row 16](GCloud/test_snaps/11-23_06-00_Sat.jpg) has no sign of congestion, while [row 17's image](GCloud/test_snaps/11-23_07-00_Sat.jpg) has a little jam brewing up near the Johor customs at the top right. As for [row 18's image file](GCloud/test_snaps/11-23_08-00_Sat.jpg), there's already a full blown traffic jam that spans along the entire road.

Let's try again but this time we apply sin-cos encoding to the time variable.

```
df['hour_sin'] = np.sin(2 * np.pi * df['Time of Day'] / 24)
df['hour_cos'] = np.cos(2 * np.pi * df['Time of Day'] / 24)
df.drop('Time of Day')
```

From what I learnt about sin-cos encoding (I like to call it cyclic encoding, it sounds cooler but no one calls it that) is to think of it like a circle on x and y axes ⭕, so the end of the line (12am) joins up with the start (1am).

The hour_sin column gives the vertical position (y-axis value), and the hour_cos column gives the horizontal position (x-axis value). At the end I get rid of the original 'Time of day' column, so we can have a fair test to see if encoding really helps the LinReg model perform better.

Let's compare the congestion predictions for rows 7 to 18 now that we have encoded the time values. I'll also add the time of day and previous predictions as additional columns so we can better compare the results.

```
    Mon  Tue  Wed  Thu  Fri  Sat  hour_sin      hour_cos      congestion_prediction     Time of Day     previous_congestion_prediction 
7     0    0    0    1    0    0  8.660254e-01 -5.000000e-01               0.581194     8               0.327395     
8     0    0    0    1    0    0  7.071068e-01 -7.071068e-01               0.838372     9               0.395527
9     0    0    0    1    0    0  5.000000e-01 -8.660254e-01               1.064359     10              0.463658
10    0    0    0    1    0    0  2.588190e-01 -9.659258e-01               1.243755     11              0.531790
16    0    0    0    0    0    1  1.000000e+00  6.123234e-17               1.711023     6               2.113028
17    0    0    0    0    0    1  9.659258e-01 -2.588190e-01               1.977073     7               2.181160
18    0    0    0    0    0    1  8.660254e-01 -5.000000e-01               2.247915     8               2.249292
```
Don't be put off by the weird values in the sin and cos columns, thats just what happens when you run a number through the sin() or cos() function.

For rows 7-8, it predicted a slightly greater level of congestion, which is not a major issue, but it is still wrong since there were no jams in the photos for [row 7](GCloud/test_snaps/11-21_08-00_Thu.jpg) and [8](GCloud/test_snaps/11-21_09-00_Thu.jpg). The performance for row 18 is about the same, with both past and present predictions hovering around 2.2 when really the predicted value should be between 4 and 5.

However, the new prediction for rows 9 and 10 more than doubled its previous one 📈. Although the congestion level in the images corresponding to rows [9](GCloud/test_snaps/11-21_10-00_Thu.jpg) and [10 LINKKK](GCloud/test_snaps/11-21_11-00_Thu.jpg) should be closer to 4 or 5, its still a big improvement. It's a step in the right direction, which I'm very happy to see, so I'll use the encoded version of the time data for the rest of this project.

Additionally, for rows [16](GCloud/test_snaps/11-23_06-00_Sat.jpg) and [17](GCloud/test_snaps/11-23_07-00_Sat.jpg), which by right should have a congestion prediction closer to 0 and 1 respectively, also has some small improvements. The new congestion predictions are lower than before, especially row 16. 

Although the predictions are not spot on 🎯, it is good to note that we are using one of the simpler machine learning models, Linear Regression. With no tuned hyperparameters, its unlikely that it would predict perfectly. 

In fact I expected less, but it was able to predict about half of the test data correctly, for the most part anyway ✅. One big flaw of using this model in our case is that Linear Regression assumes a linear relationship between the independent and dependent variable, in our case being the congestion value and time/day of the week.

That is obviously not the case, as heavy congestion can happen early in the morning ☀️ as well as late at night 🌙. My assumption is that the model overfitted to the 'time' variable and was slightly biased towards the thinking that higher 'hour_sin/hour_cos' value 🔺 --> greater congestion 📈, or something along those lines.

This should be a starter model, where we are just dipping our toes into ML. Next lets try a Random Forest Regressor model 🌲, which does not assume a linear relationship and should handle non-linear patterns better than our LinReg model.

### 4.2: Random Forest (and Decision Tree) Regression

The code in this chapter can be found in [Predicting_with_RFR.py](python_scripts/Predicting_with_RFR.py).

#### Random Forest Regression
There are 2 types of random forest models as far as I know, Random Forest **Classifier** and Random Forest **Regressor**. Since we are predicting continuous values and not classes/categories, we will be using the latter.

The thing I like about random forest models 🌲 is that they consist of multiple decision trees, and their individual decision tree models only use a fraction of the total variables each. This means that for example, a tree would get the columns 'Mon, Wed, Sat', while another might get the columns 'Mon, Thur, hour_sin'. This allows the first model to find meaningful relationships between the 'day' variables and congestion instead of overfitting to the 'time' variables. 

Meanwhile, the latter model is still finding patterns between hour_sin and congestion, not just completely ignoring the column and letting its information go to waste 💩

Random forest models also have other unique features specifically to prevent overfitting and find relationships between every feature and the output. This [article](https://www.geeksforgeeks.org/random-forest-algorithm-in-machine-learning/) gives a simple introduction to random forest models, should you be unfamiliar with them. Its super easy to understand, and its the same website I learnt about and took notes on random forest models when I first started on machine learning 📚

Since we converted the training and test data into csv files earlier in Chapter 4.1, we don't need the code for constructing the Dataframes, we can just pull the df from the csv files 📄. Hence, our python script for this chapter [predicting_with_RFR.py](python_scripts/Predicting_with_RFR.py) has much less code and is simpler to navigate.

```
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
```
Starting off with the libraries imported, we need 🐼 pandas 🐼 for storing the data we will be pulling from the csv files 📝. Scikit-learn (sklearn for short) is a machine learning library with numerous machine learning models 🤖  as well as tools for prepping your data and evaluating outputs. However, in this chapter we will just be using the Decision Tree Regressor model and its big brother, the Random Forest Regressor model, starting off with the latter.

```
1   train_df = pd.read_csv('train_df.csv')
2   test_df = pd.read_csv('test_df.csv')

3   y_column = train_df.pop('congestion_area')
4   rfr_model = RandomForestRegressor()
5   rfr_model.fit(train_df, y_column)

6   rfr_predictions = rfr_model.predict(test_df)
7   test_df['congestion_prediction'] = pd.Series(rfr_predictions)
8   print(test_df.head(20))
```

First off, we need to get the data. Lines 1 and 2 read the csv files with the data 🗂️ and convert them into training and testing pandas dfs. Line 3 separates the congestion area column ✂️ from the original df, Line 4 defines the ML model being used, and Line 5 trains the model by calling the 'fit' method 🏋️‍♂️

Line 6 feeds the test data to the trained RFR model for it to begin its predictions, while Line 7 attaches the predictions column to the end of test_df. Lastly, Line 8 prints the first 20 rows of test_df, although I'll only show the relevant rows here. I'll also manually add the 'Time of day' and LinReg model results as the last 2 columns 📝

```
    Mon  Tue  Wed  Thu  Fri  Sat      hour_sin      hour_cos  congestion_prediction     LinReg_results (with sin-cos encoding)  Time of Day
7     0    0    0    1  0    0    8.660254e-01 -5.000000e-01               0.090114     0.581194                                    8
8     0    0    0    1  0    0    7.071068e-01 -7.071068e-01               0.802815     0.838372                                    9
9     0    0    0    1  0    0    5.000000e-01 -8.660254e-01               2.897047     1.064359                                    10 
10    0    0    0    1  0    0    2.588190e-01 -9.659258e-01               1.945836     1.243755                                    11
16    0    0    0    0  0    1    1.000000e+00  6.123234e-17               0.631085     1.711023                                    6
17    0    0    0    0  0    1    9.659258e-01 -2.588190e-01               1.477880     1.977073                                    7
18    0    0    0    0  0    1    8.660254e-01 -5.000000e-01               3.377438     2.247915                                    8
```
Immediately we can see some improvements. If you remember, the images for rows [7](GCloud/test_snaps/11-21_08-00_Thu.jpg) and [8](GCloud/test_snaps/11-21_09-00_Thu.jpg) are devoid of cars on the road to Johor, so the congestion value should be closer to 0. We can see that the RFR model has predicted a smaller value for both rows 📉, especially row 7 with only 0.09 👍

Furthermore, take a look at rows 9 and 10. They both have increased 🔺, but row 9 has a congestion value of 2.89, really high! And true enough, the image for [row 9](GCloud/test_snaps/11-21_10-00_Thu.jpg) has a traffic jam spanning along the entire length of road, same for [row 10](GCloud/test_snaps/11-21_11-00_Thu.jpg).

But heres where it gets **really** good. Line 16 shows a prediction value of 0.6, which is true if you look at the corresponding [image](GCloud/test_snaps/11-23_06-00_Sat.jpg), no jam. Look at Line 17, which indicates the startings of a traffic jam with a not too high but not too low congestion value of 1.47. What do you see in the [image](GCloud/test_snaps/11-23_07-00_Sat.jpg)? At the top right, you can see some cars starting to pile up and form a small jam 🚗🚙, near the entrance to the Johor customs!

Now for the grand finale, Line 18, coming in with the highest value we have seen yet at 3.37 arbitrary units 📈. A near perfect prediction, as the jam in the corresponding [image](GCloud/test_snaps/11-23_08-00_Sat.jpg) has fully taken form and now snakes the entire stretch of road between the customs of the two countries.

I would have liked for some of the rows congestion values, especially row 10's, to be higher 🔺, since the magnitude of the jams in their corresponding images look like 4s or 5s. However, thats my fault for drawing the bounding boxes of varying sizes, causing their areas to defer greatly. I should have known that bounding boxes are for identifying objects and not meant to be used in the way I am using them now.

I think from now on, I will just rate the congestion situation on a scale from 1 to 5 without drawing bounding boxes, based on how many fifths of the causeway the cars take up. It won't be as cool as using CVAT bounding boxes and the object detection model YOLO 🤖, but I think this is the right choice. It will lead to more consistent congestion values and take up less time ⏳. Sometimes the simplest option is best.

#### Decision Tree Regression
Unless I was trying to create a model that I could easily understand its regression process, or save a miniscule amount of computational space 💻, I probably would not pick a decision tree regressor model 🌲 over a random forest regressor model 🌲🌲🌲. However, I do want to see how the Decision Tree Regressor model fares against its more robust counterpart, the Random Forest Regressor model, and see how large the difference in predictions are, if any.

```
19  test_df = pd.read_csv('test_df.csv')
20  dtr_model = DecisionTreeRegressor()
21  dtr_model.fit(train_df, y_column)
22  dtr_predictions = dtr_model.predict(test_df)
23  test_df['congestion_prediction'] = pd.Series(dtr_predictions)
24  print(test_df.head(20))
```
In Line 19 we re-define a new test_df since the previous test_df already has the prediction column appended to it. Line 20-24 are the same as Line 4-8 above, except with a DTR model 🌲 this time. The code in this chapter is very similar to that in Chapter 4.1, its just much simpler to understand now that we don't need to code the data preparation 📝. Same as before, I'll add the RFR's results column and 'Time of Day' column to the new test_df.

```
    Mon  Tue  Wed  Thu  Fri  Sat      hour_sin      hour_cos  congestion_prediction     RFR_prediction      Time of Day
7     0    0    0    1    0    0  8.660254e-01 -5.000000e-01               0.000000           0.090114          8
8     0    0    0    1    0    0  7.071068e-01 -7.071068e-01               0.595000           0.802815          9
9     0    0    0    1    0    0  5.000000e-01 -8.660254e-01               3.165000           2.897047          10
10    0    0    0    1    0    0  2.588190e-01 -9.659258e-01               1.905000           1.945836          11  
16    0    0    0    0    0    1  1.000000e+00  6.123234e-17               0.000000           0.631085          6
17    0    0    0    0    0    1  9.659258e-01 -2.588190e-01               1.160000           1.477880          7
18    0    0    0    0    0    1  8.660254e-01 -5.000000e-01               3.675000           3.377438          8
```
Now this is interesting. The single decision tree regressor model correctly predicts that there is no jam for row 7, predicts a lower value than the RFR model for row 8 ⬇ and predicts a higher value for row 9 ⬆️, all of which are improvements 🥳. Not sure why all the models think there is a decrease in congestion at 11am, but both models predict a value around 1.9, so thats a draw between the two models.

For the Saturday rows, it again correctly predicts no jam at 6am for row 16, predicts a small build up of congestion similar to RFR model in row 17, but the DTR prediction is less which I feel is more accurate 🎯 refer to the [row 17 image](GCloud/test_snaps/11-23_07-00_Sat.jpg) and see if you agree. Lastly, it predicts a higher congestion value for row 18, which is also an improvement since the full blown congestion in [row 18's image](GCloud/test_snaps/11-23_08-00_Sat.jpg) should have a value between 4 and 5. 

That makes it 6 rows in favour of the decision tree regressor model and 1 row which ended in a draw, a clear win for the DTR model 🥇.

But why? Isn't the RFR model, which averages the output from multiple decision trees 🌳🌳🌳 generally considered 'superior' to the single DTR model, which only consists of a single 🌳 decision tree?

What I think has happened is that the DTR model has overfitted more to the data, hence the values it outputs are more 'extreme', closer to zero when there is no jam and closer to 5 when there is jam. While the DTR model performs better when trained on our tiny training dataset of 293 training rows, it might perform worse as the dataset increases into different periods of the year 🗓️ and overfitting becomes a larger problem 🚩.

We only have the data for 2 months, so overfitting to the congestion patterns in these 2 months may not pose a problem for now, on the contrary even producing more accurate results as we have just seen. But as we gather data from other months and people using the causeway start to change their behaviour, overfitting to unique details instead of generalising to the large dataset will be detrimental to the output ⚠️. 

Put it this way, right now the overfitted model will have more accurate output. But for a larger dataset, although the model that generalizes (in this case the RFR model) will not have output that perfectly matches the actual outcome, it will definitely be closer to the right answer than whatever the overfitted model outputs.

I like the way the model is performing so far. However, every good machine learning engineer knows that an ML model is only as good as the data its fed, no matter how well the model is configured and tuned ⚙️. So before we get into the nitty gritty tuning, lets work on feature engineering 🔧.

### 4.3: Feature Engineering

I'd like more variables for Machine Learning than just day 📅 and time 🕓, so in this subchapter I'll be trying to come up with more. Variables are kind of like clues for an ML model; the more you have, the more accurate the output prediction.

We could add month, but we barely have 2 months worth of processed data, so I'll hold off on that until we have data from more months. Another variable I'm considering is public holiday/presence of public holiday 🎄🧧🍊. I say presence because people tend to travel a few days before or after the actual holiday, not just on the day itself. Our processed data happens to fall on the school holiday/Christmas period 🎅🏻🎁, so lets start with this variable.

First I'll identify the school holiday periods for schools in Singapore in 2024 and 2025 📚🏫

![nonpolyhols](progress_pics/Fig-4.1-sch_hols.jpg)

Fig 4.1: School holiday periods for JCs, as well as primary and secondary schools. 2024 on the left in white, and 2025 on the right in black

Looks like aside from the end of the year, the holiday period of all 3 education institution types perfectly align, so I'll set the generic year end 'sch hols' period to follow that of junior colleges. Let's take a look at the holiday periods for the polytechnics of Singapore that overlap with the dates of our web-scraped image data.

![tpoly](progress_pics/Fig-4.2-temasek_poly_hols.jpg)

Fig 4.2: Temasek Polytechnic's holiday schedule 

![sgp](progress_pics/Fig-4.2-temasek_poly_hols.jpg)

Fig 4.3: Singapore Polytechnic's holiday schedule 

![nyp](progress_pics/Fig-4.4-nanyang_poly_hols.jpg)

Fig 4.4: Nanyang Polytechnic's holiday schedule 

![ngeeann](progress_pics/Fig-4.5-ngee_ann_hols.jpg)

Fig 4.5: Ngee Ann Polytechnic's holiday schedule 

![reppoly](progress_pics/Fig-4.6-republic_poly_hols.jpg)

Fig 4.6: Republic Polytechnic's holiday schedule

As we can see, the holiday periods of polytechnics mostly overlap between early/mid December 2024 to early Jan 2025 🗓️. For simplicity's sake, I will just make the 'sch hol period' to include polytechnics as well.

We can feed this information to our machine learning model as binary columns ✅❌, 

for example: `column name: 'within sch hols period'` , `values: True/False`

As for public holidays, the only public holidays we should be concerned with given our current data are 25th Dec 2024 🎅🏻🎄, which is Christmas on a wednesday, and 1st Jan 2025 🎇🥳, New Year's which is also on a Wednesday.

Update: As the amount of congestion data has piled up over the months 📈 and we now have a substantial amount, I'll also include other public holidays that occur in the year, not just Christmas and New Years. 

My plan is to have a 'public hols period' column, which will show whether the date of the row 📆 falls within 3 days of a public holiday 🎉. Both school holiday periods as well as public holiday periods will be represented by a single column each, you will see later on in my code.

Additionally, I'll be adding the following:

**1) full datetime value**
   
    This is to make it easier to determine whether the row's date is within the various holiday periods 📆. Datetime values are easy to work with.
     
**2) month value**

    For tracking trends of the months within the year 📈📉.
     
**3) exact date value (1st to 31st)**

    For tracking trends within the month 📈📉.

**4) day of year value (1 to 365)**

    One worry I have for the feature 'exact date value' above (3) is that the ML model may wrongly learn that rows of the same date value are very similar, when they really are not. 

    For example, the model might see a row of date March 21st in the training data, and afterwards have to predict a row of date August 21st. The 2 dates have little in common, and its unlikely they will have similar congestion patterns as well. 

    However, the model's prediction for the congestion value for August 21st may be heavily influenced by March 21st's congestion value since they have the same 'date value'.

    Hence, I have come up with this new variable, 'day of the year' value, just in case that happens, but we still want a metric that can tell the model the date of the row at a more granular level than the month value.

**5) week number**

    Again, similar to (4), another countermeasure to the potential overfitting problem stemming from (3). However, this still has the potential to make the model overfit on week number for other months, just not as likely as 'exact date value' (3).

**6) sin & cos of date value**

    Similar to the cyclical encoding of time values, this feature aims to illustrate to the ML model at what point in the month the row's date is. The start, middle, or end of the month.

**7) sin & cos of day of year value**

    Same as (6), except instead of showing what point in the month the row's date is at, this feature shows at what point the row's date is in the year.

Another idea i have for a column is 'amount of jam in the previous hour' or previous few hours (not familiar enough with this method yet, TBC). An instance is likely to have a jam if there was already a build up of cars in the previous hour/hours 🚙🚗💨. I only recently learned this, its known as 'lagging' and we can implement it using the 'shift' function from pandas. It will kinda look like this in a train.csv:

```
    ...     congestion_value     previous_hour  
0   ...     2.0                  NaN  
1   ...     5.0                  2.0  
2   ...     3.0                  5.0  
3   ...     0.0                  3.0
```

Below is an excerpt from the [csv](python_scripts/data_to_attach.csv) with all the new columns I'm planning to add.

Its a little messy and cramped, as all csv files are. I apologise for that.

```
month,exact_date_value,week_value,date_sin,date_cos,day_of_year,day_of_year_sin,day_of_year_cos,full_date_ymd,sch_hol_period,public_hol_period
11,20,3,-0.7907757369376986,-0.6121059825476627,325,0.3375228995941133,0.9413173175128472,2024-11-20,False,False
11,20,3,-0.7907757369376986,-0.6121059825476627,325,0.3375228995941133,0.9413173175128472,2024-11-20,False,False
11,20,3,-0.7907757369376986,-0.6121059825476627,325,0.3375228995941133,0.9413173175128472,2024-11-20,False,False
```

Of course, we won't be using all these features in the final ML model training for the webapp. This chapter was more of a brainstorming session 🧠 to come up with as many possibly helpful features as possible.

In the following chapter, we will be testing all these features using k-folds validation and see which actually help reduce loss 🧐, then filter the features accordingly to obtain the most optimal set of features 🎯.

So far, the independent variables we have are:
1) month (Jan, Feb, etc)
2) exact_date_value 🗓️ (eg: 21st, 8th)
3) week (1 to 4, since a month has around 4 weeks)
4) sch_hol_period 📚
5) [ublic_hol_periods (Christmas🎅🏻, New Years🥳, etc)
6) day_of_year (1-365)
7) sin and cos of exact_date_value
8) sin and cos of day_of_year
TBC) previous hour's traffic 🚙🚗💨

When fed to a machine learning model, hopefully the model can identify meaningful patterns 📈 between them and the congestion level of the target road. 

As you can see from the csv excerpt, I have already prepped the new features neatly in a df with a python file, [feature_engineered_data_prep.py](python_scripts/feature_engineered_data_prep.py). 📝

Lets take a look at the code used to prep the 8 new features into a tidy [csv](python_scripts/data_to_attach.csv). I'll break up the code into parts to make it more digestible 🧩.

(Line 1-6)

```
rating_template = r"GCloud\rating_"

1    for x in range(4, 15):
2        rating_path = rating_template + str(x) + '.txt'
3        with open(rating_path, "r") as file:
4            for line in file:
5                if len(line) < 1:
6                    break
7                else:
```

Similar to the previous data preparation, I define a naming template for the rating files, then 'for' loop through the numbers 4 to 15 to go through all the relevant rating files 🔄.

I then check whether the line has more than 1 character before continuing, as the last line does not have any content. This is due to the way txt files deal with '\n' newlines. This 'if' statement will only execute on the last line.

(Line 7-17)

```
7                else:
8                    parts = line.split('_')
9                    date_parts = parts[0].split('-')
10                   month = date_parts[0]
11                   exact_date = int(date_parts[1])
12                   week_no = 1
13                   for m in range(1, 4):
14                       if exact_date < m * 7:
15                           break
16                       else:
17                           week_no += 1
```

Same as before, I split the filename into parts. However, we only care about the first part, the date 🗓️, as you can see in Line 9. I first extract the month and date. Then, I check what week of the month it is in Lines 12-17 by seeing if the date value is greater or smaller than multiples of 7 up to 28.

(Line 18-22)

```
18                   date_sined = np.sin(2 * np.pi * exact_date / 31)
19                   date_cosed = np.cos(2 * np.pi * exact_date / 31)
20                   year = '2025-'
21                   if int(month) >= 9:
22                       year = '2024-'
23                   datetime_object = pd.to_datetime(year + str(parts[0]), format='%Y-%m-%d')
```

After cylical encoding of the date value using numpy's sin and cos functions, I check whether the month value is greater than 9. If it is, that means the data was collected in 2024. Otherwise, the 'year' defaults to 2025.

A rather crude way of determining the year, and it will stop working once we start to collect data in the 9th month of 2025 ⛔. I'm looking to change the way the year is determined in the near future, but not now.

(Line 23-27)

```
23                   datetime_object = pd.to_datetime(year + str(parts[0]), format='%Y-%m-%d')
24                   day_of_year = datetime_object.dayofyear
25                   day_of_year_sined = np.sin(2 * np.pi * exact_date / 365)
26                   day_of_year_cosed = np.cos(2 * np.pi * exact_date / 365)
27                   datetime_object = str(datetime_object)[:-9]
```

First, I attach the year to the month and date to form the full date 🗓️, then I convert it to a datetime object to find its 'day_of_the_year' value (the one that ranges from 1 to 365). 

After cyclical encoding of the 'day_of_year' value, I convert the full date value back to a string to remove the last 9 characters, which are the default time values '00:00:00' 🕓. 

They are assigned to datetime objects by default when they are saved to a csv file 📑, but they are of no use since we already have the time value for the rows. Also they are incorrect.

(Line 28-30)

```
27                   datetime_object = str(datetime_object)[:-9]
28                   new_row = [month, exact_date, week_no, date_sined, date_cosed, day_of_year, day_of_year_sined, day_of_year_cosed, datetime_object]
29                   df_to_attach.loc[len(df_to_attach)] = new_row
30       print(f'rating_{x} done')
```

I then compile all the new data into a list called 'new_row' and add it to the df 📝. At the end of the 'for' loop, I print a little log 💬 stating that the info in that particular rating file has been recorded down, before moving on to the next file. 

*feature engineering of 'lagging' variable columns* TBC!

In the next chapter, we will be using testing the loss values for each newly engineered feature to see which ones to keep, and which to discard.

### 4.4: Feature Selection Testing (in progress)
First, lets see how good our RFR model is without the extra features from feature engineering. I labelled the rest of the pictures 🖼️ (snaps 4, 5, 6 & 7) and trained the model on those too. However, I labelled the last 4 'snaps' folder pictures differently, straight up rating the congestion on either side of the causeway on a scale of 0-5 instead of using CVAT bounding boxes. 

Drawing them for every image takes too long ⌛, and the bounding box areas are not consistent.

To test how good the model is, lets use 2 relatively simples metrics 🧐: mean actual error (MAE) and root mean squared error (RMSE). MAE will show us the average difference between the predicted and actual values, while RMSE will place more emphasis on large errors due to its 'squaring' nature. 

This is helpful for seeing if the model is doing well for certain instances but not doing so well for others, since the larger errors are penalised more.

```
1    df = pd.read_csv("newdata.csv")
2    y_column_jb = df.pop('congestion_scale_jb')
3    y_column_wdlands = df.pop('congestion_scale_wdlands')
4    X_train, X_test, y_train, y_test = train_test_split(df, y_column_jb, test_size=0.2, random_state=0) # start off with jb
5    rfr_mae = mean_absolute_error(y_test, rfr_predictions)
6    rfr_rmse = mean_squared_error(y_test, rfr_predictions)**0.5
.
.
10    print(f"rfr mae: {rfr_mae} ")
11    print(f"rfr rmse: {rfr_rmse} ")   
```

I compiled all the data we have so far and did a 80% train, 20% test split. Normally I would do a 70/30 split ✂️, which you would know if you saw in the other repositories the way I go about my Kaggle competitions. But as we have limited image data that has been labelled with a congestion value, I chose to prioritise training data with an 80/20 split instead. 

The code above currently tests the model trained on data from the road to Johor, hence the y_column passed for the split in Line 4 is 'y_column_jb'. But not to worry, we will change that later on ✍️ and test the model for the road to Woodlands as well.

After testing both, here are the results, rounded off to 4dp:

**road to JB model**
- rfr mae: 0.3366
- rfr rmse: 0.7619
- ratio: 2.2637 

**road to Wdlands model**
- rfr mae: 0.6925
- rfr rmse: 1.2608
- ratio: 1.8208

Looks like the congestion on the road to JB is more predictable, with the MAE and RMSE being quite low (compared to the range of our values, 0-5). However, the RMSE being more than double the MAE implies there are some cases of large deviations in predicted values from the actual value. Overall, not too shabby for a first test 🤝.

The model for the other side of the road does not look as promising 😔. While the RMSE to MAE ratio is less than the other model, meaning there are no 'abnormally larger than usual' errors, thats probably because the MAE is already so high (more than double the previous MAE value). The fact that the MAE in this case is about 13% of the max congestion value, 5, is a little concerning but not a huge problem. 

However, the RMSE is 1.26 arbitrary units, a quarter of the congestion value range, which is a big problem 🚩. This means that when predicting the congestion on the road to Woodlands based on user input data 🗓️🕝, the predicted value output back to the user may differ from the actual value by more than 1 au. Thats a lot, considering the max congestion value is 5au.

Based on the EDA I did in [Chapter 3.2](#32-exploratory-data-analysis-eda), the congestion patterns for the road to Woodlands is certainly more inconsistent. The JB road model is nearly there but the Woodlands one needs some serious tinkering 🔧, and perhaps more training data for it to better generalise to the unpredictable nature of the traffic jams coming into Woodlands Checkpoint from JB.

Now lets see whether the new features will help to bring down the loss values 📉. I hope they do, otherwise all that feature engineering would have been a big waste of time.

We will test them in an existing python file, [Predicting_with_RFR.py](python_scripts/Predicting_with_RFR.py), instead of creating a new one. I think I've made too many python files 🗃️.

Prior to this, the python file already had a function to test RFR models coded in Chapter 4.2, you can see its explanation [here](#random-forest-regression). 

I made some minor tweaks to it 🔧 to include the train/test splitting (Line 4) for greater efficiency, as you can see below. 

I also created 'df_loss' to store the loss values (Line 1), so that its easier to compare between loss values of the various features.

```
1    df_loss = pd.DataFrame(columns=['feature', 'mae', 'rmse', 'mae_to_rmse ratio'])
    
2    def train_test_rfr(X, y, column_name, save_model=False):
3        print(X.shape, y.shape)
4        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
5        rfr_model = RandomForestRegressor()
6        rfr_model.fit(X_train, y_train)
7        rfr_predictions = rfr_model.predict(X_test)
8        # X_test['congestion_prediction'] = list(rfr_predictions)
9        rfr_mae = mean_absolute_error(y_test, rfr_predictions)
10       rfr_rmse = mean_squared_error(y_test, rfr_predictions)**0.5
11       rmse_to_mae = rfr_rmse/rfr_mae
12       print(f"rfr mae: {rfr_mae} ")
13       print(f"rfr rmse: {rfr_rmse} ")
14       print(f'ratio: {rmse_to_mae}')
15       new_row = [column_name, rfr_mae, rfr_rmse, rmse_to_mae]
16       df_loss.loc[len(df_loss)] = new_row
17       if save_model == True:
18           joblib.dump(rfr_model, "rfr_model_jb.joblib") # saving rfr weights for App Engine
```


Next, we execute the code to find out the loss values when each feature is added, for every feature one at a time 🔎.

```
1    df = pd.read_csv('newdata.csv')
2    df_to_attach = pd.read_csv('data_to_attach.csv')
3    new_features = []
4    for feature_name in df_to_attach:
5        new_features.append(feature_name)
    
6    y_column_jb = df.pop('congestion_scale_jb')
7    y_column_wdlands = df.pop('congestion_scale_wdlands')
    
8    for feature_name in new_features:
9        df[feature_name] = df_to_attach[feature_name]
10       train_test_rfr(df, y_column_jb, feature_name) # depends on which road you want to test
11       df.drop(feature_name)

```
(Line 1-5)

To start, I extract the original columns and the new columns ✂️, storing them in 'df' and 'df_to_attach' respectively. Then, I store the new column names in a list, new_features.

(Line 6-11)

After separating the two y_columns from the df ✂️, I iterate through 'new_features' and add each feature column to the original df. 


I chose to start with y_column = y_column_jb, we will do the same for y_column_wdlands later on.

Then, I call the train_test_rfr function to find and add the loss values to df_loss 📝, before removing the feature from the df so that we can test the next feature in the list.

Before going into the new loss values, let's see what the loss values are without any new variables first, when y-column = y_column_jb:

```
# original loss values from snaps 4-7 without new features (4dp):
mae = 0.3366
rmse = 0.7619 
ratio = 2.2637

# loss values from snaps 4-14 without new features (4dp):
mae: 0.9166942560262104 
rmse: 1.5240956662682845 
ratio: 1.6625997776784447
```

As expected, with more data that spans over a larger period of time, patterns and trends become more diverse, ultimately leading to higher loss values overall 📈.

Keeping that in mind, lets see how the loss values when the new features are added compare:

```
# with new features
             feature        mae       rmse   rmse_to_mae ratio
0              month   0.838329   1.540698            1.837822
1   exact_date_value   0.674292   1.178735            1.748107
2         week_value   0.683278   1.188597            1.739550
3           date_sin   0.662335   1.170298            1.766927
4           date_cos   0.661014   1.163488            1.760157
5        day_of_year   0.666203   1.196155            1.795482
6    day_of_year_sin   0.660283   1.193352            1.807335
7    day_of_year_cos   0.659929   1.183392            1.793211
8   sch_hol_period     0.665448   1.202109            1.806464
9   public_hol_period  0.671415   1.209479            1.801387
```

The df above can be found in this [csv file](python_scripts/loss_data_jb.csv)

This looks good, all the new features managed to reduce both mae and rmse values 📉. One exception is the 'month' feature, which reduced mae a little but caused rmse to increase slightly.

While the actual loss values are not exactly stellar, its encouraging to see that the feature engineering I did actually made a difference in lowering loss values. 

This means what we are doing is working, its a step in the right direction ❤️‍🩹.

As for the 'month' feature, I don't plan to completely not use it, but it's clearly not as effective as it should be 🤔. I'll leave it aside for now, but I'll try and get some use out of it later on in the chapter.

Since all but one of the new features reduced the loss values by large percentages, I'll use them all for now (except 'month', still need time to figure that one out).

However, I still have a few more tests I need to run, to ensure no redundant features slip through the cracks 🧐 and get implemented in the final model.

Improving loss metrics is good and all, but thats only one of the requirements for being a good feature. Next up, I'll be testing for multicollinearity between features 🔬, which is not good for ML models. 

We have quite a number of features anyway, so its good to trim them down a little, since too many columns can make the model less interpretable 😵‍💫 and more prone to overfitting. Also, many features don't necessarily mean better results.

The RFR file is getting quite messy, lets create the correlation matrix in the [feature engineering prep python file](python_scripts/feature_engineered_data_prep.py) instead:

```
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="RdBu")
plt.show()
```
The following parameters of the sns.heatmap() function serve different purposes to ensure the heatmap is outputted in a way we can understand more easily 🤓:

- "annot=True" writes the correlation value inside the coloured boxes. If it were set to False, we would not see the number, just the heatmap colours
  
- 'fmt=".2f"' makes sure all the correlation values inside the boxes are rounded to 2dp. Without this, the heatmap would be very messy with long and incomprehensive numbers strewn everywhere.
  
- 'cmap="RdBu"' defines the red-blue colourmap in matplotlib, which makes it such that a squares of correlation values closer to -1 and 1 are coloured red 🟥 and blue 🟦 respectively, while those with values closer to 0 are more whitish in colour ⬜.
  
Since we want to avoid numbers close to -1 as well as 1, I thought it would be good to make values further away from them be of a more contrasting colour ⬜, making it easier to tell whether a square has a high (🟥🟦 = 👎) or low (⬜ = 👍) modulus correlation value.

Here are the results:

![](progress_pics/Fig-4.7-feature_correlation_heatmap.jpg)

Fig 4.7: Heatmap showing correlation values between features, as well as between features and the two y-columns.

A good rule of thumb I learned is that if the correlation value is < 0.4, there is no multicollinearity. As we can see, a large majority of the squares are whitish in colour (⬜ = 👍) with correlation values not surpassing 0.4. However, there are a few bad eggs here and there.

- First off, the pale orange squares 🟧 of value -0.47. Those show the correlation between `hour_cos`, an independent variable (x), and `congestion_value_wdlands`, a dependent variable (y).

    Since the correlation is not between two independent variables, there is no multicollinearity, so no cause for alarm 😮‍💨. 

    In fact, this is actually good news, because it means the feature 'hour_cos' is a good indicator of the congestion condition on the road to woodlands.

- Next, a slightly paler orange square of value 0.42, slightly higher than the multicollinearity threshold. This square involves the features `day_of_year_cos` and `public_hol_period`. 0.42 is not very alarming, but still good to 📝 take a mental note of.
  
- This next one is pretty alarming. The feature `week_value` has very high modulus correlation values of -0.92 🟥, 0.97 🟦 and -0.85 🟥 with the features `day_of_year_cos`, `day_of_year_sin`, and `date_sin` respectively. Theres a high chance I'll remove the `week_value` feature later on, its just too correlated with too many other features.

- Another blue square of value 0.95 🟦 representing the correlation value between the features `day_of_year` and `sch_hol_period`.

- Lastly, the feature `date_sin` is highly correlated with the features `day_of_year_cos` and `day_of_year_sin`. The correlation values are 0.80 🟦 and -0.82 🟥 respectively.

    There is a chance I might remove `date_sin`. But since it comes as a pair with `date_cos`, I'm debating whether I should remove both or keep `date_cos` only.

Moving on, lets check out the loss values when y-column = y_column_wdlands:
```
# original loss values from snaps 4-7 without new features (4dp):
mae = 0.6925
rmse = 1.2608
rmse_to_mae ratio = 1.8208

# loss values from snaps 4-14 without new features (4dp):
mae: 1.6800370535424127 
rmse: 2.0927483098343385 
rmse_to_mae ratio: 1.2456560439674296
```

Similar trend from before in that the loss metrics are worse overall 📈 when y_column = y_column_wdlands as compared to when y_column = y_column_wdlands.

```
# with new features
             feature         mae      rmse  rmse_to_mae ratio
0              month    1.802642  2.286182           1.268239
1   exact_date_value    1.379175  1.775633           1.287461
2         week_value    1.377712  1.775881           1.289007
3           date_sin    1.372665  1.772797           1.291500
4           date_cos    1.360896  1.763427           1.295783
5        day_of_year    1.317476  1.735460           1.317261
6    day_of_year_sin    1.309835  1.715894           1.310008
7    day_of_year_cos    1.313066  1.725410           1.314032
8    sch_hol_period     1.318537  1.741869           1.321059
9    public_hol_period  1.303774  1.724481           1.322684
```
The df above can be found in this [csv file](python_scripts/loss_data_wdlands.csv)

Again, a decrease in mae and rmse for all but one of the new features. Looks like the new features' success was not a fluke 😎.

After looking at the performance of the new features 📊, as well as taking the correlation matrix heatmap into consideration, I've decided to remove the following features:
- week_value

  This feature shows signs of multicollinearity with 3 other features ⚠️, the most out of them all. While it did reduce the mae when implemented, the model still has the 2nd highest mae of all the other models which incorporated other features.

- day_of_year

  The information provided by this feature can be found in its cylical encoded counterparts `day_of_year_sin` and `day_of_year_cos`. Coupled with the fact that its highly correlated with `sch_hol_period` 👎, its a no brainer to remove.

- date_sin

  Without the `week` column values, we can't really tell where in the year this row’s info was taken 📅. `date_sin` is also highly correlated to `dayy_of_year_sin` and `day_of_year_cos`.

As for `day_pf_year_cos`, I will not remove it even though it has a correlation value of 0.42 with `public_hol_period`. Thats barely above the value I stated before, 0.4. 

Nothing compared to the correlation values of the other features removed, which range from 0.7 to 0.9. So keeping `day_pf_year_cos` around shouldn't pose much of a problem. I hope.

Now that we are done with that, lets take a look at our new 'holiday period' features 🎉🏖️. 

We know from our results above that the 2 holiday columns *do* in fact improve the loss 📉. However, I have a sneaky suspicion that theres a class imbalance in one or both of the columns 🧐, something I'd like to check.

```
1    def count_true(df, column_name):
2        count_true = df['column_name'].sum()
3        print(f'number of rows with 'True' for 'sch_hol_period' column = [count_true}')
4        total_no_of_rows = len(df)
5        print(f'total number of rows = {total_no_of_rows}')
6        print(f'Percentage of rows with 'True' = {int(count_true)/total_no_of_rows}')
    
7    count_true(final_df, 'sch_hol_period')
8    count_true(final_df, 'public_hol_period')
```
(Line 1-6)

I made a little function that checks for the number of rows with value = 'True' ✅ for a given column in a given df. 

It outputs the number (Line 3), before printing the total number of rows 📝 (line 4) as well as the percentage of rows with 'True' (Line 6). 

(Line 7-8)

Then, I call the function, passing the two holiday period features 🎉 in as parameters.

Here are the results:
```
number of rows with 'True' for 'sch_hol_period' column = 732
total number of rows = 2119 
Percentage of rows with 'True': 0.3454459650778669

number of rows with 'True' for 'sch_hol_period' column = 96
total number of rows = 2119
Percentage of rows with 'True': 0.045304388862671074
```

Looks like the percentage of rows that have 'True' for the school holiday period 🎒🏖️ feature is 34.5%, and 4.5% for the public holiday 🎄🧧 feature (1dp).

While 34.5% is only a mild class imbalance and does not warrant any changes, a percentage of 4.5% is very clearly a severe case of class imbalance ⚠️ that requires our attention.

We don't want a situation where the model overfits on non-public holiday rows due to the train data being mainly made up of rows not within the public holiday period ❌.

To see if this will happen, I'll be using k-folds validation instead of a standard train/test split to test the generalizing power of the model 🧐 when the holiday period features (as well as all the other features) are implemented. 

K-folds validation splits the data into 'k' parts and trains the model 'k' times. 

The following code can be found in this [python file](python_scripts/Predicting_with_RFR.py)

```
1    def cross_val(model=rfr_model, X=final_df, y=y_column_jb):
2        losses = cross_val_score(model, X, y, cv=8, scoring='neg_mean_absolute_error')
3        losses = np.abs(losses)
4        for x in range(len(losses)):
5            print(f'fold {x}: {losses[x]}')
6        print(f'average mae: {np.mean(losses)}')

7    cross_val()
```
(Lines 1-3)

I create a cross_val_score object called 'losses' which will store all the loss values 📝. In this case, it will just be 'negative MAE', which I defined together with the number of folds I want (cv=8). Regular MAE would be more straightforward, but the cross_val_score function only does not have it 😔. 

Afterwards, I converted all the negative MAE values into positive ➕ using numpy's absolute function.

(Lines 4-7)

Due to there being 8 folds, the model was trained 8 times, hence there are 8 loss values obtained. I used a 'for' loop 🔄 to print out the fold number together with its corresponding MAE loss value, before calculating and printing the average of the 8 losses using numpy's mean function. Lastly, I called the function.

```
fold 0: 0.8011698113207547
fold 1: 0.6146037735849057
fold 2: 1.030264150943396
fold 3: 0.7907169811320754
fold 4: 0.9013207547169813
fold 5: 0.8610943396226415
fold 6: 0.5869056603773585
fold 7: 1.018598484848485
average mae: 0.8255842445683248
```

As we can see, the MAE is quite inconsistent, with values ranging from a low 0.6 👍 to as high as 1.0 👎. This means there are some row instances that the model cannot predict well. Those rows may be rows that fall within the public holiday period, or it could be a another specific combination of column values that puzzles the model 😵‍💫. Unfortunately, I am unable to pinpoint what rows is giving the model a hard time as of this moment.

Now that I think about it, it seems quite a waste to not use the 'month' column. 

It should be providing a wealth of useful information to the model since its a good representation of the different seasons in a year, yet its increasing the mae and rmse 🤔. 

I have a feeling the model is misunderstanding the relationship between the numerical 'month' column and the congestion values, in that it thinks a bigger 'month' value means larger congestion value 📈, or something along those lines. 

Let's try a different approach, one-hot encoding the month values instead of having them as numerical values all in one column. 

```
# one-hot encoding of month here, adding the column from final_data.csv
1    month = final_df.pop('month')
2    df['month'] = month
3    df = pd.get_dummies(df, columns=['month'])
4    df = df.drop(['month_1'], axis=1)
5    print(df.head(5))

# testing without the new features first
6    train_test_rfr(df, y_column_jb) # start with jb as y_column
```

(Lines 1-2)

First, I transfer the `month` column from the df with all the new features to the original df.

(Lines 3-5)

Next, I call get_dummies from the pandas library on the month column to get 12 'month columns'. Then, I drop one of the encoded month columns to prevent multicollinearity.

Where is the multicollinearity you may ask? Well, if 11 of the 12 one-hot encoded `month` columns were 'False' ❌, Then you would instantly know that the last one was 'True' ✅. That is a prime example of multicollinearity betweem features.

(Lines 5-6)

Lastly, I print the first 5 rows of the df 📝 to make sure all the columns are correct and the values have no problems (see below), before calling the testing function I made earlier, 'train_test_rfr'.

```
   Mon  Tue  Wed  Thu  Fri  Sat  hour_sin  hour_cos  month_2  month_3  month_4  ...  month_11  month_12
0  0.0  0.0  1.0  0.0  0.0  0.0  0.258819  0.965926    False    False    False  ...      True     False
1  0.0  0.0  1.0  0.0  0.0  0.0  0.500000  0.866025    False    False    False  ...      True     False
2  0.0  0.0  1.0  0.0  0.0  0.0  0.707107  0.707107    False    False    False  ...      True     False
3  0.0  0.0  1.0  0.0  0.0  0.0  0.866025  0.500000    False    False    False  ...      True     False
4  0.0  0.0  1.0  0.0  0.0  0.0  0.965926  0.258819    False    False    False  ...      True     False
```

Lets see if one-hot encoding helps prove the month column's worth 💎. I'll be testing using y-column_jb as the dependent variable:

```
# loss values from addition of one-hot encoded month values
rfr mae: 0.8460125912786498 
rfr rmse: 1.5448904939684378
ratio: 1.826084516819679
```

Looks like although the loss values are better than when none of the new features were used, they did not improve more than when the month column was not encoded 👎. Dang it.

Another idea I have for the month columns is - instead of splitting the feature into 12 separate columns (which would likely trigger the curse of dimensionality and increase loss values 👎), we decrease the number of new features by sorting the month values into quarters of the year 🗓️.

So month values 1, 2, and 3 (Jan, Feb, Mar) will represent 1 column, the 1st quarter of the year 🗓️. If the row's month column has a value of 4, 5, or 6 (Apr, May, June), the column representing the 2nd quarter of the year will have the value 'True' ✅. I think you get the idea.

The following is my code for encoding the 'month' values into 'yearly quarter' values.

```
1    def quarter_col(month_value):
2        if month_value <= 3:
3            return 'Q1'
4        elif month_value <= 6:
5            return 'Q2'
6        elif month_value <= 9:
7            return 'Q3'
8        else:
9            return 'Q4'
        
10   df['year_quarter'] = df['month'].apply(quarter_col)
11   df = df.drop(['month'], axis=1)
12   df = pd.get_dummies(df, columns=['year_quarter'])
13   df = df.drop(['year_quarter_Q4'], axis=1)
14   print(df.columns)
15   train_test_rfr(df, y_column_jb)
```

(Lines 1-9)

I make a function which returns the corresponding year quarter value 🔢 when a month value is passed in it.

(Lines 10-12)

I apply the function to the df and create a new column for the quarter values, called 'year_quarter'. Then I get rid of the original 'month' column 🗓️ and get dummy columns for the 'year_quarter' column.

(Lines 13-15)

First, I drop one of the four new 'year_quarter' columns for multicollinearity reasons (I randomly chose 'year_quarter_Q4'). Then I print the columns of the df for a final check 🔎, before calling the custom function to see the new loss values.


```
rfr mae: 0.8005795933306458 
rfr rmse: 1.4387099823922096
ratio: 1.7970855045239842
```

Slightly better mae and rmse than the original month column, and way better than the 12 one-hot encoded month columns 🌟. Looks like this time, the one-hot encoding was a success 🎯.

Now, let's try using only the selected features, and see if removing the multicollinear features really helps.

Columns being used: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'hour_sin', 'hour_cos', 'day_of_year_sin', 'day_of_year_cos', 'sch_hol_period', 'public_hol_period', 'year_quarter_Q1', 'year_quarter_Q4']

When y_column = y_column_jb:

```
rfr mae: 0.7150990004492364 
rfr rmse: 1.2407860746318913
ratio: 1.7351248901934
```

When y_column = y_column_wdlands:

```
rfr mae: 1.4146160152740341 
rfr rmse: 1.8250879333103731
ratio: 1.2901649024218236
```
This is odd... Removing correlated features almost always improves model performance 🚀, yet the loss values (for when all the chosen features are used) are higher 📈 than when individual columns were used by themselves.

Let's try using all the new features we acquired 🌟 (including the 'removed' columns that show high multicollinearity).

Columns being used: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'hour_sin', 'hour_cos', 'week_value', 'date_sin', 'date_cos', 'day_of_year', 'day_of_year_sin', 'day_of_year_cos', 'sch_hol_period', 'public_hol_period', 'year_quarter_Q1', 'year_quarter_Q4']

When y_column = y_column_jb:

```
rfr mae: 0.6705896226415093 
rfr rmse: 1.2117450966458594
ratio: 1.8069845636332587
```
When y_column = y_column_wdlands:

```
rfr mae: 1.2999056603773587 
rfr rmse: 1.7204476435915226 
ratio: 1.3235173105501223
```
Loss values are lower than when only the chosen features were used 📉, but these still are not low enough. We obtained lower, better mae values when we were testing out individual features (0.66 for y_column_jb and 1.30 for y_column_wdlands). 

Since we are using them together 🤝, they should be performing better than they were individually.

As of right now, these are the best models I can come up with 😖. But there is definitely a specific subset of the features, both new and old, that when used will yield a lower mae than 0.66 for when y_column = y_column_jb and < 1.3 for when y_column = y_column_wdlands 👍.

Unfortunately, aside from 'for' looping 🔄 through every single combination of features, I am not sure how to find that combination at the moment. 

For now, I'll just implement all the features 📝, as well as the one-hot encoded quartered month columns, into another model and save it as a joblib file as well 💻 for future implementation into the webapp in [chapter 5.4](#54-creating-mainpy-v2-and-appyaml).

That concludes the feature engineering and testing for this model 🤝, for now at least 😤.

In the next chapter, let's see if we can improve the accuracy of our model even more than we already have, this time by adjusting the model's hyperparameters ⚙️.

### 4.5 Hyperparameter Tuning (tbc)
There are numerous hyperparameters that can be tweaked in the RFR model to further improve our loss metrics 📉, even if by just a little. 

I'm not an expert, so I'll only be looking into the more basic hyperparameters 😁, such as the following:

- `max_depth`, lets us choose how deep a tree in the forest is allowed to grow 𖣂
- `n_estimators`, allows us to change the number of trees in the forest 🌲
- `criterion`, this allows us to choose which loss metric to consider when splitting at a node ⚙️
- `bootstrap`, this lets us choose whether we want to reuse rows when training the model 🔄
- `max_features`, this lets us choose the number of features the model randomly chooses from when splitting a node 🔢 *(use k folds to test dis)*
- `min_samples_leaf`, this allows us to decide the minimum number of rows required in a leaf 🌱

Let's get into it 💪, starting off with the first hyperparameter: max_depth

```
max_depth_list = [5, 7, 9, 11, 13]
for x in range(len(max_depth_list)):
    rfr_model = RandomForestRegressor(random_state=0, max_depth=max_depth_list[x])
```

To see which depth will obtain the smallest loss values, i will 'for' loop through a list of depth values: [6, 8, 10, 12, 14]. A reminder to all of us that the loss values of the base model when all the variables are used, without hyperparameter tuning, are the following (after setting random_state=0, mb I forgot earlier):

```
rfr mae: 0.6731839622641508 
rfr rmse: 1.209741415531778
ratio: 1.7970443197473076
```
When y_column = y_column_wdlands:

```
rfr mae: 1.2999056603773587 
rfr rmse: 1.7204476435915226 
ratio: 1.3235173105501223
```

Keeping these values in mind, lets take a look at the loss values when each of the max_depth values are used. For time and simplicity's sake, I will only show the MAE for the road to Johor.

```
max_depth = 6, rfr mae = 0.7412137978905754
max_depth = 8, rfr mae = 0.6896147016265989
max_depth = 10, rfr mae = 0.6684006708449132
max_depth = 12, rfr mae = 0.670419573641038
max_depth = 14, rfr mae = 0.6705209665849877
```

The lowest MAE we got was from a max_depth value of 10, with the MAE dropping from 0.67318 to 0.66840. 

We will use this max_depth value in the final model, but not for the next few models where we are further experimenting with the rest of the hyperparameters. This is to ensure that any improvements in MAE is purely due to the target hyperparameter being tuned.

For the next hyperparameter, `n_estimators`, similar to `max_depth`, I'll be iterating through a list of values to see which results in the lowest MAE.

```
n_estimators_list = [15, 17, 19, 21, 23]
for x in range(len(n_estimators_list)):
    rfr_model = RandomForestRegressor(random_state=0, n_estimators=n_estimators_list[x])
```

MAE for each value of `n_estimators`:

```
n_estimator = 15, rfr mae = 0.6803459119496856
n_estimator = 17, rfr mae = 0.678274139844617
n_estimator = 19, rfr mae = 0.6740317775571003
n_estimator = 21, rfr mae = 0.6698113207547169
n_estimator = 23, rfr mae = 0.6734003281378178
```

Another MAE below 0.67 has been obtained, this time from changing the `n_estimator` to 21.

As for the `criterion` hyperparameter, I will be testing the 2 basic values out of the 4, 'absolute_error' and 'squared_error' to see which yields the best MAE as well as RMSE values. This hyperparameter determines whether the model trains to reduce MAE or MSE.

The default value is 'squared_error' (MSE loss metrics are listed above, when no hyperparams are applied), so I'll only test 'absolute_error' and see if its any better.

`rfr_model = RandomForestRegressor(random_state=0, criterion='mae')`

When `criterion` == 'absolute_error':

```
rfr mae: 0.7686084905660377 
rfr rmse: 1.284930574073432 
ratio: 1.6717621387803712
```

Looks like criterion = 'absolute_error' not only results in a higher RMSE value, the MAE value is also higher. `criterion` = 'squared_error' is the clear winner here, So I won't touch this hyperparameter in the final model.

For the `bootstrap` hyperparam, the default value is 'True', so I'll be testing the model when its 'False' and see if the loss values are better than that of the default model.

When `bootstrap` == True, it basically means the same data can be sampled again when training the model, so they are essentially 'reused' when training the model.

`rfr_model = RandomForestRegressor(random_state=0, bootstrap=False)`

```
rfr mae: 0.6334669811320754 
rfr rmse: 1.4964108790261865 
ratio: 2.3622555296440786
```

**Damn**, MAE decreased from 0.673 to 0.633. However, RMSE did increase by quite a bit, from 1.21 to 1.50. This means that while overall, the loss decreased, the larger losses became bigger. I'm not too sure what to do here.

The increase in RMSE is significantly larger, so for now, I'll prioritize that and keep bootstrap = True. However, this may change in the future.

Moving on to `max_features`, the default value is 'n_features' which means all features are utilised for the training of all trees in the forest. Well that may sound good, there are some pros to not using all 19 features. 

I'll be trying out the following values: [4, 7, 10, 13, 16], before only listing the MAE values when y_column == y_column_jb, for simplicity and time's sake. Don't worry, I still do look at the RMSE.

```
max_features_list = [4, 7, 10, 13, 16]
for x in range(len(max_features_list)):
    rfr_model = RandomForestRegressor(random_state=0, max_features=max_features_list[x])
```

MAE results for variation of max_feature values:

```
max_features = 4, rfr mae = 0.6902122641509434
max_features = 7, rfr mae = 0.6747405660377359
max_features = 10, rfr mae = 0.6722169811320754
max_features = 13, rfr mae = 0.6612971698113207 (btw the rmse here is 1.712)
max_features = 16, rfr mae = 0.6631839622641508
```

Excellent MAE from max_features == 13, with the MAE being the lowest we have seen so far. However, similar to when we turned off bootstrap sampling, the RMSE has skyrocketed from 1.210 to 1.712 unfortunately.

The improvement in MAE is big, but the increase in RMSE is even bigger, so I'll leave `max_features` at its default value for now, using all the features.

For the last hyperparameter we will be tampering with, `min_samples_leaf`, the values I will be experimenting with are: [2, 4, 7, 12]. The default value is 1.

```
min_samples_leaf_list = [2, 4, 7, 12]
for x in range(len(min_samples__list)):
    rfr_model = RandomForestRegressor(random_state=0, min_samples_leaf=min_samples_leaf_list[x])
```

Here are the results:

```
min_samples_leaf = 2, rfr mae = 0.6827621472474067
min_samples_leaf = 4, rfr mae = 0.7185515207927632
min_samples_leaf = 7, rfr mae = 0.7471483231193558
min_samples_leaf = 12, rfr mae = 0.77560062027817
```

Looks like the MAE only increases with the `min_samples_leaf` value, so I'll stick to the default value and not touch this hyperparameter in the final model.

Now lets set up the two hyperparameters that showed improvement and see the final MAE:

`rfr_model = RandomForestRegressor(random_state=0, max_depth=10, n_estimators=21)`

Here are the MAE and RMSE when y_column = y_column_jb:

```
rfr mae: 0.6646568578353077 (prev value = 0.6731839622641508)
rfr rmse: 1.1976507344339455 (prev value = 1.209741415531778)
```

However, when y_column == y_column_wdlands:

```
rfr mae: 1.3922500431026001 (prev value = 1.2999056603773587)
rfr rmse: 1.7841667460062003 (prev value = 1.7204476435915226)
```

We can see that while the loss metric values when predicting congestion on the road to JB has improved, the same hyperparameters has caused the MAE and RMSE to increase for the other side of the causeway. 

Instead of testing all the hyperparameters again, for y_column == y_column_wdlands, I will use random search to find the optimal combination of hyperparameter values.

### Finding optimal hyperparameter values using RandomizedSearchCV

First, lets create a dictionary of all the hyperparameters we will be tuning, and their values:

```
param_dict = {
    'max_depth': max_depth_list, # 5 values
    'n_estimators': n_estimators_list, # 5 values
    'max_features': max_features_list, # 5 values
    'min_samples_leaf': min_samples_leaf_list # 4 values
}
```

Now lets define the random search object and fit it to our training data, before printing out the best hyperparameter values and corresponding loss metrics when applied to the test data:

```
X_train, X_test, y_train, y_test = train_test_split(trainfinal_df, y_column_wdlands, test_size=0.2, random_state=0)

random_search = RandomizedSearchCV(
    estimator=rfr_model,
    param_distributions=param_dict,
    n_iter=60,  # Number of parameter combinations to try
    scoring='neg_mean_squared_error',
    cv=5,
    verbose=2,
    random_state=0,
)

random_search.fit(X_train, y_train)

best_model = random_search.best_estimator_
y_pred = best_model.predict(X_test)
print(mean_absolute_error(y_test, y_pred))
print(f'max_depth: {best_model.max_depth}')
print(f'n_estimators: best_model.n_estimators')
print(f'max_features: {best_model.max_features}')
print(f'min_samples_leaf: best_model.min_samples_leaf')
```

The results are as follows.

When y_column = y_column_jb:

```
0.6723551549271564
max_depth: 12
n_estimators: 23
max_features: 13
min_samples_leaf: 1
```

When y_column = y_column_wdlands:

```
1.3496258330542605
max_depth: 12
n_estimators: 23
max_features: 13
min_samples_leaf: 1
```

Using random search cross validation still cannot find us the optimal hyperparameters, as these MAE results are still slightly worse than what we have obtained before. 

It will take more time and will stress my laptop abit, but I will try using grid search to find the optimal parameters.

```
grid_search = GridSearchCV(
    estimator=rfr_model,
    param_grid=param_dict,
    cv=5,
    verbose=1,
    scoring='neg_mean_absolute_error',
)
```

I also changed the param_dict, getting rid of some hyperparams which we already know the best values to so that we can reduce the number of permutations. 

```
max_depth_list = [10, 12, 14, 16]
n_estimators_list = [15, 17, 19, 21, 23, 26, 30, 32, 35]
max_features_list = [8, 10, 12, 15, 19]
```

I also added some extra values to `n_estimators_list` since the best value for that is the greatest value in the list, 23. That means that a larger number of trees in the forest than 23 might lead to better results.

The results are as follows.

When y_column = y_column_jb:

```
0.6643241902961728
max_depth: 14
n_estimators: 30
max_features: 12
min_samples_leaf: 1
```

Decent improvement, breaking the 0.67 MAE plateau. Looks like increasing the upper limit of the 'n_estimators' hyperparameter was the right call, as the best model has `n_estimators = 30`. 

When y_column = y_column_wdlands:

```
1.2840808406542723
max_depth: 16
n_estimators: 15
max_features: 10
min_samples_leaf: 1
```

Marginally better MAE, but the difference is so small I'm not sure if it really matters or its just noise. 

Regardless, doing a grid search, while more time consuming than random search, has allowed us to obtain hyperparameter values that, when used, surpass our previous MAE best scores.

Currently, the model being deployed in the Johorscrape website is the old one, with the default hyperparameters and no new features. I will implement these hyperparameter values for their respective y_columns in GCloud, as well as the new hyperparameters, at the end of Chapter 5.4 [here](mainpy-v3).




(TBC!)

## Chapter 5: Automation and Website Making
### 5.1: Making HTML and CSS for Frontend
Quite excited for this, I've always admired aesthetic looking websites ✨ and have a couple ideas for one in mind 💡. That said, I only have very minimal knowledge of HTML from scraping websites, and no experience whatsover with CSS. However, a friend of mine said its quite easy to pick up, so I'll be drafting up some website design prototypes on Canva 🖼️ while learning HTML & CSS at the same time 📚.

Here is what I came up with:

![insert canva ting here](progress_pics/Fig-5.1-canva_ss.jpg)

Fig 5.1: Canva website draft

Ideally, this is what I want the user to see as soon as he enters the website. No fluff and straight to the point, with a pretty background of the causeway, in the afternoon on the left 🌇 and night on the right 🌃.  I did this to try and push the idea of "same causeway, different time".

I'm no artist, but I think it looks nice :)
 

You can see the orange rounded-edge boxes with date, time and AM/PM. In the actual HTML website, those would be the buttons where u can select the date and time 📲.

I also intend to add a 'How to Use' guide below as you scroll down 📘 (with the background not moving as you scroll cuz damn that looks cool), but for now this will do. Now its time to churn this out in HTML for our actual website frontend.

Update: The first version of the HTML for the website is done! Let me take you through it, starting with the <head> tag.

![insert part 1 of HTMLINKKK](progress_pics/Fig-5.2-HTML_style_ss_p1.jpg)

Fig 5.2: Styling portion of HTML version 1

The head tag contains the CSS for the website, although I'll probably be moving this to a separate CSS file moving forward 📁 to make the HTML file easier to read. This is very beginner CSS 👶🏻, nothing too fancy, so I wont go into everything in detail. 

I defined the [background](progress_pics/website_bg2.jpg) for the body (basically the entire website) in Line 10. Then I made the <body> element have all its elements inside align to the centre (Line 16). For the font colour I chose 'Alice Blue', although its less blue than it is white ◻️ (Line 14). Basically white with a slight tint of blue 💧.

For the top class (Line 19), it contains all the text in the website, which is just the title as well as the little slogan right below it. I wanted them to be well separated ↕️ from the top of the screen, as well as from the 'select date and time' buttons, hence it has a top and bottom padding of 120px. The <body> is already aligned to the center, so theres no need for side padding.

For the column class (Line 38), i wanted the date and time buttons to be side by side 📅🕒 like in the Canva draft and not have a new row for every element, so I added 'display: inline block' in Line 39. The column class is nested in <body>, so the group of buttons are aligned to the center.

The "where-you-click" class is exactly that, its the class for the elements which you click on 👉🔘, the date and time buttons. I added a slightly grey border (Line 58) to the transparent button (Line 60). I rounded the button corners (Line 59) for a more aesthetic look and made the text colour white, although thats probably not necessary since I already defined a whitish text colour in <body>.

![insert ss of body tag HEREEEEEEEE](progress_pics/Fig-5.3-HTML_body_ss_p2.jpg)

Fig 5.3: 2nd part of HTML version 1

Moving on from CSS to the actual HTML, I created the first of the 3 🔘🔘🔘 input buttons in Lines 77-80, 'Date'. The input type "date" makes it such that when clicked 👆, it produces a calendar 🗓 where you can pick a date. 

The time button is made in Lines 81-97 🕓. The "select" tag gives the dropdown ▼ rows when the button is clicked to reveal the possible time values you can pick 👆, which are defined in the <option> tags. The AM/PM button is similar, except with only 2 options. 

I did not give the AM/PM button a label for aesthetic purposes ✨, as you can see in Fig 5.2 below theres no AM/PM label next to the button. Also the AM/PM dropdown values after clicking make it kinda self explanatory without the need for a label.

All this gives us this frontend output:

![insert HTML first vers HEREEEEEEEE](progress_pics/Fig-5.4-html_state_1.jpg)

Fig 5.4: First prototype of website's HTML.

The HTML file for our website can be found [here](GAE/templates/starter_html_mine.html) 📂, although its contents may be changed throughout the project as I learn more HTML & CSS and make improvements 💫. I'll also be making a [CSS file](GAE/static/styles.css) to separate the styling content from the actual HTML. The CSS and other static files such as jpeg files 🏞️ will be stored in the [static](GAE/static) folder.

### 5.2: Creating Backend with Flask, main.py, and then app.yaml
With a rough version of the html and css files ready, we can shift our focus to the backend of the website ⚙️.

#### main.py + changes to HTML to accomodate backend
To start, lets make main.py 📝 which will set up Flask as well as control what will be outputted back to the user. For now, we won't be outputting any ML predictions, just printing back out the input date 📆 and time 🕒 given by the user. 

This is because I want to make sure the actual html and main.py work together seamlessly to properly output data 📤 before I start bringing in joblib files and machine learning models.

```
1    from flask import Flask, render_template, request

2    app = Flask(__name__)

3    @app.route('/')
4    def home():
5        return render_template('index.html')
```
First, I import Flask, the foundation of our web application build 🌐. It will provide the necessary tools we need to properly set up our website 🔧, such as render_template and request. 

"render_template" is used to load in HTML files together with their css, as well as any variables you want to pass to it. "request" allows us to obtain any data inputted 📥 by the user on the website, such as date or time.

In line 3, the '/' represents the root url. It means that the following function `home()` will define the "main page" of the website, basically what will greet the user the first time he/she enters the website.

The main function itself is very simple, just a single line (Line 5). It displays the html page with its css 📰 without any additional variables (since the user just entered the website, they have not submitted any input).
```
6    @app.route('/predict', methods=['POST'])
7    def predict():
8        date_value = request.form.get('date')
9        time_hour = request.form.get('hour')
10       ampm = request.form.get('ampm')
11       return render_template('index.html', date=date_value, hour=time_hour, ampm=ampm)

12   if __name__ == "__main__":
13       app.run(debug=True)
```
In Line 6, the '/predict' means that when the html button, which is of type=submit (i'll show the updated html later), is clicked 👆, '/predict' is appended to the end of the url 🔗 and the function in Line 7 is called. The user input is obtained (Lines 8-10) before the html file is rendered, but this time with the relevant variables 📅🕒 (Line 11).

The 'POST' method is specified in Line 6 so that only POST requests trigger the predict() function. It is one of 2 request methods and is meant for requests that include transferring of data 📲 to the backend. Thats why predict() is called when a button of type=submit is clicked, since it sends input data.

I also changed the html file abit. Before, the html file only had to display the buttons 🔘, it did not actually have any backend or output. It was essentially a skeleton of the website 🦴. I'll explain the parts which were added, not the whole thing since I already explained the bulk in [Chapter 5.1](#51-making-html-and-css-for-frontend)

```
1        <div class="top">
2            <div class="title">Johorscrape<sup style="font-size: 18px;">&copy;</sup></div>
3            <div class="sub-title">Tell us when, and we'll handle the rest :)</div>
4        </div>
5        {% if date %}
6            <p>Date: {{date}}</p> <p>Time: {{time}} {{ampm}}</p>
7            <p>Prediction: {{pred}} units</p>
8        {% endif %}
9    <form action="/predict" method="POST" class="datetime-container">
10           <div class="column">
11               <label for="date">Date</label>
.
.
.
56                   <option value="PM">PM</option>
57               </select>
58           </div>
59           <button type="submit">Submit</button>
60    </form>
```
Lines 5-8 and Line 59 were added after creating main.py, they are meant to handle the output returned by the backend, main.py, as well as to pass input data to the backend 📲 respectively.

The {% if date %} is basically a python 'if' statement but in HTML and Flask syntax. This is so that the output is only shown 📰 if theres a valid 'date' input from the user. Why did I not include 'if time' and 'if AM/PM'? 🤔 Because they already have a default value, so its impossible to submit input without a valid 'time' and 'AM/PM' value.

I actually learnt this {% if %} stuff from chatgpt, not from a book or man-made resource, which might be frowned upon by some. But as long as it gets the job done and I understand exactly how it works, as well as how to use it, I don't see a problem. 

Me personally, I draw the line when the code is completely made by AI 🤖, or 90% made by AI and the other 10% is just changing of variable names and other minor knick-knacks. But who gives a toss what I think hmm?

#### Test run + first thoughts
Anyway, here's the 1st website test run, I ran it using 'python main.py' on the Google shell terminal 📟. This is just a test run on a local port to make sure everything runs fine, more refinements to the website visual will be made over time. 

![OIII](progress_pics/Fig-5.5-outputs_the_input_vid.gif)

Fig 5.5: Website test run, output printed is the input date and time

As you can see, the website mechanisms work just fine, no edge cases (so far) that cause the website to glitch out or crash 👍. As it should be, its quite a simple website so far. The data can be input by the user smoothly 🤳, the UI is easy to understand 📱, and the output is printed out quickly after the submit button is pressed 📲. The input and output aesthetics could do with some work though.

This is not run on GAE yet, that requires the app.yaml file 📂 which we will create and go over later on. 

One thing I'm slightly annoyed with is that, after submitting your input, typically you would refresh the page to submit another input, another date an time. However, when I refresh 🔄, the website stores the data from before and continues to output the previous output 💢. To actually clear the previous input and start afresh, you have to click the submit button again 👆.

I tried using `sessions.pop('date')` after the output was returned, which is supposed to make the website 'forget' the previous input data, but that didn't work . I also tried `{% if request.method == GET %}`, because by right a page refresh is a GET method not a POST, but after checking the logs I realized: a refresh of a page which was loaded in via a 'POST' is still a 'POST' request, not 'GET'. 

Its not a major flaw, but its still a little annoying 💢. I hope to find a solution to this, but for now I'll move on with the rest of the website build. There's bigger fish to fry 🐟, now is not the time to fret over this small stuff.

Now that we know the frontend is able to send input data to the backend, and the backend can send output back without any hiccups, we can focus more on what **kind** of output we want to be sent. Not just the date and time like before, but also the prediction value 📊.

I'll also add an image of what the congestion situation will likely look like 🖼️, in case the prediction value is not enough to convey how severe the traffic jam will be 🚙🚗💨 to the user. These pictures will have a red line annotated on the road to show a rough estimate of where the traffic jam is likely to end at that instance. I have 6 photos ranging from a scale of 0 - 5, with 0 being no jam at all and 5 being max congestion. You can see them below.

![](progress_pics/Fig-5.6-zero_to_five_pics.gif)

Fig 5.6: Images showing congestion values from 0-5, with red lines annotated on the roads.

I also added images scaling from 0 to 5 in congestion intensity for the woodlands side of the causeway.

### 5.3: .joblib file and Project Folder structure
#### Making ML weights portable with Joblib
For our website backend, we don't want to be training the ML model again and again 🔁 every time a user sends in their input. Furthermore, we would need to have the training data on hand all the time, which would take up a lot of space 🗃️. All this wastes a lot of time ⌛, is computationally expensive, and overall a very stupid way to set up our website 🤡. 

So instead, we will train the model beforehand **once**, then store the trained model's weights for later use 📦.

This is where the joblib package comes in handy. With just one line of code, we can save the model's weights after training ⚖️. The following code is from [Predicting_with_RFR.py](python_scripts/Predicting_with_RFR.py), the only change is the joblib line.

```
# Random Forest Regressor model
rfr_model = RandomForestRegressor()
rfr_model.fit(train_df, y_column)
joblib.dump(rfr_model, "rfr_model.joblib") # NEW LINE, saving rfr weights for App Engine

rfr_predictions = rfr_model.predict(test_df)
```
After saving the weights in a joblib file named rfr_model.joblib, I can move this file to the 'johorscrape_website' project folder 🗂️ in GCloud shell editor together with the rest of the files. Now we can reference it whenever we have to make a prediction, without having to train a fresh model every time 🏋.

#### Project folder structure
As of right now, this is how the project folder's file structure in the gcloud shell editor is looking:
```
/johorscrape_website
    |── myenv/
    |   └── packages, libraries, etc
    |── app.yaml
    |  
    |── static/
    |   └── website_bg2.jpg
    |	└── 1_jam.jpg
    |	└── 2_jam.jpg
    |	└── 3_jam.jpg
    |	└── 4_jam.jpg
    |	└── 5_jam.jpg
    |	└── styles.css
    |	└── mobile.css
    |	└── website_bg2.jpg
    |	└── website_bg.jpg
    |  
    |── templates/
    |  └── index.html
    |  
    |── main.py
    |  
    |── requirements.txt
    |    
    |── rfr_model.joblib
```
Starting off with `myenv`, thats the virtual environment (venv) that stores all the installed libraries 🗂️ listed in requirements.txt, the second last file near the bottom of the project folder. Its only necessary for test runs with `python main.py` though, GAE has its own environment to store the downloaded libraries.

`app.yaml` contains code which configures how GAE deploys our website. Right now its still an empty file 📁, but we will get to it once we need to deploy the website publicly 🌐.

The `templates/` folder contains the main HTML file, index.html. I'm not too sure why a whole folder is needed for just for one file, but this is by default how website files should be organized 🗄, with css files inside static/ and html files inside templates/.

`main.py` as you know contains the backend for our website, and `rfr_model.joblib` contains the weights of our pre-trained random forest regressor model 🌲🌲🌲.

The `static/` folder contains all the css files, as well as image files which I intend to output in the website 🖼️. The {number}_jam.jpg files are pictures of the causeway 🛣️ at different levels of congestion, with 1 meaning 'no jam' to 5 meaning 'chock full of cars' 🚙🚗💨. 

You may notice that there is one more css file, mobile.css. Its basically the same as styles.css, but for when someone opens the website through their mobile phone 🤳, or a device of different dimensions to a laptop/desktop. You may be wondering, why is this necessary 🤔?

So far, every time I have entered the website, it has been from my laptop 👨‍💻, so the website is opened in landscape mode. It looks great, formatting and space between elements have been hand-tuned to perfection by yours truly 🔧. But enter the very same url in your iPhone or Samsung galaxy 📱, and you get something that looks like this...

![](progress_pics/Fig-5.7-chopped_css_fone.jpg)

Fig 5.7: How the website looks like when viewed from a Samsung Galaxy S8+.

As you can see, css that looks good for one device may not look as good for another. Rather, it can be pretty hideous 🤮.

This is where mobile.css comes in. Its very similar to styles.css, except I changed the [background image](GAE/static/website_bg.jpg) to something more potrait friendly 🌃. I also edited the text sizes to make the words fit the screen sizes of mobile phones 📱.


### 5.4: Creating main.py v2 and app.yaml
#### main.py v2
After adding the joblib file to the project folder, we can now reference its weights ⚖️ in main.py and use it to properly output a prediction value 📲. Lets see the changes in main.py.
```
...
3    import joblib
4    import pandas as pd
5    import numpy as np
...
9    rfr_model = joblib.load('rfr_model.joblib')
10   cols = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'hour_sin', 'hour_cos']
...
21          ampm = request.form.get('ampm')
22          input_df = pd.DataFrame(np.zeros((1, 8)), columns=cols)
23          date_obj = datetime.strptime(date_value, '%Y-%m-%d')
24          day_abbr = date_obj.weekday()
25          if day_abbr < 6:
26              input_df.iloc[0, day_abbr] = 1
27          if ampm == 'PM':
28              time_hour = float(time_hour + 12)
29          input_df['hour_sin'] = np.sin(2 * np.pi * float(time_hour) / 24)
30          input_df['hour_cos'] = np.cos(2 * np.pi * float(time_hour) / 24)
31          prediction = rfr_model.predict(input_df)
32          return render_template("index.html", date=date_value, time=time_hour, ampm=ampm, pred=round(prediction[0], 3), pic_no=round(prediction[0], 0))
```
First, I imported 3 additional packages (Lines 3-5). Joblib to load in the weights from rfr_model.joblib ⚖️, pandas 🐼 to create an input table for the rfr_model, since we need to feed the ML model data in table format, and numpy for the π value which we use in Lines 27-28.

I load in the weights (Line 9) and create a row of column names for the pandas dataframe (Line 10). After that I create the df with a single row of 8 zeros, one for each of the 8 columns (Line 22). I convert the date_value 📅, which is the date input by the user, from a string to a datetime object (Line 23), before finding out what day of the week it is (Line 24) in index format. 0 stands for Monday, 6 stands for Sunday, and I think you can figure out the rest.

Once again, to avoid multicollinearity, I did not add a column for 'Sunday'. I check if the day index is < 6. If it is, that means its not a Sunday, so I proceed to change the corresponding column value from 0 (❌) to 1 (✅) in Line 26. I also make sure to add an extra 12 hours to the time_value if the time is in 'PM', since the RFR model was trained with 24 hour time 🕒.

i apply sin-cos encoding to the 'time_hour' value 🕒 (Line 29-30), then store the numpy array of predictions in the variable 'prediction' (Line 31).

In Line 30, I render the HTML file 📂 and pass all the relevant variables to it. The new additions are the 'pred' and 'pic_no' arguments. I round the prediction off to 3dp for 'pred' so that the output does not look to messy, and to nearest whole number for 'pic_no' because the jam images in [static/](GAE/static) only represent whole number values from 1-5. 

Notice how I type 'prediction[0]' instead of just 'prediction', thats because the 'prediction' variable itself is a numpy array. To extract the actual integer value, I have to iterate through the array.

Now let's test run this and see how the output looks like. I'll run it with just the prediction value first (Fig 5.5), then if there are no issues I'll include the jam image in the output too 🖼️ (Fig 5.6). You can see how they turned out below.

![](progress_pics/Fig-5.8-output_with_number_vid.gif)

Fig 5.8: Test run with prediction value included

And here it is with the image included 🖼️

![](progress_pics/Fig-5.9-output_with_pic_vid.gif)

Fig 5.9: Test run with both prediction value and jam image included

Looks like the base structure of the website is complete! Now we can finally move on to deploying this thing for real 🚀 on Google App Engine (GAE) so that everyone can use it. This does not mean that the development of the website HTML and CSS will be halted though, I will continue to improve the visuals ✨ and overall performance of the website as inspiration strikes and my skills continue to improve.

**Implementing new joblib 2.0 files**

(Update) If you refer to [Chapter 4.4](#44-feature-selection-testing-in-progress), you will notice that new features have been introduced. A new model joblib file has been created, and that means extra steps to implement it into the webapp. Since the number of columns in a row required by this model is different compared to the first joblib file I made, we will have to make some changes to main.py in GCloud.

#### app.yaml
To run the website on GAE, we need an app.yaml file, as mentioned before when showcasing the project folder structure. We already have one, but its still empty, so let's change that 😎.

```
1  runtime: python312

2  handlers:
3    - url: /static
4      static_dir: static/
5    - url: /.*  
6      script: auto
```
In Line 1, I specify the Python version I'm using, Python 3.12, which is the latest version 🐍 at the time of doing this project.

Afterwards, I specify some handlers. I reference the static/ folder for css files or images in [index.html](GAE/templates/index.html), like so:
```
        <link href="../static/styles.css" rel="stylesheet" media="screen and (min-width:600px)">
```
so I need to let GAE know that href links starting with `/static` are referring to the 'static/' folder 📂 (Line 3-4). In Line 6, I tell GAE to route any request in my website 📢, regardless of POST or GET, to the backend. 'script: auto' (Line 6) tells it to auto detect the backend file, which in our case is main.py 📌.

A very basic app.yaml file, but necessary for GAE to deploy the website publicly 🌐.

Now, all we have to do is type `gcloud app deploy` in the terminal to get the website up and running. You can now use any device to access the website yourself [here!](https://sapient-metrics-436909-v6.appspot.com#1739003720204209127) 🎉.

#### main.py v3

Due to addition of new features and changes to hyperparameter values, it falls on me to create a new 'predict()' function in main.py, one that will extract the new features from the data, as well as change the hyperparameters to their optimal values depending on which side of the road is chosen.

Here is the current 'predict()' function in main.py:

```
def predict():
    date = request.form.get('date')
    if date:
        date_value = request.form.get('date')
        time_hour = request.form.get('hour')
        time24 = time_hour
        ampm = request.form.get('ampm')
        road_to = request.form.get('road_to')
        input_df = pd.DataFrame(np.zeros((1, 8)), columns=cols)
        date_obj = datetime.strptime(date_value, '%Y-%m-%d')
        day_abbr = date_obj.weekday()
        roadfrom = None
        dark_hours = [20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6]
        condition = 'light'
        if day_abbr < 6:
            input_df.iloc[0, day_abbr] = 1
        if ampm == 'PM':
            time24 = float(time_hour) + 12
        if int(time24) in dark_hours:
            condition = 'dark'
        if road_to == 'Johor':
            # rfr_model = rfr_model_jb_2
            rfr_model = rfr_model_jb
            roadfrom = 'Woodlands'
        if road_to == "Woodlands":
            # rfr_model = rfr_model_wdlands_2
            rfr_model = rfr_model_wdlands
            roadfrom = 'Johor'
        input_df['hour_sin'] = np.sin(2 * np.pi * float(time24) / 24)
        input_df['hour_cos'] = np.cos(2 * np.pi * float(time24) / 24)
        prediction = rfr_model.predict(input_df)
        prediction = round(prediction[0], 1)
        needle_angle = prediction * 0.2 * 244 + 233
        pic_no = int(round(prediction, 0))
        if road_to == 'Woodlands':
            folder_name = 'wdlands_pics'
        else:
            folder_name = 'jb_pics'
        pic_name = f'{folder_name}/{pic_no}_{condition}'
        estimated_duration = '5-10 mins'
        if prediction > 4.5:
            estimated_duration = '> 2 hours'
        elif prediction > 3.5:
            estimated_duration = '1-2 hours'
        elif prediction > 2.5:
            estimated_duration = '40-60 mins'
        elif prediction > 1.5:
            estimated_duration = '20-40 mins'
        elif prediction > 0.5:
            estimated_duration = '10-15 mins'
        return render_template("output.html", date=': ' + date_value, time=': ' + time_hour, ampm=ampm, pred=prediction, pic_name=pic_name, needle_angle=needle_angle, road_to=': ' + road_to, roadto = road_to, roadfrom = roadfrom, estimated_duration=estimated_duration)
    else:
        return render_template("indextest.html")
```

There has been a couple of changes since you last saw it in [main.py v2](#mainpy-v2), such as addition of a waiting time prediction, a picture name to choose the right picture to illustrate a rough idea of how crowded the causeway is, as well as a needle angle which shows the severity of the congestion from green to red on a semi-circle meter.

But now we are going to make even more changes. Lets first take a look at the new features added:

```
1    week_value
2    date_sin
3    date_cos
4    day_of_year
5    day_of_year_sin
6    day_of_year_cos
7    sch_hol_period
8    public_hol_period
9    year_quarter_Q1
10   year_quarter_Q2
11   year_quarter_Q3
```

Excluding the original features, we have 11 new features to add, so thats 11 more pieces of data we need to extract from the data. Should be a piece of cake, since we did it [before](python_scripts/feature_engineered_data_prep.py). Now we just need to copy paste to GCloud App Engine, with some minor tweaks.

The following code for each new feature will be slot into the code above, updating the `predict()` function to create main.py v3.

First, we gotta add the new features as columns, so I'll be editing the 'cols' list in the original `predict()` function:

```
cols = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'hour_sin', 'hour_cos', 'week_value', 'date_sin', 'date_cos', 'day_of_year', 'day_of_year_sin', 'day_of_year_cos']
```

I excluded the last 5 features, as they are boolean columns and need to be set up differently, so I'll define the column later on below.

**1) week_value**

For this feature, I'll do a simple counter to see if the date value is > than a certain multiple of 7, up till the number 4.

```
exact_date = int(date_value[-1])
week_no = 1
for m in range(1, 4):
    if exact_date < m * 7:
        break
    else:
        week_no += 1
input_df['week_value'] = week_no
```

**2) date_sin & 3) date_cos**

Quite straightforward, just calculating sin and cosine of exact_date using numpy.

```
date_sined = np.sin(2 * np.pi * exact_date / 31)
date_cosed = np.cos(2 * np.pi * exact_date / 31)
input_df['date_sin'] = date_sined
input_df['date_cos'] = date_cosed
```

**4) day_of_year, 5) day_of_year_sin, & 6) day_of_year_cos**

Similar to date_sin and cos, just apply numpy's sin and cos functions, as well as the datetime package.

```
datetime_object = pd.to_datetime(exact_date, format='%Y-%m-%d')
day_of_year = datetime_object.dayofyear
day_of_year_sined = np.sin(2 * np.pi * exact_date / 365)
day_of_year_cosed = np.cos(2 * np.pi * exact_date / 365)
input_df['day_of_year'] = day_of_year
input_df['day_of_year_sin'] = day_of_year_sined
input_df['day_of_year_cos'] = day_of_year_cosed
```

**7) sch_hol_period & 8) public_hol_period**

I start with defining the holiday periods in lists within a list, then use for loops to check if the datetime object falls within the ranges.

```
sch_hols_periods = [['2024-11-23', '2024-12-31'], ['2025-3-15', '2025-3-23'], ['2025-5-31', '2025-6-29'], ['2025-9-6', '2025-9-14'], ['2025-11-22', '2026-1-1']]
public_hols_periods = [['2025-1-28', '2025-1-31'], ['2025-3-29', '2025-3-31'], ['2025-6-9', '2025-6-12'], ['2025-6-5', '2025-6-8'], ['2025-10-17', '2025-10-20'], ['2025-12-23', '2025-12-26']]

sch_hol_period = False
for sch_period in sch_hols_periods:
    start = pd.to_datetime(sch_period[0])
    end = pd.to_datetime(sch_period[1])
    if datetime_object > start:
        if datetime_object < end:
            sch_hol_period = True
            break

public_hol_period = False
for public_period in public_hols_periods:
    start = pd.to_datetime(public_period[0])
    end = pd.to_datetime(public_period[1])
    if datetime_object > start:
        if datetime_object < end:
            public_hol_period = True
            break

input_df['sch_hol_period'] = sch_hol_period
input_df['public_hol_period'] = public_hol_period
```

**9) year_quarter_Q1, 10) year_quarter_Q2, & 11) year_quarter_Q3**

The last few features to sort out, just a simple case of adding in the 'quarter' columns to the input_df row, then checking the month value to assign the right quarter value to it.

```
input_df['year_quarter_Q1'] = False
input_df['year_quarter_Q2'] = False
input_df['year_quarter_Q3'] = False

month_value = int(date_value[1])
if month_value <= 3:
    input_df['year_quarter_Q1'] = True
elif month_value <= 6:
    input_df['year_quarter_Q2'] = True
elif month_value <= 9:
    input_df['year_quarter_Q3'] = True
```

Lastly, we gotta define a random forest regressor model for both sides of the causeway, with their respective optimal hyperparameters.

For y = y_column_jb,

```
rfr_model_jb = RandomForestRegressor(random_state=0, max_depth=14, n_estimators=30, max_features=12)
rfr_model_jb.fit(trainfinal_df, y_column_jb)
joblib.dump(rfr_model_jb, 'rfr_model_jb_3.joblib')
```

For y = y_column_wdlands,

```
rfr_model_wdlands = RandomForestRegressor(random_state=0, max_depth=16, n_estimators=15, max_features=10)
rfr_model_wdlands.fit(trainfinal_df, y_column_wdlands)
joblib.dump(rfr_model_wdlands, 'rfr_model_wdlands_3.joblib')
```



## Chapter 6 - ResNet Neural Network for Labelling Traffic Images
### 6.1: Prepping Input Data
Last time we tried to automate labelling of input data, it didn't go so hot (see [chapter 2](#21-opencv-and-yolov4) for that). Going at it again, fingers crossed that a ResNet model will do better. 

Also, I've decided to drop the emojis, don't want people thinking this documentation is AI generated.

As we are all should be familiar with by now, the most important part of any ML model is its data. To prep our snaps jpegs, we need to do a few things:

1) collate the image file paths of all the images we will be using, as well as all the manual ratings in the txt files
2) process the images into a format that can be passed into the tensorflow NN model
3) combining the ratings and images into a TF dataset, then and randomizing and train-test splitting

#### Collating data
Simple python for loops and the os package does the trick:

```
folders_no = [7, 30] # 4391 images and rating pairs
snaps_folder_template = rf"C:/Coding/Project-JBridge/GCloud/all_snaps/snaps_"
ratings_file_template = rf"C:/Coding/Project-JBridge/GCloud/rating_"

all_snaps_filepaths = []
to_jb_ratings = []
to_wdlands_ratings = []
```
Defining the range of snaps folder numbers we will be using, the template for the image folder paths and rating.txt file paths, as well as the lists which we will store the filepaths and ratings in.

```
for x in range(folders_no[0], folders_no[1]):
    # sort out snaps first
    snaps_folder_path = snaps_folder_template + str(x)
    print(f'accessing {snaps_folder_path} for snaps...')
    for snap_name in os.listdir(snaps_folder_path):
        snap_path = snaps_folder_path + '/' + snap_name
        print(snap_path)
        all_snaps_filepaths.append(snap_path)
```
Looping through the folder numbers, I attach the number to the end of the folder template to get the full folder path, then use os to loop through the jpeg file names in the folder. For each file name, I combine it with the folder path to get the full image path, then add it to the filepaths list.

```
    # now to sort out ratings
    ratings_file_path = ratings_file_template + str(x) + '.txt'
    print(f'digging thru rating_{x} text file for ratings')
    with open(ratings_file_path, 'r') as f:
        for line in f:
            to_jb_ratings.append(float(line[-3]))
            to_wdlands_ratings.append(float(line[-2]))
```
Same deal with the ratings, except I dont have to use os to loop through lines in a text file. 

I take the second and third last character in each line, which are the ratings for the roads towards Johor and Woodlands respectively. (The last character is actually the newline character, '\n')

#### Process the images files
This part I owe to Claude for telling me what image format and size is expected by the Tensorflow model, as well as providing me the code to carry out this process.

```
# preprocessing function from claude
def load_and_preprocess_image(filename, label):
    # Read image file
    img = tf.io.read_file(filename)
    # Decode image (use decode_jpeg or decode_png as appropriate)
    img = tf.image.decode_jpeg(img, channels=3)
    # Resize to expected input size
    img = tf.image.resize(img, [224, 224])
    # Preprocess for ResNet (normalizes to [-1, 1] range)
    img = resnet50.preprocess_input(img)
    
    return img, label
```

The first 3 steps is probably quite easy to understand, but I'll explain the last one in greater detail.

For every image, they have shades of red, blue and green in each pixel, represented something like this:

img = [[R, G, B], [R, G, B], ...]

The number for each RGB value can range from 0 to 255. But the resnet50 model weights were obtained from training 1.28 million images with RGB values centered around 0, apparently neural networks perform better with inputs normalized around zero.

The `preprocess_input` function does exactly that, subtracting the mean R, G and B values of the 1.29 million dataset (123.68, 116.779, and 103.939 respectively) from all our input images.

```
to_jb_array = np.array(to_jb_ratings, dtype=np.float32)
to_wdlands_array = np.array(to_wdlands_ratings, dtype=np.float32)
```
Lastly, I convert the rating lists into numpy arrays with numpy floats


#### forming the TF dataset
```
target_array = to_jb_array
print(len(all_snaps_filepaths), len(target_array))
full_dataset = Dataset.from_tensor_slices((all_snaps_filepaths, target_array))
full_dataset = full_dataset.map(load_and_preprocess_image, num_parallel_calls=10) # cuz i got 12 cores
full_dataset = full_dataset.shuffle(buffer_size=1000, seed=7)
```

First, I define a variable 'target_array' and assign it to whichever rating array I'm working on, either jb or wdlands.

Then I use the from_tensor_slices function to link the image filepaths and rating floats together in a dataset, before calling the image preprocessing file earlier on the images of the dataset. 

Lastly, I shuffle the dataset a 1000 images at a time to randomize the rating order in the dataset, and set a seed for the shuffling so that its replicable when I shuffle next time.

```
split_number = int(len(target_array) * 0.8)
train_dataset = full_dataset.take(split_number) # cant use [:split_number] cos tf datasets dont support
val_dataset = full_dataset.skip(split_number)
train_dataset = train_dataset.batch(32) # train 32 images at a time, reduces overfitting
val_dataset = val_dataset.batch(32)
```
Can't forget the ol'train test split. This time we are using a 80% train 20% test split. We don't need to do a randomized split like in Chapter 4 because we already shuffled it before.

Thats most of the data prep done, but there is one more thing we can do to potentially improve our model value and reduce noise.

#### Snaps Masking
As you can see in the [snaps folders](gcloud/all_snaps), the images not only contain the road, but they also show the trees, guardrails, the occasional train, as well as the reservoir. These do not contribute to determining the congestion condition and can potentially confuse the model. The water body particularly, as it reflects the lit up buildings in Johor at night.

To remedy this, I took to Canva to try and create a mask for the images.

![Fig 6.1](progress_pics/Fig-6.1-masked_incomplete)

Fig 6.1: Image mask (incomplete)

As you can see, the pixels not consisting of road or congestion are relegated to RGB(0, 0, 0). However, some pixels in the image that make up the cars or road might also be black, so lets make it such that there is only 2 colours in the mask.

![Fig 6.2](progress_pics/Fig-6.2-masked_full)

Fig 6.2: Full image mask

Keep in mind that this is NOT going to be the training data we are passing into the model. This is known as a 'mask'. 

It has the same dimensions as the snaps, and it will essentially tell the model, 'the pixels of me that are black, turn the corresponding pixels on the training image black too. The pixels of me that are white, leave them as is', like so:

```
mask = tf.io.read_file(mask_path)
mask = tf.image.decode_jpeg(mask, channels=3)
mask = tf.image.resize(mask, [224, 224])          
mask = mask / 255.0 # convert 255 in white regions to 1
```

Very similar to the `load_and_preprocess_image` function, except we only have to do this once. Now lets change the function slightly so we can carry out masking and display the masked image using matplotlib.

```
def TEST_load_and_preprocess_image(filename):
    """Load image and preprocess for ResNet"""
    # Read image file
    img = tf.io.read_file(filename)
    # Decode image 
    img = tf.image.decode_jpeg(img, channels=3)
    # Resize to expected input size
    img = tf.image.resize(img, [224, 224])
    
    img_blacked = img * mask
    
    # showing img
    plt.figure(figsize=(8, 8))
    plt.imshow(img_blacked.numpy().astype('uint8'))  # .numpy() is a TensorFlow method
    plt.title("Image with top 5 rows blacked out")
    plt.axis('off')
    plt.show()
```

Lets test out the masking on a random snap and see how it goes. If all goes according to plan, the output should look something like Fig 6.1.

![Fig 6.3](progress_pics/Fig-6.3-snap_after_masking.jpg)

Fig 6.3: Snap after applying mask

Excellent, the masking is perfect. The image quality might be terrible compared to what we are used to, but this is because tensorflow's ResNet50 model only acccept 224x224 pixel images, thats why the quality is so potato. 

While I'm at it, I might as well also try masking the non-target lane as well. Might seem like overkill, but I'll try anything once. In this case, since we are training for jb_rating, I masked the right side of the road.

![Fig 6.4](progress_pics/Fig-6.4-jb_masked_full,jpg)

Fig 6.5: Mask with non-target lane covered as well

And thats data prep done :)

### 6.2: Experimenting With Different Hyperparameters
With the data prepped, all thats left to do is feed it into the model and let it do its thing. For this first test run, I'll be using unmasked training data. The model will be going through 20 epochs (20 iterations of training), and the dropout rate will be 0.4 (40% of neurons in each layer are randomly left out of the training for every epoch).

Here are the results of the 20th epoch:

![Fig 6.5](progress_pics/Fig-6.5-first_resnet_results.jpg)

Fig 6.5: First loss results from resnet model on snaps

Better than I expected for a first try. Then again, this is a model with weights obtained after training for months on millions of pictures, so it would obviously outperform my little yolov8 model. Furthermore, we are detecting 'areas of congestion' here, not 'number of cars' like with yolov8 which is a much harder task.

Taking a look at val_loss = 0.5332 (which in rmse would be 0.5332^0.5 = 0.7302) and val_mae = 0.4663, I'd say automated labelling of snaps is definitely doable.

On its first try, the resnet model is already producing ratings quite close to mine, averaging less than half an arbitrary unit in loss for each rating. Furthermore, the val RMSE, 0.7302, is not much greater than the MAE. RMSE punishes larger losses more severely, so this means there aren't massive individual losses either.

A decent starting point, now lets see if the model can catch even more complex patterns without overfitting. I'm talking about increasing the number of units in the final dense layer from 128 to 256.

#### Number of units in outer dense layer

`    layers.Dense(256, activation='relu'), # increased from 128 to 256 `

I've put the results in a pandas Dataframe to make it easier to compare the results against the 128 unit layer model

![Fig 6.6](progress_pics/Fig-6.6-128_vs_256_neurons_results.jpg)

Fig 6.6: Loss values of model with 256 units in outer dense layer vs 128 units

Comparing them side by side, we can see that the 256 unit model does better, but only in training losses (and marginally in val_mae). Its val_mse is much greater than that of the 128 unit model, probably due to overfitting. 

Now we know to stick with 128 units for the rest of this model.

#### Dropout rate
The dropout rate decides the fraction of units in a layer that 'go to sleep', essentially not participating in the training, for a particular epoch. It adds randomness and reduces likelihood of the model overfitting.

Initially, the value was 0.4. Lets see how the loss values are like with dropout rate set to 0.3:

```
# Epoch 19/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 68s 609ms/step - loss: 0.3950 - mae: 0.3226 - val_loss: 0.3433 - val_mae: 0.3206
# Epoch 20/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 67s 608ms/step - loss: 0.4237 - mae: 0.3403 - val_loss: 0.4001 - val_mae: 0.3835
```

If we compare the 20th epoch results with Fig 6.1, when dropout rate was 0.4, the val_loss (mse) and val_mae decreased from 0.5332 to 0.4001, and 0.4663 to 0.3835, respectively.

This is a huge improvement in validation loss. Additionally, the training loss values are also much closer now, which suggests a more robust model. 

On a side note, while the model is already doing stellar with 20 epochs, could probably do with more, as the decrease in val_loss over epochs does not seem to be slowing down much, even at the end.

I'm inferring this from the best fit line I plotted for the last 12 epochs' mse values when dropout rate = 0.3:

![Fig 6.7](progress_pics/Fig-6.7-val_loss_best_fit_epoch_9_to_20.jpg)

Fig 6.7: Best fit line of val_loss against (epochs - 8)

However, it already takes quite a long time to test each variable with 20 epochs. So for this chapter, I'll be testing each hyperparameter with only 10 epochs, before leaving the testing of best epoch number to last.

Anyway, now let's try dropout rate 0.2:

```
# Epoch 19/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 560ms/step - loss: 0.3483 - mae: 0.3091 - val_loss: 0.3792 - val_mae: 0.3271
# Epoch 20/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 563ms/step - loss: 0.3692 - mae: 0.3205 - val_loss: 0.4184 - val_mae: 0.3587
```

Very similar val loss to when dropout rate = 0.3, just a tad higher. That would not be a problem, if not for the fact that the training loss is so much lower than before. This implies overfitting to training data.

I added the best fit line of val_loss against epoch number for dropout rate = 0.2 next to 0.3, as you can see below.

![Fig 6.8](progress_pics/Fig-6.8-best_fit_dropout_0.2_vs_0.3.jpg)

Fig 6.8: Best fit line for val_loss against (epoch-8) for dropout rates 0.2 (red) and 0.3 (purple).

I removed an outlier at epoch 13 (0.8, abnormally high) and replaced it with a much lower value, yet the red line still hovers above the purple, showing a higher mean val_loss.

After experimenting, I conclude, based on my 1 billion iq brain thinking, that we should go with a dropout rate of 0.3 moving forward.

#### Managing Skew
This next part is not exactly hyperparameter tuning, but it might make a small improvement to our model loss. Only one way to find out.

From the countless hours I have spent labelling the snaps, I know that the proportion of snaps of ratings 0 and 5 are much greater than that of those with ratings 1 to 4. To confirm this, lets see the distribution of ratings across the snaps.

```
unique, counts = np.unique(to_jb_array, return_counts=True)
for rating, count in zip(unique, counts):
    print(f"{rating}: {count} images")
```

I use np.unique to get all the unique ratings (0, 1, 2, 4, and 5) as well as their counts, then zip them and use a for loop and print each unique label and its respective count. I do this for the to_jb_array first, then to_wdlands_array.

Here are the results for jb (left) and wdlands (right):

 0: 3461 images, 2479 images
 1: 108 images, 227 images
 2: 79 images, 177 images
 3: 99 images, 211 images
 4: 98 images, 323 images
 5: 546 images, 974 images

As you can see, the count for ratings 0 and 5 are much greater than the rest for both sides of the road. to_jb_array has more rating 0s, while to_wdlands_array has more ratings 5s.

So my plan for the next training is to assign greater weights to snaps of the underepresented ratings, then train again with the most recent optimum hyperparameter values and see the results.

It was to my understanding that the greater the weight, the more emphasis the model will put on snaps of that rating during training. While that is true, I also did not know that the weighted average had to equal to 1 (roughly). So I can't just take 1/count, I have to multiply by a constant as well, scaling_factor. 

```
scaling_factor = 731.83 # 4391/6
custom_weights = {}

# to see snaps rating distribution (do for to_wdlands as well) AND making weights
unique, counts = np.unique(to_jb_array, return_counts=True)
for rating, count in zip(unique, counts):
    weight = scaling_factor/count
    custom_weights[int(rating)] = float(weight)
    print(f"{rating}: {count}")

...
...

# Training
results = full_regression_model.fit(
    train_dataset,
    validation_data = val_dataset,
    epochs = 12, # switching to 12 epochs instead, 20 takes way too long
    class_weight = custom_weights
)

```

As the distribution code already loops through the rating counts, I used it to make the weight dictionary as well. The only extra code added is the weight scaling formula and adding the calculated weights into the weight dictionary, custom_weights. Then I add the dict to the model for training. Now we wait for the results.

```
Epoch 10/12
110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 560ms/step - loss: 1.0154 - mae: 0.9155 - val_loss: 1.8310 - val_mae: 0.9922
Epoch 11/12
110/110 ━━━━━━━━━━━━━━━━━━━━ 160s 1s/step - loss: 1.0843 - mae: 0.8648 - val_loss: 1.8250 - val_mae: 1.0388
Epoch 12/12
110/110 ━━━━━━━━━━━━━━━━━━━━ 71s 633ms/step - loss: 1.0308 - mae: 0.8307 - val_loss: 1.0805 - val_mae: 0.8338
```

Damn, the model is doing terribly, like really bad. Loss and MAE are more than doubled as compared to without weights, for both training and validation. Even if its only 12 epochs, the model was doing much better at epoch 12 without weights.

I'm not an expert, but I think this could be due to the fact that my validation dataset has roughly the same ratings distribution as the training dataset, and so the disproportional distribution of data is actually an advantage. 

As this model is not to predict ratings and is solely to rate snaps, since my snaps naturally skew towards 0 and 5 (might be cuz each snap is taken 1 hour apart), I will not be implementing custom weights. For now...

#### Learning Rate

Next we will be changing the learning rate, which basically decides how extreme the changes in weight are after each epoch when trying to adapt to the loss metrics.

```
full_regression_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), # optimizer decides how model weights are updated during trng, have no idea how it works
    loss='mse',  # Mean Squared Error
    metrics=['mae']  # Mean Absolute Error
)
```

I was looking at Fig 6.3, which showcases the best model performance so far (128 units in dense layer and 0.3 dropout). While the loss gradient is negative and loss is definitely decreasing, the loss keeps jumping up, then going down, then up again, as epochs progress. This leads me to believe that the model can converge better with smaller steps at higher epochs.

I'll only be testing values lower than our current LR, 0.001, as increasing it only saves time and compute but often times does not improve model performance and loss, starting with 0.008.

```
Epoch 18/20
110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 558ms/step - loss: 0.3622 - mae: 0.3200 - val_loss: 0.4629 - val_mae: 0.3610
Epoch 19/20
110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 556ms/step - loss: 0.3799 - mae: 0.3256 - val_loss: 0.3533 - val_mae: 0.3517
Epoch 20/20
110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 559ms/step - loss: 0.3889 - mae: 0.3361 - val_loss: 0.3843 - val_mae: 0.3487
```

Better than when LR = 0.001. Lets see how the best fit lines of their last 12 epochs' MSE compare.

![Fig 6.9](progress_pics/Fig-6.9-best_fit_LR_0.001_vs_0.0008.jpg)

Fig 6.9: LR = 0.001 vs LR = 0.0008

The results and best fit lines are very similar, so the small LR is not underfitting. I know that with enough epochs, the smaller LR model will always triumph. 

Because I don't want my laptop to explode, I'll try one last LR value, 0.0005. and plot the losses of the last 12 epochs so we can better compare with LR = 0.0008.

```
Epoch 18/20
110/110 ━━━━━━━━━━━━━━━━━━━━ 273s 2s/step - loss: 0.3328 - mae: 0.3102 - val_loss: 0.4165 - val_mae: 0.3572
Epoch 19/20
110/110 ━━━━━━━━━━━━━━━━━━━━ 235s 2s/step - loss: 0.3751 - mae: 0.3301 - val_loss: 0.3289 - val_mae: 0.3290
Epoch 20/20
110/110 ━━━━━━━━━━━━━━━━━━━━ 273s 2s/step - loss: 0.3322 - mae: 0.3161 - val_loss: 0.3896 - val_mae: 0.3410
```

![Fig 6.10](progress_pics/Fig-6.10-best_fit_LR_0.0008_vs_0.0005.jpg)

Fig 6.10: LR = 0.0008 vs LR = 0.0005

It still looks like decreasing the LR decreases val_loss further, with the difference in loss between LR = 0.0008 and LR = 0.0005 potentially increasing as epoch number increases.

Perhaps the next thing to do now would be to test even lower LR values, like 0.0003, but I think I'll stick with 0.0005, as I dont want to need to implement too many epochs for the model to converge to the optimal weights. Too much compute. I may come back in the future to try a lower LR, but for now lets move on to the next hyperparameter, batch size.

#### Batch Size
The batch size is exactly what it sounds like - how many images the model is trained on at a time before updating its weights. Too great a value and you risk underfitting, while too small a value can lead to overfitting. 

As of now, the batch size we have been using thus far is 32. Looking at the losses from the past training results, the difference between training and validation losses is not high. This means overfitting is not a problem yet.

Lets try and go as close to overfitting as possible, without actually overfitting, by halving batch size to 16.

```
Epoch 18/20
220/220 ━━━━━━━━━━━━━━━━━━━━ 70s 314ms/step - loss: 0.3805 - mae: 0.3334 - val_loss: 0.4920 - val_mae: 0.3846
Epoch 19/20
220/220 ━━━━━━━━━━━━━━━━━━━━ 62s 280ms/step - loss: 0.4554 - mae: 0.3608 - val_loss: 0.3585 - val_mae: 0.3096
Epoch 20/20
220/220 ━━━━━━━━━━━━━━━━━━━━ 62s 280ms/step - loss: 0.4139 - mae: 0.3406 - val_loss: 0.4001 - val_mae: 0.3390
```

Thats really good, our best validation MAE so far. The val_loss (MSE) is slightly higher than the best score we have achieved. I may test this batch size value out at higher epochs.

Out of curiosity, what if we try increasing it to 64?

```
Epoch 18/20
55/55 ━━━━━━━━━━━━━━━━━━━━ 64s 1s/step - loss: 0.3669 - mae: 0.3405 - val_loss: 0.4732 - val_mae: 0.4189
Epoch 19/20
55/55 ━━━━━━━━━━━━━━━━━━━━ 64s 1s/step - loss: 0.3717 - mae: 0.3471 - val_loss: 0.4135 - val_mae: 0.3855
Epoch 20/20
55/55 ━━━━━━━━━━━━━━━━━━━━ 64s 1s/step - loss: 0.3554 - mae: 0.3372 - val_loss: 0.5269 - val_mae: 0.3896
```

Its training loss is very low but validation loss is higher than ever. I thought larger batch sizes were supposed to generalize better and overfit less. Odd...

Either way, looks like batch_size 32 is the best option. Slightly annoyed that I spent all that time just to arrive at that conclusion.

Regarding the results from when batch size = 16, while the smaller batch size model indeed does worse, my guess is that the model is learning more noise due to the small batch size, essentially 'fitting' to the noise. Hence making it perform worse than batch_size = 32 in training, even though its supposed to fit closer and potentially even overfit to training data.

So my thinking is, with the masked snaps, theres less noise in the image, which might allow the model to fit closer without learning too much noise. To check this, I'll be comparing batch_size = 32 and 16 again, but this time while training on the masked training data. The other hyperparameter values will be the optimal values we have found out so far in this subchapter.

First time training with the masked images, I'm quite excited.

When batch size = 32:

```
Epoch 18/20
110/110 ━━━━━━━━━━━━━━━━━━━━ 66s 595ms/step - loss: 0.3650 - mae: 0.3370 - val_loss: 0.3988 - val_mae: 0.3428
Epoch 19/20
110/110 ━━━━━━━━━━━━━━━━━━━━ 66s 592ms/step - loss: 0.3422 - mae: 0.3105 - val_loss: 0.4045 - val_mae: 0.3250
Epoch 20/20
110/110 ━━━━━━━━━━━━━━━━━━━━ 66s 594ms/step - loss: 0.3845 - mae: 0.3349 - val_loss: 0.4229 - val_mae: 0.3515
```

Slightly worse than unmasked with same hyperparam values. By the way, you can see most of the results from the 20th epoch for each test [here](rating_w_resnet/rn_results_unblacked).

I believe in the potential of the masked snaps, I'm not giving up that easily. 

Lets try using them again with batch size = 16:

```
Epoch 18/20
220/220 ━━━━━━━━━━━━━━━━━━━━ 62s 279ms/step - loss: 0.3818 - mae: 0.3349 - val_loss: 0.6140 - val_mae: 0.3897
Epoch 19/20
220/220 ━━━━━━━━━━━━━━━━━━━━ 62s 281ms/step - loss: 0.3869 - mae: 0.3248 - val_loss: 0.3349 - val_mae: 0.3352
Epoch 20/20
220/220 ━━━━━━━━━━━━━━━━━━━━ 62s 278ms/step - loss: 0.4157 - mae: 0.3451 - val_loss: 0.4010 - val_mae: 0.3593
```

Very similar but still slightly off our best score, which was achieved with unmasked data and batch size = 16. Looks like the resnet model learnt that the pixels outside the road dont affect the congestion rating, which shows how good it is.

These 2 configurations (masked AND unmasked + bs = 16) are quite good, so I'll be keeping them around for testing with higher epochs later on. The masked model is currently behind, but who knows it might converge better as epochs increase.

Lets go again with batch_size = 16, but this time with mask v2 (covering non-target lane) and see if it does any better than its predecessor.

```
Epoch 18/20
220/220 ━━━━━━━━━━━━━━━━━━━━ 66s 298ms/step - loss: 0.4020 - mae: 0.3419 - val_loss: 0.4700 - val_mae: 0.3421
Epoch 19/20
220/220 ━━━━━━━━━━━━━━━━━━━━ 64s 288ms/step - loss: 0.3813 - mae: 0.3220 - val_loss: 0.3672 - val_mae: 0.3244
Epoch 20/20
220/220 ━━━━━━━━━━━━━━━━━━━━ 64s 289ms/step - loss: 0.4002 - mae: 0.3429 - val_loss: 0.4012 - val_mae: 0.3731
```
The last epoch is average, but look at epoch 19. The best validation losses we have seen in Chapter 6 so far. Will be training with mask v2 on images moving forward.

One last test, I'll be trying batch_size = 8. I'll be back with the results tomorrow, the desktop fan is making some disturbing noises now after the last training.

```
Epoch 18/20
439/439 ━━━━━━━━━━━━━━━━━━━━ 66s 149ms/step - loss: 0.4437 - mae: 0.3649 - val_loss: 0.3800 - val_mae: 0.3478
Epoch 19/20
439/439 ━━━━━━━━━━━━━━━━━━━━ 67s 150ms/step - loss: 0.4071 - mae: 0.3380 - val_loss: 0.3784 - val_mae: 0.3570
Epoch 20/20
439/439 ━━━━━━━━━━━━━━━━━━━━ 75s 170ms/step - loss: 0.4318 - mae: 0.3554 - val_loss: 0.4554 - val_mae: 0.3638
```

Similar to when batch_size = 16, but batch size 8 takes a longer time to train, so I'll stick to 16 as the optimal value.

#### Unfreezing base model
Before, only the outer dense layer we created on top of the base model was being trained. `base_model.trainable = True` allows the base layer weights to be trained and updated as well.

In my eyes, this could go either way. The base model weights could pick up useful patterns in the snaps and improve, or the already good resnet weights could learn useless noise from the snaps and get worse.

Compared to resnet50s training data, ours is not exactly as high quality. Each car makes up a very small fraction of the pixels, and traffic congestion states can look very different despite having the same rating.

As a baseline, I'll use the unmasked data first, with batch_size = 16 together with the trainable base layers option set to TRUE.

```
Epoch 10/20
220/220 ━━━━━━━━━━━━━━━━━━━━ 694s 3s/step - loss: 0.1466 - mae: 0.1694 - val_loss: 0.0549 - val_mae: 0.1051
Epoch 11/20
220/220 ━━━━━━━━━━━━━━━━━━━━ 424s 2s/step - loss: 0.1212 - mae: 0.1556 - val_loss: 0.1321 - val_mae: 0.1852
Epoch 12/20
220/220 ━━━━━━━━━━━━━━━━━━━━ 237s 1s/step - loss: 0.1556 - mae: 0.1755 - val_loss: 0.2274 - val_mae: 0.2125
```

GSYDFGWFGEYWIFGUERSG

Before we apply mask v2 to the training data, I will try using the unmasked data again, but this time with batch_size = 8. Don't wanna leave any stones unturned. 

For time's sake, I'll set epochs = 12 only.

```
Epoch 10/20
439/439 ━━━━━━━━━━━━━━━━━━━━ 227s 516ms/step - loss: 0.1480 - mae: 0.1748 - val_loss: 0.2113 - val_mae: 0.1972
Epoch 11/20
439/439 ━━━━━━━━━━━━━━━━━━━━ 229s 520ms/step - loss: 0.1762 - mae: 0.1961 - val_loss: 0.0549 - val_mae: 0.0920
Epoch 12/20
439/439 ━━━━━━━━━━━━━━━━━━━━ 230s 523ms/step - loss: 0.1617 - mae: 0.1785 - val_loss: 0.0712 - val_mae: 0.1155
```
Both batch size 8 and 16 were able to achieve new validation loss lows, so I'll again be sticking to bs = 16 for time and compute sake. 

Now lets see how training with mask v2, bs = 16, and trainable base layers does:

```
Epoch 10/12
220/220 ━━━━━━━━━━━━━━━━━━━━ 235s 1s/step - loss: 0.1793 - mae: 0.2085 - val_loss: 0.3622 - val_mae: 0.3316
Epoch 11/12
220/220 ━━━━━━━━━━━━━━━━━━━━ 235s 1s/step - loss: 0.2589 - mae: 0.2340 - val_loss: 0.1191 - val_mae: 0.2008
Epoch 12/12
220/220 ━━━━━━━━━━━━━━━━━━━━ 236s 1s/step - loss: 0.2273 - mae: 0.2250 - val_loss: 3.0835 - val_mae: 1.4428
```

Decent validation losses on the second last epoch but just not enough to best the unmasked training, also what the balls is going on in epoch 12 I have no idea.

Its sad, but it looks like I'll have to abandon the masks. Although I'm still confused as to how showing the reservoir and the other side of the bridge can influence loss values so much. 

Overfitting is a suspect, but the unmasked snaps also have the same pixels as the masked, so that doesnt make sense to me. 

If you guys have an inkling, do telegram me.

#### Optimizing Hyperparameter Mix 
So far, we have determined the optimal values for the following hyperparameters:

- outer dense layer unit number: 128 units
- dropout rate = 0.3
- learning rate: 0.005
- batch size: 16
- trainable base model: True

Call me kiasu, but while these values proved to be the best when tested alone, a different combination of hyperparameter values might do better.

For example, when testing dense layer unit numbers, 128 did the best. But that was when dropout rate had not been optimized from 0.4 to 0.3. Who knows, a higher unit number might do better with a lower dropout rate. 

This is just an example, I have 1 or 2 real suspicions which I will discuss below.

1) Learning rate not low enough after I set trainable base model to True. 

After quickly converging and getting stellar val_MAE of 0.12 and 0.15 in epoch 3 and 4, the loss kept hovering around the same minimum for the rest of the epochs. You can see for yourself in lines 303 to 327 [here](full_epoch_losses.txt)

I have a feeling that with a lower learning rate combined with trainable base layers, the weights can converge better and reduce loss further. Lets test this with a lower learning rate of 0.00036.

```
Epoch 10/12
220/220 ━━━━━━━━━━━━━━━━━━━━ 242s 1s/step - loss: 0.1615 - mae: 0.1795 - val_loss: 0.0724 - val_mae: 0.1367
Epoch 11/12
220/220 ━━━━━━━━━━━━━━━━━━━━ 235s 1s/step - loss: 0.1242 - mae: 0.1609 - val_loss: 0.0871 - val_mae: 0.1434
Epoch 12/12
220/220 ━━━━━━━━━━━━━━━━━━━━ 235s 1s/step - loss: 0.1205 - mae: 0.1560 - val_loss: 0.0498 - val_mae: 0.1136
```