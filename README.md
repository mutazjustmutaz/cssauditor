
>This is voodoo. The question is: Is this too much?

~ Terry Davis

As your web application grows bigger it's easy to lose control of its CSS code. This application helps you regain control by going through your code files and showing you the location of style attributes, style tags, repeated colors, and unused CSS classes.

### Features & Usage:

**Show "style" attributes:** It's bad practice to mix CSS code with HTML code. This option shows you all HTML and PHP files where the "style" attribute is used, along with a list of the elements in which it's used.
```
python cssauditor.py --styleatts [PATH/TO/HTML/OR/PHP/FILE/OR/FOLDER]
```


**Show <style> tags:** Using style tags isn't as problematic as using style attributes, but you still need at least to keep track of CSS code defined that way. This option shows you all HTML and PHP files in which the style tag is used.
```
python cssauditor.py --styletags [PATH/TO/HTML/OR/PHP/FILE/OR/FOLDER]
```


**Show Repeated colors:** CSS colors which are repeatedly used should be placed inside variables. This option shows you repeated colors and their occurence frequency. 
```
python cssauditor.py --colors [PATH/TO/CSS/FILE/OR/FOLDER]
```


**Show unused classes:** A common problem is that classes defined in CSS files sometimes end up being unused in HTML/PHP files. This option shows you the paths of CSS files that contain unused classes, along with the names of those classes.
```
python cssauditor.py --unused [PATH/TO/CSS/FILE/OR/FOLDER] [PATH/TO/HTML/OR/PHP/FILE/OR/FOLDER]
```

### Notes:

1- HTML/PHP folders are searched recursively. CSS folders are NOT searched recursively.

2- Don't forget to put the path in double quotes if it contains spaces.

### Status:

This Python application, while useful, is meant as a prototype for an application which I will write in C. The reason is that Python is relatively slow, and performance is crucial in an application of this type.

As a result, I haven't put as much effort as I could have into testing, refactoring, and optimization. And I also don't plan to add more features. 
