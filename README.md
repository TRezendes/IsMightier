# Is Mightier

## A website to help people contact their representatives

<br />

>*True,—This!*
*Beneath the rule of men entirely great*
*The pen is mightier than the sword. Behold*
*The arch-enchanters wand!— itself a nothing!—*
*But taking sorcery from the master-hand*
*To paralyse the Cæsars—and to strike*
*The loud earth breathless!—Take away the sword—*
>
>*States can be saved without it!*

~[*Richelieu; Or the Conspiracy*, Edward Bulwer-Lytton](https://archive.org/details/richelieuorconsp00lyttiala/page/38/mode/2up)

They say that the pen is mightier than the sword, and while the sword has its place in revolution, the pen is available more readily to more people. This project aims to make it as easy as possible for American citizens to contact their elected representatives about important issues.

While I hope that *Is Mightier* may someday address many pressing issues facing our nation, the first issue that it will address is the fascist assault on the rights of trans people.

### Site in its infancy

This project is only just beginning. I have several goals:

1. Implement a means for a constituent to look up their current elected representatives. √
2. Collect a database of pieces of letters that can be combined to create coherent letters so representatives are not bombarded with identical letters from multiple constituents.
3. Make it simple to edit or customize a letter if a constituent wants to. √
4. Download the letter as a PDF.
5. Match certain letters/letter parts in the database to particular bills and the representatives that are most connected to them.

The basics of this site should be fairly easy to put together. I hope to have the representative search done first, followed by some whole letters that can be personalized to a particular representative. I will start with Pennsylvania, as that is my home state, and then expand to states with the most dramatically awful pending legislation.

### Where Things are At

3/3/2024

When it comes to projects, I have a tendency to let the perfect be the enemy of the good. I easily get so bogged down in trying to add and perfect features that I miss out on ever shipping anything. As of right now, the site's basic functionality works. You can search by address or location to find the elected representatives for that area. The site can then present the representative's contact information and a letter to send to them.

You can see from the list above that there are still a lot of refinements I would like to make. For the moment, though, I am going to stop attempting to add functionality and focus on filling the database with content. With the basic functionality in place, if I write some letters and get them in the database, the site can go live. So that's the plan.

### The technicals

This site is [Flask](https://flask.palletsprojects.com/en/3.0.x/) on the backend. It uses Google's [Civic Information API](https://developers.google.com/civic-information) to do representative lookup. The database is implemented in [PostgreSQL](https://www.postgresql.org/).
I'm not looking for contributors at the moment, but, assuming this project gets some legs under it, I plan to solicit letters for the site. More letters and more authors means more variety as well as more passion.
<br />
<br />

### Acknowledgements and Licenses

1. Congressional data from <https://github.com/unitedstates/congress-legislators>
    - [Creative Commons Zero v1.0 Universal](https://github.com/unitedstates/congress-legislators/blob/main/LICENSE)
2. StateFace font by ProPublica from <https://propublica.github.io/stateface/>
    - [MIT License](https://github.com/propublica/stateface/blob/master/LICENSE.txt)
3. StateFace replacement/prepend CSS by [Paul Smith](https://github.com/paulsmith)
4. W3-CSS from <https://www.w3schools.com/w3css/>

  <br />

---

<br />

![GitHub](https://img.shields.io/github/license/TRezendes/IsMightier?color=%235bcefa&style=flat-square)
