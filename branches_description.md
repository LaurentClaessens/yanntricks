# debug

There are two non working test pictures. We are dealing with them here.

# passes

In `figures_demo`, create three lists of figures instead of one.

- The first one contains all of them
- The second one contains only the pictures which need two compilation passes
- The third one contains only the pictures which need three compilation passes

Then the script `testing.sh` will launch `figures_demo` three times with 
a parameter indicating the list to be used.
The aim is to compile each picture only the right number of time. This should reduce the 
test time.
