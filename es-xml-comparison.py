from lxml.html.diff import htmldiff
from lxml import html
import os
from lxml import etree
import xml.etree.ElementTree as ET
import re
import time
import namedentities
# import logusage
# import getpass

r'''
**Summary:**
This script compares two sets of xml files and generates html files (1 html file for each xml file comparison) showing
the original text, the revised text and the merged text, with any deleted text highlighted in red and inserted text
highlighted in green. There is also an option to generate xml files with deleted text wrapped in `<del>` tags and inserted
text wrapped in `<ins>` tags.

**Required inputs:**
* The user should save:
    * the original files in this folder: '//voyager/edit\_systems/XML\_comparison/1. Original files/'.
    * the revised files to compare against the original files in this folder: '//voyager/edit\_systems/XML\_comparison/2. Revised files/'.
    
    **NOTE:** The user should delete any files that might already be in these folders. The revised files do not need to have
       the same file names as the original files though they do need be saved in the same order as the original files - for
       that reason, it helps if both sets of files have the same file names (or at least if the start of file names are the same).

**Outputs:**
* For each xml file comparison, an html file is outputted here: '//voyager/edit\_systems/XML\_comparison/3. Output html files/'
  * each html file shows the original text in the left-hand column, the revised text in the middle column, and the merged text
    in the right-hand column with any deleted text highlighted in red and any inserted text highlighted in green.
  * each html file will have the same name as the original file. If changes have occurred in the revised file, '\_comparison\_changes' 
    will be appended to the file name. If no changes have occurred, '\_comparison\_no\_changes' will be appended.'
    
  **NOTE:** Each html file only displays the text from the xml file and specific changes to the text. The xml tags and
   any variation in the tags will not be displayed.
     
  * **Optional:** For each file comparison, an xml file can be outputted here: '//voyager/edit\_systems/Katherine/XML\_comparison/3. Output xml files/'.
     * The xml file will have any deleted text encompassed in `<del>` tags and any inserted text encompassed in `<ins>` tags.
     * If the user wants this functionality they will need to uncomment the penultimate 3 lines of code.

**Issues:**
  * There are some formatting issues with the merged text column of the outputted html file: line breaks disappear in
    paragraphs where there have been lots of changes so the text just appears in one giant block.
'''

# get the start time of running the script
start_time = time.time()

# set file count to zero
file_count = 0

# log usage of this script
#logusage.addtolog(getpass.getuser(), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), os.path.basename(__file__))

# declare folder paths...
# folder path to original set of xml files:
original_folder_path = '//voyager/edit_systems/XML_comparison/1. Original files/'
# folder path to revised set of xml files to compare against original:
compare_folder_path = '//voyager/edit_systems/XML_comparison/2. Revised files/'
# folder path to where the outputted html files will be saved:
output_html_path = '//voyager/edit_systems/XML_comparison/3. Output html files/'
# folder path to where the outputted xml files will be saved. NOTE: this is optional.
output_xml_path = '//voyager/edit_systems/XML_comparison/4. Output xml files/'

# check if file path exists
def does_url_path_exist(urlpath):
    if not os.path.isdir(urlpath):
        print('That folder doesn\'t exist!')
        time.sleep(5)
        quit()

does_url_path_exist(original_folder_path)
does_url_path_exist(compare_folder_path)

