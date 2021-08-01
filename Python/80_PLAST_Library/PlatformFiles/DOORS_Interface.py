# coding: utf-8
'''
Created on Jun 13, 2014

@author: uidv9994
'''

# overallPreconditions = []
# overallStepDetails = []

class Precondition:
    def __init__(self):
        self.preconditions = []
        
    def addChildPrecondition(self, prec):
        self.preconditions.append(prec)
        
    def getChildPreconditions(self):
        return self.preconditions
    
class Step:
    def __init__(self):
        self.childSteps = []
        self.expectedResults = []
        self.comments = []
        self.testerComments = []
        
    def addChildStep(self, step):
        self.childSteps.append(step)
        
    def addExpectedResult(self, er):
        self.expectedResults.append(er)
        
    def addComment(self, c):
        self.comments.append(c)
        
    def addTesterComment(self, tc):
        self.testerComments.append(tc)
        
    def getChildSteps(self):
        return self.childSteps
    
    def getExpectedResults(self):
        return self.expectedResults
        
    def getComments(self):
        return self.comments
        
    def getTesterComments(self):
        return self.testerComments
    
class TestPlan():
#     overallPreconditions = []
#     overallStepDetails = []
    def __init__(self):
        self.listOfSteps = []
        self.listOfPreconditions = []
    
    def addStep(self):
        st = Step()
        self.listOfSteps.append(st)
        return st
        
    def addPrecondition(self):
        pr = Precondition()
        self.listOfPreconditions.append(pr)
        return pr
    
    def export(self):
#         global overallPreconditions
#         global overallStepDetails
        overallPreconditions = []
        overallStepDetails = []
        list_getChildSteps = []
        list_getExpectedResults = []
        list_getComments = []
        list_getTesterComments = []
        
        for precondition in self.listOfPreconditions:
            for childPreconditions in precondition.getChildPreconditions():
                overallPreconditions.append(childPreconditions)
        
        for step in self.listOfSteps:
            for childSteps in step.getChildSteps():
                list_getChildSteps.append(childSteps)
            for expectedResults in step.getExpectedResults():
                list_getExpectedResults.append(expectedResults)
            for comments in step.getComments():
                list_getComments.append(comments)
            for testerComments in step.getTesterComments():
                list_getTesterComments.append(testerComments)
                  
            overallStepDetails.append(list_getChildSteps)
            overallStepDetails.append(list_getExpectedResults)
            overallStepDetails.append(list_getComments)
            overallStepDetails.append(list_getTesterComments)
            list_getChildSteps = []
            list_getExpectedResults = []
            list_getComments = []
            list_getTesterComments = []
        return overallPreconditions, overallStepDetails
            
# testplan = TestPlan()
# 
# precondition = testplan.addPrecondition()
# precondition.addChildPrecondition("stop target")
# precondition.addChildPrecondition("delete all breakpoints")
# precondition.addChildPrecondition("reset target")
# precondition.addChildPrecondition("run target")
# 
# step_1 = testplan.addStep()
# step_1.addChildStep("childStep1 of step_1")
# step_1.addChildStep("childStep2 of step_1")
# step_1.addChildStep("childStep3 of step_1")
# step_1.addExpectedResult("The quick brown fox jumps over the lazy dog")
# step_1.addComment("this and that")
# step_1.addTesterComment("Oh darling I made a boo boo!")
# 
# step_2 = testplan.addStep()
# step_2.addChildStep("childStep1 of step_2")
# step_2.addChildStep("childStep2 of step_2")
# step_2.addChildStep("childStep3 of step_2")
# 
# step_3 = testplan.addStep()
# step_3.addChildStep("childStep1 of step_3")
# step_3.addChildStep("childStep2 of step_3")
# step_3.addChildStep("childStep3 of step_3")
# 
# return testplan.export()