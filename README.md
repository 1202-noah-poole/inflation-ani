# Minimum Wage Animation

Main purpose of the project was to create an animation using the matplotlib animation class. I decided to create an animation of the change in minimum wage over time, both the actual dollar amount as well as the adjusted-for-inflation amount. I got the minimum wage data from the Department of Labor, in which I just manually created a dictionary for the data, and I got the inflation data from the Bureau of Labor Statistics. The cleanup was essentially just calculating the actual inflation numbers, and then getting it all properly formatted in a data frame that I could use for the graph. 

Creating the actual animation wasn't too difficult. I had used matplotlib before so most of what I was doing was familiar. The animation aspect was a little tricky to get but in the end it wasn't as difficult as it needed to be. Although practically speaking animated graphs are often not the best way to visualize information, especially with how long Python takes to do anything, it was still fun to do and overall I'm pleased with how it turned out.

Here's the resulting graph:

.

![inflation animation](https://user-images.githubusercontent.com/89417792/210717267-aad3fa90-6ca3-4bc5-9e27-43ea94be571e.gif)

