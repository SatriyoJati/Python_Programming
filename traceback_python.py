import traceback
import sys
import traceback_python_first

a = 10
b = 0

try :
    try:
        traceback_python_first.div_with_error(b,a)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_linenox`
        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
except Exception as e:
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno
    print("Exception type: ", exception_type)
    print("File name: ", filename)
    print("Line number: ", line_number)
