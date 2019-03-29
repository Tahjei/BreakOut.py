# Breakout
For the second half of the semester, we will be recreating the classic Atari game, Breakout.

![Breakout](/docs/img/breakout.jpg)

## Purpose
Labs 10-14 will constitute the remainder of the semester and will involve the development of the classic Atari game Breakout.
Lab 9 was an introduction to working in real-time environments.
Now that you have had time to play with and experiments with developed code, it is time to start writing it yourself.

That being said, these labs serve 3 main purposes:
* Giving you exposure to larger codebases (similar to the first incremental project).
* Working with and achieving __milestones__ (you may already be familiar with this if you've taken ENGR 121).
* Working as part of a team to achieve success in coding.
 
> __PAIRED PROGRAMMING:__ We will be implementing paired programming in a similar fashion as the previous half of the semester.
Working as part of a group always presents a new set of challenges due to the differences and opinions of others.
I encourage everyone to treat this project as an opportunity to improve collaborating with others (even if you are already an excellent programmer).
Always keep in mind that companies are looking for individuals who can work well with a team, this is true across every discipline.

>__TAKE AWAY:__ At the end of the semester, you should have something that you would be proud to show off to your friends and family.
You may also be able to add this project as part of your resume when you're looking for internships.

## Schedule
In order to better help you succeed at this project, we have divided it into 5 parts.
Each part will consist of a 1-Week lab, and will have milestones that you will be required to meet.
The last lab of the semester will not be a work lab, but instead a time to present what you've achieved.

> __NOTE:__ This schedule and milestones of _future labs_ are subject to changes depending on the status of most groups.

* __Lab 10 - Inheritance__
  * This lab will focus on implementing game objects as the children of PyGame Sprites.
  * This lab will have you create all objects and multiple, different bricks.
* __Lab 11 - Real-time programming II__
  * This lab will focus on working in the update loop.
  * Unlike lab 9, there will be a larger emphasis on debugging movement code and fixing issues related to real-time systems.
  * In this lab you should also begin to track items such as lives and levels.
* __Lab 12 - Binary File I/O__
  * This lab will focus on using File I/O to store gamedata and allow a game to be saved.
* __Lab 13 - Integration__
  * This lab is designed to give you a week to add your own touches to the game.
  * Ideas will be given, but feel free to add whatever you want to the game.
  * This lab will offer you an opportunity to catch up if you have fallen behind.
* __Lab 14 - Presentations__
  * This week will consist of the end-of-semester "Super" quiz.
  * You will present your projects in 5 minute time slots.

>__NOTE: EVEN THOUGH THE ENTIRETY OF THE PROJECT WILL BE GIVEN IN WEEK 10, WE STRONGLY DISCOURAGE TEAMS FROM GOING AHEAD.
IF YOU AND YOUR PARTNER CHOOSE TO WORK AHEAD, PLEASE WORK TOGETHER, ANY CODE WHICH WAS NOT WORKED ON JOINTLY WILL NOT RECEIVE PARTICIPATION CREDIT.__

### Grading Overview
* 100 points | Week 10 Milestones (graded on Week 11)
* 100 points | Week 11 Milestones (graded on Week 12)
* 100 points | Week 12 Milestones (graded on Week 13)
* 100 points | Week 13 Milestones (graded on Week 14, as part of the presentation)
* 100 points | Week 14 Presentation
* 300 points | Final Project Submission (due `4/26/2019 at 11:59 pm`)

All weeks will count the same as a normal lab (100 points).
The final presentation will also count as a normal lab grade.
The final project submission will be due during finals week and will give you an opportunity to reclaim points if you've missed some milestones.

## Project Updates
Because this project is subject to change throughout the semester, the instructors may release a manual change from time to time.
Because we are using git to distribute this project, fetching changes is very simple.

```
git remote -v
```
This command will print out your origin and upstream repos.
Origin is the repository that you push to and upstream is an ancestor repository that you can fetch from.
```
git remote add upstream https://gitlab.pcs.cnu.edu/cpsc250-<instructor's last name>-<crn>-s19/cpsc250l-breakout-s19.git
```
This command is used to add the original repo as an ancestor repository you can fetch changes from, only run this command if the `git remmote -v` only returns an origin repo.

```
git fetch --all
```
This command will synchronize the repositories by fetching changes between them.
This effectively pulls the changes from the upstream repo.

```
git merge upstream/<branch name> --no-commit
```
Merges the changes from the ancestor repo.
The branch name will be given to you when you need to update.

```
git add --all
git commit -m "<Message>"
git push origin master
```
Add, commit, and push the changes to your remote repo (origin).

## Academic Integrity
Before beginning the project, I want to take the time to remind everyone that the CNU Honor Code applies to this lab course and this project.
Cheating under any circumstances will not be tolerated, and will result in a grade of a 0 and a report to CHECS.

### Cheating
This project will be more complex than projects given in the past, and will offer opportunities for students to write very diverse code.
With this in mind, code between groups should be very different.
Spotting copied code will be very easy with this project, please do not even attempt to copy code without documenting it.

### Collaboration & Empty Hands
Understanding this, I want groups to be successful.
To that end, I understand that sometimes a helping hand is needed.
You may work with individuals outside of your group, so long as you follow the empty hands policy (see the lab syllabus).
That is, you discuss ideas and concepts with other, but do not take anything away from the meeting (i.e. If you draw ideas on a whiteboard, the whiteboard should be erased, and you should not have taken notes from it).
Additionally, I expect all parties involved to cite their collaboration sessions as part of their code.
If I see similar code, I can excuse it more easily if satisficing documentation is provided. 

### Online Resources
Breakout is a classic game that many other schools may also use as introductory level projects.
Due to this, there will undoubtedly be repositories that contain complete or nearly complete solutions.
Please resist the urge to copy solutions from online.
You will find great satisfaction in getting your project to work by yourself.
If you copy from someone else, you will not get the same satisfaction; in essence, you will be cheating yourself out of the reward for coding.

If for some reason find yourself disobeying the above advice, please cite where your got your code from.
Failure to do so will be considered plagiarism, and will be treated the same as if you copied code from another student in class.
Please do not take a complete solution from online, I cannot give you credit for it even, if it is cited.
If you are stuck in a spot and need a nudge in the right direction, you may copy code snippets from online (e.g. GitHub, StackOverflow).
So long as you cite them, I will only take off a few points per instance.

# Lab 10 - Inheritance
This lab will be based on utilizing inheritance to help facilitate creating game objects.

__Why should we use inheritance?__
If you remember from lecture, child objects inherit attributes and functions from their parents.
In the case of PyGame and game development in general, a lot of work is required to setup a valid game object.
Fortunately, PyGame comes equipped with the `Sprite` class in the `sprite` module (`pygame.sprite.Sprite`).
This sprite object is a template that is already setup to work seamlessly in PyGame.

## Understanding Sprites

All sprites are composed of 2 primary elements, an image (which is what is seen on screen), and a collision field (which is used to determine the bounds of an object).
By separating these 2 elements, you gain increased control over the physics in the game environment.

The important object to take note of in this relationship is the bounding box, which is a nested class called `pygame.Rect`.
When you instantiate a new sprite object, you can refer to its bounding box via the `rect` attribute (e.g. `mysprite.rect`).
This bounding box is the principle method behind moving objects on screen (think about when you moved the paddle to the bottom of the screen in Lab 9).
There are 2 ways of easily moving sprites, the first is to use the `move` function, and the second is to use the sub-points on the rectangle (more on that later).
The move function is essentially a setter for the sprite, it takes in a list containing an x and y coordinate and moves the ball to the location specified.
The location is based on the screen location where the top left corner is the origin and the x-axis increased to the right, and the y-axis increases when going down (Y is inverted from a normal Cartesian coordinate system).

The other method, as described above, is to use the subpoints of the Rect object.
These points refer to 9 points on the rectangle's perimeter: `topleft`, `bottomleft`, `topright`, `bottomright`, `midtop`, `midleft`, `midbottom`, `midright`, and `center`. 
All of these points are set with a tuple containing an x and a y position (e.g. `(x, y)`).
There are also other dimensions which may be used to align the sprite, these include:
* `x` and `y`, which refers to the top left of the sprite.
* `top`, `left`, `bottom`, and `right`, which refers to either the x or y of a given side.
* `centerx` and `centery`, which refer to the x or y of the center of the Sprite.
> __NOTE:__ These dimensions only require single dimensional data, like an int.

As state earlier, you can also influence the size of the object, via its collision box.
This can be done by working with the following variables:
* `size`, which takes in a tuple containing the new width and height
* `width`, and `height`, which contains the elements individually

I recommend looking through the full __[Documentation](https://www.pygame.org/docs/ref/rect.html)__ for a the `pygame.Rect` object, as there is a lot to explore with this object.

## Creating the Objects

For this lab, we need to focus on 3 objects: a ball, a paddle, and a brick.
You can use the code from last week as a starting point, however, going forward we will be using this repository.
You should run the game to test your code and make sure that it is working.

### The Ball
The ball will bounce around on the sides of the screen, and will be deflected when it hits a Brick.
It will also be deflected when it hits the paddle.
Unlike in Tom's Pong, however, the ball will not bounce off of the bottom of the screen, but will fall through the screen.
The ball should start on top of the paddle, aligned on to the `centerx` of the screen.
> __NOTE:__ The ball does not need to start out stationary on the paddle or have user input to start, for this lab, having the ball launch from the start is sufficient.

### The Paddle
The paddle will move across the bottom of the screen to deflect the ball upwards.
The paddle should start in the bottom, middle of the screen.
The paddle should not be able to leave the screen.
That is, `screen.left <= paddle.left` and `paddle.right <= screen.right`.

The paddle should deflect the ball based on where the ball lands on the paddle (See below).
![Ball Deflection](/docs/img/ball_deflection.png)

### The Brick
A brick should sit in its designated location and not move.
A brick should have a health value associated with it.
When a ball impacts the brick, it should be damaged.
When a brick's health reaches 0, it should be destroyed (i.e. removed from the screen).

## Submission
For this lab, you will present your results to your instructor in the Week 11 Scrum.
Your instructor will ask additional questions regarding your implementation and other general knowledge.

## Rubric
* 40 - Participation
* 25 - Ball working correctly
  * 5 - Ball starts out on top of the paddle and is bounced upward.
    > You may also start the ball above the paddle and have it drop down (either implementation is acceptable.)
  * 10 - Ball is deflected when it hits a brick (Movement does not need to be perfect).
  * 10 - Ball is deflected when it hits the paddle.
  The ball should tend toward the left when hitting the left side of the paddle, and to the right when hitting the right.
* 5 - Paddle Working correctly
  * 5 - Paddle does not leave the bounds of the screen.
* 30 - Brick working correctly
  * 15 - Bricks should have health that is decreased when a ball hits it.
  * 15 - Bricks should be destroyed when their health reaches 0.

# Lab 11 - Real-Time Programming II: Game States
Now that we have created classes for each of the Breakout objects, it is time to get the game working.

## Game States
One of the most important aspects to creating a real-time project is to design it with various __[states](https://en.wikipedia.org/wiki/State_(computer_science))__ in mind.
For our game, all a state means is that we have a past, a present, and a future that we need to be aware of.

States all have a definition (what they do), and a transition (how they change over time).
These series of states make up a __state diagram__.
For any large project, your should define your state diagram by hand before implementing it in code (e.g. creating a whiteboard sketch, Microsoft Visio diagram, etc).

For our project, the model will be provided to you, your job is to translate it into code.

Let's create a simple model using Breakout.

#### State Definitions:
In Breakout, we have 3 primary states: a play state, a pause state, and a game over state.
* During the game state, the behavior of the program should allow it to take user input, process game changes, and display the changes back to the user.
* During the game over state, the game should sit idle and wait for a user to restart the game (classically, this would be an arcade machine waiting for a user to insert enough coins to play).
  In our case, this is just the game waiting for the user to press the space bar.
* During the pause state, the game should sit idle and wait for a user to un-pause the game.

#### State Transitions
Now that we have defined our states, we need to define our state transitions.
* We should have our game start in the game over state, since it is how the game will have ended previously.
  The Game over state should be what the game loads into upon initialization.
* The game over state is very simple to model: it transitions to the play state when and only when the user gives the input.
  * If the game is terminated, the state will not change.
* The play state is a little bit more complex, since it involves multiple branching paths.
  * The play state will transition into the pause state when the user pauses the game, and
  * the play state will transition to the game over state when the user runs out of lives or the user terminates the game manually.
* Finally, the pause state is very similar to the game over state since it transitions to the play state when a user un-pauses the game.

![State Diagram](/docs/img/breakout_states.png)
> Because your final game may be different than the given game, your diagram may eventually differ than what is described above.

## Implementing States
The obvious follow up questions is __"How do I write this in code?"__
There are many ways to implement state transitions.
In a larger project, you would likely use objects to contain various behaviors and change the object pointers to transition states.
In this project, it will be easier to use integer or boolean states to control the transitions.
Below is a __pseudocode__ example.

```
# NOTE: Escape is used to quit the game, space is used to start the game,
# and return is used to pause.
# Your code will vary!

GAME_OVER = 0
PLAY      = 1
PAUSED    = 2

state     = GAME_OVER
exitgame  = False

while not exitgame:
    # Exit the game
    if user_input() == ESC:
        exitgame = True
        continue

    # Game Over State
    if state == GAME_OVER:
        show_text("Game Over")
        show_subtext("Press space to play.")
        if user_input() == SPACE:
            state = PLAY
            continue

    # Paused State
    elif state == PAUSED:
        show_text("Paused")
        if user_input() == RETURN:
            state = PLAY
    
    # Play State
    else:
        run_game()
        
        if lives <= 0:
            state = GAME_OVER
            continue
        
        if user_input() == RETURN:
            state = PAUSED
            continue
```
> If you are unfamiliar with a continue statement, it is a control statement (similar to a break or return).
  A continue, however, does not break out of a loop, but instead goes to the top of a loop.
  For example, the continues in the pseudocode would all immediately jump up to the `while not exitgame` loop.

## Debugging Movement
In this lab you will start debugging the motion of the ball, and the collisions on bricks.
This is one aspect in which you will have a lot of freedom to design your own motion.
I encourage you to implement ideas outside of the given code to implement movement.
The only restriction is that your movement should not feel bad to play with, and you should not experience clipping with the paddle and the ball or a brick and the ball.

## Game Statistics
In addition to the states and movement, you will also start keeping track of the score, lives, and level.

When a user hits a block (or destroys a block, you can choose), the score should be incremented.

When a user destroys the last block in a level, a set of new blocks should appear as part of a new level.
Your ball should also be reset to its initial position when a level changes.
Your level should increment upon completion of the last level.

Every time the ball goes off screen, the lives of the player should decrease by 1.

When a user runs out of lives, the game should end.
When the user starts up the game again, the level should be reset to 1, the score should be set to 0, and the number of lives should be reset to the starting number.


## Submission
For this lab, you will present your results to your instructor in the Week 12 Scrum.
Your instructor will ask additional questions regarding your implementation and other general knowledge.

## Rubric
* 40 - Participation
* 25 - Working States in the Game
  * 15 - Implemented a Game Over Screen
    * 5 - Game Over screen is displayed when the game starts.
    * 5 - Game Over screen transitions to the game upon user input.
    * 5 - Game Over screen is displayed when the user runs out of lives
  * 10 - Working pause menu
    * 5 - Pause menu is triggered by user input. (Pause menu cannot be activated during the Game Over screen)
    * 5 - Pause menu is terminated by user input.
* 15 - Brick deflection is fluid and fun to play (i.e. not buggy)
* 15 - Game keeps track of score, lives, and level.
  * 3 - Score is increased when hitting bricks (or destroying them).
    > I will leave this as a creative choice to you.
  * 3 - Lives are decreased when the ball falls off the screen.
  * 3 - Levels are increased when a user destroys the last block on the screen.
  * 3 - New Bricks are generated when a user completes a level.
    > __NOTE:__ An ideal game would also reset the ball at this point.
  * 3 - Score, lives, and level are reset when it is game over.

# Lab 12 - Binary File I/O
One way that we will modernize this game is by allowing the user to save.
When the original Breakout was developed there was no way of saving a game, and once the power was turned off, all scores and progress were lost.

We will use binary file I/O to save and load the game.

The game should be saved whenever a user exits the screen.
If there is a save file present upon loading the game, the previous game state should be loaded instead of starting a new game.
If the user runs out of lives during the game, any previous save files should be deleted.
If the game is loaded into its game over state, no save file should be created.

__Things you will need to keep track of.__
* Game
  * Score
  * Level
  * Lives
* Ball
  * Location
    * X-Position
    * Y-Position
  * Motion
    * Velocity
    * Theta
    * __OR__
    * X-Velocity
    * Y-Velocity
  * State __(Use this for Lab 13)__
    * Power-Up Status
      * Power-Up Type
      * Power-Up Time
* Paddle
  * Location
    * X-Position
    * Y-Position
* Bricks __(for each brick)__
  * Location
    * X-Position
    * y-Position
  * Status
    * Health
    * Power-Up Brick __(Use this for lab 13)__



   
## Submission
For this lab, you will present your results to your instructor in the Week 13 Scrum.
Your instructor will ask additional questions regarding your implementation and other general knowledge.

## Rubric
* 40 - Participation
* 30 - Saving and loading games works
* 15 - No extraneous files are created
* 15 - Stale save files are deleted once the game ends

# Lab 13 - Integration
This will be the final lab for this project.
In this lab you will add to your game to make it stand out and be truly unique.

There are no general guidelines to this lab other than whatever you add should be significant.
> __NOTE:__ As a rule of thumb, you should put in at least the same level of effort into this lab as the other labs in the project.

For those who may have fallen behind in previous weeks, please use this lab as an opportunity to catch back up and created something you can be proud of.

## Ideas
* Use File I/O or Binary File I/O to save high scores and the names of the best players. __(Medium)__
* Add a power up to the game:
  * Add a damage powerup that destroys all bricks and is not deflected by bricks. __(Medium)__
  * Add a multi-ball powerup that allows for 3 balls to be present on the screen at once. __(Hard)__
  * Add a powerup that  temporarily increases the size of the paddle. __(Medium)__
* Add an acceleration due to gravity which changes how the ball moves. __(Medium)__
* Add varying coefficients of restitution that change how ball reflects (more or less velocity) __(Medium)__
* Modify the force that various bricks impart on the ball upon deflection. __(Medium)__
* Create a requirement that certain bricks must be destroyed before others. __(Hard)__
* Add sound effects or background music to your game. __(Easy-Hard)__
* Create new fancier sprites. (Please don’t simply pilfer online assets). __(Easy-Hard)__

## Polishing your Game
Before your demo and submit your final game, please make sure that the game itself looks and feels good to play.
Polish is very important on a front-facing product.

Additionally, since I will be checking through your code, please clean up your code and __refactor__ it to be as clean as possible.
If you need to tips on implementing this, please refer to the lab syllabus.

## Submission
For this lab, you will present your project during Lab 14.
If you have any addiitonal content other than the game, you will submit this via Scholar in the "Presentations Assignment".

## Rubric
* 40 - Participation
* 30 - You game has at lease 1 unique feature (or several smaller features)
* 20 - Your game has been polished up (i.e. you have decent looking sprites and other assets)
* 10 - Your game's code was polished before submission.

> __NOTE:__ This last lab is meant as an opportunity to have fun and enjoy the fruits of your labor in the last weeks.
A lot of the grade is going to be based on effort.

# Lab 14 - Presentations

The first 30 minutes of this lab will involve taking the "Super" quiz. Which will count for 2 quiz grades (4% of your overall grade).

The remaining 75 minutes will be spent on group presentations.
Each group will present their project.
The purpose of this lab is to gain additional practice presenting and evaluating the presentations of others.

I want to see the following information from each group:
* Demo of the game (include multiple levels and power-ups if applicable).
* What challenges did you face during development (from each partner)?
  How did your team solve these?
  > __NOTE:__ These can be both in terms of code and disagreements with the team
* What did you enjoy about the project (from each partner)?
* What did you learn from the project (from each partner)?

You and your partner must present for no fewer than __4 minutes__ and no longer than __6 minutes__.
If your presentation is too long or short I will take off 10 points per minute (__yes, I will be timing__).
> You and your partner should practice presenting before the final lab (At least run through it once)!

If you take longer than 7 minutes, I will likely cut you off (don't make me do this)!

> __NOTE:__ If you and your partner do not have a way of presenting, please let me know beforehand so that I can download and load your project for your presentation.
I will use your most up-to-date GitLab version, make sure that all of your changes are pushed and that you give me the correct repository.

## Submission
In order to receive credit for this lab, you must be present in lab to present your Breakout game.
You must also be present for the duration of the lab to watch other groups present, only excused absences will be allowed.
I will evaluate your presentation in class.
You should have some supplemental material for your presentation once you have finished demonstrating your game (e.g. slides).
> Include screenshots from your game, just in case you have issues with your demo.

## Rubric
* 25 - Live demo of your game.
* 40 - Discussion about your project (e.g. Challenges, enjoyment, knowledge gained).
* 35 - Quality of the presentation.
  * Did you keep on topic?
  * Did you have supplemental content (e.g. slides)?

__Presentation Length?__
I will take the final score from above and take off points for going under 4 minutes or over 6 minutes.
For example, a presentation that goes for 6:30 minutes or 3:30 minutes would lose 5 points, while a project that goes for 4:00 minutes exactly or 5:59 minutes would not lose any points.

# Additional Documentation

[Command Line Interfaces](docs/cli.md)

[Installing with pip](docs/numpy_matplotlib_installation.md)

[Instantiation Example](docs/car_example.md)

[PyGame Docs & API](https://www.pygame.org/docs/)
