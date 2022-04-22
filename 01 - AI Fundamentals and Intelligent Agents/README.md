# Artificial Intelligence Fundamentals and Intelligent Agents

#### 1. Define artificial intelligence (AI). Find at least 3 definitions of AI that are not covered in the lecture.
- ([Merriam Webster](https://www.merriam-webster.com/dictionary/artificial%20intelligence), 31.08.2021):  
"A branch of computer science dealing with the simulation of intelligent behavior in computers."
- ([Britannica](https://www.britannica.com/technology/artificial-intelligence), 31.08.2021):  
"the ability of a digital computer or computer-controlled robot to perform tasks commonly associated with intelligent beings."
- ([Lexology](https://www.lexology.com/library/detail.aspx?g=5424a424-c590-45f0-9e2a-ab05daff032d), 31.08.2021):  
"The theory and development of computer systems able to perform tasks normally requiring human intelligence, such as visual perception, speech recognition, decision-making, and translation between languages."

#### 2. What is the Turing test, and how it is conducted?
The Turing test is a test designed to determine if an AI is intelligent or not. The test is conducted with a human interrigator asking questions through a computer, the interrigator does not know ether it is an actual human at the other end, or the AI. The AI is intelligent if the interrigator isn't sure after the interview wether it is a human or not.

#### 3. What is the relationship between thinking rationally and acting rationally? Is rational thinking an absolute condition for acting rationally?
Thinking rationally is using the uncertainty and probablity to rach conclusions. Acting rationally is using the already available information to find an optimal action. This means an agent can perform a logical action without thinking rationally based on what information is available.

#### 4. Describe rationality. How is it defined?
Rationality is for an agent to perform the action that will yield the most optimal results, in other words, the agent "understands" the environment it is in. This means that for a sequence of observations and knowledge the agent has, it should select the optimal action.

#### 5. What is Aristotle’s argument about the connection between knowledge and action? Does he make any further suggestion that could be used to implement his idea in AI? Who was/were the first AI researcher(s) to implement these ideas? What is the name of the program/system they developed? Google about this system and write a short description about it.
Aristotle argued that actions are a connection between goals and knowledge of the action's outcome. To reach a desired goal, the knowledge is necessary to take the correct action. Aristotle's algorithm was a further suggestion that could be used to implement his idea in AI. The idea is to assume the goal, and then consider how it is attained. This is also known as goal-based analysis. Aristotle's algorithm was implemented by Allen Newell and Herbert Simon in their GPS program. *General Problem Solver* (GPS) was the first useful AI program, and was written in 1959. Simon and Newell made GPS' problem-solving algorithm similar to how humans solve problems, by performing means-ends analysis. The basic algorithm can be summarized as follows:

```
Consider the goals
if ( the goals are already achieved ) {
  we're done.
} else {
  the goals can be achieved by applying some operators.
}
```
An operator is made out of:

- The action
- The preconditions
- The change of conditions from taking the action.


#### 6. Consider a robot whose task it is to cross the road. Its action portfolio looks like this: look-back, lookforward, look-left-look-right, go-forward, go-back, go-left and go-right.

  - **While crossing the road, a helicopter falls down on the robot and smashes it. Is the robot rational?**  
    Yes. The robots task is to cross the road using all its available actions. None of these actions allow the robot to look upwards. The action is therefore rational because there is nothing the robot could have done to prevent being hit by the helicopter.

  - **While crossing the road on a green light, a passing car crashes into the robot, preventing it from crossing. Is the robot rational?**  
    No. Despite the robot having a green light, the robot still has the action "look-left-look-right". The rational behaviour here would be to look use this action when the light is green, this way the robot could detect hazards and then use the action "go-back" to avoid geting hit.

#### 7. Consider the vacuum cleaner world described in Chapter 2.1 of the textbook. Let us modify this vacuum environment so that the agent is penalized 1 point for each movement.

  - **Can a simple reflex agent be rational for this environment? Explain your answer**  
    No. A simple reflex agent will simply check if the current square is dirty, if it isnt it will move to the other square. This means if both squares are clean the robot wil continue to move back and forth, being penalized each time, without actually performing any work. ie.

  - **Can a reflex agent with state be rational in this environment? Explain your answer.**  
    Yes. If the agent has an internal state it can use to "remember" if it has cleaned a square or not, thus when it has made sure both squares are clean it has enough information to stop moving, and avoid being penalized.

  - **Assume now that the simple reflex agent (i.e., no internal state) can perceive the clean/dirty status of both locations at the same time. Can this agent be rational? Explain your answer. In case it can be rational, design the agent function.**  
    Yes. This agent can be rational because it can now "see" wether it should move to the other square or not and not just move blindly. This way the robot can avoid being penalized by unnecesary movement. We can implement this agent like this:

    ```python
    """
    Function returns action the agent should take based on its current position and the state of the two squares.
    """
    def SimpleReflexAgent(squareA, squareB) -> Action:
      # Clean the current square agent is in, if it is dirty
      if currentSquare.isDirty:
        return "Suck"

      if currentSquare == squareA:
        # Agent is in square A
        if squareB.isDirty:
          return "Right"

      else:
        # Agent is in Square B
        if squareA.isDirty:
          return "Left"

      return None
    ```


#### 8. Consider the vacuum cleaner environment shown in Figure 2.2 in the textbook. Describe the environment using properties from Chapter 2.3.2, e.g. episodic/sequential, deterministic/stochastic etc. Explain selected values for properties in regards to the vacuum cleaner environment.
The environment is:
- Partially Observable:  
  The agent can only view the square it is currently in, instead of all the available squares at once.

- Single Agent:   
  The vacuum cleaner agent is the only agent in the environment.

- Deterministic:   
  Environment is only influenced by the agent.

- Episodic:   
  Agent performs one action at a time, and the next action does not depend on the action before.

- Static:   
  The environment does not change while the vacuum cleaner is deliberating.

- Discrete:  
  There is only a finite number of actions the vacuum cleaner can take and there's a finite number of states the environment can have.

- Known:  
  The outcome is given for all the actions the agent takes.

#### 9. Discuss the advantages and limitations of these four basic kinds of agents:

  **(a) Simple reflex agents**  
  Advantages:  
    - Fairly simple to implement because it acts on direct knowledge, has no memory and no goal of the action it's performing.

  Limitations:  
    - Very simple, and can only be used for very simple controllers.

  **(b) Model-based reflex agents**  
  Advantages:  
    - Can update it's internal state or memory, and it also has a knowledge of how entities relevant to itself work.

  Limitations:  
    - Cannot know about any logic that was not implemented.


  **(c) Goal-based agents**  
  Advantages:  
    - Able to evaluate sequences of actions and take that action that will get the agent closer to its goal.  
    - The agent can easily change its behavior according to the specified goal.

  Limitations:  
    - Not so effective, and
    - The agent's goal may not be rational.

  **(d) Utility-based agents**  
  Advantages:  
    - Able to look at several variables at once to determine what the best action is.
    - Learns while performing its actions.

  Limitations:  
    - Has no memory of how the environment was, so it looks at the current state of the environment and how it can improve the environment.
