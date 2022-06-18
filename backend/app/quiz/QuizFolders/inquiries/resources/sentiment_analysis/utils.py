# Global variables regarding scales
OLD_MAX = 1
OLD_MIN = -1
NEW_MAX = 5
NEW_MIN = 1
OLD_RANGE = 2
NEW_RANGE = 4

# Convert scale [-1,1] to scale [1,5]
def convert_scale(compound):
    new_value = (((compound - OLD_MIN) * NEW_RANGE) / OLD_RANGE) + NEW_MIN
    return new_value

def get_index_average(opinion):
    sum_index = 0
    num_index = 0

    print("Opinion:", opinion)

    for key in opinion['InquiryAnswer']['Properties']:
        sum_index += int(opinion['InquiryAnswer']['Properties'][key])
        num_index += 1
    
    index_average = sum_index / num_index
    return index_average