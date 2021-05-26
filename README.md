# ESI Publications

In this repository, you can find the PDF and a bib file of all our publications.

## Contributing

1. Fork this repository
2. Change the bib file in your fork and add the PDF
3. Open a Pull Request from your fork to the master branch here with your PDF and change to the bib file.
4. Check after 5 minutes that [our publications web page](https://www.ei.tum.de/esi/publikationen/) looks good. Looking bad mostly means an empty page with an error in the browser's developer console.

## Manual Checks

1. Check that under your paper there is no other paper that is in press. This will result in the year container to be split and looks weird when rendered. See the screenshot below:

![image](https://user-images.githubusercontent.com/20195407/119685580-c611ac80-be45-11eb-8304-9c9acf8cc63e.png)

2. DOI value is URL, not just the number.
3. The key of the paper in the bib file should be created by you using the surnames of the authors. For a paper written by "Clark Kent, Bruce Wayne, Harley Quinn" in 2001, use the key `kwq:2001`.

## To Do

- Check whether the bib file can render fine using GitHub actions but also allow local tests
