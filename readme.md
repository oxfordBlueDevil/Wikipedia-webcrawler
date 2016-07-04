# Wikipedia Web Crawler

- We built a wikipedia web crawler that folows a random wikiepedia article's trace to the philosophy page each time by visiting the first link in the article's content that is not within parantheses or italicized.

## Notes

1. The percentage of pages that lead to philosophy is 92.421% where the total of random Wikipedia pages visited was 541.

2. The distribution of path length of 500 pages that reached the Philosophy Wikipedia article is shown in the figure provided in the PageLength_Distribution.png file. As the figure demonstrates, the distribution is negatively skewed since it has a long tail in the negative direction. 

3. In our implementation, we used a global hashtable to cache visited pages that lead to the Philosophy Wikipedia article. The hashtable maps visited pages to a 2-tuple value where the first entry is the path length between the visited page and the philosophy page and the second entry is the Page link path. If a random starting page leads to a link that has been already cached, we would then access the cache to determine the random starting page's path length to the Philosophy Wikipedia article. This approach reduces the number of https requests necessary for 500 random starting pages.