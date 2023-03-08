
def bar(progress, size=10, empty_char=":white_large_square:", full_char=":blue_square:"):
    output = ""
    show = round(progress/size)
    output += (full_char * show) + (empty_char * (size-show))
    return output
