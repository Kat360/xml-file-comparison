# Comparing xml files

## Summary
This script compares two sets of xml files and generates html files (1 html file for each xml file comparison) showing
the original text, the revised text and the merged text, with any deleted text highlighted in red and inserted text
highlighted in green. It uses the `lxml` built-in function `htmldiff`.

## Required inputs
* File path to the original set of xml files.
* File path to the revised set of xml files.
* File path to where the outputted xml files should be saved.

**NOTE:** The revised files do not need to have the same file names as the original files though they do need be saved in 
the same order as the original files.

## Outputs
* For each xml file comparison, an html file is in the user-specified folder.
  * each html file shows the original text in the left-hand column, the revised text in the middle column, and the merged text
    in the right-hand column with any deleted text highlighted in red and any inserted text highlighted in green.
  * each html file will have the same name as the original file. If changes have occurred in the revised file, '\_comparison\_changes' 
    will be appended to the file name. If no changes have occurred, '\_comparison\_no\_changes' will be appended.'

**NOTE:** Each outputted html file will only display the text from the xml file and highlight specific changes to the text. The xml tags and any variation in the tags will not be displayed.

## Issues
  * There are some formatting issues with the merged text column of the outputted html file: line breaks disappear in
    paragraphs where there have been lots of changes so the text just appears in one giant block.