# loop through xml files in both folders
for original_file, compare_file in zip(os.listdir(original_folder_path), os.listdir(compare_folder_path)):
    # confirmation
    print('Comparing ' + "'"+ original_file + "'" +' with ' + "'" + compare_file + "'" + ' ....')
    if original_file.lower().endswith('.xml') and compare_file.lower().endswith('.xml'):
        # count how many file comparisons are being made
        file_count += 1
        # file names without extensions
        original_file_no_ext = original_file.split('.xml')[0]
        compare_file_no_ext = compare_file.split('.xml')[0]
        # read the two sets of files
        original_data = open(original_folder_path + original_file, 'r', encoding='utf-8').read()
        # get rid of extraneous spaces between tags (often created if the file is saved after pretty printing)...
        original_data_string= re.sub(r'>\s+<', '><', original_data)
        original_data_string = re.sub(r'\s{2,}', ' ', original_data_string)
        original_data_string = re.sub(r'\n+', '', original_data_string)
        # replace original file with tidied version
        with open(original_folder_path + original_file, 'w') as f:
            f.write(namedentities.hex_entities(original_data_string))
            f.close()

        compare_data = open(compare_folder_path + compare_file, 'r', encoding='utf-8').read()
        # get rid of extraneous spaces between tags (often created if the file is saved after pretty printing)...
        compare_data_string= re.sub(r'>\s+<', '><', compare_data)
        compare_data_string = re.sub(r'\s{2,}', ' ', compare_data_string)
        compare_data_string = re.sub(r'\n+', '', compare_data_string)
        # replace original file with tidied version
        with open(compare_folder_path + compare_file, 'w') as f:
            f.write(namedentities.hex_entities(compare_data_string))
            f.close()

        # parse the xml files to get the root and convert to strings...
        # recover=True: helps skip some parsing errors. Delete if you want parsing errors highlighted.
        # remove_pis = True: removes process instructions (obviously)
        original_tree = ET.parse(original_folder_path + original_file, etree.XMLParser(encoding='utf-8', recover=True,
                                                                                       remove_pis=True))
        original_root = original_tree.getroot()
        original_xml_str = etree.tostring(original_root, encoding='utf8', method='xml', xml_declaration=False,
                                          pretty_print=True).decode('utf-8')

        compare_tree = ET.parse(compare_folder_path + compare_file, etree.XMLParser(encoding='utf-8', recover=True,
                                                                                    remove_pis=True))
        compare_root = compare_tree.getroot()
        compare_xml_str = etree.tostring(compare_root, encoding='utf8', method='xml', xml_declaration=False,
                                         pretty_print=True).decode('utf-8')

        # this bit does the comparison...
        # get the diff html from lxml built in method
        # htmldiff inserts 'del' tags around any deleted text and 'ins' tags around any inserted test
        diff_version = htmldiff(original_xml_str, compare_xml_str)
        # the following is some clean up after a lot of errors from malformed xml (tags not closed properly etc)
        diff_version = diff_version.replace('<br>', '<br/>').replace('<hr>', '<hr/>').replace('&lt;', '<')\
            .replace('&gt;', '>')
        diff_version = re.sub(r'<img ([^>]*)>', r'<img \1 />', diff_version)
        diff_version = re.sub(r'>\s+<', '><', diff_version)
        diff_version = re.sub(r'\s{2,}', ' ', diff_version)
        diff_version = re.sub(r'\n+', '', diff_version)

        # prepare for conversion to html...

        # diff_version1 = etree.fromstring(DiffedVersion, parser=None)  # this can bring up some parsing errors. Use below
        diff_version1 = html.fromstring(diff_version, parser=None)
        diff_version1 = etree.tostring(diff_version1, pretty_print=True).decode('utf-8')

        # replace the 'del' and 'ins' tags with span tags with inline css.
        # The inline css will highlight any text within the 'del' tags red and text within the 'ins' tags green.
        tags = re.findall('<.*?>', diff_version1)
        for tag in tags:
            if tag == '<del>':
                diff_version1 = diff_version1.replace('<del>', '<span style="background-color: #ff5555">')
            elif tag == '</del>':
                diff_version1 = diff_version1.replace('</del>', '</span>')
            elif tag == '<ins>':
                diff_version1 = diff_version1.replace('<ins>', '<span style="background-color: #55ff55">')
            elif tag == '</ins>':
                diff_version1 = diff_version1.replace('</ins>', '</span>')
            else:
                # delete all other tags so what's left is the xml text and the span tags for displaying the highlighting
                # in the outputted html file.
                diff_version1 = diff_version1.replace(tag, '')


        # # The below was originally uncommented doesn't appear to have any effect on outputted text so I've commented out
        # # remove empty lines from string
        # lines = diff_version1.split("\n")
        # non_empty_lines = [line for line in lines if line.strip() != ""]
        # diff_version1 = ""
        # for line in non_empty_lines:
        #     diff_version1 += line + "\n"
        # diff_version1.strip()

        # remove line breaks within opening and closing span tags
        span_tags = re.findall('<\s*span[^>]*>\s*.*?\s*<\s*/\s*span>', diff_version1)
        for span_tag in span_tags:
            span_tag1 = span_tag.replace('\n', '')
            diff_version1 = diff_version1.replace(span_tag, span_tag1)

        # if there are insertions or deletions in the file, append '_comparison_changes' to the outputted html file.
        if 'span' in diff_version1:
            append_file_name = '_comparison_changes.'
        # if there are no changes, append '_comparison_no_changes' to the outputted html file.
        else:
            append_file_name = '_comparison_no_changes.'

        # build the html file...
        # the file will be structured in 3 columns (i. original file text, ii. revised file text, iii. merged text)

        # set the css
        style = '<style>{box-sizing: border-box;} .column {float: left;width: 32%;padding: 7px;}  .row:after {content: ' \
                '"";display: table;clear: both;}' \
                '.div {overflow: scroll;} .p {font-family: "Helvetica";}</style>'

        # html string for the merged text with tracked changes:
        merged_html_string = '<div class="column"><h2>Merged Text</h2>'
        for line in diff_version1.split('\n'):
            merged_html_string += '<p>' + str(line).rstrip().lstrip() + '</p>'
        merged_html_string += '</div>'

        # html string for the original text:
        original_html_string = '<div class="column"><h2>Original file: ' + original_file + ' </h2>'
        for line in original_xml_str.split('\n'):
            original_html_string += '<p>' + line + '</p>'
        original_html_string += '</div>'

        # html string for the revised text:
        compare_html_string = '<div class="column"><h2>Revised file: ' + compare_file + '</h2>'
        for line in compare_xml_str.split('\n'):
            compare_html_string += '<p>' + line + '</p>'
        compare_html_string += '</div>'

        # full html string:
        full_html_string = '<html>' + style + '<body><div class="row">' + original_html_string + compare_html_string\
                           + merged_html_string + '</body></div></html>'

        # write the html file
        with open(output_html_path + original_file_no_ext + append_file_name+'html', 'w', encoding='utf-8') as f:
            f.write(full_html_string)
            f.close()

        # # uncomment to write xml file
        # with open(output_xml_path + original_file_no_ext + append_file_name + 'xml', 'w') as fl:
        #     fl.write(namedentities.hex_entities(diff_version))
        #     fl.close()

print("\nTask complete!\n" + str(file_count) + " set(s) of xml file comparisons have been made.\nThis script took",
      time.time() - start_time, "seconds to run.\nThe html files are saved here: " + "'" + output_html_path + "'.")
