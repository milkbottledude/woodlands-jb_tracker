TLDR, heres the outline of what will be done in this project.

Stage 1: Testing to see if selenium can enter the LTA woodlands causeway website. If yes, we will try to extract the jpeg link of the woodlands checkpoint at that point in time, then download it and save it in my laptop using requests. This will all be done using PyCharm.

Stage 2: We will now be moving on to the machine learning part of the project. Using the few jpegs of the woodlands causeway bridge that were downloaded, I will attempt to use Keras, YOLO(You only look once), TensorFlow, or Pytorch to make a machine learning model that can count the number of cars on the bridge.

Stage 3: I will pick the most suitable and convenient machine learning frameworks out of those mentioned above, and utilise it in the rest of my project. Now we will be attempting to automate this whole process, from starting the code for selenium to scrape the website, all the way to counting the number of cars and saving the number in a csv file. To automate all of this, i will be using Google Cloud Run, because my broke ass cannot afford AWS. It is simply a matter of moving all the code in PyCharm to Google Cloud's code editor and editing the code to ensure it works in Google Cloud's CLoud Run.

Stage 4: After quantifying the crowdedness data of the bridge for different days and different time of days, we can visualise this data through the use of bar graphs to try and identify any patterns or relationships, as well as any hidden factors that may influence the number of cars on the bridge. 
If time permits, i will also use machine learning methods to identify patterns that i could not identify myself, either through simple linear models from sklearn or more complex models such as neural networks from TensorFlow. I will probably use the latter.


Hello guys, been a while since i updated the README, there have been some big changes. Due to the not so sharp quality of the snapshots from the LTA live cameras, it is near impossible for YOLO to learn what pixels constitute a car with so little pixels to play with.
So instead of trying to identify individual cars, i will be getting YOLO to try and learn to identify areas of congestion/traffic jam. The area of concern is larger and that gives YOLO more pixels to work with. 

As you can see from the commit messages, the model is not learning congestion areas well, but it is certainly performing better than when it tried to identify individual cars. It was able to identify a small fraction of congestion (Fig smth). That was with about 100 training images.
YOLO should require about 1000 images to really have a good sensing of what pixels make up a traffic jam. Currently i only have 200 manually labelled images, so in the meantime i will try and identify any relationships between the traffic jams and the date and time of the picture, using both manual and machine learning means.

The plan is to calculate the total area of the purple squares, which represent the amount of traffic congestion, and make that the dependent variable. Independent variables would be things like
- day (Sunday, Tuesday, etc), 
- time of day (perhaps more people like to cross over to Johor at night compared to morning)
- season (is it festive season? Is it christmas week, is it the day before Deepavali?)

The goal is to use these indicators to justify the dependent variable, which will also hopefully allow us to more or less predict the state of the bridge on a future date and time.

However, you may be wondering: there are 2 lanes, how do we determine whether the jam is on the road towards Johor, or towards Woodlands? If we use all 100 of our labelled images and plot the centres of the purple boxes representing areas of jam, you can see a distinct separation between the coordinates representing jam on one road and jam on the other (Fig 2 distinct coord grps).
To distinguish whether a jam is on one road or the other, we can plot a line on the plot and simply see whether the coordinate lies below or under the line (Fig smth with line). I used agaration to get the formula of the line u see in the graph, -0.94x + 1.18. However, you may see that there is a small problem with a straight line graph.

As you can see above (Fig orange line), there are some coordinates that belong to the top lane but are sneaking below the separating line, which could lead the machine learning model to think that the area of congestion is on the wrong road. To fix this, we could either ignore all points to the left of the orange line, or use a curved line. 

I might try experimenting further later to get a better line with a curved top that better separates the lanes, but for now we will simply ignore all points with x values smaller than that of the orange line, which has the formula 'x = 0.28'. 

P.S: The reason why the jam coords may not line up as you can see below (Fig side by side), thats because the coordinates from YOLO are in normalized format, where (0, 0) is at the top left of the image while (1, 1) is at the bottom right. 
Contrary to that, matplotlib plots their graph in a format more easy on the eye for you and I, with (0, 0) being at the bottom left and (1, 1) at the top right.

