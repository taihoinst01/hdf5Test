from difflib import SequenceMatcher


def run(sentence, modelNumberList):
    similarResult = {} # (모델넘버, 정확도)
    similarResult["maxRatio"] = 0
    similarResult["modelnumber"] = ''
    for modelNumber in modelNumberList:
        ratio = similar(str(modelNumber[0]), str(sentence[0]))
        # print('sentence: ' + sentence[0] + ' \\ modelnumber: ' + modelNumber[0] + ' \\ ratio: ' + str(ratio))
        
        if ratio > similarResult["maxRatio"]:
            similarResult["maxRatio"] = ratio            
            similarResult["modelnumber"] = modelNumber[0]
    return similarResult

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

