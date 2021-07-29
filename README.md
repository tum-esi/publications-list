# ESI Publications

In this repository, you can find the PDF and a bib file of all our publications.

## Contributing

1. (optional) Fork this repository
2. Clone the repository
3. Change the bib file in your fork and add the PDF
4. Open a Pull Request from your fork to the master branch here with your PDF and change to the bib file.
5. Check after 5 minutes that [our publications web page](https://www.ei.tum.de/esi/publikationen/) looks good. Looking bad mostly means an empty page with an error in the browser's developer console. Also, clicking the PDF should open the pdf file.

## Manual Checks

1. Check that under your paper there is no other paper that is in press. This will result in the year container to be split and looks weird when rendered. See the screenshot below:

![image](https://user-images.githubusercontent.com/20195407/119685580-c611ac80-be45-11eb-8304-9c9acf8cc63e.png)

2. DOI value is URL, not just the number.
3. The key of the paper in the bib file should be created by you using the surnames of the authors. For a paper written by "Clark Kent, Bruce Wayne, Harley Quinn" in 2001, use the key `kwq:2001`.
4. The filename should look like `https://tum-esi.github.io/publications-list/PDF/2021-DATE-Worst-Case%20Failover%20Timing%20Analysis%20of%20Distributed%20Fail-Operational%20Automotive%20Applications.pdf`. So you need to manually insert the domain name but also replace spaces with a `%20`. 


## To Do

- Check whether the bib file can render fine using GitHub actions but also allow local tests
