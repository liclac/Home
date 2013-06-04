! 23 May 2013, 16:35
Triple-Booting a Mac
====================

Dual-Booting is having two OSes (such as Mac OS X and Windows) installed at the same time, which you can then choose between when your computer starts. On a Mac, this is really easy to set up, but if you try to add a third OS to that and you're running OS X 10.7+, you're going to need to spend 10 minutes fixing something before the third is bootable…

---

**Those of you who just want the fix:**  
Jump down to the appropriately titled section *"The Fix"*.  
Those of you who want to understand the problem, read on.

---

"Missing operating system"
--------------------------
Half a year ago, I was a linux newbie. I had tried Ubuntu out a bit in a Virtual Machine, and now I wanted to try it out on my real hardware. As a guide instructed me, I installed [rEFIt](http://refit.sourceforge.net/) (development has since moved to the fork [rEFInd](http://www.rodsbooks.com/refind/)), installed Ubuntu to a third partition after my Windows partition, and put the bootloader on the partition.

**"No operating system found"** was what my laptop told me when I tried to boot it up.

After a bit of research, it turns out this is a rather simple problem, with a simple fix.

The Problem
-----------
Back in the '80s, the Microsoft engineer who designed the MBR (Master Boot Record) format never thought we'd need more than four partitions or disks larger than 2 TB.  
Nowadays, we have a newer format called GPT, or GUID Partition Table, that supports up to 128 partitions (and space for more can be added), as well as disks up to 8 ZB - that's 8589934592 Terabyte!

However, Windows, as the eternal roadblock in the face of improvement it is, still uses MBR.  
64bit versions of Windows 7 and all versions of Windows 8 /can/ boot from GPT disks, but 32bit Windows 7 and Windows XP are still far more common than both of those combined.

As a workaround for this, it's possible to have /both/ an MBR table *and* a GPT table on the same disk. This is an ugly hack that limits OSes that only see the MBR to partitions within the first 2TB and four partitions, but hey, it's better than nothing.  
Bootcamp, as the helpful chap it is, kindly creates such a hybrid for you and lets you install Windows on the GPT table OS X requires. However, as of 10.7 (Lion), it creates this hybrid with:

* An EFI System Partition (mandatory)
* Your OS X partition
* Your OS X "Recovery HD" partition
* Your Bootcamp partition

But hey, this leaves no room for a third OS! However, that Recover HD doesn't actually need to be in the MBR (neither does your OS X partition, but being able to access those files from Windows is nice). So, we can just edit the MBR table and take that out!

Note that a Hybrid MBR works by having both a GPT table and an MBR table, and copying partitions from the GPT to the MBR, so you're not deleting the partition; you're basically just hiding a partition from Windows that it will never use anyways. All your partitions are safe in the GPT.

The Fix
-------
<p class="alert alert-warning">
<strong>Warning:</strong><br />
I wouldn't recommend doing this from Windows, ESPECIALLY not a Windows installation on your local disk, as it will likely freak out once you're done.
</p>

First off, you're going to need a little program called [gdisk](http://sourceforge.net/projects/gptfdisk/). On Linux, this is most certainly preinstalled or at least available in your distro's repository. For Mac, download and install the package from the site.  

Once you have gdisk installed, open up a terminal. Don't worry if you've never even seen one of those before, you just have to type exactly what I say into it.

To open a terminal:

* On **Mac OS X**, use one of:
	* Type "Terminal" into Spotlight (the magnifying glass in the menu bar) and pressing Enter
	* Open `/Applications/Utilities/Terminal.app` in Finder
* On **Linux** (assuming you have a graphical UI running):
	* Look through the application menu - most desktops have it there somewhere
	* Try pressing *Ctrl+Alt+T* or *Cmd+T*, most desktop bind it to one of those
	* The one universal way is to press *Ctrl+Alt+F1* to drop out of the graphical UI (Ctrl+Alt+F7 or Ctrl+Alt+F8 goes back to it)
	* If that somehow doesn't work, you may have an oddball distro (really old Fedora Core versions come to mind) that swaps the slots. Ctrl+Alt+F2 should drop you out of the GUI and Ctrl+Alt+F1 back in.

---

Once you have a terminal, run one of:  
**(OS X)** `sudo gdisk /dev/disk0`  
**(Linux)** `sudo gdisk /dev/sda`  
Both of these target your main hard drive; other drives should be on `/dev/disk1`, `/dev/disk2`, etc. on OSX, and `/dev/sdb`, `/dev/sdc`, etc. on Linux.

<p class="alert alert-error">
<strong>WARNING:</strong><br />
From now on, make sure to type EXACTLY what I say. Running the wrong command can potentially destroy entire partitions!<br />Nothing is saved until you run <code>w</code> and type "yes", so if anything goes wrong, don't hesitate to press Ctrl+C (Cancel) to immediately cancel and start over!
</p>

First off, run `p` (type it and press Enter), to make sure you have targeted the right disk. The correct one should have an "EFI System Partition", your OSX Partition, a "Recovery HD", then your two installed OSes. If it's not the right one, type `q` to quit and try a different disk.

Write down the partition numbers (the leftmost column) of your OSX partition (not the Recovery HD) and your two additional OSes somewhere, or just make sure you can scroll up to look at that table. For Windows, you want the BOOTCAMP partition (or whatever the partition for your C-drive is called). For Linux, you want the partition with */boot/* on it - not the Swap partition, if you have one.

Now it's time to create a Hybrid MBR:

1. Run `r` (for Recovery commands) and `h` (for Hybrid MBR)
2. Enter the three partitions' numbers separated by spaces, and press Enter
3. It'll ask you if you want to place the GPT EFI partition first in the MBR - your answer to this doesn't really matter, but I usually answer "no"
4. It'll now go through all the partitions you entered...
    1. It'll ask for an MBR hex code; the default should be just fine, so just press Enter
    2. Next, it'll ask you if you want to set a Bootable flag. Just answer "y" or "yes" (case-insensitive) for all of them
5. Run `w` (for Write), read the warning and answer "y" or "yes" to save your newly crafted Hybrid MBR
6. Run `q` to quit

You're done! Assuming you installed the bootloader correctly (Windows' bootloader in the MBR and your 3rd OS's to its partition), you should now be able to boot it.