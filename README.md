# xcd


## Introduce

XCD is a quick directory changer. In practice work, 
we generally switch between several commonly used directories. 
When you use XCD to switch directories, XCD will remember these directories
so that you can quickly switch to the history directory next time.

Usage examples:

**xcd**            : List the current stack and its indices.

**xcd \<path,bookmark\>**   :if is path, Add "path" to your directory stack and cd there,if is a bookmark,cd here.

**xcd -b \<name\> \<path\>**   : Add "path" to your bookmark with the name .

**xcd -B \<name\>**   : remove a  bookmark with the name .

**xcd -h**         : Print this help.

## Install

curl https://raw.githubusercontent.com/elicec/xcd/master/xcd_install.sh -L > xcd_install.sh && sudo sh xcd_install.sh


