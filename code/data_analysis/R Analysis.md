We defined the following R function:

```R
plot_data <- function(file) {
  dat = read.csv(file, header=TRUE)
  layout(matrix(1:12, ncol=3))
  for (cat in c("closed_qa","summarization","brainstorming")) {
    for (comp in c("structure","informativity","on.topic","correctness")) {
      dat_tmp = subset(dat, category == cat)[,comp]
      barplot(table(dat_tmp))
}}}
```

and ran it on the merged annotation file, which includes the following columns:

```
id,structure,informativity,on-topic,correctness,category
```

The output prints a matrix of barplots ordered as follows:

<table>
  <tr>
    <th></th>
    <th>Closed QA</th>
    <th>Summarization</th>
    <th>Brainstorming</th>
  </tr>
  <tr>
    <th>Structure</th>
  </tr>
    <tr>
    <th>Informativity</th>
  </tr>
    <tr>
    <th>On topic</th>
  </tr>
    <tr>
    <th>Correctness</th>
  </tr>
</table>

The function is stoed in the `plot_data.rda` file and can be run with the following commands:

```R
file = "[The file containing the merged data]"
plot_data = load("plot_data.rda")
plot_data(file)
```