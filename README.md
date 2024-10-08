# Refraction-Demonstration

The purpose of this little project was to challenge myself to see what I could create in a day of coding.

I decided to go with a demonstration of Snell's Law: $n_1\sin(\alpha_1) = n_2\sin(\alpha_2)$, as the mathematics was something that I was already familar with. Furthermore, I had a fairly good idea on how to visualise the rays in Python, this would be accomplished with Pygame. During the summer as a way of improving my comfort with coding in Python, I started to learn some more Python libraries, one of these was Pygame and I saw this mini-project as a means of testing my knowledge of it.

## How the Code Works

What seemed like the simplest way of implementing Snell's Law was to treat the eray lines as vectors. This would mean when drawing the vectors as pygame lines, I would only need to specify the start point of the line, the magnitude (this could be constant among all lines) and the angle the vector was being drawn at.

For this to work, I needed to establish a coordinate system from which to measure angles relative from. I decided to go with the standard expression of a unit circle: $(\cos(\theta),\sin(\theta))$, when $\theta = 0$ the vector would be (1,0).
Additionaly to calculate the angle between vectors required using the dot product: $\arccos(\frac{\vec{a}\cdot \vec{b}}{|\vec{a}||\vec{b}|})$.
Something I had to be aware of was the direction of the vectors a and b as, if one was in the "wrong" direction it would result in a larger angle than the one I actually required.

Finally, to draw the refracted ray I just needed to find the refracted angle using Snell's Law: $\alpha_2 = \arcsin{\frac{n_1\sin{\alpha_1}}{n_2}}$.
It was also important to have code handling the case where $\frac{n_1 \sin{\alpha_1}}{n_2} > 1$, so internal reflection could be demonstrated.

The way angles were calculated required an identification of which quadrant the mouse was.
This was because using a fixed coordinate system meant that, the angles required to draw the reflected and refracted light needed to be calculated in different ways.

## Future Improvements
There are lot of potential developments the code could experience.
For example, it would be interesting to explore more of optical theory, such as the ray path through different lenses.
Or even try to create a program that is based on 'first-principles' like Fermat's theorem.