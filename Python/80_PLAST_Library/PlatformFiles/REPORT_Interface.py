# coding: utf-8
'''
Created on 05.03.2015

@author: Laurentiu Nitu
'''

import os
import xlsxwriter
import PlatformFiles.HTML_Interface as HTML
from time import strftime, localtime
from datetime import datetime
from xml import etree
from xml.etree.ElementTree import Element, SubElement, ElementTree
import xml.etree.ElementTree as ET

def StyleText(color, alignment, font, weight, size, text):
    return "<p style='font-family:%s;background-color:%s;font-size:%sx;text-align:%s;font-weight:%s'> %s </p>" % (font, color, size, alignment, weight, text)

class report_generator:
    def __init__(self, variant, overalltestbegin, overalltestend, req_counter, nrOfPassedTests, nrOfFailedTests, nrOfManualTests, nrOfErrorTests, listOfExecutedTests, isJenkinsUsed):
        self.variant = variant
        self.overalltestbegin = overalltestbegin
        self.overalltestend = overalltestend
        self.req_counter = req_counter
        self.nrOfPassedTests = nrOfPassedTests
        self.nrOfFailedTests = nrOfFailedTests
        self.nrOfManualTests = nrOfManualTests
        self.nrOfErrorTests = nrOfErrorTests
        self.listOfExecutedTests = listOfExecutedTests
        self.isJenkinsUsed = isJenkinsUsed
    
    def GetXlsxReport(self, data, results_data_xlsx):
        
        ###### XLSX SETTINGS
        OFFSET_BETWEEN_INFORMATIONS = 2
        BEGIN_TITLE_FROM_ROW = 1
        BEGIN_GENERAL_INFORMATION_FROM_ROW = BEGIN_TITLE_FROM_ROW + OFFSET_BETWEEN_INFORMATIONS
        BEGIN_TEST_INFORMATION_FROM_ROW = BEGIN_GENERAL_INFORMATION_FROM_ROW + OFFSET_BETWEEN_INFORMATIONS + len(data)
        COLUMNWIDTH = 35
        FONTSIZE = 25
        BEGINCOLUMN = 'A'
        ENDSUMMARYCOLUMN = 'B'
        ENDDETAILEDCOLUMN = 'K'
        
        if (self.isJenkinsUsed):
            wb = xlsxwriter.Workbook(strftime(os.environ['PLAST_WA_PATH'] + "Reports/PLAST_TestLog_" + self.variant + ".xlsx", localtime()))
        else:
            wb = xlsxwriter.Workbook(strftime(os.environ['PLAST_WA_PATH'] + "Reports/%Y-%m-%d-%H%M%S_TestLog_" + self.variant + ".xlsx", localtime()))
        ws = wb.add_worksheet(strftime("Report_%Y-%m-%d-%H%M%S", localtime()))
        
        ###### Generating Microsoft Excel Report
        titleFormat = wb.add_format({'bold': True})
        titleFormat.set_font_size(FONTSIZE)
        ws.set_column(BEGINCOLUMN + ':' + ENDDETAILEDCOLUMN, COLUMNWIDTH)
        ws.write(BEGINCOLUMN + str(BEGIN_TITLE_FROM_ROW), "TEST REPORT", titleFormat)
        
        ###### Write general information table
        ws.add_table(BEGINCOLUMN + str(BEGIN_GENERAL_INFORMATION_FROM_ROW) + ':' + ENDSUMMARYCOLUMN + str(BEGIN_GENERAL_INFORMATION_FROM_ROW + len(data)), {'autofilter':False, 'style': 'Table Style Light 14', 'data': data, 'columns':[
                                                      {'header': 'INFORMATION'},
                                                      {'header': 'RESULT'}]})
        
        ###### Write tests information table
