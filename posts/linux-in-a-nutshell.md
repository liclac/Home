! 12 May 2013, 20:45
Linux in a nutshell
===================

Linux has gained quite a bit of steam lately, especially with the release of Windows 8 and Steam for Linux. However, it also comes with a fair share of confusion, as Linux is quite different from Windows or OSX.  
  
I'll try clearing up some of the most common misunderstandings here, along with listing the main "flavors" (known as Distros) available.

Quick Facts
-----------
The most common misunderstandings about Linux, in order of how frequently I hear them. I ask you to quickly read through these (at least the bold parts).

* **Linux is just the kernel**, what manages the system's heartbeat, so to speak.  
Everything from how programs are installed to what comes preinstalled is up to a Distribution (or "distro") built on top of the kernel.

* **There is no one true version of Linux**, unlike with OSX and Windows, nor is any of the distributions better or worse than the others. They're made by different people, who do things differently. Choose the one you like best.

* On user-friendly distros, **you do not need to use the terminal**. You may be given instructions involving copypasting commands into the terminal, but this is almost always because these instructions are easier to write than to describe a series of clicks.

* **You're not forced to use a particular UI**. If you don't like how things look or act, you're free to customize or completely replace the UI. You can have several UIs installed, and choose which one to use when you log in.

* **Programs are fully compatible between distros**. You can take a program originally built on Ubuntu and run it on Fedora.  
There are, however, multiple ways of packaging programs (the two biggest formats being *.deb* and *.rpm*), but that's just the packaging, and it's easy to convert between them.

Distros for Dummies
-------------------
Now onto what you're most likely reading this post for: the quick guide to Linux Distros. Keep in mind that these are just the "big" ones - anyone can make their own distro, so naturally there are other ones floating around.

Also note that I have personally used all of the distros listed below - all of this is taken from **first-hand experience**, not rumors and reputations.

&nbsp;

&nbsp;

&gt; [Ubuntu](http://ubuntu.com/)/[Linux Mint](http://linuxmint.com/)
-----------------------------------------------------------------
![Ubuntu Logo](http://design.ubuntu.com/wp-content/uploads/ubuntu-logo14.png)

**Target Audience:** Beginners, home users  
**Focus:** Ease of use, beginner-friendliness

**Pros:**

* Most things will "just work"
* heaps of tutorials and information available.

**Cons:**

* Power users will find that the simplifications sometimes get in their way…
* Suffers from political problems

---
**To a new user, I strongly recommend Linux Mint, as it gives you a fully functional system right out of the box.**

---
**Ubuntu:**  
[Ubuntu](http://ubuntu.com/) is the distro most aimed towards beginners. With a large official repository (software catalogue), strong commercial support from companies like Valve (the makers of [Steam](http://steampowered.com/)), this is the definite choice for a new user. Most things will "just work", or work with minimal effort.

In addition, there is a large number of "derivatives" or "respins" of Ubuntu - the same base system, but with different default UI and software selection. Among others, there are [Ubuntu GNOME](http://ubuntugnome.org/) (uses the GNOME desktop by default), [Kubuntu](http://www.kubuntu.org/) (uses the KDE desktop) and the lighweight [Xubuntu](http://xubuntu.org/) (XFCE). A full list can be found [here](http://www.ubuntu.com/about/about-ubuntu/derivatives).

**Mint:**  
The most well-known derivative of Ubuntu is an unofficial one called [Linux Mint](http://linuxmint.com). Mint tries to resolve the issues caused by Canonical's (the company behind Ubuntu) political and financial needs, and comes with its own "Cinnamon" desktop preinstalled - a desktop very similar to that found in Windows XP - as well as a quite pretty green theme to replace Ubuntu's orange.

In short, Mint works a lot better than Ubuntu out of the box, due to including things that Ubuntu can't (such as certain multimedia codecs).

*(There is also a Mint version available that uses the MATE desktop, but last I checked, it had some issues with what passes for a start menu. Not recommended for a first impression.)*

&gt; [Fedora](http://fedoraproject.org/)
-----------------------------------
![Fedora Logo](https://fedoraproject.org/w/uploads/2/2d/Logo_fedoralogo.png)

**Target Audience:** Adventurers, developers  
**Focus:** Cutting-edge software

**Pros:**

* You'll always have the latest features available

**Cons:**

* The package manager (what you use to install things) is RIDICULOUSLY slow
* Relatively little software available

---
Fedora is a distro for the adventurous, who likes playing around with powerful features. It's also a distro for developers who like having the latest libraries available, and nothing getting in their way.

I wouldn't recommend it for home use though, as it requires a fair bit of tinkering to get things working, but for those who like being in control, but feel that Arch Linux is a bit too much, this is a quite good choice. Also, if you miss certain copyrighted software, install the **RPMFusion** repository.

There is also the more stability-focused relative **CentOS**, which is a popular choice on servers, and the paid version **Red Hat Enterprise Linux**, which includes enterprise support (which is useless for home users, but invaluable to large companies).  
The biggest difference between Fedora and CentOS/RHEL is that Fedora always has the latest bells and whistles, while CentOS and RHEL hold back in order to guarantee stability - it'd be really bad if your web server or entire business went down due to a previously unknown bug in a critical library.

As an aside, it should be mentioned that the US Military uses RHEL extensively - this speaks quite a bit for its reliability.

&gt; [Arch Linux](http://archlinux.org/)
-----------------------------------
![Arch Logo](https://d11xdyzr0div58.cloudfront.net/static/logos/archlinux-logo-dark-90dpi.ebdee92a15b3.png)

**Target Audience:** Power-users and people who really know what they're doing  
**Focus:** "Keep it simple"

**Pros:**

* Your system is what you make it - no more, no less
* No bloat or anything unnecessary stealing resources
* [The wiki](http://wiki.archlinux.org/) is amazing

**Cons:**

* If you don't know what you're doing, and can't figure it out, you're screwed.

---
Arch Linux is Linux for those who really know what they're doing.  
It doesn't even have an automatic installer - instead, it has a tutorial teaching you how to manually install everything, helped out by various utility scripts - and obviously no desktop, or even a graphical interface (beyond a commandline, of course).

This means you can min/max your computer and squeeze every bit of performance out of it, customize EVERYTHING to your liking and have complete control over every corner of your system, from upstart to login to desktop to shutdown process. It also means you have **no safety nets**. You're in charge of your computer, and you can wreck it if you do something wrong.

If you know what you're doing, and you want to use what you know, this is your distro. If you don't, you really should use something more user-friendly.

Also, Arch Linux is a Rolling Release distribution - it doesn't have version numbers, and every user is responsible for keeping his or her system up to date and working by him-/herself.

&nbsp;

&nbsp;

Notable Mentions:
-----------------

**Debian:**  
One of the oldest distros around.

There are two main "branches" of Debian - Stable and Unstable.

Stable is exactly what it says on the tin: it **does not crash**, period - this is why most serious web hosts use it. However, it also comes at the price of being constantly behind on updates.

Unstable is what Ubuntu (and thus also Mint) is based on, and if you're a home user, you really should use that instead. Ubuntu keeps up with Debian Unstable, and with every release cycle, they apply patches to make it more suitable for that purpose.

**Gentoo:**  
Extremely difficult to install, hard to maintain, but if done right, the resulting system can be VERY fast. Everything is recompiled and tailored for your computer before installation, which gives unparalleled performance, but prepare to wait for hours for larger packages to install.  
For reference, my laptop (a 2010 Macbook Pro) takes nearly two hours to compile Qt 5.

If you were told to install Gentoo by a certain imageboard, you're being trolled, and should most certainly reconsider.