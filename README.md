During the summer of 2018, I travelled to Cambridge to intern at the [Berkman Klein Center for Internet and Society](http://cyber.harvard.edu/getinvolved/internships_summer) at Harvard Law School. Out of the many organizations and projects at the Berkman Klein Center "dedicated to exploring, understanding, and shaping the way we use technology," I worked at the [Library Innovation Lab](https://lil.law.harvard.edu/). At the Library Innovation Lab, which work focuses on the intersection of libraries, technology, and law, my manager gave me the opportunity to "build something cool." I took on the creation of a project from start to finish, which you can read about here.

My project idea started with my interest in storytelling and retelling. I had a few big questions: What can we learn about the spread of (mis)information from how people remember and retell stories? What is the importance of oral storytelling? How can we use oral story retelling to build empathy? What is my moral responsibility as a creator? 

What started as a wide range of ideas, evolved into a full-functioning art piece. With the guidance of my coworkers, I brought ideas through an iterative design process, which resulted in my project: an interactive storytelling device called Redial. In order to create Redial, I rewired a rotary phone to a Raspberry Pi, wrote Python code to control the interaction with the phone, and built the basics of a related website in R Shiny. You can view all my commented code on this Github. 

If you are interested in my project so far, please read on to see what I learned!


![Redial](https://github.com/jdegrootlutzner/redial/blob/master/images/slide-jpgs/intro.jpg)
 

![Motivation](https://github.com/jdegrootlutzner/redial/blob/master/images/slide-jpgs/motivation.jpg)

Oral storytelling is powerful. From early days in human evolution, the process of gathering around campfires and sharing stories allowed our ancestors to pass on valuable information. 

Oral storytelling is intimate. During gatherings with friends and families we sit, eat, and talk. We share stories about our low and high moments.

Oral storytelling is personal. The emotion behind an orator's words makes their story more relatable. 

I brainstormed ideas about how to capture the value of oral storytelling. In order to see if the idea of studying the oral retelling of stories, I tested out playing the Telephone Game with different types of stories. I tried different length stories, different perspectives, and different tones. I explored different forms of stories, including jokes, music, and instructions. If I changed key characteristics about the identity of the characters in the story, would they remember the story differently? I recorded the iterations of the retellings and analyzed how they changed over time. The idea seemed promising. 

I became most interested in the idea of trying to build empathy through storytelling and I moved on to explore the best user interaction to achieve this goal.

 
![Concept](https://github.com/jdegrootlutzner/redial/blob/master/images/slide-jpgs/concept.jpg)

After brainstorming and testing a few ideas out, I decided to create a physical device that people could house story retellings. The idea was this: People would come up to a phone, dial a number from 1 to 9 to listen to a unique first-person story, and then retell the story back into the phone while maintaining the first-person perspective. People could also dial the operator to hear more about the concept or tell their own story.

The phone would function like the Telephone Game in which the story changes over time. My goal was to be able to save all of the iterations of the story, analyze the changes, and make the story iterations viewable on a website so that users could see how their story changed overtime. I liked the idea of the physicality of the phone because it requires people to physically present. Much like a fire, people have to be physically present to hear the stories and I hoped this would create more emotional involvement as well.

I began the process of creating the phone.

![Construction](https://github.com/jdegrootlutzner/redial/blob/master/images/slide-jpgs/construction.jpg)

To make this physical instillation, I rewired a rotary phone to a small, low-cost computer called a Raspberry Pi. The Raspberry Pi has a number of "pins" (as shown on the right side of the photo of the computer chip above), which allowed me to attach the wiring from the phone. The pins read input and send output from and to the phone. Although I have a computer science background, I had not worked with hardware before this project and the process had a steep learning curve. 
 
![Website](https://github.com/jdegrootlutzner/redial/blob/master/images/slide-jpgs/website.jpg)

Above is a prototype for the website for Redial. On the left the user can listen to the recordings, and on the right the user can find the transcriptions of the stories. I used the Google Speech to Text API to transcribe the recordings. 

The story showcased above is one of the more comical stories I tested out. The green highlighted text is the original story, which is about going on a date with a guy who eats the raw meat at a Korean barbecue restaurant. I like this story because although the original story has a few specifics, a bad date is still a relatable experience. I imagined that the experience would be interesting for the listener because they do not know whose story it was originally. However, as you can see, the story quickly devolved! This made me change my thinking.

![Feedback](https://github.com/jdegrootlutzner/redial/blob/master/images/slide-jpgs/feedback.jpg)

I found a few different observations that helped me make Redial more effective. 

For one, I changed the process so that the story would stay stagnant. I found that the story changed too much when . Occasionally, people would leave the phone part way through without finishing the story, or one person would change the story completely. One bad actor could destroy the whole lineage of stories. This might be interesting for a separate research project but I wanted my installation to focus on building empathy. 

I also found that people were happy to tell a long story, but had a limit on how long they would listen. The ideal length for listening was under 30 seconds because after that time people would lose interest. However, sometimes people would tell stories way longer than two minutes.

Overall, I found the project to be a success. In the future, I would like to finish the website and examine user interaction when their is a website involved. I would also like to test out this idea in different spaces. Perhaps in abandoned street telephones.

I would like to thank everyone at the Library Innovation Lab and at the Berkman Klein Center for their help and participation in the project. Thank you Anastasia for the help with the hardware! I learned a lot this summer and had a lot of fun.

Thank you for taking the time to read this. If you have any questions or are interested in continuing this project, please reach out to me by email below.


![Thank You!](https://github.com/jdegrootlutzner/redial/blob/master/images/slide-jpgs/thank-you.jpg)