#         end_line = 17 + self.nrOfExecutedTests
        ws.add_table(BEGINCOLUMN + str(BEGIN_TEST_INFORMATION_FROM_ROW) + ':' + ENDDETAILEDCOLUMN + str(BEGIN_TEST_INFORMATION_FROM_ROW + (self.req_counter)), {'autofilter':False, 'style': 'Table Style Light 14', 'data': results_data_xlsx, 'columns':[
                                                      {'header': 'Covered Requirement'},
                                                      {'header': 'Test name'},
                                                      {'header': 'Test case duration (H:M:S)'},
                                                      {'header': 'Test description'},
                                                      {'header': 'Test result'},
                                                      {'header': 'TC Preconditions'},
                                                      {'header': 'TC Test Steps'},
                                                      {'header': 'TC Expected Results'},
                                                      {'header': 'TC Comment'},
                                                      {'header': 'Tester Comment'},
                                                      {'header': 'Safety Requirement'}
                                                      ]})
        wb.close()
        
    def GetHtmlReport(self, data, results_data_html):
            ###### Generate the General Info Table
            htmlcode = HTML.table(data, col_align=['left', 'left'], header_row=['Information', 'Results'], style="background-color:lightgray")
            if (self.isJenkinsUsed):
                File = open(strftime(os.environ['PLAST_WA_PATH'] + "Reports/PLAST_TestLog_" + self.variant + ".html", localtime()), 'w')
            else:
                File = open(strftime(os.environ['PLAST_WA_PATH'] + "Reports/%Y-%m-%d-%H%M%S_TestLog_" + self.variant + ".html", localtime()), 'w')
            File.write(StyleText('orange', 'Center', 'Verdana', 'bold', '50', 'TESTS OVERVIEW'))
            File.write('<br><br>' + htmlcode)
            File.write('<br><br>')
            
            ###### Generate the Results Table
            File.write(StyleText('orange', 'Center', 'Verdana', 'bold', '50', 'LIST OF TEST CASES') + '<br><br>')
            
            ###### Color the Passed/Failed statement
            for testcase in results_data_html:
                if testcase[4] == 'Passed':
                    testcase[4] = "<font color='limegreen'>Passed</font>"
                elif testcase[4] == 'Failed':
                    testcase[4] = "<font color='red'>Failed</font>"
                elif testcase[4] == 'Error':
                    testcase[4] = "<font color='orangered'>Error</font>"
                elif testcase[4] == 'No Run':
                    testcase[4] = "<font color='gray'>No Run</font>"
                    
            ###### Add link to the description of each test case
            for testcase in results_data_html:
                id_ = testcase[0]
                testcase[0] = "<a href='#%s'>%s</a>" % (id_, id_)
            htmlcode = HTML.table(results_data_html, header_row=['Test case name',
                                                     'Test case duration (H:M:S)',
                                                    'Test description',
                                                    'Test result'],
                                                    style="background-color:lightgray")    
            File.write(htmlcode + "<br><br>")
            
            ###### General the individual test case description tables
            File.write(StyleText('orange', 'Center', 'Verdana', 'bold', '50', 'TEST CASE STEPS') + '<br><br>')
            header = ['Covered Requirement', 'Test Name', 'TC Preconditions', 'TC Test Steps', 'TC Expected Results', 'TC Comment', 'Tester Comment']
            for testExecuted in self.listOfExecutedTests:
                results_data2 = []
                results_data2.append(header)
                if testExecuted.getResult() == 0:
                    results_data2.append([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getPreconditions(), testExecuted.getSteps(), testExecuted.getExpectedResults(), testExecuted.getComments(), testExecuted.getTesterComments()])
                else:
                    if testExecuted.getResult() == 1:
                        results_data2.append([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getPreconditions(), testExecuted.getSteps(), testExecuted.getExpectedResults(), testExecuted.getComments(), testExecuted.getTesterComments()])
                    else:
                        if testExecuted.getResult() == 2: 
                            results_data2.append([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getPreconditions(), testExecuted.getSteps(), testExecuted.getExpectedResults(), testExecuted.getComments(), testExecuted.getTesterComments()])
                        else:
                            if testExecuted.getResult() == 3: 
                                results_data2.append([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getPreconditions(), testExecuted.getSteps(), testExecuted.getExpectedResults(), testExecuted.getComments(), testExecuted.getTesterComments()])
                
                rd2 = results_data2
                File.write("<section id=%s>" % (rd2[1][0]))
                htmlcode = HTML.table(rd2, style="background-color:lightgray")
                File.write("</section>" + htmlcode + "<br><br>")
                
    def GetXmlReport(self, data, results_data_xml, plast_version):
        if (self.isJenkinsUsed):
            f = open(strftime(os.environ['PLAST_WA_PATH'] + "Reports/PLAST_TestLog_" + self.variant + ".xml", localtime()), 'w')
        else:
            f = open(strftime(os.environ['PLAST_WA_PATH'] + "Reports/%Y-%m-%d-%H%M%S_TestLog_" + self.variant + ".xml", localtime()), 'w')
            
        root = etree.ElementTree.Element('xml')
        
        ####
        table0 = etree.ElementTree.SubElement(root, "PlatformTable")
        tr = etree.ElementTree.SubElement(table0, "tr")
        td = etree.ElementTree.SubElement(tr, "td")
        td.set("plast_version", str(plast_version))
        
        table1 = etree.ElementTree.SubElement(root, "SummaryTable")
        for row in data:
            td = etree.ElementTree.SubElement(table1, "td")
            td.set(str(row[0]).replace(' ', '').replace(':' , '').replace('(' , '').replace(')' , ''), str(row[1]))
                  
        table2 = etree.ElementTree.SubElement(root, "DetailsTable")
        for test in results_data_xml:
            tr = etree.ElementTree.SubElement(table2, "tr")
            td = etree.ElementTree.SubElement(tr, "td")
            td.set("requirement", str(test[0]))
            td = etree.ElementTree.SubElement(tr, "td")
            td.set("testName", str(test[1]))
            td = etree.ElementTree.SubElement(tr, "td")
            td.set("duration", str(test[2]))
            td = etree.ElementTree.SubElement(tr, "td")
            td.set("description", str(test[3]))
            td = etree.ElementTree.SubElement(tr, "td")
            td.set("testResult", str(test[4]))
            td = etree.ElementTree.SubElement(tr, "td")
            td.set("precondition", str(test[5]))
            td = etree.ElementTree.SubElement(tr, "td")
            td.set("testSteps", str(test[6]))
            td = etree.ElementTree.SubElement(tr, "td")
            td.set("expectedResults", str(test[7]))
            td = etree.ElementTree.SubElement(tr, "td")
            td.set("comment", str(test[8]))
            td = etree.ElementTree.SubElement(tr, "td")
            td.set("testerComment", str(test[9]))
            td = etree.ElementTree.SubElement(tr, "td")
            td.set("safetyRequirement", str(test[10]))
           
        # write the file to disk
        et = ET.ElementTree(root)
        self.IndentXML(root)
        et.write(f, encoding='utf-8', xml_declaration=True, method="xml") 
        f.close()
        
    def IndentXML(self, elem, level=0):
        '''
        Sets the cosmetics of the xml file
        
        elem = the element from which to begin arranging
        level = the level of depth
        '''
        i = '\n' + '\t' * level
        if len(elem):
            if not elem.text or not elem.text.strip():
              elem.text = i + '\t'
            if not elem.tail or not elem.tail.strip():
              elem.tail = i
            for elem in elem:
                self.IndentXML(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
              elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
              elem.tail = i
