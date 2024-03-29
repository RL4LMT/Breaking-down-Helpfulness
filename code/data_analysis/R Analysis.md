We defined the following R functions:

```R
plot_all <- function(file) {
  dat = read.csv(file, header=TRUE)
  layout(matrix(1:12, ncol=3))
  for (cat in c("closed_qa","summarization","brainstorming")) {
    for (comp in c("structure","informativity","on.topic","correctness")) {
      dat_tmp = subset(dat, category == cat)[,comp]
      barplot(table(dat_tmp))
}}}

plot_relevance <- function(file) {
  dat = read.csv(file, header=TRUE)
  dat[dat=="2" | dat=="3" | dat=="4"] = "1" # replace scores with 1 (= relevant)
  dat = rbind(dat, c(-1,0,0,0,0,"brainstorming")) # force 0 columns
  layout(matrix(1:12, ncol=3))
  for (cat in c("closed_qa","summarization","brainstorming")) {
    for (comp in c("structure","informativity","on.topic","correctness")) {
      dat_tmp = subset(dat, category == cat)[,comp]
      barplot(table(dat_tmp), names.arg=c("Not relevant", "Relevant"), border=NA, col=c("#FF7256","#8EE5EE"))
}}}

plot_performance <- function(file) {
  dat = read.csv(file, header=TRUE)
  layout(matrix(1:12, ncol=3))
  for (cat in c("closed_qa","summarization","brainstorming")) {
    for (comp in c("structure","informativity","on.topic","correctness")) {
      dat_tmp = subset(dat, category == cat)[,comp]
      dat_tmp = c(dat_tmp,c("1", "2", "3", "4")) # force all columns
      barplot(table(dat_tmp, exclude=0), names.arg=c("1", "2", "3", "4"), border=NA, col=c("#f58a22","#f8c11d","#b5be2f","#72b043"))
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