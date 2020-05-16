# XML file comparison

## Summary
This script compares two sets of xml files and generates html files (1 html file for each xml file comparison) showing
the original text, the revised text and the merged text, with any deleted text highlighted in red and inserted text
highlighted in green. It uses the `lxml` built-in function `htmldiff`.

## Required inputs
* The user should save:
    * the original files in this folder: '//voyager/edit\_systems/XML\_comparison/1. Original files/'.
    * the revised files to compare against the original files in this folder: '//voyager/edit\_systems/XML\_comparison/2. Revised files/'.

    **NOTE:** The user should delete any files that might already be in these folders. The revised files do not need to have
       the same file names as the original files though they do need be saved in the same order as the original files - for
       that reason, it helps if both sets of files have the same file names (or at least if the start of file names are the same).

## Outputs
* For each xml file comparison, an html file is outputted here: '//voyager/edit\_systems/XML\_comparison/3. Output html files/'
  * each html file shows the original text in the left-hand column, the revised text in the middle column, and the merged text
    in the right-hand column with any deleted text highlighted in red and any inserted text highlighted in green.
  * each html file will have the same name as the original file. If changes have occurred in the revised file, '\_comparison\_changes' 
    will be appended to the file name. If no changes have occurred, '\_comparison\_no\_changes' will be appended.'

  **NOTE:** Each html file only displays the text from the xml file and specific changes to the text. The xml tags and
   any variation in the tags will not be displayed.

## Issues
  * There are some formatting issues with the merged text column of the outputted html file: line breaks disappear in
    paragraphs where there have been lots of changes so the text just appears in one giant block. Please do let me know
    if there's a way of correcting this.
